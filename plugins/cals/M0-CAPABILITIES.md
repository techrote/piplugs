# CALS M0 — capability checkpoint

**Checkpoint:** 2026-11-22. **Status:** Partial M0 source intake, successful offline proof; no host/native runtime integration yet.

| Capability | Source observation | Execution status |
|---|---|---|
| OMP native `task`, optional parallel batching, `agent://` and Agent Hub | [OMP task docs](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md) and [Agent Hub](https://github.com/can1357/oh-my-pi/blob/main/docs/agent-hub.md) at inspected SHA `ad9206d87c1685d539312e9a0f750dc6c526dd6f` | **SOURCE CONFIRMED; runtime UNTESTED** |
| OMP native project skill discovery | [Skills docs](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md): `.omp/skills/<name>/SKILL.md` | **SOURCE CONFIRMED; runtime UNTESTED** |
| GPTopus quota/key split | [Chlaude-GPTopus](https://github.com/techrote/Chlaude-GPTopus), `usage.mjs`, `openai.mjs` at inspected `edd9392eae931ef19db82c84eb4d6d1167583fc4` | **SOURCE CONFIRMED; no OMP port and no billed call** |
| CyberSand GEN-007/Workbench generated-start | [CyberSand contracts](https://github.com/techrote/cybersand/blob/main/docs/systems/explore001-generated-playable-maps.md) at inspected main `00cdb02f103265b6dc5224c68283e9a0c8cb449f` | **SOURCE CONFIRMED; native execution UNTESTED** |
| Offline CALS document validator | `tools/validate_contracts.py` + fixture pair | **TESTED LOCALLY** via Python 3.13; see PR evidence |
| OMP binary | No `omp` executable in this execution container | **UNAVAILABLE** |
| Godot executable/native CYSD runtime | No `godot` executable in this execution container | **UNAVAILABLE** |
| Paid request-level policy enforcement, cross-host ledger sharing | Need actual provider/auth lifecycle spike | **BLOCKED / NOT IMPLEMENTED** |
| Noninteractive Workbench native material application | Requires verified existing source route and source-matched build | **UNTESTED** |

### Evidence and immediate next engineering gates

The tests exercise only typed design-document consistency: correct and mismatched 2048×1024 Iron Wound regional sockets, graph-level region connectivity, lease freshness, protected-write checks and malformed inputs. Passing them **cannot** certify full-res native material IDs, real traversal, rendering or saved-start persistence.

**Next host spike:** Install or run a pinned OMP version in the intended Windows/OMP environment; run `omp skill list`, verify exact `task`/`agent://` behavior, spawn two confined agents with a test shared joint and deliberately refuse an unauthorized edit. Record actual command, version, tool permissions, logs and exit codes.

**Next native spike:** Pin CyberSand source+binary SHA, test a small valid GEN-007 recipe using existing Godot tools, capture a genuine screenshot and establish whether a supported headless Workbench generated-start import exists. Do not add APIs or claim import success if absent.

**Paid route gate:** Keep external API dispatch disabled by default until actual request-before-charge authorization, per-key account routing, response settlement and cross-process quota concurrency are verified. No private-gallery uploads, unapproved automated merges or Web restoration are part of this slice.
