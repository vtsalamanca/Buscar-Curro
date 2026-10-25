"""Offline BC-04 snapshot management. Never uploads or schedules anything."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from state_safety import create_snapshot, parse_state, restore_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="operation", required=True)
    make = subs.add_parser("create", help="Create an immutable local archive")
    make.add_argument("--state", type=Path, required=True)
    make.add_argument("--output", type=Path, required=True)
    restore = subs.add_parser("restore", help="Verify snapshot and atomically restore to local path")
    restore.add_argument("--archive", type=Path, required=True)
    restore.add_argument("--state", type=Path, required=True)
    check = subs.add_parser("inspect", help="Verify snapshot; print counts only")
    check.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    if args.operation == "create":
        if args.state.is_symlink():
            raise ValueError("state_symlink")
        state = parse_state(args.state.read_bytes())
        digest = create_snapshot(state, args.output)
        print(json.dumps({"saved": str(args.output), "state_sha256": digest}))
    elif args.operation == "restore":
        if args.archive.resolve() == args.state.resolve():
            raise ValueError("archive_and_state_must_differ")
        state = restore_snapshot(args.archive, args.state)
        print(json.dumps({"restored": str(args.state), "documents": len(state["documents"])}))
    else:
        state = restore_snapshot(args.archive)
        queues = state.get("bc02", {}).get("queues", {})
        statuses = {status: sum(
            1 for queue in queues.values() for item in queue.values() if item.get("status") == status
        ) for status in ("checked", "pending", "prefiltered", "error", "not_listed")}
        print(json.dumps({"valid": True, "documents": len(state["documents"]),
                          "candidates": sum(map(len, queues.values())),
                          "queue_statuses": statuses}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
