# CALS-001 — Proposed data contracts and execution protocol

**Status:** VERSION-0 DESIGN CONTRACT; these are *external CALS documents*, not current CyberSand or OMP APIs.  
**Compatibility:** Each adapter must prove conversion to an existing source-pinned runtime contract before use.  
**Rule:** Preserve exact native evidence and reject unknown required schema versions.

## Contents

1. [Conventions and common envelope](#1-conventions-and-common-envelope) — Names, coordinates, hashes and schema identity.
2. [World Bible and intent](#2-world-bible-and-intent) — Shared, immutable design brief and macro plan.
3. [Region leases and boundary joints](#3-region-leases-and-boundary-joints) — Prevent conflicting authors and discontinuities.
4. [Work orders and design proposals](#4-work-orders-and-design-proposals) — Isolate agent creativity from material authority.
5. [Negotiation and decisions](#5-negotiation-and-decisions) — Persist contested choices and resolve affected interfaces.
6. [Native admission lifecycle](#6-native-admission-lifecycle) — Preview, apply, verify and Save as different states.
7. [Evidence and reviewer records](#7-evidence-and-reviewer-records) — Typed captures, objective checks and critical feedback.
8. [Worker policy and accounting](#8-worker-policy-and-accounting) — Enforce GPTopus-style routing and budgets.
9. [Checkpoint and recovery model](#9-checkpoint-and-recovery-model) — Stop/resume without falsely claiming completion.
10. [Validation and compatibility rules](#10-validation-and-compatibility-rules) — Reject ambiguity and preserve engine contracts.

## 1. Conventions and common envelope

All CALS machine documents should be UTF-8 JSON, with JSON Schema in the later implementation. Markdown may accompany them for artistic reasoning but must not override the machine contract.

Every durable machine document includes:

| Field | Requirement |
|---|---|
| `schema_id`, `schema_version` | Exact identity; no implicit migration |
| `run_id`, `document_id`, `revision` | Stable provenance; revisions are append-only |
| `source` | Immutable CyberSand Git SHA; optional separate runtime fingerprint |
| `world_bible_sha256` | Hash of canonical accepted World Bible JSON |
| `creator`, `created_at_utc` | Worker identifier and UTC timestamp |
| `status` | Explicit state from the relevant state machine |
| `input_sha256` | Content identity for dependencies, including reference cards |

A native state receipt additionally records platform, Godot version, generation fingerprint, native library hash or verified build identity, scene/test tool and actual source-bound output digest.

**Spatial system:** True 2D orthographic side elevation. Integer material-cell coordinates; `x` grows right, `y` grows down, origin at top-left of the finite local canvas. Rectangles are half-open `[x,x+w) × [y,y+h)`; nonnegative integer extents. Distinguish local canvas coordinates from generator global signed coordinates; transforms must be explicit and validated. No top-face/isometric/perspective geometry in the first pilot.

**Determinism:** Seeds are explicit, stable per region and operation. Canonicalization/hashing must be documented and tested across JSON roundtrips (including int/float behavior). Never use hash stability as a substitute for same-source native generation validation.

## 2. World Bible and intent

`world-bible.v1` is the single accepted macro design authority. Before construction, the director obtains a concept and freezes enough of the document to make region work safe. Later revisions invalidate affected work.

Illustrative CALS schema instance (not directly consumable by CyberSand):

```json
{
  "schema_id": "piplugs.cals.world-bible",
  "schema_version": 1,
  "run_id": "pilot-iron-wound-001",
  "revision": 1,
  "status": "ACCEPTED_FOR_PROPOSALS",
  "canvas": {
    "width": 2048, "height": 1024,
    "coordinate_space": "local-cell-top-left-y-down",
    "play_plane": "play"
  },
  "design": {
    "name": "Iron Wound",
    "setting": "abandoned industrial undercity with a broken transit viaduct",
    "view": "exact orthographic side elevation",
    "visual_priorities": [
      "coherent skyline", "distinct landmark", "deliberate open voids",
      "navigable structural transitions", "restrained microdetail"
    ],
    "forbidden": [
      "isometric perspective", "solid wall across mandatory routes",
      "decorative unsupported physical claims"
    ]
  },
  "regions": [
    { "id": "foundry", "rect": [0, 0, 736, 1024] },
    { "id": "viaduct", "rect": [736, 0, 624, 1024] },
    { "id": "reservoir", "rect": [1360, 0, 688, 1024] }
  ],
  "routes": [
    { "id": "main-traverse", "from": "foundry-entry",
      "to": "reservoir-exit", "required": true }
  ],
  "material_policy_ref": "policies/verified-materials.json",
  "joint_contract_refs": [
    "joints/foundry-viaduct.json",
    "joints/viaduct-reservoir.json"
  ],
  "reference_cards": [],
  "world_bible_sha256": "<computed by writer at acceptance>"
}
```

The placeholder hash above is illustrative. Before acceptance, the writer fills it from the canonical bytes and validates the resulting record. For real runtime use, source IDs, created timestamps and the common envelope are mandatory, even when omitted from a short example.

**Hard fields:** dimensions, projection, mandatory route endpoints, protected void areas, global material policy, region ids, shared connection agreements. **Soft fields:** story, atmosphere, desired silhouette, motif palette, relative detail budgets. Agents may challenge the latter; any change to hard fields requires a new accepted revision and dependency invalidation.

A World Bible may reference retrieved design cards. A card must include source path/hash, license/provenance where known, crop identifiers, direct visual observations, interpretations and unresolved uncertainties. An image never grants permission to copy or upload it.

## 3. Region leases and boundary joints

Avoid shared writable map JSON. The coordinator exclusively maintains a versioned `regions/index.json` and `joints/index.json`. Workers write immutable unique proposals under assigned paths.

A lease record contains:

```json
{
  "schema_id": "piplugs.cals.region-lease",
  "schema_version": 1,
  "run_id": "pilot-iron-wound-001",
  "region_id": "foundry",
  "holder": "architect-a",
  "revision": 3,
  "bounds": [0, 0, 736, 1024],
  "permitted_operations": ["propose", "inspect"],
  "protected_mask_sha256": "<validated mask digest>",
  "joint_revision_dependencies": {
    "foundry-viaduct": 2
  },
  "status": "ACTIVE",
  "lease_generation": 4
}
```

An active lease is not a permission to modify the live World. It only defines exclusive *proposal ownership*. Leases are granted and revoked by one coordinator using atomic writes/compare-and-swap against a generation number. Expired or revoked leases cannot publish accepted proposals. Worker death must not trigger an unsafe implicit reassignment.

**Joint contract** fields:

- `joint_id`; neighboring region IDs; owner of border cells; absolute half-open interface band.
- Named socket anchors (location, width/height, orientation, passage type, elevation, destination route).
- Minimum required clearance determined from an actually chosen actor/traversal profile; placeholder values must not be treated as tested physics requirements.
- Shared structural/cosmetic material intent plus compatibility/capability IDs resolved against the actual runtime.
- Allowed variation inside an explicitly bounded tolerance, impact on protected empty space and guard-test reference.
- Revision, signed acceptance *records* of both proposals (identities and hashes, not cryptographic agent signatures) and director decision.

Example negotiation: the foundry proposes a service tunnel exit at one elevation; the viaduct proposes a bridge deck at another. Neither is installed. The director requests one revised connector, the traversal checker tests the agreed opening, and both proposals are invalidated until their declared joint revision matches.

**Conflicts:** Intersecting unleased edits; conflicting material at a shared cell; connector location mismatch; blocked required route; and mixed policy/source revisions are automatic hard failures. Do not resolve by applying whichever edit was written last.

## 4. Work orders and design proposals

A `work-order.v1` includes task ID, question to solve, approved World Bible digest, region/connector lease, relevant material/runtime capabilities, read-only observation bundle, source-aligned references, allowed tools, proposal path, model budget and explicit stop/handback condition.

Each specialist returns one or more immutable `proposal.v1` records rather than committing to an already-running World:

```json
{
  "schema_id": "piplugs.cals.proposal",
  "schema_version": 1,
  "run_id": "pilot-iron-wound-001",
  "proposal_id": "foundry-architecture-v3",
  "agent_id": "architect-a",
  "region_id": "foundry",
  "world_bible_revision": 1,
  "region_lease_generation": 4,
  "joint_revisions": { "foundry-viaduct": 2 },
  "status": "PROPOSED",
  "kind": "generator-recipe-and-overlays",
  "generator_recipe_path": "proposals/architect-a/foundry-v3/recipe.json",
  "generator_recipe_sha256": "<computed>",
  "overlay_program_path": "proposals/architect-a/foundry-v3/edits.json",
  "overlay_program_sha256": "<computed>",
  "intended_connections": ["foundry-viaduct"],
  "claimed_effects": ["room hierarchy", "service shaft", "lower bypass"],
  "known_uncertainties": ["exact worker native material catalogue"],
  "evidence_refs": []
}
```

CALS `proposal` is **not** the CyberSand GEN-007 recipe schema. The path must point to a separately validated *genuine* existing native recipe and, if necessary, a bounded edits format the current Workbench can actually ingest. The adapter must reject unsupported operations rather than silently rasterize arbitrary model pictures or invent a new engine import format.

**Permitted program categories:** existing native generator recipe/module parameters; editor-supported bounded primitive batches; valid imported design-pack rectangles when a supported, tested conversion exists. All shapes need exact coordinates, materials, budgets and ordering, including intentional erase/material-zero writes.

**Edit semantics:** A repeated operation is not automatically idempotent. Every admitted operation needs an operation ID plus a precondition (World/region revision and stored-material hash where supported). Duplicate delivery cannot be applied twice. Partial native success is preserved as partial evidence, not retroactively called atomic.

## 5. Negotiation and decisions

OMP `agent://` messages enable live peer negotiation, but the *durable protocol* is an append-only `decisions.jsonl` and a compact accepted contract file written by one authority.

Every decision records:

- `decision_id`, affected region/joint IDs, problem, proposer and evidence.
- Competing candidate IDs, requested checks and their actual results.
- `RESOLVED` / `EXPERIMENT` / `DEFERRED` / `BLOCKED`, reason and decision owner.
- Winner and affected dependency hashes; explicit invalidation list for stale candidates.

A message from another agent is advisory unless the coordinator has accepted it into a new contract revision. Avoid pretending peer agreement has applied a material edit or legally granted file ownership.

For design disputes without hard constraints, optional independent reviewers should see the *same frozen evidence* without agent identities or prior ratings. Preserve meaningful minority opinions. The owner can override soft rankings, but cannot override a proof-of-physics or corruption failure without changing the acceptance designation.

## 6. Native admission lifecycle

Proposed state machine:

```text
PROPOSED
    -> SCHEMA_VALIDATED
    -> NATIVE_COMPILED
    -> PREVIEW_CAPTURED
    -> DIRECTOR_ACCEPTED
    -> ADMISSION_PENDING
    -> APPLIED_PARTIAL | APPLIED_COMPLETE | REFUSED
    -> READBACK_VERIFIED
    -> SAVED_START
    -> FRESH_PROCESS_REOPEN_VERIFIED

Any stage -> BLOCKED / STALE / CANCELLED / FAILED
```

Key distinctions:

1. `SCHEMA_VALIDATED` means only that external structures and native recipe shapes passed validators.
2. `NATIVE_COMPILED` needs an actual native generator/bridge result with source-aligned runtime identity.
3. `PREVIEW_CAPTURED` records a display/cell capture, not a World mutation.
4. `DIRECTOR_ACCEPTED` is approval to *attempt* mutation, not confirmation of success.
5. `APPLIED_*` comes only from authoritative native host receipts. Requested/pending/queued counts do not count as changed material.
6. `READBACK_VERIFIED` compares actual stored material and protected area with expected changes, allowing explicit partial outcomes.
7. `FRESH_PROCESS_REOPEN_VERIFIED` reconstructs the authored start under an independently relaunched source-matched runtime and compares acceptable hashes/receipts.
8. None of these represents evolved simulation-state persistence or an unconditional claim of stable gameplay.

The integrator owns serial dispatch, cancellation and World replacement synchronization. It must ensure the simulation/render worker is safely quiescent or use an existing native ownership boundary before the next mutation. A timeout can leave uncertain state; do not retry blindly.

**Receipt shape** includes requested/validated/eligible/applied/unchanged/refused/partial counts; operation IDs; pre/post native generation, revision and tick; stored-material readback hashes; expected vs actual material deltas; source/runtime fingerprint; duration; explicit failure code; and file identity. Require separate receipts for generator install, edit batch, save and fresh reopen.

## 7. Evidence and reviewer records

An `evidence-manifest.v1` should include artifact path, SHA-256, media/type, source/provenance, world revision, native platform, capture renderer, view bounding box, zoom, timestamp, and whether the subject is a **source illustration**, **synthetic native-ID preview**, **genuine Godot frame**, **native stored-material readback** or **physics observation**.

A review report should have independently verifiable parts:

```json
{
  "schema_id": "piplugs.cals.review",
  "schema_version": 1,
  "candidate_id": "world-assembly-v2",
  "rubric_revision": "quality-bar-2026-11",
  "hard_gates": [
    { "name": "bounds-and-materials", "result": "PASS", "evidence": "checks/geometry.json" },
    { "name": "fresh-reopen", "result": "UNTESTED", "evidence": null }
  ],
  "soft_review": {
    "silhouette": { "score_0_to_5": 4, "reason": "landmark legible at atlas scale" },
    "coherence": { "score_0_to_5": 3, "reason": "left-to-center transition needs reinforcement" }
  },
  "blocking_issues": [],
  "proposed_edits": ["repair viaduct/foundry seam"],
  "uncertainty": ["no confirmed physical playtest"]
}
```

The complete rubric is CyberSand's seven-axis `docs/world-design/QUALITY_BAR.md`. A partial JSON report need not list all axes until a final accepted aesthetic assessment; final acceptance must cover all seven plus appropriate visual comparisons. Soft scores are observations from judges, not objective evidence or confidence probabilities. All hard gates must be PASS, or the final artifact remains a qualified partial result.

## 8. Worker policy and accounting

A `dispatch-authorization.v1` is created **before** every remote call (and again at retries, resumed agents and replacement models). It records: worker alias, resolved model and provider, *credential profile identifier* (not key), service tier, operation ID, allowed tools, source-scope restrictions, max tokens/steps/calls, estimated USD ceiling, UTC budget group, reservation ID and expiry, plus cancellation owner.

Adapt GPTopus's `bridge/usage.mjs` invariants:

- Atomic interprocess exclusive admission; used plus reserved tokens counted before dispatch.
- Separate Astra/premium and Terra daily groups and explicit model allowlist; reject unauthorized group switching.
- Charge exactly once by stable response ID when available; for missing usage, apply a conservative estimate; ambiguous network outcomes hold reservation until reconciled.
- UTC reset affects new reservations only; a started request remains tied to its admission day.
- Corrupt/unreadable ledger means guarded workers stop. Straight-key calls are separately governed by an actual paid budget limit.
- Show usage/cost source and uncertainties. `MonthlyAllowanceUsd` is not a genuine paid cap.

A **separate run budget** limits total provider calls, model-token estimates, wall time, live agents and native CPU/IO/capture operations. If a price/tier has not been verified, refuse to quote a trustworthy USD ceiling rather than pretending the cost is zero. Authorization is not just a CLI prompt: the request path must call the policy gate before billing can occur.

## 9. Checkpoint and recovery model

Suggested run directory (outside CyberSand and outside the public piplugs checkout, with ignore rules):

```text
cals-runs/<run-id>/
  manifest.json
  policy-snapshot.json
  brief/world-bible-vN.json
  references/cards/
  regions/index.json
  regions/leases/
  joints/
  work-orders/
  proposals/<agent>/<candidate>/
  decisions.jsonl
  native/receipts/
  native/readback/
  captures/
  reviews/
  checkpoints/<revision>/
  logs/redacted/
  release-candidate/
```

**Durability:** Immutable candidate files, atomic temporary-write+rename for indexes, stable hashes and one lock/lease authority. Keep successful, failed and rejected candidates separately; do not erase failures when rebuilding a best-of selection. Local model/API credentials stay out of run records.

**Restart:** Acquire exclusive run lock; read manifest/source identity; examine active external jobs; reconcile pending quota reservations; verify latest complete checkpoint hashes; check OMP agent status from native host, not stale JSON; mark uncertain operations `NEEDS_RECONCILIATION`. Resume only from a deterministic next work order, reusing an OMP agent *when it is truly live or revivable* and context/lease still matches. Otherwise create a fresh worker with a full bounded handoff.

**No guarantee of rollback:** A native partial operation or elapsed simulation tick may change reality. Use actual verified snapshots or regenerate the exact authored baseline in a disposable process, then replay accepted operations with checks; do not assume Undo restores evolved physics.

## 10. Validation and compatibility rules

Minimum schema tests: malformed YAML/JSON, duplicate ID, unknown required version, out-of-bounds rectangles, negative size, invalid material, invalid source SHA, stale World Bible, stale lease, dangling connector, overlapping ownership, cross-region edit, protected-cell change, idempotency replay, canceled/partial receipt, conflicting peer resolutions, inconsistent hashes, corrupt resume and quota-ledger corruption.

Cross-platform tests must exercise Windows path escaping, long paths and spaces; Godot/native mismatch; headless and graphical source identity; UTC rollover; abrupt child process exit; concurrent reservations; and PII/secret redaction.

**Runtime compatibility checklist:** Confirm actual OMP API/tool permission isolation, tested native source/build fingerprint, GEN-007 recipe support, chosen Gentek catalogue availability, material/rectangle budget, generated-start v1/Setup-v2 validation and available fresh-process replay tests. If a feature belongs to an unmerged CyberSand PR, this must be explicitly recorded and the default path must not require it.

**Version policy:** No speculative migration of existing CyberSand persisted manifests. CALS schemas are independent, explicitly versioned and may evolve only through adapters with tests. End-to-end admission always remains an existing CyberSand-defined format.

See [ARCHITECTURE.md](ARCHITECTURE.md), [DELIVERY-PLAN.md](DELIVERY-PLAN.md) and the worked [PILOT.md](PILOT.md).
