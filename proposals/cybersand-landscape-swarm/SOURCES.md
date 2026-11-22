# CALS-001 — Inspected source ledger, compatibility and open questions

**Read-only source inventory conducted:** 2026-11-22.  
**Status:** These observations are based on repository files and metadata; **none is a live OMP/GPTopus/CyberSand integration test**. Source may advance after the recorded commits.

## 1. Baselines and provenance

| Source | Inspected identity | Design role |
|---|---|---|
| [techrote/piplugs](https://github.com/techrote/piplugs) | Initially empty repository with intended default `main` | New proposal / future OMP plugin home |
| [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) | `ad9206d87c1685d539312e9a0f750dc6c526dd6f` | Active native orchestration, task/agent capabilities |
| [techrote/Chlaude-GPTopus](https://github.com/techrote/Chlaude-GPTopus) | `edd9392eae931ef19db82c84eb4d6d1167583fc4` | Worker policies, key split, quota/response accounting |
| [techrote/cybersand](https://github.com/techrote/cybersand) | `00cdb02f103265b6dc5224c68283e9a0c8cb449f` | Existing native world and authoring contracts |
| [CyberSecurityChuck/Oh-My-PI](https://github.com/CyberSecurityChuck/Oh-My-PI) | `0b1649784a9f8812f45a3525d3c797f7a6157974` | Historical `swarm-extension` design reference only |

A future implementation must freeze the **actual** checked-out source SHA and binaries. This document's SHA is an inspection baseline, not authority to assume unmerged code was accepted.

## 2. GPTopus — what actually exists

- [README and worker table](https://github.com/techrote/Chlaude-GPTopus/blob/main/README.md): Six workers: `sol`, `astra`, `luna`, `flex6-1`, `daily-astrafree` and `daily-terrafree`. Two separate API key profiles, an OpenAI Responses bridge, configurable service tiers, usage diagnostics and local tests. README reports 31 passing local Node tests, but those tests were **not executed** during this plan.
- [`plugins/openai-workers/hooks/register.js`](https://github.com/techrote/Chlaude-GPTopus/blob/main/plugins/openai-workers/hooks/register.js): Claude Code native mod hook for six named subagents and provider routing; model/tier configuration, max steps, timeout, handback. **Not an OMP extension entry point.**
- [`plugins/openai-workers/hooks/step.js`](https://github.com/techrote/Chlaude-GPTopus/blob/main/plugins/openai-workers/hooks/step.js): Turn-step continuation, OpenAI function-call translation and Claude subagent handback; **not portable as-is**.
- [`plugins/openai-workers/hooks/tools.js`](https://github.com/techrote/Chlaude-GPTopus/blob/main/plugins/openai-workers/hooks/tools.js): Strict positive tool list `Read`, `Edit`, `Write` and `Bash` with argument filtering. OMP has a different tool/permitted-process surface.
- [`plugins/openai-workers/bridge/openai.mjs`](https://github.com/techrote/Chlaude-GPTopus/blob/main/plugins/openai-workers/bridge/openai.mjs): Free/straight key profile selection, OpenAI HTTP Responses create/poll/cancel, tier validation, model estimates, normalization. Source prices/models/tiers must be rechecked before billing; request mode uses `background: true` / `store: true`.
- [`plugins/openai-workers/bridge/usage.mjs`](https://github.com/techrote/Chlaude-GPTopus/blob/main/plugins/openai-workers/bridge/usage.mjs): Local protected free-key quota groups; UTC-day attribution; lock-directory serialization; in-flight tokens; response-ID deduplication; conservative timeout/missing usage; fail-closed ledger corruption.
- [`plugins/openai-workers/bridge/server.mjs`](https://github.com/techrote/Chlaude-GPTopus/blob/main/plugins/openai-workers/bridge/server.mjs): Node MCP stdio bridge, paginated responses and usage diagnostics. May be a fallback donor if an OMP-specific provider adapter is needed.
- [Quotas and billing](https://github.com/techrote/Chlaude-GPTopus/blob/main/docs/QUOTAS_AND_BILLING.md): 250k premium and 2.5M Terra nominal daily targets; local default 10% overrun allowance, 12k-token reservation, 16 in-flight guard; complimentary-programme eligibility **not promised**; `$88` monthly field is informational, not a payment limit.
- [Architecture/security](https://github.com/techrote/Chlaude-GPTopus/blob/main/docs/ARCHITECTURE.md) and [configuration](https://github.com/techrote/Chlaude-GPTopus/blob/main/docs/CONFIGURATION.md): Claude handles tool authorization; two keys never silently fall back; keys stored via Windows DPAPI or environment on other platforms.

**Important GPTopus reuse risk:** Its local ledger does not account for arbitrary external clients or native OMP requests on the same key. Either unify cross-host admissions with compatibility tests or conservatively partition budgets. Do not call `OPENAI_API_KEY` free merely because it is a distinct credential.

**License:** [GPTopus plugin license](https://github.com/techrote/Chlaude-GPTopus/blob/main/plugins/openai-workers/LICENSE) is MIT. Preserve attribution and license text if implementation later copies or adapts source. Current docs are *descriptions*, not copied implementation.

## 3. Oh-My-PI — existing native features

- [Active repository](https://github.com/can1357/oh-my-pi): the modern upstream differs from the older fork. Its maintained `task` system is the logical orchestration substrate, not the historical optional swarm extension.
- [Native task tool](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md): Parallel child agents, `tasks[]` batching, optional background work, agent output/history, `task.maxConcurrency`, model routing constraints and optional workspace isolation. Documentation describes default concurrency of 32; for CALS use a smaller explicit cap. Child default model/override and tool capability must be tested on the exact installed build.
- [Agent Hub](https://github.com/can1357/oh-my-pi/blob/main/docs/agent-hub.md): live roster, activity, transcript, human steering, killing/revival and `agent://` communication. More appropriate for creative negotiation than fixed DAG waves.
- [Extension authoring](https://github.com/can1357/oh-my-pi/blob/main/docs/skills/authoring-extensions.md): TypeScript extension factories, commands, tool registration, hooks and per-project plugin discovery. Exact supported dispatch intercept semantics **not established** by this inspection.
- [Native OMP worker docs](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md): headless subagent tool approval can be forced to `yolo`. Safe read-only behavior therefore needs actual sandbox/tool controls, not prompt assertions. Per-call model overrides may require explicit host settings.
- [`workflowz` and `orchestrate` intent routing](https://github.com/can1357/oh-my-pi/blob/main/docs/magic-keywords.md): Existing native workflow mechanisms worth proving before coding another scheduler.
- [OMP MIT license](https://github.com/can1357/oh-my-pi/blob/main/LICENSE): credit and preserve notices for any adapted upstream code.

**Old swarm-extension, inspected and rejected as foundation:** [fork tree](https://github.com/CyberSecurityChuck/Oh-My-PI/tree/main/packages/swarm-extension) and [upstream deletion](https://github.com/can1357/oh-my-pi/commit/b0a94a8fc003dfa1164cca6c508772577f68ec7b). It has YAML dependency graphs and parallel waves, but state loads are not execution resume, agents share an uncoordinated filesystem, and dependent waves proceed after failures. [Upstream issue #7895](https://github.com/can1357/oh-my-pi/issues/7895) documents the removal and points toward native task orchestration.

## 4. CyberSand — current source boundaries

- [Shared Workbench data authority](https://github.com/techrote/cybersand/blob/main/docs/architecture/shared-workbench-authoring-data.md): Distinguishes procedural/ordinary **baseline**, acknowledged ordered authored edits, derived preview and **live evolving session**. Native C++/existing worker owns real material; queued edits are not applied proof.
- [Generated playable maps](https://github.com/techrote/cybersand/blob/main/docs/systems/explore001-generated-playable-maps.md): GEN-007 final `play` plane → existing Workbench; generated-start v1 wraps unchanged Setup-v2. Named Save records authored start, not evolved dynamic state. Existing runtime must verify generator identity and bounded export/reopen.
- [Generated map codec](https://github.com/techrote/cybersand/blob/main/godot/scripts/workbench_generated_map.gd): `cybersand-generated-start-v1`, embedded recipe/provenance and receipt limits; native recipe hashes and reconstructible bounded content.
- [Workbench Setup v2](https://github.com/techrote/cybersand/blob/main/godot/scripts/workbench_setup.gd): `MAX_RUNS`/`MAX_STAMPS` of 32,768 and a 1 MiB JSON budget in source. Installed native bridge capabilities and actual validators are definitive; never equate 32,768 stamps to unrestricted pixel capacity.
- [Architectural Generator](https://github.com/techrote/cybersand/blob/main/docs/systems/architectural-generator.md): Declarative schema-4 architecture compilation, versioned native modules and a real Workbench generated-preview path. The page also documents proposed 80-Gentek expansion in distinct Draft/HOLD integration candidates. This plan **does not assume all 80 are accepted into main**.
- [Workbench generation tools](https://github.com/techrote/cybersand/blob/main/godot/scripts/worldgen_workbench_tools.gd): Operates on copied plans/recipes and diagnostics; no native World pointer in authoring background jobs.
- [Example native recipes](https://github.com/techrote/cybersand/tree/main/examples/worldgen): Source examples include `architectural-three-style.json`, typed/semantic and grammar recipes, for schema/execution probes.
- [Landscape qualification runner](https://github.com/techrote/cybersand/blob/main/tools/qualify_workbench_landscapes.py): Source-bound large-map test support, real fresh Godot processes and preserved evidence. Must be exercised on a matching built runtime to establish actual results.
- [World-art capture](https://github.com/techrote/cybersand/blob/main/godot/tools/world_art_capture.gd): Candidate capture interface to inspect in M0, not automatically asserted to support arbitrary external CALS proposals.
- [World-design pack adapter](https://github.com/techrote/cybersand/blob/main/godot/tools/world_design_pack_adapter.gd): **Presentation-only** immutable native-ID RG8 raster adapter; no World material writes. Do not confuse its rendering with a live level import.
- [World-design atlas](https://github.com/techrote/cybersand/tree/main/docs/world-design) and [QUALITY_BAR](https://github.com/techrote/cybersand/blob/main/docs/world-design/QUALITY_BAR.md): 15 themed design-only collections with eight proposals each; original quality bar has seven visual dimensions and explicit native/source-vs-schematic evidence boundaries. Do not automatically publish SANDMAPS reference art.

**Existing owner roadmap:** [WORLD-STEER-001 #549](https://github.com/techrote/cybersand/issues/549) and [WORLD-STEER-BATCH-001 #579](https://github.com/techrote/cybersand/issues/579) already propose curated design knowledge, native grid batches and staged collaborative authoring. These are roadmap/design authority, not blanket permission to start related training experiments or assume all Draft features exist.

**Web scope:** [Web threading guide](https://github.com/techrote/cybersand/blob/main/docs/operations/web-threading.md) and [build guide](https://github.com/techrote/cybersand/blob/main/docs/operations/github-development-and-release.md) document separate compatibility/threaded profiles and current build issues. The existing export runs a Web demonstrator, not the complete ordinary authoring Workbench. M0/M1–M6 must not depend on Web restoration.

## 5. Unverified assumptions and research tasks

| Assumption/question | Present disposition | Required evidence |
|---|---|---|
| Can OMP truly bind independent OpenAI keys and enforce a budget **before each** native `task` model call? | **UNKNOWN** | Executed minimal OMP extension/provider spike with mocked endpoints and no unintended request |
| Can an OMP plugin intercept actual native worker retry/revival calls for quota checks? | **UNKNOWN** | Crash/retry/resume tests, source-matched host instrumentation |
| Can GPTopus's free-key ledger be shared unmodified across simultaneous Claude and OMP processes? | **UNSAFE TO ASSUME** | Cross-process schema/lock/usage/idempotency migration suite |
| Do current OpenAI model IDs, tiers, quotas and complimentary entitlements match GPTopus's current constants? | **ACCOUNT/UPSTREAM DEPENDENT** | Current OpenAI docs plus actual account entitlement, approved small live smoke |
| Can CALS install material changes headlessly using an **existing** CyberSand Workbench interface? | **UNKNOWN** | Existing import/install executable proof; otherwise manual-owner import |
| Which GEN-007/Gentek modules are available in accepted main and in installed native binaries? | **MUST DISCOVER** | Catalogue and runtime fingerprint readback, actual generator execution |
| Can required traversable routes be proven for chosen actor mechanics? | **NOT YET** | Selected player collision profile, actual native/collision/traversal test |
| Are live Water/Brine/degradation setups stable across accepted gameplay ticks? | **NOT TESTED BY PLAN** | t=0/60/600+ source-matched tests and human assessment |
| Does OMP guarantee review-only child isolation when shell tools are enabled? | **NO PROMPT-ONLY ASSURANCE** | OS permission/worktree enforcement tests, capability audit |
| Will multi-agent negotiation improve level coherence? | **HYPOTHESIS** | Matched baseline vs negotiated pilot, objective and blind subjective evidence |

## 6. Publication and claims discipline

This source ledger supports a **plan**, not a working implementation. It does not claim successful OMP installation, provider calls, a compiled native engine, a rendered world or a playable Workbench saved start.

Future work should append an execution ledger with: source/ref/date, commands run, exit codes, actual passed/failed assertions, real artifact SHA-256s, model/provider/tier identities, cost/usage evidence, reviewer identity and decisions. Mark mocks, static analysis, read-only evidence, real runtime tests and owner acceptance separately.

If any source or runtime differs from the inspected identity, refresh relevant contracts and rerun required checks. Do not use an older source's passing test or documented feature to qualify a newer implementation.

**Plan links:** [Overview](README.md) · [Architecture](ARCHITECTURE.md) · [Contracts](CONTRACTS.md) · [Delivery plan](DELIVERY-PLAN.md) · [Pilot](PILOT.md).
