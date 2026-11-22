# CALS-001 — Engineering delivery plan and acceptance gates

**Status:** IMPLEMENTATION PLAN ONLY, no code executed or end-to-end behavior demonstrated.  
**Repository:** `techrote/piplugs`. **Target:** optional OMP plugin; CyberSand remains unchanged.

## Contents

1. [Scope, outputs and strategy](#1-scope-outputs-and-strategy) — Define the smallest useful product and its non-goals.
2. [M0: source and capability preflight](#2-m0-source-and-capability-preflight) — Prove real host and engine boundaries before designing against them.
3. [M1: minimal orchestration skill](#3-m1-minimal-orchestration-skill) — Demonstrate native OMP peer negotiation without paid inference plumbing.
4. [M2: GPTopus worker-policy port](#4-m2-gptopus-worker-policy-port) — Enforce two-key routing, reservations and cost controls.
5. [M3: CyberSand native authoring adapter](#5-m3-cybersand-native-authoring-adapter) — Produce source-exact materials and saved-start evidence.
6. [M4: collaborative composition](#6-m4-collaborative-composition) — Resolve seams, protected regions and design conflicts.
7. [M5: independent critique and refinement](#7-m5-independent-critique-and-refinement) — Improve the actual native result without uncontrolled iteration.
8. [M6: end-to-end pilot and packaging](#8-m6-end-to-end-pilot-and-packaging) — Compare against a baseline and document a safe installation path.
9. [Test matrix and adversarial cases](#9-test-matrix-and-adversarial-cases) — Make false success difficult.
10. [Security, resource and failure budgets](#10-security-resource-and-failure-budgets) — Protect credentials, source and spending.
11. [Definition of done and owner gates](#11-definition-of-done-and-owner-gates) — Separate engineering readiness, art acceptance and publication.
12. [Risks, contingencies and deferred work](#12-risks-contingencies-and-deferred-work) — Preserve a minimal viable path when a capability fails.

## 1. Scope, outputs and strategy

**Target product:** `piplugs` packages one optional `cals` OMP skill/extension. A user supplies a written landscape brief and optional local images. OMP forms a small agent team, derives a versioned World Bible, negotiates region interfaces, generates legal external proposals, runs existing source-pinned CyberSand tools, captures genuine evidence, reviews/repairs selected defects and exports a reproducible Workbench-authored start candidate for owner approval.

**MVP scope:** One finite 2048×1024 side-elevation play plane, three adjacent districts, two contractual shared boundaries, at least one continuously traversable route, one distinctive focal structure, material-valid source and a real render. The work should be reproducible across a fresh process. Actor/physics validation is conditional on the actual selected runtime capability.

**Non-goals:** No new CyberSand runtime code, no new stored-world format, no giant model training campaign, no 3D assets, no automatic external art publication, no web rebuild, no always-on orchestration server, no unattended multi-day model loop and no GitHub merge to CyberSand.

**Preferred implementation layout after approval (paths do not exist yet):**

```text
plugins/cals/
  package.json                    # OMP package manifest only if required by current host
  src/index.ts                    # narrow OMP command/status entry point
  src/policy/*                    # GPTopus-derived tested policy adapter, not Claude mods
  src/contracts/*                 # schema validators and canonicalization
  src/plan/*                      # coordinator; leases/joint checks, no native World
  src/cybersand/*                 # local source-pinned CLI/file adapter
  src/receipts/*                  # deterministic evidence and snapshots
  skills/landscape-studio/SKILL.md
  agents/*.md                     # only where current OMP discovery supports roles
  test/fixtures/                 # small, deterministic, no API keys
  test/*.test.*
examples/cals-pilot/            # sample brief and expected fixture shapes, not billed inference
docs/                             # installation, threat model and measured acceptance evidence
```

The proposal documents in this directory are the **design authority** until an implementing PR names replacements. Implement vertical slices rather than first writing an abstract generic agent framework.

## 2. M0: source and capability preflight

**Dependencies:** None. **Allowed changes:** design/test harness and isolated spike only.

Tasks:

1. Pin OMP, GPTopus and CyberSand exact Git SHAs and local binary identities. Capture Windows/Godot toolchain, OMP install version and host configuration, without exposing secrets.
2. Inspect current OMP extension/plugin lifecycle, `task` invocation, `agent://` messaging, isolated workspaces, subprocess permission model, model-selection restrictions and whether pre/post provider-call interception is available.
3. Prove two authenticated profiles can be resolved *distinctly* in OMP (with a stub first) and that an external dispatcher can gate every chargeable request, including retries and agent revival. If not, document provider-adapter fallback.
4. Confirm CyberSand native GEN-007 schema and sample recipe validity; actual installed module catalogue and material/rectangle limits; generated-start v1/Setup-v2 path; source/runtime hashes; path to a real capture; exact fresh-process import/reopen test.
5. Check which promised authoring capabilities actually exist on accepted main. Treat pending PAINT/agent/Gentek/depth candidates as opt-in separate lanes, not baseline requirements.
6. Establish smallest headless/no-network fixture to validate a 64×64 or comparable finite material canvas and a deterministic screenshot. Keep all original stdout/stderr/exit status.

**Evidence:** `capabilities.json` (method and tested yes/no), source ledger, process logs, verified build identity, exact sample command and clean failure handling.

**Gate M0:** No planned interface can be marked `implemented` without an executed probe. Missing model gating or native write API is not grounds to modify CyberSand automatically; use an alternate external/fixture path or stop the relevant slice.

## 3. M1: minimal orchestration skill

**Dependencies:** M0 host discovery. **No direct OpenAI requests required.**

Deliver a small OMP skill with director and three specialists, a fixture World Bible, typed leases/work orders and an integration-reader role. Prove one directed agent spawn, one parallel batch, one live peer negotiation, one revision/invalidated proposal, one restart/follow-up and one read-only critic.

Implementation details:

- Define a **small roster of specialized roles**, not a permanent subagent hierarchy: director, architect, terrain designer, traversal checker, critic.
- Keep the proposal protocol in external JSON files (`CONTRACTS.md`) with unique paths, hashes and a single manifest/lease writer.
- Prefer OMP's current native `task`, `wait`/`agent://`, `history://` and Agent Hub. Do not embed the removed swarm-extension or imitate its own process pool.
- Restrict outputs to a per-agent directory and report. Treat changes to `AGENTS.md` or a shared World Bible as coordinator-only.
- Test a message arriving after an agent becomes idle/parked and handling of an agent whose result is truncated or unavailable.
- Handle inherited child prompt/tool permissions as real capabilities; prove that an evaluation-only agent cannot write to the integration output.

**Gate M1:** Two specialists negotiate one shared connector, produce nonconflicting immutable proposals, and the director correctly detects stale or conflicting lease generations. A failed worker must block dependent final integration rather than being silently treated as done.

## 4. M2: GPTopus worker-policy port

**Dependencies:** M0 dispatch capability. Can develop in parallel with M1 typed contracts.

Port only tested policy primitives and their original license/attribution. Preserve source identities and add differential tests against donor fixtures. **Do not** import GPTopus Claude-specific `turn.step`/`session.start` hooks into OMP.

Core deliverables:

- Six named worker-profile aliases (matching GPTopus where still supported), with explicit model/tier/provider/account choices and capability checks. Unknown or unavailable model is a configuration error, not a chargeable fallback.
- Two isolated key profiles (free-programme and standard) with usable Windows credential storage and non-Windows equivalent; no key exposure in debug output, model messages or evidence bundle.
- Atomic, cross-process admission for free-group quotas, with one correct daily/response identity, pending reservations, conservative accounting on lost responses, UTC rollover and corruption fail-closed.
- Actual enforceable paid-budget admission independently from the informational GPTopus `MonthlyAllowanceUsd` setting. If reliable per-call priced estimates and a cap are not available, disable unattended straight-key usage by default.
- Lifecycle integration: reserve before dispatch, settle once on final usage, reconcile after timeout/crash/retry, deny unauthorized automatic provider/key/tier switching.
- Test per-agent max steps, max concurrent requests, cancellation, abort propagation, config precedence, no billing under parser/proposal errors.
- Expose `cals status`/equivalent diagnostics reporting actual configured profiles and local reservations; never claim the ledger equals provider billing.

**Specific negative acceptance tests:** no free key; no standard key; unsupported tier; wrong model for quota group; nearly-full quota; two processes racing for last reservation; duplicate response replay; unknown POST outcome; corrupted ledger; UTC midnight crossing; attempt to switch failed free worker to paid profile; cost estimate unavailable; unauthorized model fallback; agent resumption without new policy check.

**Gate M2:** In a mocked request transport, no remote request is ever issued before policy admission; a simulated concurrent crash cannot erase reservations or admit duplicate work. Real provider smoke is separate, explicitly owner-authorized and billed only after mock tests.

## 5. M3: CyberSand native authoring adapter

**Dependencies:** M0 native discovery, M1 contracts. No need to wait for paid M2 smoke; deterministic fixtures can call the native engine.

**Preferred implementation:** A thin local command/file adapter that validates recipe and source identity, invokes existing source-matched Godot/native qualification tooling, captures results, then invokes the accepted generated-start pathway. Do not invent a new Web RPC API or rely on the separate Web demo controller.

Required functions (proposed external interface; not existing CyberSand methods):

- `capabilities()`: exact engine/Godot/build/material/module/format/bounds support.
- `validateProposal(proposal,worldBible,joints)`: strict schema, coordinates, region and protected-cell guards.
- `generatePreview(sourceRecipe,region)`: actual finite GEN-007 proposal with copied material data and receipts.
- `capture(candidate)`: labeled full/viewport/detail images from a proven native/Godot capture path, with source and renderer hash.
- `installApproved(candidate)`: one serial transaction through an **existing** authorized Workbench/native route; refuses if this exact route cannot be called or reproduced safely.
- `readback(revision)`: actual stored material and changed-region receipts; never count only queued/apply-intent operations.
- `saveAndReopen(candidate)`: deterministic saved-start persistence plus fresh-process verification where the runtime supports it.

If the accepted Workbench has no external headless import/install route, use an **offline complete recipe + tested owner-facing manual import** as the M3 deliverable. Explicitly mark automated application `UNSUPPORTED`; do not sneak in a new engine API under the banner of a thin adapter.

Respect source capability claims for native material IDs, reaction behavior, actor spawns, pressure/water policy and paint/flatten. A prepared generator may yield a valid starting static canvas without asserting live physics stability. Separate `play` plane from optional semantic far/background planes.

**Gate M3:** One generated source recipe imports through an existing validated path, generates source-bound native material output, obtains real screenshots, and survives same-source fresh-process Save/reopen. If native binaries differ, record fingerprint mismatch and fail without reinterpretation.

## 6. M4: collaborative composition

**Dependencies:** M1 and M3; M2 paid smoke only if selecting hosted inference.

Deliver the full three-region choreography of [PILOT.md](PILOT.md):

1. Director proposes macro world plan and constraints.
2. Traversal agent reserves mandatory routes and passage/surface interface contract.
3. Adjacent builders independently propose district geometry and connection endpoints.
4. Peer-negotiated conflicts become new `joint` revisions; stale dependent candidate files are automatically rejected.
5. Single integrator validates ordering, occupancy, negative-space constraints, native capability budgets and seams.
6. Every installed chunk/region is read back; failed/partial writes do not allow downstream acceptance.

**Gate M4:** Both shared boundaries connect under the verified chosen traversal model. Injected conflicting material edits, blocked voids, stale lease and wrong seed cause refusal without unrelated region damage. Repeat fixed seeds and compare accepted native output identities.

## 7. M5: independent critique and refinement

**Dependencies:** M4 validated candidate and actual capture.

Use original CyberSand seven-axis visual rubric. Critic(s) inspect the same candidate and genuine evidence, with implementer identities and earlier subjective scores withheld where practical. A separate structural validator supplies objective data.

Implement finite revision rounds with:

- Initial frozen artifact, rubric, source/runtime identity and acceptance baseline.
- Distinct proposed, approved and applied edits with predicted impact and actual before/after evidence.
- Targeted patch selection (e.g., one seam, one focal point, one clutter cluster), not whole-map regeneration.
- Preservation of last best **verified** candidate, negative outcomes and reasons.
- Hard stop on unchanged/no improvement after an agreed number of rounds, token/time budget, invalidated source or unresolved blocker.
- Owner selection for art direction. No model quorum or averaging can create a `production accepted` flag.

**Gate M5:** An independent reviewer identifies a seeded defect, a worker repairs only the affected proposal, and both native hard checks and a separately recorded soft review are rerun. A visually stronger but untraversable iteration must be rejected.

## 8. M6: end-to-end pilot and packaging

**Dependencies:** M0–M5 relevant gates. **Not authorisation to deploy/merge.**

Execute two matched pilot conditions:

- **Baseline A:** Three agents independently build regions from the same brief, without negotiated joint contracts, under comparable token/time/tool budgets; integration errors are honestly counted.
- **Swarm B:** Director, joint/lease negotiation, native validation and iterative critic using the same source, seeds, materials and target.
- Repeat with at least two source-seed configurations before generalizing; report failures and incomplete runs, not only selected winner. Avoid comparing tool-rich swarm with tool-poor control as a pure orchestration effect.

Package an optional OMP extension/skill with pinned supported versions, installation instructions for Windows 11, Linux fallback only where tested, `--dry-run` validation or equivalent, built-in doctor/status diagnostics, example fixtures, clean uninstall and license notices. Keep example images/manifests small; no private source or key material in package.

**Gate M6:** The owner can reproduce the exact native case from instructions, inspect the saved start in ordinary Workbench and understand every limitation. Tests/recorded results establish any advertised benefits of swarm collaboration. No unconditional "better than references" claim.

## 9. Test matrix and adversarial cases

| Layer | Positive tests | Adversarial/negative tests |
|---|---|---|
| Schema | Roundtrip, hash, version, canonical coordinates | Unknown version, huge arrays, path traversal, malformed JSON |
| OMP agent layer | Batch, directed message, revive, cost attribution | Child crash, stale context, duplicate agent, unauthorized write |
| Lease/joint layer | Nonoverlap, revision change, seam agreement | Same cell conflict, socket mismatch, stale lease, impossible route |
| GPTopus adaptation | 2-key routing, group quotas, reconciled response | Key substitution, timeout ambiguity, corrupt ledger, 2-process race |
| CyberSand generator | Native recipe, source-matched validation/capture | Invalid module, wrong materials, revision mismatch, budget exhaustion |
| Native apply | Serial acknowledged edits, actual stored IDs | Out-of-region write, denied protected cell, canceled partial mutation |
| Persistence | Fresh-process generated-start Save/reopen | Truncated manifest, drifted native ABI, lost erase ordering |
| Review | Blind rubric, separate hard/soft judgement | Bad screenshot provenance, hallucinated render/physics, false pass |
| Recovery | Restart at last proven checkpoint | Mid-write crash, runaway child, stale process, reservation leakage |
| End-to-end | Reproducible three-district pilot | Low available memory, missing provider, no GUI, owner cancels |

Test layers need clear status tags: `PASS` (actually executed), `FAIL`, `SKIP` (reason), `UNTESTED`, `PARTIAL`. A mocked API/renderer cannot prove real hosted inference or Godot gameplay. Repository source presence and CI workflow existence are not execution evidence.

**Suggested commands after implementation:** Node/Bun unit and integration runner for schema/policy, OMP smoke launched in a temporary project, Godot headless native qualification and actual graphical capture on source-matched Windows build, then fresh-process authored-start reopen. Every command should preserve stdout/stderr, exit code, SHA and artifact hashes.

## 10. Security, resource and failure budgets

**Default strategy:** start with **no paid API**, then explicit finite budget profiles for real tests. Example *provisional* pilot gates: three concurrently active workers, 1 integrator, one critic, finite per-agent request/step ceiling, no auto key/tier switching, capped generated shapes/regions, mandatory Stop/cancel. These are operator-tunable targets, not validated settings.

Do not mistake GPTopus's 250k/2.5M daily local admission targets, 10% headroom or `$88` reference for actual free entitlement or spend control. Paid routes require reliable admission constraints, account verification where feasible and explicit owner permission.

External input and model-generated Bash are hostile until bounded. Use file allowlists, run-specific subdirectories, symlink/path-traversal protections, OS-backed isolation, no access to credential stores/entire home, no unapproved `git push`/`rm`/dependency installation and read-only referee tools. OMP's headless subagents may operate in `yolo` mode; an instruction in a prompt is not an access-control boundary.

**Resource controls:** concurrency per provider and total, finite native job duration, max PNG/pixel/output count, max captured logs and disk retention, run timeout, process tree cleanup, and fixed source SHA. Abort must stop new dispatch first, attempt safe existing native cancellation, then preserve ambiguous outcomes for inspection. Do not reapply an uncertain edit.

## 11. Definition of done and owner gates

| Gate | Required condition | Decision authority |
|---|---|---|
| G0 — Feasibility | M0 OMP/native capability matrix with executable proofs | Engineering reviewer |
| G1 — Orchestration | Valid OMP peer collaboration and ownership enforcement | Engineering reviewer |
| G2 — Spend/credential safety | Live request admission is enforceable; all negative accounting tests pass | Engineering + owner consent for paid test |
| G3 — Native fidelity | Source-matched generator/captures, material receipts, Save/reopen | Native/runtime reviewer |
| G4 — Coherent level | Named joints, intentional voids, traversable routes and real scene integration | Native + traversal reviewer |
| G5 — Art quality | All seven CyberSand visual axes independently considered, with original comparison; owner evaluates | Human owner |
| G6 — Distribution | OMP installation/uninstall, security, platform scope, provenance, version pins, licensing | Owner release decision |

**Engineering done** does not imply **owner art accepted**, **playtested** or **merged**. A partial level or a negative feasibility result is an acceptable reported outcome. Do not change CyberSand main, promote any Draft PR, upload private references or publish binaries without subsequent explicit authorization.

## 12. Risks, contingencies and deferred work

| Risk | Impact | Contingency |
|---|---|---|
| OMP has no supported pre-provider dispatch gate | Free/paid-key segregation can be bypassed | Implement narrow explicit provider adapter or disable that worker route |
| GPTopus/OMP model API shapes drift | Accidental tier/credential fallback or runtime error | Pinned adapter contract tests, unsupported combination refusal |
| Existing Workbench lacks headless external install | Can't fully automate world import | Author source-valid recipe + native previews and perform explicitly manual Workbench acceptance |
| 2048×1024 native generation/capture is slow or stalls | Swarm wastes time/resources | Start small, require bounded metrics, serial native ops and Stop; preserve partial outputs |
| Agent negotiation becomes circular | More chatter than construction | Director controls finite decision deadline; test alternatives or block |
| Stale proposals after contract changes | Broken seams/material overwrites | Digest-based invalidation and one indexed acceptor |
| Visual critic rewards noise/paint volume | Cluttered, unreadable landscape | Frozen rubric, blind review, side-by-side viewport/crop checks, human selection |
| False runtime claims | Corrupted or unplayable output falsely shipped | Native receipts, actual capture provenance, independent reopen |
| Shared GPTopus/OMP key bypasses ledger | Unintended overrun | Shared guarded ledger or conservative budget partition; paid route default off |
| Enormous image/reference corpus causes data leak | Privacy, cost and latency | Local RAG-like selection of a few hash-identified cards; no full-corpus upload |

**Deferred:** Web/WASM Workbench parity, remote/cloud orchestration, persistent-area streaming, actor autonomous gameplay composition, SLM fine-tuning, novel Gentek schemas, new CyberSand brush contracts, multi-machine agent brokers, automatic public asset publishing and unattended continuous generation. These are separate programmes after a validated first native level.

References: [ARCHITECTURE.md](ARCHITECTURE.md), [CONTRACTS.md](CONTRACTS.md), [PILOT.md](PILOT.md), [SOURCES.md](SOURCES.md).
