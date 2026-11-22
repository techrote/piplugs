# CALS-001 — First collaborative landscape pilot

**Pilot ID:** `pilot-iron-wound-001`  
**Purpose:** Demonstrate that *negotiating agents* produce a more coherent and usable place than similarly capable agents composing disconnected slices.  
**Status:** SPECIFICATION / NOT EXECUTED. The coordinates, roles and target checks below are proposed experimental inputs, not output or proof of a working level.

## Contents

1. [Creative brief](#1-creative-brief) — Establish visual identity and playable objectives.
2. [Spatial macro plan](#2-spatial-macro-plan) — Assign three districts with coherent interfaces.
3. [Agent choreography](#3-agent-choreography) — Specify when specialists diverge and negotiate.
4. [Worked seam negotiation](#4-worked-seam-negotiation) — Show why a swarm matters beyond independent drawing.
5. [Candidate production and runtime evidence](#5-candidate-production-and-runtime-evidence) — Define actual preview, apply and review outputs.
6. [Visual and physical acceptance](#6-visual-and-physical-acceptance) — Separate ambitious aesthetics from genuine engine validation.
7. [Controlled A/B experiment](#7-controlled-ab-experiment) — Test the added value of collaboration.
8. [Handback and extension conditions](#8-handback-and-extension-conditions) — Specify the output and next experiments.

## 1. Creative brief

**Name:** Iron Wound — an abandoned industrial undercity where a damaged transit viaduct crosses a large service chasm and meets a flooded industrial storage zone.

**Canvas:** 2048 × 1024 cells, orthographic *exact* side elevation; x positive right, y positive down. No top/platform faces, diagonal/isometric perspective, arbitrary background illustration replacing actual foreground material, or inaccessible decorative interiors masquerading as gameplay space.

**Primary artistic goal:** A sense of one constructed and later damaged place. Vertical machinery, exposed structural systems and deep engineered voids should explain how the city worked, how it fell into disrepair and where a small player can move. Preserve a hard, metallic silhouette with restrained colour accents and plausible material transitions. Avoid generic repeated square towers, indiscriminate surface greebles and decorative vegetation engulfing every region.

**Primary gameplay goal:** A clear entrance-to-exit traversal, optional vertical exploration, at least one alternative route and accessible room/shaft relationships. **Actual player dimensions, clearance and traversal mechanics are not guessed here**; M0 discovers the supported profile and native tests convert named routes into verified clearances.

**Planned visual hierarchy:**
- **Macro:** One dominant severed viaduct, two subordinate industrial landmarks and strong open shafts/chasm.
- **Meso:** Plausible bridge support load paths, floors, access hatches, piping ducts, scaffolding and causeways.
- **Micro:** Sparse material seams, exposed bolts/joints, wear, rust bands, debris, cable terminations, fracture lines and repair traces—only if the runtime material/palette supports them.
- **Void:** Large intentional transparent/empty cutaways and traversable negative space; do not simply cut an inaccessible hole or leave the entire perimeter blank.

## 2. Spatial macro plan

Partition **proposal ownership**, not separate physical Worlds:

| Region | Half-open local coordinates | Landmark and character | Boundary requirements |
|---|---|---|---|
| `foundry` | x: 0–735, y: 0–1023 | Rusted furnace spine, loading alcoves, layered service corridors | Connect to viaduct's main level and one lower duct |
| `viaduct` | x: 736–1359, y: 0–1023 | Collapsed transit truss above a broad void, supports and alternative crossing | Match foundry portal and reservoir landing without severing player path |
| `reservoir` | x: 1360–2047, y: 0–1023 | Sealed tank vault, broken channels, compressed machinery terraces | Receive viaduct path and expose a legible exit |

Two explicit joint contracts:

- `J-FV` at x=736, foundry↔viaduct; named `service-gateway` plus `maintenance-bypass`.
- `J-VR` at x=1360, viaduct↔reservoir; named `main-landing` plus optional lower conduit.

The *position, elevation and clearance* of these connectors are planning decisions to be tested against actual intended player/actor physics. Do not hardcode them as accepted just because both artists describe the same number.

**Global protected routes:** `R-MAIN` connects entry to exit; `R-ALT` provides an alternative crossing or loop; `R-ACCESS` links any required upper/lower facility. Mark their union, plus agreed clearance margins, as a protected occupancy mask. Only a director-approved route revision may resize/relocate that mask.

**Environmental continuity:** Industrial steel/masonry palette with localized rusty/oxidized bands; the viaduct may be broken but retain a credible support logic; the reservoir can have water only if the selected native World and solver qualification support the requested bounded behavior. A decorative still-water illustration is never labeled a simulated reservoir.

## 3. Agent choreography

This is a dynamic OMP coordination plan, **not** a static YAML requirement.

| Phase | Active workers | Durable output / checkpoint |
|---|---|---|
| P0: independent concepts | Director + 2–3 short proposal agents | Alternative macro silhouettes and a concise pros/cons comparison |
| P1: director convergence | Director + traversal planner | Frozen World Bible, route graph, region leases, joint v1 |
| P2: parallel construction | Foundry architect, viaduct architect, reservoir/environment architect | Separate valid native recipe/overlay proposals; no shared file edits |
| P3: interface negotiation | Adjacent pairs + traversal checker; director resolves | Joint v2/3 decisions; rejected stale proposal identities |
| P4: composition | Single integrator, optional read-only source reviewer | Native final play-plane preview, seams, material hashes, error reports |
| P5: critique | Independent visual critic + structural validator | Seven-axis visual report, route checks, targeted edits to attempt |
| P6: bounded repair | Original owning specialist, then integration + critic | Verified revision or retained best accepted baseline |
| P7: owner inspection | Owner, assisted by OMP | Original screenshots, Workbench saved-start candidate and evidence summary |

Agents can discuss across phases using native `agent://` messages. The director may ask a specific worker to revise an interface without discarding the rest of its region. The finite stage limits prevent open-ended conversation loops or redundant decoration.

**Pilot budget:** Start with three concurrent construction specialists and one serialized native integrator; limits for calls/tokens/USD/time/CPU/disk are configured before model dispatch. First fixture runs should use no external inference. The first billed run requires explicit owner permission, verified credentials and tested GPTopus-style safeguards.

## 4. Worked seam negotiation

**Situation:** The foundry architect proposes an elevated rail access door, while the viaduct architect proposes a lower transit deck. Both independently valid modules would create a discontinuity at x=736.

**Expected successful process:**

1. Both agents publish `proposal` files with their intended socket IDs, positions, clearances and joint revision; no material is applied.
2. The external geometry checker reports `J-FV: CONNECTOR_ELEVATION_MISMATCH` with exact coordinates, not a vague aesthetic complaint.
3. The director asks the neighboring specialists to propose up to two viable fixes: (A) a stepped service stair/shaft with access; (B) rerouting the deck to a lower access point while preserving a striking bridge silhouette.
4. The traversal specialist evaluates actual route legality with the chosen actor/collision assumptions. If neither passes, `J-FV` stays `BLOCKED` and the region is not integrated.
5. The director selects a plan or requests an owner decision, publishes `J-FV revision 2` and invalidates *both* proposals referencing revision 1.
6. The two local specialists revise only the necessary geometry, then a single integrator renders the complete seam and verifies exact native readback.
7. The critic checks visual plausibility: is the connector physically legible, and does it make the neighboring districts look like the same designed facility?

**This is the essence of the experiment:** A good swarm pays for cross-boundary negotiation instead of merely making more images at the same time.

Other injected failures to test: support column across `R-MAIN`; decorative pipe ending in empty air at border; two workers replacing the same cell; overzealous greebles filling an approved chamber; physically active sand/water placed in an unstable structure without qualifying simulation evidence.

## 5. Candidate production and runtime evidence

Expected local handback artifacts:

```text
pilot-iron-wound-001/
  brief/world-bible-v1.json
  references/cards/*.json
  regions/leases/*.json
  joints/J-FV-vN.json
  joints/J-VR-vN.json
  proposals/<agent>/<revision>/{recipe.json,edits.json,notes.md}
  decisions.jsonl
  native/receipts/{generation,apply,readback,reopen}*.json
  captures/{full,viewport,detail,material-ids}*.png
  reviews/{visual,structure,traversal}*.json
  release-candidate/{start-manifest,source-provenance,readme}*
  report.md
```

The starred paths denote types of outputs, **not** presupposed native filenames. The implementing adapter shall specify and test the exact CyberSand format. Receipts must distinguish synthetic material-ID previews from actual graphical Godot capture and observed simulation.

**Capture stages:** composition full view; each landmark; both inter-region seams; selected closeups demonstrating useful micro-detail; intentional voids; a route/collision overlay; state before and after any physically dynamic test. Native readback may be material IDs rather than a rendered appearance. Capture each with SHA, source/runtime identity, dimensions, crop and renderer.

**Native sequence:** Validate source recipe(s) → compile/generate selected finite region → capture non-mutating preview → director selects accepted composition → if supported, install in disposable Workbench World via an existing method → confirm actual changed cells → Save authored start → restart Godot → Load/reconstruct → compare accepted properties. If installation is not externally accessible, stop at a verified recipe+preview and perform a separately described manual Workbench import; do not claim the stage passed.

## 6. Visual and physical acceptance

**Hard gates:** Valid native materials and bounds; source/runtime fingerprint compatibility; route occupancy protected; shared sockets and required access verified under the *chosen actual* traversal model; no unauthorized region overlap; saved-start reconstructibility; no silently dropped accepted erasures/overpainting; and no unreconciled partial writes.

**Visual rubric:** Reuse all seven existing CyberSand world-design `QUALITY_BAR.md` axes: silhouette/scale hierarchy; architectural/geological richness; micro-detail authenticity; value/colour discipline; environmental narrative; coherent integrated composition; cross-theme distinctiveness. The documented aspirational goal is at least 4/5 in each axis **with written evidence and actual captures**. Aesthetic scores remain independent judgments, not reproducible hard checks.

**Human questions:** Does the place feel authored? Is the viaduct structurally convincing? Can one read the routes at full scale? Does the negative space serve both composition and play? Does the world remain interesting when examining the main structures at close range? Can a user actually play the saved start?

**Physics gates:** Where Water/Brine/Sand or reactive materials are used as operational elements, run source-matched native tests and report observed t=0/60/600+ (or the applicable test cadence), material conservation, leakage/collision, timing and stability. Do not infer from a static screenshot. A dry fixed version may be accepted as an aesthetic preview while dynamic claims remain `UNTESTED`.

## 7. Controlled A/B experiment

Test the *collaborative method* rather than just "three artists can make more pixels":

- A and B receive the same theme, source checkout, target canvas, module catalogue, starting seed set and material allowlist.
- Both get comparable aggregate model tokens/calls and native operation budgets, and the same capture opportunities.
- **A** uses independent region briefs with no negotiated joint contract until final composition.
- **B** uses shared World Bible, explicit joint/socket negotiation and protected route proposals before integration.
- Preserve all generated candidates, failures and repair costs for each condition; no survivor-only winner gallery.
- Blind the visual judges to condition labels where practical. Evaluate full renders at matched scale, not only appealing crops.
- Report direct metrics: required routes connected, seam mismatches, invalid/overlapping writes, protected-cell violations, native admission rate, failed/repeated work, actual model calls/tokens, generation/capture duration, fresh reopen pass, visual rubric and owner preference.
- At least two source-seed scenarios should be examined before making claims of generality; a single showcase is a proof of concept, not statistical evidence.

**Possible negative result:** The swarm consumes more model work but does not improve perceived coherence. Accept that outcome, inspect coordination overhead, simplify the roster and preserve the evidence rather than selecting only a success.

## 8. Handback and extension conditions

The owner should receive a concise run report containing: exact Git/native/runtime source IDs; World Bible and named joint decisions; plain-language map description; full and crop screenshots with provenance; an annotated traversal map; actual native/Save/reopen outcomes; measured resource use; visual critic dissent; limitations; and a reproducible import/replay recipe.

The owner may then decide to accept the current level, request one bounded revision or commission a second environment with different structural challenges (organic cave/biomechanical lab) to test whether the method generalizes.

**Release gate:** No automatic CyberSand PR/merge, no unapproved push, no private SANDMAPS upload and no claim of fully playable success without fresh actual Workbench/native evidence and owner testing. The result of this pilot should inform whether any additional OMP orchestration code is justified at all.

See [CONTRACTS.md](CONTRACTS.md) for exact document and receipt semantics and [DELIVERY-PLAN.md](DELIVERY-PLAN.md) for implementation dependencies.
