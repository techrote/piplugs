/** CALS M1: external, read-only OMP command surface. No providers or World writes. */
import type { ExtensionAPI, ExtensionCommandContext } from "@oh-my-pi/pi-coding-agent";
import { dirname, isAbsolute, relative, resolve } from "node:path";
import { realpath } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const PACKAGE_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const VALIDATOR = resolve(PACKAGE_DIR, "tools", "validate_contracts.py");

function within(path: string, root: string): boolean {
  const rel = relative(root, path);
  return rel === "" || (rel !== ".." && !rel.startsWith("../") && !rel.startsWith("..\\") && !isAbsolute(rel));
}

/** Only explicit /cals check reads a local fixture; it never executes user-supplied commands. */
async function checkFixture(raw: string, ctx: ExtensionCommandContext): Promise<void> {
  const filename = raw.trim();
  if (!filename || /[\r\n\0]/.test(filename)) {
    ctx.ui.notify("Usage: /cals check <workspace-relative-fixture.json>", "error");
    return;
  }
  const candidate = resolve(ctx.cwd, filename);
  try {
    // Resolve symlinks before reading anything: a lexical inside-path can escape.
    const [workspaceReal, candidateReal] = await Promise.all([
      realpath(ctx.cwd), realpath(candidate),
    ]);
    if (!within(candidateReal, workspaceReal)) {
      ctx.ui.notify("CALS check accepts files inside the current workspace only", "error");
      return;
    }
  } catch {
    ctx.ui.notify("CALS check cannot resolve the candidate fixture path", "error");
    return;
  }
  const configuredPython = process.env.CALS_PYTHON?.trim();
  const interpreter = configuredPython ? [configuredPython] : process.platform === "win32" ? ["py", "-3"] : ["python3"];
  try {
    const proc = Bun.spawn([...interpreter, VALIDATOR, candidate], {
      cwd: ctx.cwd,
      stdin: "ignore",
      stdout: "pipe",
      stderr: "pipe",
    });
    const [exitCode, stdout, stderr] = await Promise.all([
      proc.exited,
      new Response(proc.stdout).text(),
      new Response(proc.stderr).text(),
    ]);
    const report = JSON.parse(stdout) as { status?: string; errors?: Array<{ code?: string }> };
    const errorCodes = (report.errors ?? []).slice(0, 12).map(x => x.code ?? "UNKNOWN");
    ctx.ui.notify(
      "CALS offline contract: " + (report.status ?? "UNKNOWN") + " (exit " + exitCode + ")" +
        (errorCodes.length ? " — " + errorCodes.join(", ") : ""),
      exitCode === 0 && report.status === "PASS" ? "info" : "error",
    );
    if (stderr.trim()) ctx.ui.notify("CALS validator stderr: " + stderr.slice(0,500), "error");
  } catch (error) {
    ctx.ui.notify("CALS validator unavailable: " + String(error).slice(0,350), "error");
  }
}

export default function registerCals(pi: ExtensionAPI): void {
  pi.registerCommand("cals", {
    description: "CALS landscape studio: scope and local contract verification (no model calls)",
    handler: async (input, ctx) => {
      const [subcommand, ...rest] = input.trim().split(/\s+/);
      switch (subcommand) {
        case "check":
          await checkFixture(rest.join(" "), ctx);
          return;
        case "status":
          ctx.ui.notify("CALS M1 offline tools available; OMP agents, native CyberSand, billing and Workbench import are NOT qualified by this command.", "info");
          return;
        default:
          ctx.ui.notify("CALS: /cals status | /cals check <workspace-relative-fixture.json>. Use /skill:landscape-studio for planning.", "info");
      }
    },
  });
}
