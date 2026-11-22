#!/usr/bin/env python3
"""Offline, read-only RustySpork/OMP proposal validation — NOT tensor surgery.

Accept only safe, explicitly non-executing proposals. Claimed digests are checked
for shape, not against weight files. This code does not load models or perform IO
other than reading a bounded JSON document and writing its JSON verdict to stdout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

SCHEMA = "piplugs.rsn-omp.experiment-proposal"
VERSION = 1
MAX_INPUT_BYTES = 262144
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
IDENT = re.compile(r"^[a-z][a-z0-9_.-]{0,79}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
TENSOR = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]{0,199}$")
DATA_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,119}$")

ARMS = {
    "reblitteration": {
        "donor", "random-matched", "naive-scale", "activation-steer", "lora-matched"
    },
    "reap-pruning": {
        "donor", "random-removal", "router-frequency", "mixed-precision-no-prune"
    },
}


def is_int(value: Any, lower: int = 0, upper: int | None = None) -> bool:
    return type(value) is int and value >= lower and (upper is None or value <= upper)


def is_pos_float(value: Any) -> bool:
    return type(value) in (int, float) and 0 < value < float("inf")


def has_name(value: Any, pattern: re.Pattern = IDENT) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def bounded_names(value: Any, max_size: int, pattern: re.Pattern = DATA_ID) -> bool:
    return (type(value) is list and 0 < len(value) <= max_size and
            all(has_name(name, pattern) for name in value) and len(set(value)) == len(value))


def local_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or len(value) > 240 or not value:
        return False
    if "\\" in value or ":" in value or value.startswith("/") or "\x00" in value:
        return False
    pieces = value.split("/")
    return (len(pieces) <= 12 and all(p not in ("", ".", "..") and
            has_name(p, DATA_ID) for p in pieces))


def validate(proposal: Any) -> dict:
    errors: list[dict[str, str]] = []
    warnings = [
        "OFFLINE PROPOSAL ONLY: no checkpoint or tensor bytes opened; hashes and model identity are unverified claims.",
        "PASS is NOT an authorization to download, infer, mutate, export or bill any model."
    ]

    def fail(code: str, detail: str):
        errors.append({"code": code, "detail": detail})

    if type(proposal) is not dict:
        fail("ROOT", "Input must be a JSON object.")
        return {"status": "FAIL", "errors": errors, "warnings": warnings}
    if proposal.get("schema_id") != SCHEMA or type(proposal.get("schema_version")) is not int or proposal["schema_version"] != VERSION:
        fail("SCHEMA", "Expected piplugs.rsn-omp.experiment-proposal version 1.")
    if not has_name(proposal.get("proposal_id")):
        fail("PROPOSAL_ID", "A simple stable proposal_id is required.")
    if proposal.get("phase") != "PLAN_ONLY":
        fail("PHASE", "Only PLAN_ONLY proposals are admitted at M0.")

    source = proposal.get("source")
    if type(source) is not dict:
        fail("SOURCE", "A source record is required.")
        source = {}
    if not has_name(source.get("repository"), REPO):
        fail("SOURCE_REPO", "Require a source repository owner/name.")
    if not has_name(source.get("revision"), COMMIT_SHA) or not has_name(source.get("sha256"), SHA256):
        fail("SOURCE_PIN", "A 40-hex revision and 64-hex claimed checksum are required.")
    if not has_name(source.get("filename"), DATA_ID):
        fail("SOURCE_FILENAME", "Use a basename with no path separators.")
    if source.get("kind") not in ("mock-toy", "mock-gguf", "safetensors", "gguf"):
        fail("SOURCE_KIND", "Unknown source representation.")
    if type(proposal.get("fixture_only")) is not bool:
        fail("FIXTURE_FLAG", "fixture_only must be explicit boolean.")
    elif proposal["fixture_only"]:
        if not str(source.get("repository", "")).startswith("synthetic/") or source.get("kind") not in ("mock-toy", "mock-gguf"):
            fail("FIXTURE_SOURCE", "Synthetic fixture requires synthetic/* repo and mock kind.")
    elif source.get("kind") in ("mock-toy", "mock-gguf") or str(source.get("repository", "")).startswith("synthetic/"):
        fail("REAL_SOURCE", "Non-fixture proposals cannot claim synthetic sources.")

    authority = proposal.get("authority")
    if type(authority) is not dict:
        fail("AUTHORITY", "Explicit plan-only authority required.")
        authority = {}
    if authority.get("mode") != "proposal-only":
        fail("AUTHORITY_MODE", "Only proposal-only authority is supported.")
    for key in ("allow_network_download", "allow_model_inference", "allow_weight_write", "allow_paid_provider"):
        if authority.get(key) is not False:
            fail("SIDE_EFFECT", f"{key} must be explicitly false.")
    for key in ("immutable_donor", "owner_approval_for_promotion"):
        if authority.get(key) is not True:
            fail("CUSTODY", f"{key} must be explicitly true.")
    if not is_int(authority.get("max_runtime_seconds"), 1, 1800):
        fail("RUNTIME_BUDGET", "Plan-only runtime budget must be 1..1800 seconds.")
    if authority.get("max_paid_usd") != 0 or type(authority.get("max_paid_usd")) is bool:
        fail("PAID_BUDGET", "Plan-only permitted paid budget is exactly zero.")

    artifact_root = proposal.get("output_root")
    if not local_relative_path(artifact_root):
        fail("OUTPUT_ROOT", "Output path must be bounded, canonical, relative and slash-separated.")

    op = proposal.get("operation")
    if type(op) is not dict:
        fail("OPERATION", "Operation record required.")
        op = {}
    family = op.get("family")
    if not isinstance(family, str) or family not in ARMS:
        fail("FAMILY", "Only reblitteration and reap-pruning plans are supported.")
    if not is_int(op.get("seed"), 0, 2**32-1):
        fail("SEED", "Explicit 32-bit integer seed required.")

    ev = proposal.get("evaluation")
    if type(ev) is not dict:
        fail("EVALUATION", "Frozen evaluation protocol required.")
        ev = {}
    cal, held = ev.get("calibration_ids"), ev.get("heldout_ids")
    if not bounded_names(cal, 10000) or not bounded_names(held, 10000):
        fail("DATASET_IDS", "Calibration/heldout IDs must be nonempty unique bounded lists.")
    elif set(cal) & set(held):
        fail("DATA_LEAKAGE", "Calibration and heldout items must be disjoint.")
    if not has_name(ev.get("calibration_sha256"), SHA256) or not has_name(ev.get("heldout_sha256"), SHA256):
        fail("CORPUS_PIN", "Calibration and evaluation digests must be provided.")
    if ev.get("calibration_sha256") == ev.get("heldout_sha256"):
        fail("CORPUS_COLLISION", "Calibration and evaluation digests must differ.")
    arms = ev.get("control_arms")
    if type(arms) is not list or not all(isinstance(x, str) for x in arms) or len(arms) != len(set(arms)):
        fail("CONTROLS", "Control arms must be unique strings.")
    if isinstance(family, str) and family in ARMS and (type(arms) is not list or not ARMS[family].issubset(set(x for x in arms if isinstance(x, str)))):
        fail("CONTROLS_MISSING", f"Missing mandatory {family} control arms.")

    if family == "reblitteration":
        target = op.get("target")
        edit = op.get("edit")
        objective = op.get("objective")
        if type(target) is not dict or not has_name(target.get("feature_id")) or not bounded_names(target.get("frozen_tensors"), 128, TENSOR):
            fail("TARGET", "Feature identity and nonempty exact frozen tensors required.")
            target = {}
        if type(edit) is not dict:
            fail("EDIT", "Explicit upstream editing plan required.")
            edit = {}
        tensors = edit.get("upstream_tensors")
        if not bounded_names(tensors, 128, TENSOR):
            fail("EDIT_ALLOWLIST", "Bounded concrete upstream tensor allowlist required.")
        else:
            if set(tensors) & set(target.get("frozen_tensors", [])):
                fail("FROZEN_OVERLAP", "Requested edit intersects frozen target tensors.")
        if not is_int(edit.get("rank"), 1, 4):
            fail("EDIT_RANK", "Only rank 1..4 planned low-rank upstream deltas are permitted.")
        if edit.get("method") != "low-rank-upstream" or not is_pos_float(edit.get("max_delta_l2")):
            fail("EDIT_METHOD", "Require bounded low-rank-upstream operation and positive max_delta_l2.")
        if type(objective) is not dict or any(not is_pos_float(objective.get(k)) for k in (
                "missed_opportunity_gain", "false_positive_penalty", "already_correct_drift_penalty", "update_norm_penalty")):
            fail("OBJECTIVE", "Require contextual gain plus false-positive, already-correct and norm penalties.")
        positives, negatives = ev.get("heldout_positive_ids"), ev.get("heldout_negative_ids")
        if (not bounded_names(positives, 10000) or not bounded_names(negatives, 10000) or
                not bounded_names(held, 10000) or not (set(positives) | set(negatives)) <= set(held)):
            fail("CONTEXT_CONTROLS", "Heldout positives/negatives must be nonempty and contained in heldout IDs.")
        elif set(positives) & set(negatives):
            fail("CONTEXT_OVERLAP", "Heldout positives and negatives must be disjoint.")
        if source.get("kind") in ("gguf", "mock-gguf"):
            warnings.append("Reblitteration on quantized weights additionally needs quant-block coupling proof; not implemented.")
    elif family == "reap-pruning":
        topo = op.get("topology")
        if type(topo) is not dict:
            fail("TOPOLOGY", "Exact source topology must be provided as a claim.")
            topo = {}
        if not all(is_int(topo.get(k), 1, 1000) for k in ("moe_layers", "experts_per_layer", "active_experts_per_token")):
            fail("TOPOLOGY", "Positive integer MoE layers/experts/active routing required.")
        elif topo["active_experts_per_token"] >= topo["experts_per_layer"]:
            fail("ROUTER", "Active top-k must be less than total experts.")
        count = op.get("remove_per_layer")
        if not is_int(count, 1, 1000) or not is_int(topo.get("experts_per_layer"), 1, 1000) or count >= topo["experts_per_layer"]:
            fail("PRUNE_COUNT", "Removal must leave at least one expert per layer.")
        elif topo.get("active_experts_per_token", 0) > topo["experts_per_layer"] - count:
            fail("PRUNE_TOPK", "Pruning must preserve enough experts for active top-k.")
        if op.get("ranking_method") != "reap-candidate" or op.get("export_policy") != "disabled-until-native-proof":
            fail("PRUNE_METHOD", "Only preflight REAP candidate and explicitly disabled export permitted.")
        if source.get("kind") not in ("gguf", "mock-gguf") or source.get("quantization") != "Q6_K":
            fail("QUANT", "Initial REAP plan explicitly targets Q6_K GGUF family.")
        if source.get("repository") not in ("synthetic/lfm2-moe", "DavidAU/LFM2.5-24B-A2B-Turbo-Brilliance-50X-NEO-MAX-Imatrix-GGUF"):
            fail("LFM_ID", "Target must be mock LFM2 MoE or named DavidAU derivative.")
        warnings.append("LFM topology/expert counts are asserted in plan; real exact Q6 source inventory is required before surgery.")

    return {"status": "PASS" if not errors else "FAIL", "errors": errors,
            "warnings": warnings, "checked": {"family": family, "fixture_only": proposal.get("fixture_only"),
                "control_arms": len(arms) if type(arms) is list else 0}}


def load_no_duplicates(items: list[tuple[str, object]]) -> dict:
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError(f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path, help="Read-only offline proposal JSON, not model weights")
    args = ap.parse_args(argv)
    try:
        if args.path.stat().st_size > MAX_INPUT_BYTES:
            raise ValueError("Proposal exceeds bounded input size")
        data = json.loads(args.path.read_text(encoding="utf-8"),
                          object_pairs_hook=load_no_duplicates,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"Non-finite JSON number: {x}")))
        result = validate(data)
    except (OSError, ValueError, UnicodeError, RecursionError) as e:
        result = {"status": "FAIL", "errors": [{"code": "INPUT", "detail": str(e)}], "warnings": []}
    print(json.dumps(result, sort_keys=True, indent=2))
    return int(result["status"] != "PASS")


if __name__ == "__main__":
    sys.exit(main())
