# RSN-OMP-001 — RustySpork as an Oh-My-PI research workload

**Status:** early implementation on a separate `piplugs` branch; do not merge without owner acceptance. **Date:** 2026-11-22.  
**Scientific repository:** [techrote/rustyspork-neurotzacken](https://github.com/techrote/rustyspork-neurotzacken). **Host:** [Oh-My-PI](https://github.com/can1357/oh-my-pi). **Worker policy reference:** [Chlaude-GPTopus](https://github.com/techrote/Chlaude-GPTopus).  
**Scope:** no CyberSand work, no donor downloads, no GPU jobs and no paid model requests.

## Contents

1. [Ownership and scientific objective](#1-ownership-and-scientific-objective) — Keep deterministic surgery outside the LLM host.
2. [Agent duties and limits](#2-agent-duties-and-limits) — Give advisors useful work but no mutation authority.
3. [Host/experiment protocols](#3-hostexperiment-protocols) — Pass proposals through strict, independent gates.
4. [GPTopus reuse](#4-gptopus-reuse) — Adopt protected accounting rather than duplicating a scheduler.
5. [Cloud preparation and CI](#5-cloud-preparation-and-ci) — Qualify the host without models or actual weights.
6. [Next milestones and acceptance](#6-next-milestones-and-acceptance) — Advance toward real RustySpork without falsely claiming results.

## 1. Ownership and scientific objective

This is **not** another swarm harness inside the RustySpork numerical runtime. Use Oh-My-PI `task`, `agent://` and agent lifecycle for asynchronous critique, discovery, calibration design and independent review. A **deterministic RustySpork controller**—defined in the separate research repo's [pending `DETERMINISTIC_LAB.md`](https://github.com/techrote/rustyspork-neurotzacken/pull/2)—owns file I/O, experiment DAG, donor locks, exact low-rank or expert pruning operations, source hashes, native GPU execution, resource ceilings and immutable trial receipts. OMP only composes reviewed plans and *consumes* evidence. The controller does not yet exist; no new runner is represented here as production ready.

Keep two independent research arms:

- **Frozen-feature reblitteration** in [RSN-001](https://github.com/techrote/rustyspork-neurotzacken/issues/1). Identify and causally validate useful feature/circuit; freeze detector weights; select earlier attention/MLP projection allowlist; try rank 1–4 upstream edits; evaluate missed-opportunity gain, false positives, already-correct stability, KL/output drift, matched-random and LoRA controls. Initial model 1–4B, not the giant Q6 specimen.
- **Source-exact LFM2.5 Turbo-Brilliance Q6 expert pruning** as covered in the [RustySpork research dossier](https://github.com/techrote/rustyspork-neurotzacken). The primary model is DavidAU LFM2.5-24B-A2B Turbo-Brilliance NEO/MAX-NEO Imatrix Q6_K, with an owner target of 3–5 GB real memory recovery without slowing or degrading useful behaviour. KAT-Coder-V2.5 REAP-50 Q6_K is an independent reference, not a baseline for LFM. Actual GGUF variant/sha/tensor layout must be pinned before any GPU or compaction work.

No subject model is downloaded by the host plugin or CI; a synthetic tensor fixture is never equivalent to source-matched native GGUF parsing.

## 2. Agent duties and limits

| Role | Proposal/evidence work | Never allowed in M0 |
|---|---|---|
| `rsn-causal` | frozen target hypotheses, upstream allowlists, contrastive controls | unfreeze targets, execute novel weights |
| `rsn-moe` | exact Q6 tensor/quant layout and REAP compaction risks | rewrite donor or claim source-equivalence |
| `rsn-evaluator` | disjoint suites, matched controls, quality/speed/VRAM criteria | choose holdouts after results; self-approve |
| `rsn-custodian` | provenance, permissions, missing evidence and stop conditions | change policy, exercise owner authority |

Roles have OMP built-in tool lists `read,grep,find`, but OMP can expose separate extension/MCP tools; list metadata is **not a security sandbox**. All live subagents must be tested on the intended host with enforced workspace and tool permissions before use on valued models. A single coordinator accepts revisions and maintains the experiment ledger; prefer direct existing OMP native communication, not static forked swarms.

## 3. Host/experiment protocols

Use `piplugs.rsn-omp.experiment-proposal` v1 as an **independent offline host admission format**; do **not** assume RustySpork's proposed `rsn.experiment.v1-proposal` is implemented or identical. Conversion requires an explicit, versioned adapter and tests after the RustySpork controller exists.

Valid M0 plan-only proposals require a claimed fully qualified donor revision/SHA, distinct evaluation/corpus hashes and disjoint case IDs, declared control arms, immutable donor, explicit `allow_network_download=false`, `allow_model_inference=false`, `allow_weight_write=false`, `allow_paid_provider=false`, `max_paid_usd=0`, and bounded runtime. Reblitteration additionally requires frozen target tensor list and disjoint upstream rank-1–4 allowlist; REAP needs feasible post-pruning top-k and non-export policy. A failed code stops downstream proposal promotion. `fixture_only=true` uses fake synthetic source identities and may be tested in CI without model weights; always label that distinction.

The preflight **never opens the donor, hashes it, validates actual tensor names, checks causal feature activation, verifies quant block packing or proves held-out task performance**. Its PASS verifies only declared plan integrity. No-op exports, donor hash checks and real inference must remain separate deterministic RustySpork gates.

## 4. GPTopus reuse

Reuse the *semantics*, not the Claude Code-specific `turn.step` hooks. The linked [ULTRA-001 Draft stack](https://github.com/techrote/Chlaude-GPTopus/issues/2) already has policy, two-key admission, durable usage accounting, recursive fleets, approval boundaries and cross-platform mocked tests. It is **not merged or live-provider accepted**. Before OMP bridge work, compare current OMP `task`/provider lifecycle to these policies and choose a small tested provider adapter if OMP cannot enforce key/model/tier binding before each billable call. Key fallback must always fail closed, not convert a free worker to a paid worker. The $88 user allowance reference remains informational, not an actual spending cap.

## 5. Cloud preparation and CI

1. CI on Ubuntu and Windows checks 36+ Python standard-library proposal tests with no network fetch of weights or live model requests. Negative fixtures assert refusal of target-frozen edits and weight writes.
2. Install pinned OMP 19.1.0 and Bun 1.4.4 in hosted tests; link `@techrote/rustyspork-omp` from an independent project, discover `rustyspork-lab` and test the `/rustyspork` TypeScript command. This is **plugin qualification**, not a real OMP team demonstration.
3. Make a source-only manifest/role check. Do **not** import undocumented OMP private agent-discovery modules from its bundled npm CLI; the supported public path differs from source files.
4. Retain text logs and optional discovery JSON as GitHub run artifacts. No donor bytes, model secrets, private local corpora or large GPU artifacts in Actions.
5. Future gate: use safe simulated OMP worker transport/no-API fixture, then a controlled real host agent-message experiment. Keep that isolated from owner-local Q6 and paid API credentials.

## 6. Next milestones and acceptance

| Milestone | Deliverable | Exit criterion |
|---|---|---|
| **H0** | Host plugin + scheme/fixture unit suite | CI passes Linux/Windows; safe plan-only command; separate install |
| **H1** | Real OMP worker lifecycle and permission denial | actual task spawn/message/revive, adversarial write refusal, complete logs; no billable model calls unless specifically approved |
| **R0** | RustySpork immutable donor inventory / no-op toy | exact hashes, bit-for-bit donor preservation, deterministic trial DAG fixture |
| **R1** | Small frozen-feature upstream edit proof | causal intervention + heldout positive/negative and matched-random comparisons; ability to fail scientific hypothesis |
| **R2** | Tiny GGUF no-op plus Q6 block/expert census | source/quant type/layout and integrity proven, no 24B mutation |
| **R3** | Protected 24 GiB LFM research pilot | owner-authorized source-exact Q6 access, candidate export and real resident-memory+behaviour metrics |
| **U0** | FRANKENFIELD atlas | honest display-to-exact-tensor coordinates and actual replayed edit receipts; GPU budget enforced |

User acceptance is independent from CI, and any authoring of large variants or live paid model calls needs separate approval. Nothing here touches CyberSand, DRIV3R, XenoField or the two existing Draft/HOLD stacks.
