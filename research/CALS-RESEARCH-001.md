# CALS-RESEARCH-001 — Beyond swarm orchestration

**Status:** recorded research programme; experiments proposed, **not yet run**  
**Owner context:** CyberSand authoring from external Oh-My-PI; no new CyberSand agent framework  
**Date:** 2026-11-22  
**Parent programme:** [CALS-001](../proposals/cybersand-landscape-swarm/README.md)  
**First implementation slice:** CALS M0/M1, with a no-model structural-contract validator and example

## Contents

1. [Research premise](#1-research-premise) — Evaluate creative and architectural value, not agent count.
2. [Ten investigation angles](#2-ten-investigation-angles) — Separate world reasoning, feedback and orchestration mechanisms.
3. [Four controlled experiments](#3-four-controlled-experiments) — Test distinct causal hypotheses with comparable resources.
4. [Research artifacts and memory](#4-research-artifacts-and-memory) — Capture decisions and verified construction traces.
5. [Evaluation and stopping](#5-evaluation-and-stopping) — Hard native checks, human aesthetic review and reproducible controls.
6. [Sequencing and boundaries](#6-sequencing-and-boundaries) — Keep CALS lightweight and defer premature engine changes.

## 1. Research premise

CALS-001 establishes **how** external agents can collaborate. This programme asks **which forms of collaboration improve coherent, traversable, distinctive 2D landscapes**. A higher token count, number of simultaneous agents, amount of painted material or judge agreement is not itself an improvement. A useful negative result can justify simplifying the swarm.

Reuse OMP native `task`, `agent://` messages and lifecycle; reuse GPTopus only for appropriately enforced worker policies; CyberSand remains the sole authority for native generation/material, rendering, physics and Workbench persistence. The Web build is optional. Do not merge experimental CyberSand PRs automatically.

**Experimental unit:** A finite, source-pinned, orthographic side-elevation landscape (initially 2048×1024 after small-fixture preflight). Freeze runtime, reference pack, actor/traversal assumptions, seeds, model budget and rubric before comparing conditions.

## 2. Ten investigation angles

| ID | Direction | Mechanism | Measurable question | Priority |
|---|---|---|---|---|
| R01 | **Inverse worldbuilding** | Experience/story and traversal sequence → route/clearance graph → architecture → materials | Are routes clearer and places more memorable than geometry-first generation? | P0 |
| R02 | **Structural grammar induction** | Recover typed components, attachments, load paths and constraints from accepted Genteks/examples | Can novel compatible structures be generated without copying existing silhouettes? | P0 |
| R03 | **Simulation-driven design** | Use controlled CyberSand runs for material interaction, collapse/leaks, debris and route discovery | Does physics feedback improve plausible damage or add playable affordances? | P0 |
| R04 | **Quality-diversity archive** | MAP-Elites-style diversity dimensions for structure, void, height and density | Do multiple design niches outperform incremental hill-climbing in novelty/selection? | P1 |
| R05 | **Architectural memory** | Curated failures, repairs, intent and native-verified recipes as reusable records | Does retrieval improve first-pass native validity/coherence? | P1 |
| R06 | **Stigmergic blackboard** | Agents respond to durable needs/opportunities inferred from current artifact state | Can decentralized work improve the world without excessive chatter? | P1 |
| R07 | **Construction semantics** | `supports`, `attaches`, `connects`, `opens-into`, `drains-to` relationships | Do explicit structural roles reduce meaningless decorative geometry? | P1 |
| R08 | **Multiscale attention** | Macro landmarks/voids → meso construction → micro detail; review-driven focus | Does progressive detailing retain silhouette and avoid filling intentional voids? | P1 |
| R09 | **Adaptive specialist team** | Recruit/retire roles based on detected deficits and evidence of marginal benefit | Is the extra agent worth coordination/compute overhead? | P2 |
| R10 | **Player-behaviour criticism** | Bounded deterministic or AI controller traverses/uses level and records failures | Do play traces expose defects missed by static route graphs and screenshots? | P2 |

R02 can investigate attachment vertices, stroke-supplied structural intent, receptacles, orientation and constrained detail fill, but should **not** assume Gentek live authoring inside Workbench. R03 may use independently restored disposable snapshots; neither simulation screenshots nor material-count checks establish load-bearing structural stability unless the native engine actually models those properties. R04 uses **computed behavior descriptors**, not ungrounded aesthetic scores. R05 begins with 15–25 reviewed design cards and verified construction traces rather than ingesting a whole local gallery into Git.

## 3. Four controlled experiments

### A — Experience-first vs geometry-first (R01)

- **Control:** independent geometry-first macro district planning, then connect traversal.
- **Intervention:** narratively specified player journey → route/void plan → compatible architecture.
- **Hold constant:** canvas, materials, native generation tools, budgets, seeds, actor clearance target, inspection.
- **Primary outcomes:** mandatory route connectivity, route clarity, number of blocked connections, owner preference, coherence rubric.
- **Confounds:** Don't give experience-first extra traversal tools or more review passes.

### B — Structural-part reasoning (R02 + R07)

- **Control:** produce a novel Gentek-like building from three accepted example descriptions.
- **Intervention:** derive attachment/socket/type/load-path rule graph first, then generate a fourth design.
- **Hard checks:** graph integrity, anchor compatibility, native material/geometry validity, allowed generated recipes.
- **Soft checks:** novelty beyond recolor, architectural believability, legibility, independent human review.
- **Do not infer physical load capacity from unmodeled structure.**

### C — Physics as creative feedback (R03)

- **Control:** static ruined architecture refined by screenshot critique.
- **Intervention:** same candidate and budget, plus *actual*, bounded source-matched native trials and material/collision readback.
- **Questions:** What changed between t=0 and selected later ticks? Did material movement create/close a path? Could a repair preserve an interesting event while maintaining required navigation?
- **Stop/guard:** separate disposable World/session, explicit solver/ABI, seed and wall-clock budget, conserve materials where applicable, rollback by reconstructing authored baseline rather than assuming undo of evolved state.
- **If dynamic claims cannot be measured, mark untested and retain only the static experiment.**

### D — Director-assigned vs opportunity-driven work (R06 + R09)

- **Control:** fixed lead and region specialist work orders.
- **Intervention:** a *small* external append-only needs board (`MISSING_CONNECTOR`, `SUPPORT_OPPORTUNITY`, `DETAIL_GAP`, `VOID_PROTECTED`, etc.) lets agents propose interventions; coordinator still leases regions and accepts changes.
- **Measurements:** verified improvements per agent call, coordination latency, duplicate proposals, ownership conflicts, communication volume and quality rubric.
- **Exit:** if adaptive scheduling yields no measurable gain, keep the simpler director model.

**Experiment order:** first offline A+B fixtures; then source-matched native A/B replay; then C; then D. Do not start a large 108+ run or model training from this programme.

## 4. Research artifacts and memory

Keep distinct, versioned record types:

1. **Visual design card:** source path/hash and permission/provenance, silhouette, spatial relationships, apparent traversal, motifs and observations vs inferences.
2. **Construction trace:** world/region/joint revision, actual supported native tool/program, verified source/material/receipts, expected and actual changes.
3. **Experience trace:** chosen actor/profile, route/play inputs, measured movement/contact outcome and uncertainties.
4. **Failure/repair pair:** minimal reproducer, violated invariant, previous candidate SHA, corrective edit, verified outcome and whether it generalizes.
5. **Human preference:** side-by-side candidate IDs, context, written choice, vetoed properties and preserved "weird" features.

Do not conflate the five records. A SANDMAPS image alone is no proof of valid CyberSand geometry, and an invented simulation narrative is no physics evidence. Use local file references instead of uploading the full SANDMAPS corpus.

A future optional quality-diversity index can classify accepted *native candidate* records by grounded descriptors (vertical extent, occupied/void fraction, connectors, route branching, motif tags). Preserve the highest-quality validated sample per descriptor niche and counterexamples; use a frozen descriptor definition and don't silently change bins mid-study.

## 5. Evaluation and stopping

**Hard gates** (objective and source-matched): parse/bounds, source/version identity, protected cells, region/joint claims, material capabilities, required routes under selected test profile, confirmed native changes, Save/reopen and applicable physics safety checks.

**Soft evaluation:** reuse CyberSand `docs/world-design/QUALITY_BAR.md` seven axes; use blind competing reviews on real full and crop renders when available, preserve dissent, give the owner final artistic authority. No aesthetic quorum can bypass a hard gate.

Every experiment needs a hypothesis, preregistered inputs and budgets, explicit failed/unavailable cases, provenance and side-by-side comparisons. Freeze the rubric before generating outcomes. Compare to a deterministic native baseline and random/legal control where appropriate. A small early negative result is more useful than another unqualified volume campaign.

**Stopping rules:** max accepted revision rounds, max model calls/tokens/cost, max native elapsed/disk, and no verified improvement for two successive rounds. On missing prerequisite, mark `BLOCKED` or `UNTESTED`; don't add another agent to paper over missing evidence.

## 6. Sequencing and boundaries

- **Immediate:** implement and test a tiny external region/joint/route-contract validator. This is an **offline contract fixture**, not a native-world validator or proof of playability. Record a deliberately mismatched connector and a fixed counterpart.
- **Next:** an OMP-native `landscape-studio` skill and a minimal agent-message pilot; evaluate actual OMP version/plugin discovery and tool safety.
- **Then:** source-matched GEN-007/native preview and Workbench manual/native import gates; compare experience-first and geometry-first proposals.
- **Only after verified value:** pursue grammar induction, simulation-guided repair, curated design memory and dynamic agent recruitment. Treat any new engine API as separate explicit approval.

**Protected baseline:** No CyberSand changes, no Web work, no unapproved model billing, no public SANDMAPS uploads or autonomous merges. Store implementing experiments in `piplugs` until the target consumer demonstrates a genuine missing external interface.

Related material: [CALS Architecture](../proposals/cybersand-landscape-swarm/ARCHITECTURE.md), [Contracts](../proposals/cybersand-landscape-swarm/CONTRACTS.md), [Delivery Plan](../proposals/cybersand-landscape-swarm/DELIVERY-PLAN.md), [Pilot](../proposals/cybersand-landscape-swarm/PILOT.md).
