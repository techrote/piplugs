#!/usr/bin/env python3
"""Read-only CALS offline region/connector/claim preflight. NOT native admission.

The pilot-fixture schema is intentionally separate from CyberSand's native
GEN-007 recipes, Workbench generated-start and CALS's proposed durable schemas.
A PASS proves internal design-document consistency, not playable traversal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMA = "piplugs.cals.offline-contract-fixture"
MAX_BYTES = 1024 * 1024
MAX_CELLS = 4_194_304
MAX_REGIONS = 32
MAX_JOINTS = 64
MAX_EDITS = 2048
NAME = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
SHA = re.compile(r"^[0-9a-f]{40}$")


def integer(value: object, minimum: int = 0) -> bool:
    return type(value) is int and value >= minimum


def rect(value: object) -> tuple[int, int, int, int] | None:
    if (not isinstance(value, list) or len(value) != 4 or
            not all(integer(v, 0) for v in value) or value[2] < 1 or value[3] < 1):
        return None
    return tuple(value)


def inside(inner: tuple[int, int, int, int], outer: tuple[int, int, int, int]) -> bool:
    x, y, w, h = inner
    ox, oy, ow, oh = outer
    return ox <= x and oy <= y and x + w <= ox + ow and y + h <= oy + oh


def intersects(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def digest(document: dict) -> str:
    """Canonical hash excludes its own digest field; do not hash self-reference."""
    without_digest = {k: v for k, v in document.items() if k != "world_bible_sha256"}
    data = json.dumps(without_digest, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def validate(data: object) -> dict:
    errors: list[dict[str, str]] = []
    warnings = ["Offline region graph/claim checks only; not a CyberSand native, renderer or gameplay test."]

    def fail(code: str, detail: str) -> None:
        errors.append({"code": code, "detail": detail})

    if not isinstance(data, dict):
        fail("INVALID_ROOT", "Root must be an object.")
        return {"status": "FAIL", "errors": errors, "warnings": warnings}
    if data.get("schema_id") != SCHEMA or data.get("schema_version") != 1:
        fail("SCHEMA", "Expected offline fixture schema v1; no automatic migration.")
    source = data.get("source_sha")
    if not isinstance(source, str) or SHA.fullmatch(source) is None:
        fail("SOURCE_ID", "source_sha must be a lowercase 40-hex Git SHA.")
    bible = data.get("world_bible")
    if not isinstance(bible, dict):
        fail("BIBLE", "world_bible must be an object.")
        return {"status": "FAIL", "errors": errors, "warnings": warnings}
    if not integer(bible.get("revision"), 1):
        fail("BIBLE_REVISION", "World Bible revision must be positive integer.")
    expected = bible.get("world_bible_sha256")
    try:
        actual_digest = digest(bible)
    except (TypeError, ValueError, OverflowError):
        actual_digest = None
    if not isinstance(expected, str) or expected != actual_digest:
        fail("BIBLE_DIGEST", "World Bible hash does not match canonical bytes excluding digest field.")
    canvas = bible.get("canvas")
    if not isinstance(canvas, dict) or not integer(canvas.get("width"), 1) or not integer(canvas.get("height"), 1):
        fail("CANVAS", "Positive integer width/height required.")
        return {"status": "FAIL", "errors": errors, "warnings": warnings}
    width, height = canvas["width"], canvas["height"]
    if width * height > MAX_CELLS:
        fail("CANVAS_CAP", f"Offline fixture canvas exceeds {MAX_CELLS} cells.")
    extent = (0, 0, width, height)
    regions_raw = bible.get("regions")
    regions: dict[str, tuple[int, int, int, int]] = {}
    if not isinstance(regions_raw, list) or not 1 <= len(regions_raw) <= MAX_REGIONS:
        fail("REGIONS", "Expected 1..32 regions.")
        regions_raw = []
    for idx, region in enumerate(regions_raw):
        if not isinstance(region, dict) or not isinstance(region.get("id"), str) or NAME.fullmatch(region["id"]) is None:
            fail("REGION_ID", f"Region {idx} requires a valid id.")
            continue
        rid = region["id"]
        r = rect(region.get("rect"))
        if rid in regions:
            fail("REGION_DUPLICATE", rid)
        elif r is None or not inside(r, extent):
            fail("REGION_BOUNDS", f"{rid}: invalid or outside canvas")
        else:
            for prior, prior_rect in regions.items():
                if intersects(r, prior_rect):
                    fail("REGION_OVERLAP", f"{rid} overlaps {prior}")
            regions[rid] = r
    lease_generations = bible.get("lease_generations")
    if (not isinstance(lease_generations, dict) or set(lease_generations) != set(regions)
            or not all(integer(v, 1) for v in lease_generations.values())):
        fail("LEASE_INDEX", "lease_generations must map exactly each valid region to a positive integer.")
        lease_generations = {}
    joints_raw = bible.get("joints")
    joints: dict[str, dict] = {}
    if not isinstance(joints_raw, list) or len(joints_raw) > MAX_JOINTS:
        fail("JOINTS", "Expected 0..64 joints.")
        joints_raw = []
    for idx, joint in enumerate(joints_raw):
        if not isinstance(joint, dict) or not isinstance(joint.get("id"), str) or NAME.fullmatch(joint["id"]) is None:
            fail("JOINT_ID", f"Joint {idx} requires an id.")
            continue
        jid = joint["id"]
        if jid in joints:
            fail("JOINT_DUPLICATE", jid)
            continue
        joints[jid] = joint
        a, b = joint.get("left"), joint.get("right")
        if not isinstance(a, str) or not isinstance(b, str) or a not in regions or b not in regions or a == b:
            fail("JOINT_REGION", f"{jid} references absent/identical regions.")
            continue
        ar, br = regions[a], regions[b]
        seam = ar[0] + ar[2]
        y, h, rev = joint.get("y"), joint.get("height"), joint.get("revision")
        if not integer(joint.get("x")) or joint["x"] != seam or br[0] != seam:
            fail("JOINT_SEAM", f"{jid} must be on exactly shared left/right boundary x={seam}.")
        if (not integer(y) or not integer(h, 1) or y < max(ar[1], br[1]) or
                y + h > min(ar[1] + ar[3], br[1] + br[3])):
            fail("JOINT_VERTICAL", f"{jid} opening not contained in both region heights.")
        if not integer(rev, 1):
            fail("JOINT_REVISION", jid)
        if not isinstance(joint.get("socket_id"), str) or NAME.fullmatch(joint["socket_id"]) is None:
            fail("JOINT_SOCKET", jid)

    proposals_raw = data.get("proposals")
    proposals: dict[str, dict] = {}
    if not isinstance(proposals_raw, list) or len(proposals_raw) > MAX_REGIONS:
        fail("PROPOSALS", "Expected at most 32 proposals.")
        proposals_raw = []
    for idx, prop in enumerate(proposals_raw):
        if not isinstance(prop, dict):
            fail("PROPOSAL", f"Proposal {idx} not an object.")
            continue
        rid = prop.get("region_id")
        if not isinstance(rid, str) or rid not in regions or rid in proposals:
            fail("PROPOSAL_REGION", f"Region {rid!r} unknown or duplicate.")
            continue
        proposals[rid] = prop
        if (prop.get("source_sha") != source or not integer(prop.get("world_bible_revision"), 1)
                or prop.get("world_bible_revision") != bible.get("revision")):
            fail("STALE_PROPOSAL", f"{rid}: source/World Bible revision mismatch.")
        if (not integer(prop.get("lease_generation"), 1) or
                prop.get("lease_generation") != lease_generations.get(rid)):
            fail("STALE_LEASE", f"{rid}: lease generation does not match World Bible.")
        allowed = prop.get("edits", [])
        if not isinstance(allowed, list) or len(allowed) > MAX_EDITS:
            fail("EDIT_COUNT", f"{rid}: edits must be an array of at most {MAX_EDITS}.")
            allowed = []
        protection = bible.get("protected", [])
        if not isinstance(protection, list):
            fail("PROTECTED", "protected must be an array.")
            protection = []
        protected_rects = []
        for item in protection:
            pr = rect(item)
            if pr is None or not inside(pr, extent):
                fail("PROTECTED_BOUNDS", f"Invalid protected rectangle {item!r}.")
            else:
                protected_rects.append(pr)
        for index, edit in enumerate(allowed):
            if (not isinstance(edit, list) or len(edit) != 5 or
                    not integer(edit[4]) or rect(edit[:4]) is None):
                fail("EDIT_FORMAT", f"{rid}: edit {index} must be [x,y,w,h,nonnegative-material-id].")
                continue
            er = rect(edit[:4])
            if not inside(er, regions[rid]):
                fail("OUT_OF_LEASE", f"{rid}: edit {index} outside assigned region.")
            if any(intersects(er, pr) for pr in protected_rects):
                fail("PROTECTED_WRITE", f"{rid}: edit {index} intersects protected space.")
        claims = prop.get("sockets", [])
        if not isinstance(claims, list) or len(claims) > MAX_JOINTS:
            fail("SOCKET_CLAIMS", rid)
            continue
        seen: set[str] = set()
        for claim in claims:
            jid = claim.get("joint_id") if isinstance(claim, dict) else None
            if not isinstance(jid, str) or jid not in joints or rid not in (joints[jid].get("left"), joints[jid].get("right")):
                fail("SOCKET_UNKNOWN", f"{rid}: joint {jid!r} not assigned.")
                continue
            if jid in seen:
                fail("SOCKET_DUPLICATE", f"{rid}: {jid}")
            seen.add(jid)
            j = joints[jid]
            for key in ("x", "y", "height", "socket_id"):
                if (claim.get(key) != j.get(key) or
                        (key != "socket_id" and not integer(claim.get(key)))):
                    fail("SOCKET_MISMATCH", f"{rid}/{jid}: {key} differs from joint revision.")
            if not integer(claim.get("joint_revision"), 1) or claim.get("joint_revision") != j.get("revision"):
                fail("STALE_JOINT", f"{rid}/{jid}: revision mismatch.")
        for jid, j in joints.items():
            if rid in (j.get("left"), j.get("right")) and jid not in seen:
                fail("SOCKET_MISSING", f"{rid}: {jid} missing.")
    for rid in regions:
        if rid not in proposals:
            fail("PROPOSAL_MISSING", rid)
    routes = bible.get("routes")
    if not isinstance(routes, list) or not 1 <= len(routes) <= MAX_JOINTS:
        fail("ROUTES", "At least one required region-graph route expected.")
        routes = []
    adjacency: dict[str, set[str]] = {rid: set() for rid in regions}
    for j in joints.values():
        a, b = j.get("left"), j.get("right")
        if isinstance(a, str) and isinstance(b, str) and a in adjacency and b in adjacency and a != b:
            adjacency[a].add(b)
            adjacency[b].add(a)
    for route in routes:
        if (not isinstance(route, dict) or not isinstance(route.get("id"), str) or
                NAME.fullmatch(route["id"]) is None):
            fail("ROUTE_FORMAT", "Route requires an id and region endpoints.")
            continue
        start, finish = route.get("from_region"), route.get("to_region")
        if not isinstance(start, str) or not isinstance(finish, str) or start not in regions or finish not in regions:
            fail("ROUTE_ENDPOINT", f"{route['id']}: missing region endpoint.")
            continue
        reachable = {start}
        fringe = [start]
        while fringe:
            here = fringe.pop()
            for nxt in adjacency[here] - reachable:
                reachable.add(nxt)
                fringe.append(nxt)
        if finish not in reachable:
            fail("ROUTE_DISCONNECTED", f"{route['id']}: region graph disconnected.")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors,
            "warnings": warnings, "checked": {"regions": len(regions),
                "joints": len(joints), "proposals": len(proposals), "routes": len(routes)}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path, help="Offline contract-fixture JSON (not a native CyberSand manifest)")
    args = parser.parse_args(argv)
    try:
        if args.fixture.stat().st_size > MAX_BYTES:
            raise ValueError(f"JSON exceeds {MAX_BYTES} byte safety cap")
        def reject_non_json_constant(value: str) -> None:
            raise ValueError(f"JSON non-finite number rejected: {value}")
        data = json.loads(args.fixture.read_text(encoding="utf-8"),
                          parse_constant=reject_non_json_constant)
        report = validate(data)
    except (OSError, ValueError, UnicodeError) as exc:
        report = {"status": "FAIL", "errors": [{"code": "INPUT", "detail": str(exc)}], "warnings": []}
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
