#!/usr/bin/env python3
"""Validate the context-first registry index and its context files.

Local:  pip install pyyaml jsonschema && python scripts/validate.py
CI runs this on every push to main and every pull request (.github/workflows/validate.yml).

Layout (context-first):
  registry.yaml               -- index: the developer-context taxonomy (progressive discovery)
  registry/<context>.yaml      -- resources for one developer context; each carries a category
  schema/index.json            -- schema for the index
  schema/entry-file.json       -- schema for a context file

A resource relevant to several contexts is listed in each of their files. Those copies
must be identical -- the consistency check below fails on any drift.
"""
import json
import sys
from collections import Counter, defaultdict
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

    # Single source for the context vocabulary: the index schema's key enum.
    vocab = set(index_schema["$defs"]["context"]["properties"]["key"]["enum"])

    collect_schema_errors("index", index_schema, index, problems)

    contexts = index.get("contexts", [])
    keys = [c.get("key") for c in contexts]

    # The index is a complete, non-duplicated taxonomy.
    for key in sorted({k for k in keys if keys.count(k) > 1}):
        problems.append(f"index: duplicate context key {key!r}")
    missing = vocab - set(keys)
    if missing:
        problems.append(f"index: missing contexts {sorted(missing)}")

    # name -> [(file, entry), ...] copies, to check cross-file consistency.
    copies = defaultdict(list)
    total = 0
    files_seen = 0
    for ctx in contexts:
        key = ctx.get("key")
        file = ctx.get("file")
        count = ctx.get("count", 0)
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
        for name, n in Counter(x.lower() for x in names).items():
            if n > 1:
                problems.append(f"{file}: {name!r} listed more than once in this context")
        for r in resources:
            copies[r.get("name", "")].append((file, r))

    # Every context file must be referenced by the index.
    referenced = {c.get("file") for c in contexts if c.get("file")}
    for path in sorted((ROOT / "registry").glob("*.yaml")):
        rel = f"registry/{path.name}"
        if rel not in referenced:
            problems.append(f"{rel}: not referenced by the index (add file + count in registry.yaml)")

    # A resource listed in several contexts must be identical in every file.
    for name, entries in sorted(copies.items()):
        canonical = entries[0][1]
        if any(entry != canonical for _, entry in entries[1:]):
            where = ", ".join(sorted(f for f, _ in entries))
            problems.append(f"{name!r}: copies differ across context files ({where}) -- keep them identical")

    if problems:
        print(f"registry is INVALID ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"registry OK -- {total} listing(s) across {files_seen} context file(s), "
          f"{len(copies)} unique resource(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
