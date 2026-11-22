import { expect, it } from "bun:test";
import { mkdtemp, symlink, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import register from "../src/index.ts";

function makeHarness(cwd: string) {
  const messages: Array<{ message: string; level: string }> = [];
  let command: any;
  register({ registerCommand(name: string, implementation: any) {
    expect(name).toBe("cals");
    command = implementation;
  }} as any);
  const ctx = { cwd, ui: { notify(message: string, level: string) { messages.push({ message, level }); } } } as any;
  return { command, ctx, messages };
}

it("registers status without dispatching a model or World operation", async () => {
  const { command, ctx, messages } = makeHarness(process.cwd());
  await command.handler("status", ctx);
  expect(messages.at(-1)?.message).toContain("NOT qualified");
});

it("rejects a path that lexically leaves its workspace", async () => {
  const { command, ctx, messages } = makeHarness(process.cwd());
  await command.handler("check ../../../../../etc/passwd", ctx);
  expect(messages.at(-1)?.level).toBe("error");
  expect(messages.at(-1)?.message).toContain("inside the current workspace");
});

it("rejects symlinked candidate escaping its workspace", async () => {
  const root = await mkdtemp(join(tmpdir(), "cals-bun-test-"));
  const external = await mkdtemp(join(tmpdir(), "cals-external-"));
  try {
    await writeFile(join(external, "secret.json"), JSON.stringify({ secret: "no" }));
    await symlink(join(external, "secret.json"), join(root, "linked.json"));
    const { command, ctx, messages } = makeHarness(root);
    await command.handler("check linked.json", ctx);
    expect(messages.at(-1)?.level).toBe("error");
    expect(messages.at(-1)?.message).toContain("inside the current workspace");
  } finally {
    await Promise.all([rm(root, { recursive:true, force:true }), rm(external, { recursive:true, force:true })]);
  }
});

it("runs the bundled Python validator against a valid workspace fixture", async () => {
  const root = join(import.meta.dir, "..");
  const { command, ctx, messages } = makeHarness(root);
  await command.handler("check fixtures/iron-wound-valid.json", ctx);
  expect(messages.at(-1)?.level).toBe("info");
  expect(messages.at(-1)?.message).toContain("PASS");
});
