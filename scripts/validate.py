#!/usr/bin/env python3
"""Validate the registry index and its category files.

Local:  pip install pyyaml jsonschema && python scripts/validate.py
CI runs this on every push and pull request (see .github/workflows/validate.yml).

Layout:
  registry.yaml               -- index: the category taxonomy (progressive discovery)
  registry/<category>.yaml     -- entries for one category
  schema/index.json            -- schema for the index
  schema/entry-file.json       -- schema for a category file
"""
import json
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "registry.yaml"
INDEX_SCHEMA = ROOT / "schema" / "index.json"
ENTRY_SCHEMA = ROOT / "schema" / "entry-file.json"


def load_yaml(path):
    return yaml.safe_load(path.read_text()) or {}


def collect_schema_errors(prefix, schema, data, problems):
    for err in sorted(Draft202012Validator(schema).iter_errors(data),
                      key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "<root>"
        problems.append(f"{prefix}: {loc}: {err.message}")


def main() -> int:
    index_schema = json.loads(INDEX_SCHEMA.read_text())
    entry_schema = json.loads(ENTRY_SCHEMA.read_text())
    index = load_yaml(INDEX)
    problems = []

    # Single source for the category vocabulary: the index schema's key enum.
    vocab = set(index_schema["$defs"]["category"]["properties"]["key"]["enum"])

    collect_schema_errors("index", index_schema, index, problems)

    categories = index.get("categories", [])
    keys = [c.get("key") for c in categories]

    # The index is a complete, non-duplicated taxonomy.
    for key in sorted({k for k in keys if keys.count(k) > 1}):
        problems.append(f"index: duplicate category key {key!r}")
    missing = vocab - set(keys)
    if missing:
        problems.append(f"index: missing categories {sorted(missing)}")

    all_names = []
    total = 0
    files_seen = 0
    for cat in categories:
        key = cat.get("key")
        file = cat.get("file")
        count = cat.get("count", 0)
        if isinstance(count, int):
            total += count

        if not file:
            if count:
                problems.append(f"index: {key!r} has count {count} but no file")
            continue

        files_seen += 1
        path = ROOT / file
        if Path(file).stem != key:
            problems.append(f"index: {key!r} points at {file!r} (file stem must equal key)")
        if not path.exists():
            problems.append(f"index: {key!r} file {file!r} does not exist")
            continue

        data = load_yaml(path)
        collect_schema_errors(file, entry_schema, data, problems)
        resources = data.get("resources", [])

        if len(resources) != count:
            problems.append(f"{file}: index count {count} != {len(resources)} entries")

        names = [r.get("name", "") for r in resources]
        if names != sorted(names, key=str.lower):
            problems.append(f"{file}: entries not alphabetical by name: {names}")
        all_names += names

    # Every file under registry/ must be referenced by the index, or its entries
    # are unreachable for an agent that follows the index.
    referenced = {c.get("file") for c in categories if c.get("file")}
    for path in sorted((ROOT / "registry").glob("*.yaml")):
        rel = f"registry/{path.name}"
        if rel not in referenced:
            problems.append(f"{rel}: not referenced by the index (add file + count in registry.yaml)")

    # Names are unique across the registry, case-insensitively (matching the
    # case-insensitive ordering check above).
    dupes = sorted(name for name, n in Counter(x.lower() for x in all_names).items() if n > 1)
    for name in dupes:
        problems.append(f"duplicate name across registry (case-insensitive): {name!r}")

    if problems:
        print(f"registry is INVALID ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"registry OK -- {total} resource(s) across {files_seen} populated categor(y/ies).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
