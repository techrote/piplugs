# CALS-001 — System architecture and decision record

**Status:** Proposed; no plugin/runtime has been implemented. **Date:** 2026-11-22.  
**Inspected baselines:** OMP `ad9206d87c1685d539312e9a0f750dc6c526dd6f`; GPTopus `edd9392eae931ef19db82c84eb4d6d1167583fc4`; CyberSand main `00cdb02f103265b6dc5224c68283e9a0c8cb449f`. Re-check these on the implementation day.

## Contents

1. [Operating principles](#1-operating-principles) — Keep OMP responsible for agency and CyberSand responsible for the world.
2. [System boundaries](#2-system-boundaries) — Define one-way authority, permissions and data flow.
3. [Agent organisation](#3-agent-organisation) — Use creative negotiation with a small, measurable roster.
4. [GPTopus reuse](#4-gptopus-reuse) — Carry forward model routing and resource controls without copying Claude-specific hooks.
5. [Native OMP integration](#5-native-omp-integration) — Use supported tools and validate extension hook availability.
6. [Coherence and conflict resolution](#6-coherence-and-conflict-resolution) — Negotiate region interfaces and avoid independent-patch collage.
7. [CyberSand integration](#7-cybersand-integration) — Use existing source-pinned native authoring and persistence.
8. [References and art direction](#8-references-and-art-direction) — Ground visual decisions in curated local evidence.
9. [Review and refinement](#9-review-and-refinement) — Separate objective correctness from subjective artistic judgment.
10. [Security and cost control](#10-security-and-cost-control) — Fail closed on unavailable enforcement.
11. [Observability and recovery](#11-observability-and-recovery) — Preserve run provenance and recover without guessing.
12. [Alternative designs and ADRs](#12-alternative-designs-and-adrs) — Record what is rejected, deferred and conditional.

## 1. Operating principles

**Product shape:** An installable optional OMP capability under `piplugs`, comprising small skills, role definitions, a policy adapter, a source-aware native-execution wrapper and test fixtures. Most behavior should be instructions and typed documents rather than long-running custom orchestration machinery.

**No engine harness:** CyberSand's ordinary Workbench remains the authority for material edits, World lifetime, physics, preview and Save/reopen. No second editable World, no agent scheduler in GDScript, no persistent remote-control server, no new game UI and no Web export prerequisite.

**No artificial consensus:** Agents should propose genuinely different creative solutions, communicate differences and reconcile interfaces. Consensus does not overrule failed material/traversal checks or substitute for owner taste.

**Conservative claims:** A source recipe is a proposal; a successful native sample is an observed material result; a screenshot is a particular renderer output; a playable map requires independent admission, runtime and fresh-process reconstruction checks.

## 2. System boundaries

```text
Human brief / optional design references
    |
OMP director (plan / negotiate / assign / synthesize)
    |             OMP native task, Agent Hub, agent://, history://
    +----> specialist author agents (isolated proposal branches/paths)
    +----> independent critics and traversal/physics reviewers
    |
CALS deterministic coordinator and policy adapter
    |-- pre-dispatch model/account/quota gate (GPTopus-inspired)
    |-- canonical World Bible + region/connector ownership
    |-- proposal compilation + semantic/schema validation
    |-- one serialized CyberSand native integration queue
    |-- evidence, checkpoints and review gates
    |
Existing CyberSand tooling (source-matched, unmodified)
    |-- GEN-007 / architectural module generation
    |-- Workbench prepared world + paint transactions
    |-- capture tools + material/readback checks
    +-- generated-start v1 + Setup-v2 Save/reopen
```

The coordinator may invoke existing command-line/test scripts but never pretends a proposed operation has applied. It carries a run identity and a verified source fingerprint through every stage. All side effects are made against a disposable, versioned evaluation workspace until explicitly approved for an owner-authored start.

**Authority map:** The director owns scheduling/decisions; region agents own only their candidate proposal files; the integration actor owns merge order; the native engine owns real applied material; the critic owns a report, not the artifact; the human owns final artistic acceptance and external publication.

## 3. Agent organisation

Pilot roster: one director; three parallel specialists (macro architecture, terrain/environment, traversal/connectivity); one later independent critic. Add detail/greeble, physics/safety, motif curator and adversarial repair agents only if pilot evidence shows marginal value.

Potential expanded studio:

| Role | Can propose | Cannot independently do |
|---|---|---|
| Creative director | World Bible, landmarks, motifs, accepted design trades | Invent native success; bypass locked interfaces |
| World/cartography planner | District extents, route graph, focal/void plan | Write final stored material |
| Structural/Gentek architect | Structural modules, sockets, room spacing, transitions | Occupy protected paths |
| Environment/geology specialist | Natural shapes, deposits, hazards, material transitions | Claim physical stability from a still image |
| Traversal engineer | Player paths, spawn/exit, access tests, clearance budgets | Infer walkability from schematic alone |
| Detail artist | Pipes, seams, machinery, wear, ornament | Fill approved voids indiscriminately |
| Independent critic | Blind aesthetic evaluation, counterexamples, regression concerns | Silently modify accepted design |
| Integration/qualification specialist | Validate and apply approved programs; audit receipts | Declare owner visual acceptance |

Do not assign three identical roles simply to increase agent count. Different prompts can still generate correlated outputs. Encourage competing proposals for macro composition, followed by shared constraints and narrowly owned construction.

**Interaction policy:** Prefer ongoing named OMP agents and `agent://` messages for iterative conversation; record durable resolutions in typed run files. Peer messages are not transactions. An agent has no authority to revise another agent's boundaries merely by sending a message.

## 4. GPTopus reuse

Donor: `techrote/Chlaude-GPTopus/plugins/openai-workers`. GPTopus uses Claude Code mod hooks to register worker types and intercept `turn.step`, then a Node stdio MCP bridge calls the OpenAI Responses API. **This host interface is not an OMP interface.** Port selected pure policies; do not vend the whole Claude Code plugin.

| Existing source | Preserve/reuse | Adapt/replace |
|---|---|---|
| `hooks/register.js` | Named roles, explicit model and tier selection, error-without-fallback policy | Claude mod registration, turn/event APIs and handback |
| `bridge/usage.mjs` | Locked persistent daily ledger, UTC-day attribution, in-flight reservations, duplicate-response handling, corrupt-ledger fail-closed | Host-neutral adapter, migrations, namespaces and unified accounting |
| `bridge/openai.mjs` | Distinct free/straight key profiles, response normalization, bounded polling/cancel and tier/model validation | OMP provider/auth integration where enforceable; live API compatibility recheck |
| `hooks/tools.js` | Positive tool allowlist and argument filtering | OMP-native tool policy and OS-backed workspace isolation |
| `bridge/server.mjs` | Small explicit dispatch boundary and usage diagnostics | Replace/retain MCP bridge only after a working OMP-specific spike |
| `tests/*.mjs` | Negative tests for routing, quota reservation, rollover and failure | Extend to native OMP, cross-process and replay scenarios |

GPTopus currently defines six named profiles (`sol`, `astra`, `luna`, `flex6-1`, `daily-astrafree`, `daily-terrafree`). Those names are useful compatible aliases; specific model strings, model families, price tables, API tiers and entitlements must be confirmed at runtime, not hardwired to 2026 assumptions.

**Key invariant:** Free-profile requests use the intended free key only; straight-profile requests use the standard key only. Any missing key, rejected model-family/tier combination or budget denial fails explicitly. No silent fallback from a nominally free request to a billable request.

**Ledger invariant:** GPTopus's nominal free-group targets (250k Astra/premium and 2.5M Terra per UTC day) are *local guardrails*, not guaranteed free allowance. Default 10% headroom and 12k token reservation are admission settings, not account limits. Its `$88` monthly allowance configuration is informational, not an API spend cap.

**Cross-host double-counting:** Two independent OMP/Claude ledgers using the same physical API key could admit more calls than intended. M2 must choose either (a) a verified shared ledger with transactional cross-process reservations and backward-compatible migration or (b) conservative, separately partitioned budgets until unification is safe. Never blindly point a new OMP ledger writer at GPTopus's existing file without schema/interprocess compatibility tests.

## 5. Native OMP integration

Inspect current OMP `docs/tools/task.md`, `docs/agent-hub.md` and `docs/skills/authoring-extensions.md` when implementing. OMP's current native tool already offers parallel subagents, `task.maxConcurrency`, optional isolated execution, agent history, peer messaging and revival. OMP also provides extension module entry points and plugin manifests. These capabilities should be invoked, not duplicated.

**Dispatch control is conditional.** It must be shown with an actual OMP spike that an external extension can enforce policy **before** a model request and settle real usage **after** it. An extension command that merely tells the main model to stay under budget is inadequate.

Evaluate in order:

1. **Native host provider/account route** if OMP allows per-worker credentials, exact key-profile pinning, model/tier inspection and policy hooks for every charged request, including retries and resumed workers.
2. **Narrow OMP provider facade or managed worker adapter** using GPTopus's tested HTTP/accounting primitives if the native path cannot enforce key separation and reservations.
3. **Fail closed / postpone paid workers** if neither path is protectable. A read-only local/fixture planning pilot can proceed without paid calls.

Do not couple to undocumented OMP private APIs until versions and compatibility tests are pinned. Reject unsupported settings rather than quietly ignoring them. OMP native `task` is the coordination primitive; a second arbitrary spawning mechanism would recreate the older swarm-extension's maintenance problem.

**Initial concurrency:** Cap the pilot at three active specialists, one integration owner and limited model requests. OMP's broader default concurrency is not appropriate for expensive drawing/model workloads. Share session and provider budgets, not only per-worker estimates.

## 6. Coherence and conflict resolution

The World Bible is a single revisioned design authority (theme, skyline, districts, route graph, landmarks, material palette, atmosphere, narrative, protected negative space). Before region work begins:

- Plan at macro scale with stable named region IDs and global coordinates.
- Identify **boundary contracts**: socket type, position/range, access clearance, material type/capability, environmental continuity, ownership of the border band and collision allowance.
- Freeze primary through-routes and intentionally empty space, then lease disjoint local regions to workers.
- Workers propose alternatives and negotiate conflicts through messages; the director resolves and writes a new revision of the specific affected contract.
- Changes to a shared socket invalidate both neighboring proposals and require targeted re-verification.
- The integrator applies region proposals in explicit order and checks real material changes and seams after every merge.
- After macro convergence, allow bounded meso/micro texture without erasing distinctive silhouettes or filling traversal voids.

Do not let direct concurrent writes to the same authoritative JSON file create last-writer-wins design decisions. Prefer immutable candidate files plus one index/lease owner; validate their hashes before selection. A file lock, transactional database or single-writer command is acceptable; agent prompt cooperation alone is not.

**Disagreement disposition:** `RESOLVED` (accepted with rationale), `EXPERIMENT` (test both), `DEFERRED` (not needed for this slice), or `BLOCKED` (needs owner/native capability). Persistent unresolved hard blockers prohibit final integration.

## 7. CyberSand integration

The first adapter must be **external and source-pinned**. Existing candidate/accepted components to discover and exercise include:

- `examples/worldgen/*.json`, `godot/scripts/architectural_generator_project.gd` and the GEN-007 schema-4 architectural modules.
- `godot/scripts/workbench_generated_map.gd` for generated-start v1 and `workbench_setup.gd` for Setup-v2.
- `godot/scripts/shared_workbench.gd`, native stored-material admission and the PAINT/agent authored-edit paths **only if available in the selected runtime**.
- `godot/tools/world_art_capture.gd` / qualification capture helpers and `tools/qualify_workbench_landscapes.py`.
- Design-only atlas packs under `docs/world-design`; these are not automatically playable native assets.

**Preferred minimum path:** Build valid native GEN-007 recipe(s), render/reference actual native final play-plane material output, use the existing generated-start import/install route, then perform a fresh-process named-save/reopen test. No new engine API should be introduced to make an invalid external program appear valid.

**Capability discovery:** At start, query the actual checkout/runtime for native module catalogue, source SHA, material IDs/capabilities, generation fingerprint, max region/stamp/rectangle budgets and available qualification scripts. The code documents Workbench source limits such as 32,768 rectangles and 1 MiB ordinary JSON, but the **installed native bridge's reported capability** and current format validation decide what is legal. Avoid embedding generated millions-of-cell output as a giant edit list.

**World ownership:** Preview is a separate immutable candidate. Install/paint belongs to one serial native owner. A successful queue admission is not readback; a saved authored start is not evolved physics-state persistence. Preserve generated baseline + ordered edits, including erase.

**Optional capabilities:** Gentek's expanded catalogue, experimental agent painting and candidate four-plane/depth features may be selectively enabled only after confirming they exist in the chosen committed source, have source-matched binaries and meet separate qualification. Do not merge unaccepted PRs to satisfy this plan.

## 8. References and art direction

Use SANDMAPS and `docs/world-design` as **retrieval and art-direction references**. The source images are not native material maps, and a reference image is not an automatically admissible game level. Default to local reference paths and hashes; do not upload the 400+ image corpus or issue novel public publications.

For each selected reference, create a compact design card: silhouette, geometry hierarchy, traversable voids, connectors, rhythm, structural meaning, material/colour discipline, storytelling motifs, evidence status and uncertainty. Distinguish visible observation from a proposed native reconstruction rule.

A good authored environment has macro landmarks, meso believable construction, micro nonrepeating greebles and negative-space discipline. Test at full-map scale and detail crops. Source-colour SVGs and actual Godot captures must be named differently.

## 9. Review and refinement

Use two review lanes:

- **Hard validation:** format/bounds, no out-of-region writes, protected cells, material capabilities, stable connectors, preserved routes, collision/traversal checks, source/runtime identity, native readback, noncorrupt Save/reopen and optional live-physics benchmarks.
- **Soft, explicitly judged:** silhouette hierarchy, believable construction, material/colour choices, storytelling, macro/meso/micro balance, cross-region cohesion and distinctiveness. Reuse CyberSand's existing seven-axis `QUALITY_BAR.md` rather than inventing a conflicting score.

The critic receives a *frozen candidate* and captured evidence, not the implementer's proposed score. Preserve dissent; a high numerical score never nullifies a hard failure. Apply targeted edits, not indiscriminate rerendering. Keep the last best **verified** candidate, a finite revision limit and a defined no-improvement stop. Human final preference remains authoritative.

## 10. Security and cost control

- Bind model, key, tier, provider and permitted tools at dispatch; check them again at resume/retry. Never trust the model to select its own billing route.
- Treat OMP child sessions and tool execution as privileged unless isolation is proven. Native OMP documentation describes forced `yolo` approval mode for headless subagents: prompts saying "read only" are insufficient. Use actual tool allowlists plus OS sandbox/worktree protection for review-only agents; prevent untrusted shell/Network/write capabilities as required.
- Workers may write only unique proposal paths. Only an integrator process may run the authoritative native apply/install path. No destructive Git operation or release publication without owner approval.
- Check secrets before sending repository context or captures to remote models. Retain only redacted logs; avoid leaking environment variables, key files and local gallery content.
- Enforce run-level max active agents, provider calls, estimated spend, wall-clock duration, native CPU/memory/command budget, disk retention and abort/cancel propagation. Show consumed plus reserved usage. Actual API charges must be checked externally.
- Define a failed provider/timeout/quota exhaustion result as **PARTIAL/FAILED**, not success by switching to another provider or silently writing fewer materials.

## 11. Observability and recovery

Every run has an immutable `run_id`, source SHA and active policy/rubric revision. Keep:

- World Bible revisions and accepted joint/region contracts;
- per-agent prompt hashes, model+key-profile IDs (never secrets), reported actual model/tier, token/usage receipts and elapsed time;
- proposal files, validation output, native fingerprints, serial apply receipts and before/after readback hashes;
- captures with type/renderer provenance, criticism, accepted/rejected revisions, owner decisions and errors;
- a replay recipe with exact generation seed, source/runtime identity and environment prerequisites.

On interruption, recover from the **last fully verified checkpoint**, reconcile running processes and pending API reservations, and invalidate stale proposals. Never infer that state marked `running` in a JSON file means an OMP agent is alive; never infer an incomplete native operation has rolled back. If baseline/run identity diverges, refuse replay rather than silently regenerate a different level.

## 12. Alternative designs and ADRs

| ID | Decision | Rationale / revisit condition |
|---|---|---|
| CALS-ADR-01 | **OMP native orchestration** over historical `swarm-extension` | Current task/Agent Hub handles richer collaboration; revisit only for audited, scheduler-specific missing capability |
| CALS-ADR-02 | **External-only integration** | Avoid complexity and regressions in CyberSand; revisit after a measured inability to produce accepted starts |
| CALS-ADR-03 | **GPTopus policy port, not Claude hook port** | Claude mod protocol is host-specific; only pure adapter logic is transportable |
| CALS-ADR-04 | **Single native mutation owner** | Protect World serial authority and deterministic receipts |
| CALS-ADR-05 | **Reference images not runtime truth** | Avoid false render/physics claims and unsupported import shortcuts |
| CALS-ADR-06 | **Hard gates independent of visual rubric** | A visually attractive but blocked/unreopenable level is not complete |
| CALS-ADR-07 | **No Web prerequisite** | Native desktop/headless source tests satisfy early authoring goals |
| CALS-ADR-08 | **Human-held publication and aesthetic approval** | Creative preference cannot be reduced to model vote |

**Next action:** M0 source/host capability spike and M1 minimal OMP skill prototype in [DELIVERY-PLAN.md](DELIVERY-PLAN.md). This is design documentation only; all runtime claims require new evidence.
