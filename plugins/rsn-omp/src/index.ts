/** RustySpork OMP M0: read-only proposal validation. Does not execute model inference or weight edits. */
import type { ExtensionAPI, ExtensionCommandContext } from '@oh-my-pi/pi-coding-agent';
import { dirname, extname, isAbsolute, relative, resolve } from 'node:path';
import { realpath } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const PACKAGE_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const VALIDATOR = resolve(PACKAGE_ROOT, 'tools', 'validate_proposal.py');

function inside(candidate: string, root: string): boolean {
  const subpath = relative(root, candidate);
  return subpath === '' || (subpath !== '..' && !subpath.startsWith('../') && !subpath.startsWith('..\\') && !isAbsolute(subpath));
}

async function check(candidateArg: string, ctx: ExtensionCommandContext): Promise<void> {
  if (!candidateArg || /[\x00\r\n]/.test(candidateArg) || extname(candidateArg).toLowerCase() !== '.json') {
    ctx.ui.notify('Usage: /rustyspork check <workspace-relative-proposal.json>', 'error');
    return;
  }
  const cwd = resolve(ctx.cwd);
  const candidate = resolve(cwd, candidateArg);
  // Lexical check first for consistent Windows/POSIX behavior, then realpath to deny symlink escape.
  if (!inside(candidate, cwd)) {
    ctx.ui.notify('RustySpork check refuses paths outside the current workspace', 'error');
    return;
  }
  let source: string;
  try {
    const [safeCwd, safeCandidate] = await Promise.all([realpath(cwd), realpath(candidate)]);
    if (!inside(safeCandidate, safeCwd)) {
      ctx.ui.notify('RustySpork check refuses paths outside the current workspace', 'error');
      return;
    }
    source = safeCandidate;
  } catch {
    ctx.ui.notify('RustySpork proposal file could not be resolved', 'error');
    return;
  }
  const python = process.env.RSN_PYTHON?.trim();
  const command = python ? [python] : process.platform === 'win32' ? ['py', '-3'] : ['python3'];
  try {
    const child = Bun.spawn([...command, VALIDATOR, source], {
      cwd, stdin: 'ignore', stdout: 'pipe', stderr: 'pipe'
    });
    const [code, stdout, stderr] = await Promise.all([
      child.exited, new Response(child.stdout).text(), new Response(child.stderr).text()
    ]);
    const report = JSON.parse(stdout) as { status?: string; checked?: {family?: string}; errors?: Array<{code?:string}> };
    const errors = (report.errors || []).slice(0, 12).map(x => x.code || 'UNKNOWN');
    const outcome = `RustySpork offline preflight: ${report.status || 'UNKNOWN'} (exit ${code}, family ${report.checked?.family || 'unknown'})`;
    ctx.ui.notify(outcome + (errors.length ? ` — ${errors.join(', ')}` : ''),
      code === 0 && report.status === 'PASS' ? 'info' : 'error');
    if (stderr.trim()) ctx.ui.notify(`RustySpork preflight stderr: ${stderr.slice(0, 400)}`, 'error');
  } catch (error) {
    ctx.ui.notify('RustySpork preflight unavailable: ' + String(error).slice(0,350), 'error');
  }
}

export default function registerRustySpork(pi: ExtensionAPI): void {
  pi.registerCommand('rustyspork', {
    description: 'RustySpork OMP proposal-only safety and contract preflight; zero model calls or weight writes',
    handler: async (input, ctx) => {
      const value = input.trim();
      if (value === 'status') {
        ctx.ui.notify('RustySpork M0 plan-only tools installed. No OMP swarm inference, GGUF editing, GPU benchmark, API billing or donor access is authorized.', 'info');
      } else if (value.startsWith('check ')) {
        await check(value.slice(6).trim(), ctx);
      } else {
        ctx.ui.notify('Usage: /rustyspork status | /rustyspork check <workspace-relative-proposal.json>', 'info');
      }
    }
  });
}
