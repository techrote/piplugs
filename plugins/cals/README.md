# CALS M0/M1 — small external CyberSand landscape-contract pilot

**Status:** Offline proof only; no installed OMP extension, hosted model calls, CyberSand native execution or playable world produced.

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

The experimental skill resides at [`.omp/skills/landscape-studio/SKILL.md`](../../.omp/skills/landscape-studio/SKILL.md), a **native project skill** discoverable when OMP is launched in this repository with OMP-native skill discovery enabled. It instructs agents to negotiate first and treat receipts as authoritative. Use `omp skill list` or equivalent current-version discovery to verify it on an actual OMP installation; this environment has not done so.

This is not yet a packaged OMP plugin. Installation into CyberSand, GitHub/other repositories or a shared user profile is explicitly postponed until the M0 API/permissions spike proves a safe integration route. The skill does not enforce budgets or filesystem permissions.

## Source identity and caveats

The sample includes an **illustrative** source SHA from the inspected CyberSand main; it does not imply a corresponding compiled native extension was loaded. Its material IDs are proposal fields only, not runtime-catalogue verification. The joint openings are declarations by agents; player clearance/route performance is untested.

See [M0 capabilities](M0-CAPABILITIES.md), [CALS contracts](../../proposals/cybersand-landscape-swarm/CONTRACTS.md), and [first pilot](../../proposals/cybersand-landscape-swarm/PILOT.md). Do not automatically adapt this offline schema into CyberSand's generated-start format.
