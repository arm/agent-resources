#!/usr/bin/env python3
"""Validate the consolidated Arm Agent Resources registry.

Local:  pip install pyyaml jsonschema && python scripts/validate.py
CI runs this on every push to main and every pull request (.github/workflows/validate.yml).

Layout:
  all-resources.yaml          -- the single resource registry
  schema/entry-file.json      -- schema for the registry
"""
import json
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "all-resources.yaml"
SCHEMA = ROOT / "schema" / "entry-file.json"


def load_yaml(path):
    return yaml.safe_load(path.read_text()) or {}


def main() -> int:
    schema = json.loads(SCHEMA.read_text())
    data = load_yaml(REGISTRY)
    problems = []

    for err in sorted(
        Draft202012Validator(schema).iter_errors(data),
        key=lambda error: list(error.path),
    ):
        loc = "/".join(str(part) for part in err.path) or "<root>"
        problems.append(f"all-resources.yaml: {loc}: {err.message}")

    resources = data.get("resources", [])
    names = [resource.get("name", "") for resource in resources]

    if names != sorted(names, key=str.lower):
        problems.append(
            f"all-resources.yaml: entries not alphabetical by name: {names}"
        )

    for name, count in Counter(name.lower() for name in names).items():
        if count > 1:
            problems.append(
                f"all-resources.yaml: {name!r} listed more than once"
            )

    if problems:
        print(f"registry is INVALID ({len(problems)} problem(s)):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print(f"registry OK -- {len(resources)} unique resource(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
