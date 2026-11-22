# CALS M0 — capability checkpoint

**Checkpoint:** 2026-11-22. **Status:** M0 partial, source intake plus successful Linux/Windows OMP package smoke and offline proof; no model-driven agent conversation, native Godot execution or paid provider integration yet.

| Capability | Source observation | Execution status |
|---|---|---|
| OMP native `task`, optional parallel batching, `agent://` and Agent Hub | [OMP task docs](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md) and [Agent Hub](https://github.com/can1357/oh-my-pi/blob/main/docs/agent-hub.md) at inspected SHA `ad9206d87c1685d539312e9a0f750dc6c526dd6f` | **SOURCE CONFIRMED; runtime UNTESTED** |
| OMP native project skill discovery | [Skills docs](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md): `.omp/skills/<name>/SKILL.md` | **LINUX + WINDOWS CI VERIFIED:** OMP 19.1.0 / Bun 1.4.4, `omp skill list --json`; [Linux](https://github.com/techrote/piplugs/actions/runs/45074193517) / [Windows](https://github.com/techrote/piplugs/actions/runs/45074193468) |
| GPTopus quota/key split | [Chlaude-GPTopus](https://github.com/techrote/Chlaude-GPTopus), `usage.mjs`, `openai.mjs` at inspected `edd9392eae931ef19db82c84eb4d6d1167583fc4` | **SOURCE CONFIRMED; no OMP port and no billed call** |
| CyberSand GEN-007/Workbench generated-start | [CyberSand contracts](https://github.com/techrote/cybersand/blob/main/docs/systems/explore001-generated-playable-maps.md) at inspected main `00cdb02f103265b6dc5224c68283e9a0c8cb449f` | **SOURCE CONFIRMED; native execution UNTESTED** |
| Offline CALS document validator | `tools/validate_contracts.py`, route chain and fixture pair | **32/32 Python checks passed on Linux and Windows**; [Linux](https://github.com/techrote/piplugs/actions/runs/45074193443) / [Windows](https://github.com/techrote/piplugs/actions/runs/45074193468); includes expected negative fixture |
| OMP binary | No local executable; Linux CI installed pinned `@oh-my-pi/pi-coding-agent@19.1.0` | **LINUX + WINDOWS CI VERIFIED** OMP pinned package install and skill discovery; interactive owner session unavailable |
| OMP package link, skill and local command | `plugins/cals/package.json`, `src/index.ts`, `skills/landscape-studio`, `agents/` | **LINUX + WINDOWS CI VERIFIED:** [Linux](https://github.com/techrote/piplugs/actions/runs/45074193517) / [Windows](https://github.com/techrote/piplugs/actions/runs/45074193468); independent package link and 4/4 Bun extension tests. Linux role manifests validated; live agent messaging/permissions untested. |
| Godot executable/native CYSD runtime | No `godot` executable in this execution container | **UNAVAILABLE** |
| Paid request-level policy enforcement, cross-host ledger sharing | Need actual provider/auth lifecycle spike | **BLOCKED / NOT IMPLEMENTED** |
| Noninteractive Workbench native material application | [M0-NATIVE-HANDOFF](M0-NATIVE-HANDOFF.md) identifies existing genuine GEN-007 install/reopen test and separate large-landscape qualification runner | **SOURCE REVIEWED, not executed** |

### Evidence and immediate next engineering gates

The tests exercise only typed design-document consistency: correct and mismatched 2048×1024 Iron Wound regional sockets, graph-level region connectivity, lease freshness, protected-write checks and malformed inputs. Passing them **cannot** certify full-res native material IDs, real traversal, rendering or saved-start persistence.

**Next host spike:** Install or run a pinned OMP version in the intended Windows/OMP environment; run `omp skill list`, verify exact `task`/`agent://` behavior, spawn two confined agents with a test shared joint and deliberately refuse an unauthorized edit. Record actual command, version, tool permissions, logs and exit codes.

**Next native spike:** Follow [M0-NATIVE-HANDOFF.md](M0-NATIVE-HANDOFF.md): pin CyberSand source+native binaries; use the existing GEN-007 512-square install/paint/save/fresh-process reopen test and the separately provenance-verified large-landscape runner with isolated user data. No native command has yet been run by CALS. Do not add APIs or claim import success if absent.

**Paid route gate:** Keep external API dispatch disabled by default until actual request-before-charge authorization, per-key account routing, response settlement and cross-process quota concurrency are verified. No private-gallery uploads, unapproved automated merges or Web restoration are part of this slice.
