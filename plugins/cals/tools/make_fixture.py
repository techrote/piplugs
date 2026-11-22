#!/usr/bin/env python3
"""Recreate reproducible offline CALS handshake fixtures (no native generation)."""
import copy
import json
from pathlib import Path
from validate_contracts import digest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'fixtures'
OUT.mkdir(exist_ok=True)
SOURCE = '00cdb02f103265b6dc5224c68283e9a0c8cb449f'

def fixture():
    bible = {
        'revision': 1,
        'canvas': {'width': 2048, 'height': 1024, 'orientation': 'orthographic-side-elevation'},
        'regions': [
            {'id': 'foundry', 'rect': [0, 0, 736, 1024]},
            {'id': 'viaduct', 'rect': [736, 0, 624, 1024]},
            {'id': 'reservoir', 'rect': [1360, 0, 688, 1024]}
        ],
        'lease_generations': {'foundry': 1, 'viaduct': 1, 'reservoir': 1},
        'joints': [
            {'id': 'foundry-viaduct', 'left': 'foundry', 'right': 'viaduct',
             'revision': 1, 'x': 736, 'y': 432, 'height': 48, 'socket_id': 'main-access'},
            {'id': 'viaduct-reservoir', 'left': 'viaduct', 'right': 'reservoir',
             'revision': 1, 'x': 1360, 'y': 432, 'height': 48, 'socket_id': 'main-landing'}
        ],
        'routes': [{'id': 'main-route', 'from_region': 'foundry', 'to_region': 'reservoir'}],
        'protected': [[40, 432, 1968, 48]],
        'design_note': 'Illustrative geometry only; sockets are agreed but no actual traversability is proved.'
    }
    bible['world_bible_sha256'] = digest(bible)
    def sock(j):
        return {k: j[k] for k in ('x','y','height','socket_id')} | {'joint_id':j['id'],'joint_revision':j['revision']}
    proposals = []
    for reg in bible['regions']:
        rid=reg['id']
        joints=[j for j in bible['joints'] if rid in (j['left'], j['right'])]
        edits = {
          'foundry': [[40, 550, 300, 24, 58]],
          'viaduct': [[790, 600, 400, 16, 58]],
          'reservoir': [[1470, 630, 300, 30, 58]]
        }[rid]
        proposals.append({
          'region_id':rid, 'source_sha':SOURCE, 'world_bible_revision':1,
          'lease_generation':1, 'sockets':[sock(j) for j in joints], 'edits':edits
        })
    return {'schema_id':'piplugs.cals.offline-contract-fixture','schema_version':1,
            'source_sha':SOURCE,'world_bible':bible,'proposals':proposals}

if __name__=='__main__':
    good=fixture()
    bad=copy.deepcopy(good)
    for proposal in bad['proposals']:
        if proposal['region_id']=='viaduct':
            proposal['sockets'][0]['y']+=24
    for name, obj in [('iron-wound-valid.json',good),('iron-wound-mismatched-socket.json',bad)]:
        (OUT/name).write_text(json.dumps(obj, sort_keys=True, indent=2,ensure_ascii=False)+'\n', encoding='utf-8')
    print('Fixture files generated')
