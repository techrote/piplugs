"""Offline design-contract checks; deliberately NOT native CyberSand tests."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / 'tools' / 'validate_contracts.py'
GOOD = ROOT / 'fixtures' / 'iron-wound-valid.json'
BAD = ROOT / 'fixtures' / 'iron-wound-mismatched-socket.json'
spec = importlib.util.spec_from_file_location('validate_contracts', VALIDATOR)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class ContractValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good = json.loads(GOOD.read_text(encoding='utf-8'))

    def check_error(self, mutate, error):
        d = copy.deepcopy(self.good)
        mutate(d)
        result = v.validate(d)
        self.assertEqual(result['status'], 'FAIL', result)
        self.assertIn(error, {issue['code'] for issue in result['errors']}, result)

    def test_valid_fixture_and_hash(self):
        result = v.validate(self.good)
        self.assertEqual(result['status'], 'PASS', result)
        self.assertEqual(result['checked'], {'regions': 3, 'joints': 2, 'proposals': 3, 'routes': 1})
        self.assertEqual(v.digest(self.good['world_bible']), self.good['world_bible']['world_bible_sha256'])

    def test_intentional_mismatch_rejected(self):
        data = json.loads(BAD.read_text(encoding='utf-8'))
        self.assertIn('SOCKET_MISMATCH', {x['code'] for x in v.validate(data)['errors']})

    def test_wrong_schema(self):
        self.check_error(lambda d: d.update(schema_version=2), 'SCHEMA')

    def test_world_bible_tampered(self):
        self.check_error(lambda d: d['world_bible']['canvas'].update(width=1024), 'BIBLE_DIGEST')

    def test_out_of_bounds_region(self):
        self.check_error(lambda d: d['world_bible']['regions'][2].update(rect=[1900, 0, 688, 1024]), 'REGION_BOUNDS')

    def test_duplicate_region(self):
        self.check_error(lambda d: d['world_bible']['regions'][1].update(id='foundry'), 'REGION_DUPLICATE')

    def test_region_overlap(self):
        self.check_error(lambda d: d['world_bible']['regions'][1].update(rect=[700, 0, 660, 1024]), 'REGION_OVERLAP')

    def test_invalid_joint_seam(self):
        self.check_error(lambda d: d['world_bible']['joints'][0].update(x=735), 'JOINT_SEAM')

    def test_unresolvable_joint(self):
        self.check_error(lambda d: d['world_bible']['joints'][0].update(right='absent'), 'JOINT_REGION')

    def test_duplicate_joint(self):
        self.check_error(lambda d: d['world_bible']['joints'][1].update(id='foundry-viaduct'), 'JOINT_DUPLICATE')

    def test_stale_joint_claim(self):
        self.check_error(lambda d: d['proposals'][1]['sockets'][0].update(joint_revision=0), 'STALE_JOINT')

    def test_missing_socket_claim(self):
        self.check_error(lambda d: d['proposals'][1].update(sockets=[]), 'SOCKET_MISSING')

    def test_stale_bible(self):
        self.check_error(lambda d: d['proposals'][0].update(world_bible_revision=999), 'STALE_PROPOSAL')

    def test_stale_lease(self):
        self.check_error(lambda d: d['proposals'][0].update(lease_generation=2), 'STALE_LEASE')

    def test_protected_write(self):
        self.check_error(lambda d: d['proposals'][1]['edits'].append([800, 440, 12, 8, 58]), 'PROTECTED_WRITE')

    def test_outside_lease(self):
        self.check_error(lambda d: d['proposals'][0]['edits'].append([740, 550, 20, 8, 58]), 'OUT_OF_LEASE')

    def test_invalid_edit_material_value(self):
        self.check_error(lambda d: d['proposals'][0]['edits'].append([1, 550, 1, 1, -1]), 'EDIT_FORMAT')

    def test_oversized_canvas(self):
        self.check_error(lambda d: d['world_bible']['canvas'].update(width=5000), 'CANVAS_CAP')

    def test_malformed_refs_are_errors_not_exceptions(self):
        self.check_error(lambda d: d['world_bible']['joints'][0].update(left=['oops']), 'JOINT_REGION')
        self.check_error(lambda d: d['proposals'][0].update(region_id=['oops']), 'PROPOSAL_REGION')
        self.check_error(lambda d: d['proposals'][0]['sockets'][0].update(joint_id=['oops']), 'SOCKET_UNKNOWN')
        self.check_error(lambda d: d['world_bible']['routes'][0].update(from_region=['oops']), 'ROUTE_ENDPOINT')

    def test_non_finite_digest_denied(self):
        self.check_error(lambda d: d['world_bible'].update(invalid=float('nan')), 'BIBLE_DIGEST')

    def test_bool_revision_denied(self):
        self.check_error(lambda d: d['proposals'][0].update(world_bible_revision=True), 'STALE_PROPOSAL')
        self.check_error(lambda d: d['proposals'][0].update(lease_generation=True), 'STALE_LEASE')

    def test_non_orthographic_projection_refused(self):
        self.check_error(lambda d: d['world_bible']['canvas'].update(orientation='isometric'), 'PROJECTION')

    def test_extreme_skinny_canvas_refused(self):
        self.check_error(lambda d: d['world_bible']['canvas'].update(width=32768, height=1), 'CANVAS_CAP')

    def test_invalid_protection_checked_without_proposal(self):
        def mut(d):
            d['proposals'] = []
            d['world_bible']['protected'] = [[-1, 5, 10, 10]]
        self.check_error(mut, 'PROTECTED_BOUNDS')

    def test_route_joint_sequence_wrong_order(self):
        self.check_error(lambda d: d['world_bible']['routes'][0].update(
            via_joint_ids=['viaduct-reservoir', 'foundry-viaduct']), 'ROUTE_SEQUENCE')

    def test_route_joint_sequence_missing_link(self):
        self.check_error(lambda d: d['world_bible']['routes'][0].update(
            via_joint_ids=['foundry-viaduct']), 'ROUTE_SEQUENCE')

    def test_route_joint_sequence_duplicate_joint(self):
        self.check_error(lambda d: d['world_bible']['routes'][0].update(
            via_joint_ids=['foundry-viaduct', 'foundry-viaduct']), 'ROUTE_SEQUENCE')

    def test_route_joint_sequence_unknown_joint(self):
        self.check_error(lambda d: d['world_bible']['routes'][0].update(
            via_joint_ids=['absent']), 'ROUTE_SEQUENCE')

    def test_missing_route_sequence_is_explicitly_unverified(self):
        d = copy.deepcopy(self.good)
        del d['world_bible']['routes'][0]['via_joint_ids']
        d['world_bible']['world_bible_sha256'] = v.digest(d['world_bible'])
        result = v.validate(d)
        self.assertEqual(result['status'], 'PASS')
        self.assertTrue(any('only region-graph reachability' in x for x in result['warnings']))

    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'duplicate.json'
            path.write_text("""{"schema_id":"x","schema_id":"x"}""" , encoding='utf-8')
            proc = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertIn('Duplicate JSON key', proc.stdout)

    def test_cli_exit_codes(self):
        good = subprocess.run([sys.executable, str(VALIDATOR), str(GOOD)], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr + good.stdout)
        self.assertEqual(json.loads(good.stdout)['status'], 'PASS')
        bad = subprocess.run([sys.executable, str(VALIDATOR), str(BAD)], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1, bad.stderr + bad.stdout)
        self.assertEqual(json.loads(bad.stdout)['status'], 'FAIL')

    def test_invalid_json_and_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'nonjson.json'
            p.write_text('{', encoding='utf-8')
            for path in (p, Path(d)/'missing.json'):
                proc = subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True)
                self.assertEqual(proc.returncode, 1)
                self.assertEqual(json.loads(proc.stdout)['errors'][0]['code'], 'INPUT')
            p.write_text('{"x":NaN}', encoding='utf-8')
            proc = subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(json.loads(proc.stdout)['errors'][0]['code'], 'INPUT')


if __name__ == '__main__':
    unittest.main()
