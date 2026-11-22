---
name: landscape-studio
description: Coordinate a bounded, external, multi-agent CyberSand landscape-design session using existing OMP task/agent tools; begin with offline region and connector contracts, not a new engine or paid swarm.
---

# CALS — Landscape Studio (M1 experimental skill)

**Status:** Planning and offline preflight only. This skill has not been smoke-tested in a running OMP session. It is not an OMP runtime extension, native CyberSand importer, sandbox or quota guard.

## Objective and boundaries

Use Oh-My-PI's **native** `task` subagents and `agent://` messaging to prepare a negotiated, coherent, true side-elevation 2D CyberSand landscape. Do not install a second World, create an engine-side scheduler, revive the Web build, or import unmerged CyberSand features. The **existing native Workbench** decides what actually applies. Never represent a JSON proposal, synthetic preview or offline region-graph pass as native playable evidence.

Read the current planning authority first:

- `research/CALS-RESEARCH-001.md` — ten research angles, four experimental questions.
- `proposals/cybersand-landscape-swarm/ARCHITECTURE.md` — ownership/agent boundaries.
- `proposals/cybersand-landscape-swarm/CONTRACTS.md` — durable proposed protocols (distinct from the offline fixture schema).
- `proposals/cybersand-landscape-swarm/PILOT.md` — Iron Wound pilot and native acceptance requirements.
- `plugins/cals/M0-CAPABILITIES.md` — what has/hasn't been proven.

## Preconditions

1. Determine actual OMP capabilities and version; verify the installed `task` shape, `agent://` messaging, tool restrictions and optional isolation. Do **not** guess the parameters, OMP evolves quickly.
2. Identify repository, current Git SHA and any source-pinned native CyberSand runtime. If Godot/OMP/credentials are absent, work in **offline planning/fixture mode** and label runtime steps untested.
3. Establish *enforced* tool/workspace isolation before giving write-capable children access to valuable repositories. OMP headless subagents may have permissive tool approvals; a prompt is not security.
4. Obtain explicit authorization and an enforceable provider policy gate before any billed OpenAI/third-party inference. GPTopus's monthly allowance is informational, not a spending cap. Never switch keys/models/tiers on failure without approval.

## Thin choreography: propose → negotiate → inspect

- **Director (lead):** Freeze a World Bible with design story, macro landmarks, width/height, protected negative space, source identity, regions and required routes. Assign only disjoint proposal files/regions.
- **Traversal specialist:** Propose route graph, joint/socket/clearance requirements, explicit unknowns about the real actor controller. Do not claim actual traversal until native/player tests exist.
- **Structural architect:** Use existing GEN-007/Gentek recipe contracts where verified; propose supports, layers, attachments, openings and joints. Avoid stamping a giant pixel map into Setup-v2 JSON.
- **Environment specialist:** Propose geology, wear, materials and environmental transition without altering protected corridors; do not claim working fluid dynamics from a static image.
- **Independent critic:** Receive the same frozen candidate and actual evidence; check the existing seven-axis CyberSand visual rubric independently from hard source/material/route checks. Preserve dissent.
- **Integrator (one owner):** Compare region/joint revisions, reject stale proposals and contradictory claims, and only later invoke an *existing* source-matched native Workbench/GEN-007 interface if available and authorized.

Where available, spawn three workers with native `task` (batch/parallel) using a shared frozen World Bible digest, distinct `region_id` and paths. Use `agent://` messages to negotiate proposed sockets before any integration. Keep peer messages advisory until the director records a **new accepted joint revision**. Do not invent an OMP tool call if it isn't currently exposed.

## First executable offline step (no external models)

From the `piplugs` repository root, run:

```sh
python3 plugins/cals/tools/validate_contracts.py plugins/cals/fixtures/iron-wound-valid.json
python3 plugins/cals/tools/validate_contracts.py plugins/cals/fixtures/iron-wound-mismatched-socket.json
python3 -m unittest discover -s plugins/cals/tests -v
```

Expect the first fixture to return `PASS` (exit 0), the second to return `FAIL` (exit 1) with `SOCKET_MISMATCH`, and tests to pass. The fixtures are **author-declared geometric contracts**, not outputs from CyberSand. The valid case confirms two neighboring specialist proposals agree on exact shared openings; the invalid case represents an elevation mismatch at the viaduct/foundry seam.

The validator checks explicit region bounds/nonoverlap, joint positions, proposal source/World Bible revisions, lease generations, socket claims, proposed edits against region ownership and protected space, and **region-graph** connectivity. It does **not** check real materials, physics, passage clearance, collision, native generation or Save/reopen.

## When actual native capabilities are established

Do not call a fictional `apply_world()` function. Find and exercise real versioned CyberSand recipes, existing headless/native qualification and the accepted generated-start Save/reopen pathway. Require runtime fingerprint, source SHA, actual material receipt, graphical screenshot provenance, and fresh-process reopen before reporting any applied outcome. If a noninteractive import is missing, stop at an externally generated recipe/preview and specify the required human Workbench import.

## Research experiments

Use the [research programme](../../../research/CALS-RESEARCH-001.md) to compare, *without automatic model spend*:

- A — experience-first world graph vs geometry-first;
- B — induced structural-attachment grammar vs direct exemplar imitation;
- C — actual native simulation feedback vs screenshot-only repair (later);
- D — fixed director assignment vs a small needs/opportunity blackboard (later).

Preserve both successful and failed candidates, keep the same budgets/tools/seed cohorts, and maintain separate objective and subjective evidence. Do not start mass generation or training as a substitute for a verified bounded pilot.

## Completion report

Present exact committed/runtime identities, which tools were actually executed, PASS/FAIL/UNTESTED distinctions, agent messages that affected durable contracts, unresolved design decisions, the artifact paths and shortest reproducible command. Stop when missing runtime, budget or tool capability blocks progress—without switching to an unapproved engine or provider.
