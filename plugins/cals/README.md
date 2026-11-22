# CALS M0/M1 — small external CyberSand landscape-contract pilot

**Status:** Offline proof plus an installable OMP M1 package candidate. Linux and Windows OMP 19.1.0 skill discovery, separate-project plugin linking and four command tests have passed GitHub CI; live agent conversations, GPTopus paid worker routing, CyberSand native execution and playability remain unqualified.

This directory begins the implementation of the [CALS-001 plan](../../proposals/cybersand-landscape-swarm/README.md) and [CALS-RESEARCH-001](../../research/CALS-RESEARCH-001.md) without modifying CyberSand.

## What works now

The standard-library Python validator reads a deliberately narrow **offline contract fixture**. It checks 3 proposed districts, two exact joint/socket agreements, proposal revision/lease claims, bounded edits, protected empty space and connectivity of the **region adjacency graph**. This is enough to demonstrate one valuable coordination invariant and produce machine-readable rejection reasons; it is **not** a GEN-007 parser or a pixel/physics validator.

```sh
python3 plugins/cals/tools/validate_contracts.py plugins/cals/fixtures/iron-wound-valid.json
# PASS, exit 0
python3 plugins/cals/tools/validate_contracts.py plugins/cals/fixtures/iron-wound-mismatched-socket.json
# FAIL, exit 1: SOCKET_MISMATCH
python3 -m unittest discover -s plugins/cals/tests -v
```

`tools/make_fixture.py` deterministically regenerates both fixtures and their canonical World Bible hash; run it when intentionally changing examples, then rerun tests. No network calls or external Python dependencies are needed.

## OMP skill

The experimental skill resides at [`.omp/skills/landscape-studio/SKILL.md`](../../.omp/skills/landscape-studio/SKILL.md), a **native project skill** discoverable when OMP is launched in this repository with OMP-native skill discovery enabled. It instructs agents to negotiate first and treat receipts as authoritative. `omp skill list --json` has succeeded on CI-installed OMP 19.1.0; real model-driven agent execution remains untested.

### Optional packaged OMP plugin (experimental)

The package at `plugins/cals/` includes an OMP `omp.extensions` manifest, `/cals status` and `/cals check` commands, a `skills/landscape-studio/SKILL.md` and four read-only specialist roles. The fixed Python validator executes without a shell, resolves symlinks and refuses fixture paths outside the working directory. It **does not** dispatch inference or modify CyberSand.

From a checkout of `piplugs` with OMP installed:

```sh
omp plugin link ./plugins/cals
omp plugin list
omp skill list --json
```

After loading the extension in the interactive OMP session, run `/cals status` or `/cals check plugins/cals/fixtures/iron-wound-valid.json` (paths are relative to the active project/workspace; for an installed package in another project, provide a fixture there). On Windows the extension uses `py -3` by default, or a trusted `CALS_PYTHON` interpreter executable.

**Verified GitHub CI:** [Linux OMP run #45074193517](https://github.com/techrote/piplugs/actions/runs/45074193517) and [Windows OMP run #45074193468](https://github.com/techrote/piplugs/actions/runs/45074193468) both linked `@techrote/cals@0.1.0`, discovered the skill independently, and passed **four Bun tests**. Windows and Linux [offline Python CI](https://github.com/techrote/piplugs/actions/runs/45074193443) pass **32 tests** each. This verifies loading/registration and local contract checking, **not** live worker spawning, messaging, paid policies or CyberSand native execution. The four role manifests were shape-validated in Linux CI; OMP's live agent-discovery/permission enforcement still requires [issue #2](https://github.com/techrote/piplugs/issues/2).

## Source identity and caveats

The route contract now also supports an ordered `via_joint_ids` sequence. Matching named regions and sockets is **not** proof that a route is navigable inside those regions; missing chains receive a graph-only warning.

The sample includes an **illustrative** source SHA from the inspected CyberSand main; it does not imply a corresponding compiled native extension was loaded. Its material IDs are proposal fields only, not runtime-catalogue verification. The joint openings are declarations by agents; player clearance/route performance is untested.

For source-matched CyberSand tests, see the [M0 native qualification handoff](M0-NATIVE-HANDOFF.md): it identifies the existing `test_workbench_generator_installed.gd` and `qualify_workbench_landscapes.py` tests and separates GEN-007 from prepared Setup-v2 landscape validation. The procedures are source-reviewed only; no native Godot test has been run by CALS.

See [M0 capabilities](M0-CAPABILITIES.md), [CALS contracts](../../proposals/cybersand-landscape-swarm/CONTRACTS.md), and [first pilot](../../proposals/cybersand-landscape-swarm/PILOT.md). Do not automatically adapt this offline schema into CyberSand's generated-start format.
