---
name: rustyspork-lab
description: Coordinate bounded RustySpork neural weight-surgery research proposals in OMP without touching donor weights, bypassing holdouts or spending provider credits.
---

# RustySpork Lab — OMP M0 dry-run skill

**Phase:** synthetic, plan-only CI prototype. This is not a model loader, REAP compactor, causal tracing framework, VRAM benchmark, or permission sandbox.

The scientific programme lives in [RustySpork](https://github.com/techrote/rustyspork-neurotzacken). In that repository, [RSN-001](https://github.com/techrote/rustyspork-neurotzacken/issues/1) owns reblitteration and [Draft PR #2](https://github.com/techrote/rustyspork-neurotzacken/pull/2) contains unmerged deterministic lab/FRANKENFIELD plans. Do not copy or silently override them. The approved specimen pair is KAT-Coder-V2.5-Dev REAP-50 Q6_K (reference) and DavidAU LFM2.5-24B-A2B Turbo-Brilliance NEO/MAX-NEO Q6_K (memory-recovery target, exact file still to be pinned).

## Roles and safety boundary

Use *native* Oh-My-PI `task` and `agent://` for specialist proposal/review when host policy allows. Never implement a parallel OMP runtime. The coordinator and agents can investigate and write **external, clearly marked proposals** only when an actual OS/OMP workspace boundary authorizes those writes. Built-in `tools: read,grep,find` on agent definitions does **not** protect from every extension/MCP tool; test permissions before relying on them.

- **Causal investigator:** hypotheses, frozen detector, eligible upstream rank-1–4 pathways, proper negative controls, held-out target activation and task-quality measurements.
- **MoE investigator:** source-exact Q6 tensor inventory research, REAP saliency methodology, 8/12/16-expert candidate budgets, router+bias remap proof. No GGUF editing from an agent.
- **Evaluator:** locks calibration and heldout corpora before results, prepares matched donor/random/frequency and no-prune controls, reports regression conditions.
- **Independent custodian:** audits donor custody, source SHA, key/billing route, frozen tensors, study power, failed trials, exact output claims and human approval.

An LLM's proposal is never an executable authorization. The **deterministic RustySpork controller, once implemented in the RustySpork repository, must own tensor writes, GPU execution, artifact hashes, outcome recording and promotion**. Do not access owner-local donor paths from CI, auto-download multi-GB specimens, or launch local GPU/cloud model calls simply to populate an example. Avoid changing CyberSand, DRIV3R or XenoField.

## First offline exercise

Run `/rustyspork status` and `/rustyspork check <relative.json>` using the optional packaged extension, or use this standard-library validator directly:

```sh
python3 plugins/rsn-omp/tools/validate_proposal.py plugins/rsn-omp/fixtures/funnel-plan.json
python3 plugins/rsn-omp/tools/validate_proposal.py plugins/rsn-omp/fixtures/lfm-q6-reap-plan.json
python3 -m unittest discover -s plugins/rsn-omp/tests -v
```

Fixture-only synthetic outputs passing the preflight show the **proposals' declared constraints are internally safe**, not that the source hashes were read or any real neuron/expert exists at those addresses. If `fixture_only` is false, the hash remains a **claim** until a separately verified inventory receipt reads the actual immutable donor. Unexpected input is a hard FAIL; do not attempt conversion to an executable weight patch.

## Completion / escalation

State who was allowed to propose; exact source and corpus identities; which controls were held aside; what actual commands ran; failures, PASS/FAIL/UNTESTED; and which gates require a human. Reblitteration needs causal proof and false-positive preservation. LFM compaction needs source-exact quant-block and router-index correctness, loader smoke, measured resident VRAM reduction, decode/prefill and behaviour results. Until then all outcomes are `PROPOSAL_ONLY` and the API-spend budget is zero.
