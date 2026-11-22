# piplugs

Planning and development home for **Oh-My-PI (OMP) extensions, skills and integrations**.

## Active proposal: CyberSand Landscape Swarm (CALS-001)

**Status: DESIGN / NOT IMPLEMENTED.** This repository currently contains a source-grounded architecture and implementation programme, **not** an installed or working OMP plugin.

The goal is to use **OMP-native subagents and peer communication**, reuse the useful **Chlaude-GPTopus** worker-policy / credential / quota logic where technically appropriate, and orchestrate a group of creative specialists to author coherent, advanced, playable **CyberSand** landscapes. CyberSand itself stays the unmodified authoritative editor, native generator, renderer and simulation runtime. The browser/Web build is optional, not a prerequisite.

Start with [CALS-001 proposal overview](proposals/cybersand-landscape-swarm/README.md).

| Document | Purpose |
|---|---|
| [Architecture](proposals/cybersand-landscape-swarm/ARCHITECTURE.md) | Boundaries, agent organisation, routing, security, integration and design decisions |
| [Protocols and data contracts](proposals/cybersand-landscape-swarm/CONTRACTS.md) | World Bible, region ownership, proposals, native transactions, run records and failure semantics |
| [Engineering plan](proposals/cybersand-landscape-swarm/DELIVERY-PLAN.md) | Milestones, ordering, tests, gates, budgets, risks and definition of done |
| [First landscape pilot](proposals/cybersand-landscape-swarm/PILOT.md) | Worked 2048×1024 pilot, collaboration choreography, output requirements and evaluation |
| [Source ledger](proposals/cybersand-landscape-swarm/SOURCES.md) | Inspected repositories and files, versions, established facts, uncertainties and further research |

### Research programme

- [CALS-RESEARCH-001 — Beyond orchestration](research/CALS-RESEARCH-001.md): ten architectural-intelligence directions, four controlled experiments (experience-first, structural grammar, physics-led design, adaptive swarm), evaluation controls and dependencies. Research is recorded; experiments are not yet executed.

### Project guardrails

- **No CyberSand changes** in this planning delivery; no second World, simulation kernel, editor, network server or browser port.
- **No production claim:** source references and design schemas are not evidence of running OMP agents, working OpenAI API credentials or importable CyberSand artifacts.
- **No unbounded inference or hidden credential fallback.** Paid model dispatch requires an enforceable budget/authorization gate; a token-ledger target is not an account-level billing guarantee.
- **No automatic publication or merges** to CyberSand; artwork and private source references stay local unless specifically approved.
- **Reassess live source/API compatibility before implementation.** OMP's native tooling and model APIs change, and the old standalone swarm-extension is not maintained in current upstream.

Source projects: [Oh-My-PI](https://github.com/can1357/oh-my-pi), [Chlaude-GPTopus](https://github.com/techrote/Chlaude-GPTopus), [CyberSand](https://github.com/techrote/cybersand).

CALS-001 was drafted on 2026-11-22. See the [source ledger](proposals/cybersand-landscape-swarm/SOURCES.md) for the inspected source commits and the distinction between verified source behavior and proposed new functionality.
