from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import process_directory


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize product images and produce an auditable manifest")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--canvas", type=int, default=1200)
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error(f"Source directory not found: {args.source}")
    manifest = process_directory(args.source, args.destination, canvas=args.canvas)
    print(json.dumps({key: manifest[key] for key in ("source_count", "duplicate_count", "canvas")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
