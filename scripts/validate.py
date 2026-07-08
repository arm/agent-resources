#!/usr/bin/env python3
"""Validate registry.yaml against schema.json.

Local:  pip install pyyaml jsonschema && python scripts/validate.py
CI runs this on every push and pull request (see .github/workflows/validate.yml).
"""
import json
import sys
from itertools import groupby
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry.yaml"
SCHEMA = ROOT / "schema.json"


def main() -> int:
    schema = json.loads(SCHEMA.read_text())
    data = yaml.safe_load(REGISTRY.read_text()) or {}
    problems = []

    # 1. Schema contract.
    for err in sorted(Draft202012Validator(schema).iter_errors(data),
                      key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "<root>"
        problems.append(f"schema: {loc}: {err.message}")

    resources = data.get("resources", [])

    # 2. Names are unique.
    names = [r.get("name", "") for r in resources]
    for name in sorted({n for n in names if names.count(n) > 1}):
        problems.append(f"duplicate name: {name!r}")

    # 3. Entries are alphabetical by name within each category.
    by_cat = sorted(resources, key=lambda r: r.get("category", ""))
    for cat, group in groupby(by_cat, key=lambda r: r.get("category", "")):
        got = [r.get("name", "") for r in group]
        want = sorted(got, key=str.lower)
        if got != want:
            problems.append(f"order: category {cat!r} not alphabetical: {got} != {want}")

    if problems:
        print(f"registry.yaml is INVALID ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"registry.yaml OK -- {len(resources)} resource(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
