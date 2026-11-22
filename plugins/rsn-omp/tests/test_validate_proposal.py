"""No-network, no-weight custody and experiment-plan preflight tests."""
import copy
import importlib.util
import json
import random
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / 'tools' / 'validate_proposal.py'
spec = importlib.util.spec_from_file_location('rsn_preflight', PROGRAM)
assert spec and spec.loader
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
FIXTURES = ROOT / 'fixtures'


class ProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.funnel = json.loads((FIXTURES/'funnel-plan.json').read_text())
        cls.lfm = json.loads((FIXTURES/'lfm-q6-reap-plan.json').read_text())

    def expect_code(self, source, action, code):
        fixture = copy.deepcopy(source)
        action(fixture)
        result = v.validate(fixture)
        self.assertEqual(result['status'], 'FAIL', result)
        self.assertIn(code, [e['code'] for e in result['errors']], result)

    def test_funnel_valid(self):
        r = v.validate(self.funnel)
        self.assertEqual(r['status'], 'PASS', r)
        self.assertTrue(any('no checkpoint or tensor bytes' in w for w in r['warnings']))

    def test_lfm_valid(self):
        r = v.validate(self.lfm)
        self.assertEqual(r['status'], 'PASS', r)
        self.assertTrue(any('real exact Q6 source inventory' in w for w in r['warnings']))

    def test_reject_frozen_target_edit(self):
        self.expect_code(self.funnel, lambda d: d['operation']['edit'].update(upstream_tensors=['layers.8.target_proj']), 'FROZEN_OVERLAP')

    def test_reject_network(self):
        self.expect_code(self.funnel, lambda d: d['authority'].update(allow_network_download=True), 'SIDE_EFFECT')

    def test_reject_paid_api(self):
        self.expect_code(self.funnel, lambda d: d['authority'].update(allow_paid_provider=True), 'SIDE_EFFECT')

    def test_reject_model_inference(self):
        self.expect_code(self.funnel, lambda d: d['authority'].update(allow_model_inference=True), 'SIDE_EFFECT')

    def test_reject_weight_mutation(self):
        self.expect_code(self.lfm, lambda d: d['authority'].update(allow_weight_write=True), 'SIDE_EFFECT')

    def test_reject_donor_not_frozen(self):
        self.expect_code(self.lfm, lambda d: d['authority'].update(immutable_donor=False), 'CUSTODY')

    def test_reject_automatic_promotion(self):
        self.expect_code(self.funnel, lambda d: d['authority'].update(owner_approval_for_promotion=False), 'CUSTODY')

    def test_reject_nonzero_budget(self):
        self.expect_code(self.funnel, lambda d: d['authority'].update(max_paid_usd=0.01), 'PAID_BUDGET')

    def test_reject_unbounded_execution(self):
        self.expect_code(self.lfm, lambda d: d['authority'].update(max_runtime_seconds=86400), 'RUNTIME_BUDGET')

    def test_reject_unknown_schema(self):
        self.expect_code(self.funnel, lambda d: d.update(schema_version=2), 'SCHEMA')

    def test_reject_ambiguous_source_sha(self):
        self.expect_code(self.lfm, lambda d: d['source'].update(sha256='bad'), 'SOURCE_PIN')

    def test_reject_fake_real_source(self):
        self.expect_code(self.lfm, lambda d: d.update(fixture_only=False), 'REAL_SOURCE')

    def test_reject_real_repo_as_fixture(self):
        self.expect_code(self.lfm, lambda d: d['source'].update(repository='DavidAU/LFM2.5-24B-A2B-Turbo-Brilliance-50X-NEO-MAX-Imatrix-GGUF'), 'FIXTURE_SOURCE')

    def test_reject_bad_output_traversal(self):
        for bad in ('../donors', 'C:/donors', '/tmp/weights', 'runs/../secrets', 'runs\\x'):
            with self.subTest(bad=bad):
                self.expect_code(self.funnel, lambda d, bad=bad: d.update(output_root=bad), 'OUTPUT_ROOT')

    def test_reject_high_rank(self):
        self.expect_code(self.funnel, lambda d: d['operation']['edit'].update(rank=8), 'EDIT_RANK')

    def test_reject_bool_rank(self):
        self.expect_code(self.funnel, lambda d: d['operation']['edit'].update(rank=True), 'EDIT_RANK')

    def test_reject_empty_edit_allowlist(self):
        self.expect_code(self.funnel, lambda d: d['operation']['edit'].update(upstream_tensors=[]), 'EDIT_ALLOWLIST')

    def test_reject_missing_false_positive_penalty(self):
        self.expect_code(self.funnel, lambda d: d['operation']['objective'].update(false_positive_penalty=0), 'OBJECTIVE')

    def test_reject_data_leakage(self):
        self.expect_code(self.funnel, lambda d: d['evaluation']['heldout_ids'].append('cal-controls'), 'DATA_LEAKAGE')

    def test_reject_corpus_collision(self):
        self.expect_code(self.funnel, lambda d: d['evaluation'].update(heldout_sha256='b'*64), 'CORPUS_COLLISION')

    def test_reject_missing_negative_controls(self):
        self.expect_code(self.funnel, lambda d: d['evaluation'].update(control_arms=['donor']), 'CONTROLS_MISSING')

    def test_reject_no_negative_holdout(self):
        self.expect_code(self.funnel, lambda d: d['evaluation'].update(heldout_negative_ids=[]), 'CONTEXT_CONTROLS')

    def test_reject_negative_not_in_heldout(self):
        self.expect_code(self.funnel, lambda d: d['evaluation'].update(heldout_negative_ids=['unknown-id']), 'CONTEXT_CONTROLS')

    def test_reject_routing_topk_after_pruning(self):
        self.expect_code(self.lfm, lambda d: d['operation'].update(remove_per_layer=61), 'PRUNE_TOPK')

    def test_reject_reap_export_enabled(self):
        self.expect_code(self.lfm, lambda d: d['operation'].update(export_policy='write-gguf'), 'PRUNE_METHOD')

    def test_reject_non_q6_donor(self):
        self.expect_code(self.lfm, lambda d: d['source'].update(quantization='Q4_K_M'), 'QUANT')

    def test_reject_wrong_lfm_donor(self):
        self.expect_code(self.lfm, lambda d: d['source'].update(repository='synthetic/other'), 'LFM_ID')

    def test_unhashable_family_is_clean_rejection(self):
        self.expect_code(self.funnel, lambda d: d['operation'].update(family=['malformed']), 'FAMILY')

    def test_malformed_heldout_is_clean_rejection(self):
        self.expect_code(self.funnel, lambda d: d['evaluation'].update(heldout_ids=[['oops']]), 'DATASET_IDS')

    def test_unsafe_reference_fixture_rejected(self):
        for p in ('funnel-plan-unsafe.json', 'lfm-q6-reap-plan-unsafe.json'):
            self.assertEqual(v.validate(json.loads((FIXTURES/p).read_text()))['status'], 'FAIL')

    def test_fuzzed_fields_fail_cleanly_without_exceptions(self):
        rng = random.Random(1701)
        fields = [
            ('operation', 'family'), ('operation', 'seed'), ('operation', 'target'),
            ('operation', 'edit'), ('operation', 'objective'),
            ('source', 'repository'), ('source', 'sha256'), ('source', 'kind'),
            ('authority', 'mode'), ('authority', 'max_paid_usd'),
            ('evaluation', 'heldout_ids'), ('evaluation', 'calibration_ids'),
            ('evaluation', 'control_arms'), ('evaluation', 'heldout_positive_ids'),
            ('evaluation', 'heldout_negative_ids'),
        ]
        values = [None, False, True, 0, -1, 5.1, [], {}, ['bad'], {'oops': 1}, '', 'bad']
        for _ in range(300):
            d = copy.deepcopy(self.funnel if rng.randint(0, 1) == 0 else self.lfm)
            parent, key = rng.choice(fields)
            d[parent][key] = copy.deepcopy(rng.choice(values))
            report = v.validate(d)
            self.assertIn(report['status'], ('PASS', 'FAIL'))
            self.assertIsInstance(report['errors'], list)

    def test_cli_positive_and_negative_exit_codes(self):
        for p, expected in [('funnel-plan.json',0), ('lfm-q6-reap-plan.json',0),
                            ('funnel-plan-unsafe.json',1), ('lfm-q6-reap-plan-unsafe.json',1)]:
            proc = subprocess.run([sys.executable, str(PROGRAM), str(FIXTURES/p)],capture_output=True,text=True)
            self.assertEqual(proc.returncode, expected, proc.stdout+proc.stderr)
            self.assertEqual(json.loads(proc.stdout)['status'], 'PASS' if expected==0 else 'FAIL')

    def test_invalid_json_and_duplicate_key(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'bad.json'
            for data in ('{','{"a":1,"a":2}','{"a":NaN}'):
                p.write_text(data)
                res = subprocess.run([sys.executable,str(PROGRAM),str(p)],capture_output=True,text=True)
                self.assertEqual(res.returncode, 1, res.stdout+res.stderr)
                self.assertEqual(json.loads(res.stdout)['errors'][0]['code'],'INPUT')

    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            proc = subprocess.run([sys.executable,str(PROGRAM),str(Path(temp)/'missing.json')],capture_output=True,text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(json.loads(proc.stdout)['status'], 'FAIL')

    def test_input_size_cap(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'oversize.json'
            p.write_text(' '* (v.MAX_INPUT_BYTES+1))
            proc = subprocess.run([sys.executable,str(PROGRAM),str(p)],capture_output=True,text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertIn('bounded input size',proc.stdout)


if __name__ == '__main__':
    unittest.main()
