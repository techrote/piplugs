# RustySpork / Oh-My-PI — M0 host capability

**Status:** source/code candidate; no neural weights or hosted inference used. This package is *not* the deterministic RustySpork surgery controller. It provides **plan-only** experiment safety checks, one OMP command and four read-only research agent definitions.

## Install as an OMP linked plugin

From the `piplugs` checkout with OMP 19.1.0-compatible runtime:

```sh
omp plugin link ./plugins/rsn-omp
omp plugin list
omp skill list --json
```

After OMP loads the extension, use `/rustyspork status` or `/rustyspork check <workspace-relative-proposal.json>`. The validator is pure Python stdlib: `python3` on Linux, `py -3` on Windows, or an explicitly trusted `RSN_PYTHON` interpreter. Plugin `src/index.ts` constrains fixture paths to the current workspace after lexical and realpath/symlink checks, launches a fixed Python script with `Bun.spawn` (no shell), and returns error codes—not file contents.

Without OMP:

```sh
python3 plugins/rsn-omp/tools/make_fixtures.py
python3 -m unittest discover -s plugins/rsn-omp/tests -v
python3 plugins/rsn-omp/tools/validate_proposal.py plugins/rsn-omp/fixtures/funnel-plan.json
python3 plugins/rsn-omp/tools/validate_proposal.py plugins/rsn-omp/fixtures/lfm-q6-reap-plan.json
```

The corresponding `*-unsafe.json` fixtures **must fail** with exit code 1.

## The boundary

- **CALS remains separate.** This plugin will not change CyberSand, its Workbench or the CALS Draft PR.
- **RustySpork remains scientific authority:** all future weight changes, exact tensor/quant decoder, original checkpoint preservation, experiments, replay and acceptance reside in [`techrote/rustyspork-neurotzacken`](https://github.com/techrote/rustyspork-neurotzacken), **not** a second OMP scheduler.
- **GPTopus stays independent:** pending [ULTRA-001](https://github.com/techrote/Chlaude-GPTopus/issues/2) already develops protected worker governance and accounting; never copy unmerged code into a billed worker path or assume OMP has equivalent pre-dispatch hooks.
- **No paid calls:** `allow_paid_provider`, `allow_model_inference`, `allow_network_download`, `allow_weight_write` must all be `false`. `max_paid_usd` is `0`. These fields govern the *offline fixture validator only*, not OMP's actual capabilities; live workers need OS/provider-level enforcement.
- **No fake science:** manifest digests are only syntax-checked here; synthetic source SHA/quant metadata do not authenticate a real donor. PASS is **not** permission to mutate weights, claim causal feature identity or report Q6 memory savings.

## Next gates

1. Verify OMP discovery and the package command with Windows and Linux CI, independently of the repository root.
2. Exercise native OMP agent task/messaging in a separately secured test workspace. Read-only role YAML is not a complete tool sandbox.
3. Implement a **small immutable-donor inventory + toy numerical causal experiment** in RustySpork's deterministic controller, with precise tests of frozen targets and matched-random edits. Preserve [RSN-001](https://github.com/techrote/rustyspork-neurotzacken/issues/1).
4. Separately prove exact Q6 quant tensor listing and no-op roundtrip on a tiny synthetic GGUF; no multi-GB downloads in CI.
5. Integrate GPTopus-derived worker policies only if runtime enforceability is established, with explicit key/usage settlement and Windows tests. No billable fallback.

[Integration architecture](../../proposals/rustyspork-omp/README.md)
