---
name: landscape-studio
description: Coordinate a bounded multi-agent 2D CyberSand landscape concept through OMP-native subagents, negotiate joint contracts and inspect offline results before any native or paid work.
---

# CALS Landscape Studio — packaged OMP skill (M1 candidate)

**Status:** Experimental OMP skill and offline contract tools. Native CyberSand and paid worker routing are unimplemented. Never claim a geometric contract is a playable level.

## Workflow

1. **Clarify intent.** Ask for missing essential game/traversal constraints only if the brief cannot support a meaningful dry-run. Preserve the requested artistic character, landmarks, desired negative space and true orthographic side-elevation viewpoint.
2. **Freeze design contract.** Establish canvas, source SHA, region leases, protected space, one or more explicitly ordered routes and shared connector/socket positions in a World Bible. Use immutable/revisioned files; no concurrent write to the same document.
3. **Delegate through built-in OMP task.** Use named specialists for architecture, environment and traversal. Spawn in parallel only with disjoint ownership and pinned shared context. Consult actual installed task schema and permission/isolation capabilities; do not invent OMP calls. Use existing `agent://` messaging for negotiated revisions when supported.
4. **Integrate offline proposals.** A single coordinator collects results and runs the standard-library validator on proposed region/route/joint contracts. A failed worker, stale lease, mismatched socket or protected-area claim blocks integration. Route sequence consistency is only a region-graph-level check.
5. **Inspect critically.** Compare alternatives without artificially flattening difference. Separate hard region/route checks from CyberSand's seven-axis visual rubric. Don't infer structural support, gameplay, physics or material validity from text or a synthetic diagram.
6. **Native admission, only if actually available.** Confirm the accepted CyberSand Git SHA, compiled Godot/native fingerprint and supported GEN-007 recipe before preview/import. Require genuine material readback, render provenance and fresh-process Save/reopen. If the engine isn't installed, stop at a clearly labeled offline candidate.

## Immediate reproducible offline command

From a piplugs checkout, `/cals check plugins/cals/fixtures/iron-wound-valid.json` calls the optional extension validator. Otherwise run:

```sh
python3 plugins/cals/tools/validate_contracts.py plugins/cals/fixtures/iron-wound-valid.json
python3 -m unittest discover -s plugins/cals/tests -v
```

A full install of this package may not contain the project-level experiment fixtures; direct a user to an appropriate local workspace fixture rather than pretending they exist. `/cals status` is diagnostics only, not credential verification.

## Boundaries and handback

- **No CyberSand source edits**, second World, browser build, unmerged catalogue assumptions, external photo upload or independent scheduler.
- **No paid inference by default.** GPTopus's free-key ledger is not ported to OMP yet. No model/key/tier fallback on missing entitlements; prompts cannot enforce quota or sandbox protections.
- Agent tool permissions and read-only critics require actual enforced OMP/OS access controls; do not claim safety from instructions alone.
- Record explicit source hashes, tested commands, outputs, failures, unresolved joints and receipt types. Never substitute offline PASS for native/world admission.

Full project design: [CALS-001](https://github.com/techrote/piplugs/tree/main/proposals/cybersand-landscape-swarm) and [CALS-RESEARCH-001](https://github.com/techrote/piplugs/blob/main/research/CALS-RESEARCH-001.md).
