#!/usr/bin/env python3
"""Deterministic synthetic fixtures only. No real weights or remote model downloads."""
from pathlib import Path
import copy
import json

DEST = Path(__file__).resolve().parents[1] / 'fixtures'
AUTHORITY = {
    'mode': 'proposal-only', 'allow_network_download': False,
    'allow_model_inference': False, 'allow_weight_write': False,
    'allow_paid_provider': False, 'immutable_donor': True,
    'owner_approval_for_promotion': True, 'max_runtime_seconds': 60,
    'max_paid_usd': 0,
}


def manifest(family: str) -> dict:
    common = {
        'schema_id': 'piplugs.rsn-omp.experiment-proposal',
        'schema_version': 1, 'fixture_only': True, 'phase': 'PLAN_ONLY',
        'proposal_id': ('rsn-funnel-toy-v1' if family == 'reblitteration' else 'rsn-reap-lfm-metadata-v1'),
        'source': {
            'repository': ('synthetic/linear-toy' if family == 'reblitteration' else 'synthetic/lfm2-moe'),
            'revision': '0123456789abcdef0123456789abcdef01234567',
            'sha256': 'a' * 64, 'filename': ('frozen-toy.json' if family == 'reblitteration' else 'mock-lfm-q6.gguf'),
            'kind': ('mock-toy' if family == 'reblitteration' else 'mock-gguf'),
        },
        'authority': copy.deepcopy(AUTHORITY),
        'output_root': ('runs/rsn-funnel-toy-v1' if family == 'reblitteration' else 'runs/rsn-reap-metadata-v1'),
        'operation': {'family': family, 'seed': 1701},
        'evaluation': {
            'calibration_ids': ['cal-opportunity', 'cal-controls'],
            'heldout_ids': ['held-opportunity', 'held-negative', 'held-already-correct'],
            'calibration_sha256': 'b' * 64, 'heldout_sha256': 'c' * 64,
            'control_arms': []
        },
    }
    if family == 'reblitteration':
        common['operation'].update({
            'target': {'feature_id': 'verified-feature-candidate', 'frozen_tensors': ['layers.8.target_proj']},
            'edit': {'method': 'low-rank-upstream', 'upstream_tensors': ['layers.6.up_proj'], 'rank': 2,
                     'max_delta_l2': 0.25},
            'objective': {'missed_opportunity_gain': 1, 'false_positive_penalty': 2,
                          'already_correct_drift_penalty': 2, 'update_norm_penalty': 0.5}
        })
        common['evaluation']['control_arms'] = [
            'donor', 'random-matched', 'naive-scale', 'activation-steer', 'lora-matched'
        ]
        common['evaluation']['heldout_positive_ids'] = ['held-opportunity']
        common['evaluation']['heldout_negative_ids'] = ['held-negative']
    else:
        common['source']['quantization'] = 'Q6_K'
        common['operation'].update({
            'topology': {'moe_layers': 38, 'experts_per_layer': 64, 'active_experts_per_token': 4},
            'remove_per_layer': 12, 'ranking_method': 'reap-candidate',
            'export_policy': 'disabled-until-native-proof'
        })
        common['evaluation']['control_arms'] = [
            'donor', 'random-removal', 'router-frequency', 'mixed-precision-no-prune'
        ]
    return common


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for fam, slug in [('reblitteration','funnel-plan'), ('reap-pruning', 'lfm-q6-reap-plan')]:
        good = manifest(fam)
        (DEST / f'{slug}.json').write_text(json.dumps(good, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        bad = copy.deepcopy(good)
        if fam == 'reblitteration':
            bad['operation']['edit']['upstream_tensors'] = ['layers.8.target_proj']
        else:
            bad['authority']['allow_weight_write'] = True
        (DEST / f'{slug}-unsafe.json').write_text(json.dumps(bad, indent=2, sort_keys=True) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
