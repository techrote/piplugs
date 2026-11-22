# CALS-001 — CyberSand Landscape Swarm for Oh-My-PI

**Classification:** PROPOSAL / architecture and implementation programme; not a working extension  
**Home:** [techrote/piplugs](https://github.com/techrote/piplugs)  
**Authoring target:** [techrote/cybersand](https://github.com/techrote/cybersand)  
**Worker-policy donor:** [techrote/Chlaude-GPTopus](https://github.com/techrote/Chlaude-GPTopus)  
**Orchestration host:** [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)  
**Reviewed:** 2026-11-22

## Mission

Build a **thin, optional OMP plugin/skill package** that coordinates multiple independently reasoning specialists to **plan, negotiate, construct, critique and selectively refine one coherent, traversable, orthographic 2D CyberSand landscape**. Use CyberSand's existing GEN-007 recipes, Gentek catalogue where available, material/paint authoring interfaces, native world ownership, preview, actual Godot captures and saved-start reconstruction. Do not build agent orchestration, a second level editor or a new simulation engine inside CyberSand.

The distinguishing requirement is **negotiated coherence**. Adjacent specialists must agree on shared interfaces, physical constraints, access paths, negative space and visual language. Independent stamps in adjacent rectangles are not enough.

### Guiding split

| Responsibility | Owner |
|---|---|
| Spawn, reuse, supervise, steer, message and isolate agents | **OMP native `task` / Agent Hub / `agent://` / `history://`** |
| Model profile, two-key routing, service-tier validation, quota admission and response accounting | **CALS external policy adapter**, adapted from Chlaude-GPTopus only where enforcement is verified |
| World Bible, region/joint contracts, synthesis, artist/critic prompts and revision policy | **CALS OMP skills + versioned files**, not CyberSand |
| Real generation, stored material authority, snapshots, paint, physics, rendering and Save/reopen | **Existing CyberSand**, unchanged |
| Human aesthetic approval, publication, destructive operations and spending permission | **Owner** |

## Critical design decisions

1. **Reuse OMP core; do not revive the removed old swarm-extension as a dependency.** The linked older implementation is a static DAG/parallel-wave runner with shared-file handoffs and weak failure propagation. Modern OMP supports native subagents, peer messaging, background jobs, isolation and Agent Hub supervision.
2. **Borrow GPTopus security/accounting semantics, not Claude Code hooks.** GPTopus's native mod `session.start`/`turn.step` bridge and tool names are not portable as-is. Port/test the small policy and accounting modules behind an OMP-compatible dispatch boundary.
3. **No prompts-as-security.** Model/provider/account choice, payment ceiling, write boundaries and native World writes need host-side enforcement; words in `SKILL.md` alone do not enforce them.
4. **One authority for material truth.** Agents produce candidate documents and native programs, not simultaneous direct edits to CyberSand's live World. A single accepted integration lane serializes actual mutations with receipts.
5. **Source and evidence first.** A schematic SVG, an AI artwork, a JSON recipe, a generated-play-plane readback and a real Godot render are different outputs. Label each honestly.
6. **Web restoration is independent.** The current Web demo is not the ordinary Workbench and its build workflow has known toolchain/coverage drift. No milestone depends on it.
7. **No automatic acceptance by vote.** Structural/physical rules are objective gates; aesthetic evaluation is evidence-backed, with explicit dissent and human final choice.

## Delivered planning documents

- [ARCHITECTURE.md](ARCHITECTURE.md): systems, topology, GPTopus porting seam, CyberSand coupling, boundaries and ADRs.
- [CONTRACTS.md](CONTRACTS.md): proposed versioned schemas, agent handoff, region leases, native receipts, evidence and recovery.
- [DELIVERY-PLAN.md](DELIVERY-PLAN.md): dependencies, milestones, tests, acceptance gates, rollback, release/non-release policy.
- [PILOT.md](PILOT.md): first 2048×1024 industrial sci-fi collaborative world, example assignments and measured comparison.
- [SOURCES.md](SOURCES.md): source commits, files inspected, existing contracts, draft features and uncertainties.

## Explicit non-goals

- No CyberSand source changes, Godot/GDExtension modifications, new HTTP/WebSocket control API, training system, distributed workers, 3D/perspective world, or automatic merging.
- No requirement to revive the Web/WASM build, run models from inside CyberSand, publish the ~400-image local SANDMAPS collection, or ship a giant plugin framework.
- No claim that a particular OpenAI key is free, a model or tier is currently entitled, or a locally calculated dollar estimate prevents an actual bill.
- No consumption of unmerged CyberSand branches by default. Candidates must be inventoried, explicitly enabled and identified by source SHA.

## Prototype selection

Start with **one director + three specialist workers + one independent critic**, all inside OMP, producing a **2048×1024 orthographic side-elevation landscape**. All construction happens in finite preview/proposal form until a controlled native integration pass verifies it. Compare this result with a same-budget independent-islands baseline, not only with screenshots from the swarm.

**Design status:** ready to review and to begin the bounded M0/M1 spike after explicit implementation approval. No runtime, credentials, model calls, patches, PRs or simulated world artifacts are created by this planning publication.
