import { expect, it } from 'bun:test';
import { mkdtemp, symlink, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import register from '../src/index.ts';

function harness(cwd: string) {
  const messages: Array<{message: string; level: string}> = [];
  let command: { handler(input: string, ctx: any): Promise<void> } | undefined;
  register({ registerCommand(name: string, impl: any) {
    expect(name).toBe('rustyspork'); command = impl;
  }} as any);
  return {
    command: command!,
    ctx: { cwd, ui: { notify(message: string, level: string) { messages.push({message, level}); } } } as any,
    messages,
  };
}

it('registers an inert diagnostics command without model calls', async () => {
  const {command,ctx,messages} = harness(process.cwd());
  await command.handler('status', ctx);
  expect(messages.at(-1)?.message).toContain('No OMP swarm inference');
});

it('accepts bounded synthetic Funnel and REAP fixtures without weight access', async () => {
  const root = join(import.meta.dir, '..');
  const h = harness(root);
  for (const p of ['fixtures/funnel-plan.json','fixtures/lfm-q6-reap-plan.json']) {
    await h.command.handler('check '+p, h.ctx);
    expect(h.messages.at(-1)?.level).toBe('info');
    expect(h.messages.at(-1)?.message).toContain('PASS');
  }
});

it('rejects unsafe frozen-target edit and unapproved weight-write plans', async () => {
  const root = join(import.meta.dir, '..');
  const h = harness(root);
  for (const p of ['fixtures/funnel-plan-unsafe.json','fixtures/lfm-q6-reap-plan-unsafe.json']) {
    await h.command.handler('check '+p, h.ctx);
    expect(h.messages.at(-1)?.level).toBe('error');
    expect(h.messages.at(-1)?.message).toContain('FAIL');
  }
});

it('rejects workspace path traversal on Windows and Linux', async () => {
  const h = harness(process.cwd());
  await h.command.handler('check ../../../../../etc/passwd.json', h.ctx);
  expect(h.messages.at(-1)?.level).toBe('error');
  expect(h.messages.at(-1)?.message).toContain('outside the current workspace');
});

it('rejects symlinked candidate path outside workspace', async () => {
  const root = await mkdtemp(join(tmpdir(),'rsn-omp-test-'));
  const other = await mkdtemp(join(tmpdir(),'rsn-external-'));
  try {
    await writeFile(join(other,'secret.json'), '{"secret":"do-not-read"}');
    await symlink(join(other,'secret.json'),join(root,'linked.json'));
    const h = harness(root);
    await h.command.handler('check linked.json', h.ctx);
    expect(h.messages.at(-1)?.level).toBe('error');
    expect(h.messages.at(-1)?.message).toContain('outside the current workspace');
  } finally {
    await Promise.all([rm(root,{recursive:true,force:true}),rm(other,{recursive:true,force:true})]);
  }
});

it('refuses non-JSON or missing proposal paths', async () => {
  const h = harness(process.cwd());
  await h.command.handler('check file.txt', h.ctx);
  expect(h.messages.at(-1)?.message).toContain('Usage:');
  await h.command.handler('check missing.json', h.ctx);
  expect(h.messages.at(-1)?.level).toBe('error');
});
