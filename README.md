# Arm Agent Resources

A curated, agent-friendly registry of **already-public Arm resources** for coding agents and
the developers who work with them. Each entry is a short pointer -- a resource that helps when
building, profiling, optimizing, or deploying software on Arm -- with just enough context for an
agent to decide whether to reach for it.

This repo is a **registry of pointers, not a mirror**. It does not host the resources; it points
to them and says, in one line, when they are useful. Keeping it small and stable lets a single
URL be referenced from agent flows while the list underneath keeps growing.

## How agents use this

An agent loads [all-resources.yaml](all-resources.yaml), matches the task against each
resource's `when_to_use` and `example_use_case`, and follows the `url` only when relevant.
The `category` field can help narrow the list by resource type.

The registry is deliberately consolidated for straightforward maintenance and short-term
usability. It can be split into smaller views later if measured token costs make that worthwhile.

## What belongs here

- **Only already open-sourced or Anaqua-cleared codebases and public documentation.** No
  internal-only repos, no gated pages, no anything that is not already public. If you are unsure
  whether a resource is cleared, do not add it. (A tool can be public even when its source repo is
  not -- point at the public product page or docs, never the internal repo.)
- Arm-delivered resources that genuinely help a higher-level software developer building on Arm.
  The initial registry does not catalog general upstream or third-party open-source resources, or
  firmware-specific resources.
- One entry per unique resource. If a resource moves, update its pointer here rather than the
  URL that references this repo.

## Layout

Everything is **YAML** so it is both agent- and script-friendly and can be checked by a
deterministic validator. Every push to `main` and every pull request is validated in CI.

```
all-resources.yaml              # the complete resource registry
schema/
  entry-file.json              # schema for all-resources.yaml
scripts/validate.py            # validates schema, ordering, and uniqueness
```

### Categories

Every resource carries a `category` so an agent can navigate the list:
`knowledge-bases`, `profiling-optimization`, `developer-tools`,
`software-libraries`, or `reference-implementations`.

### Entry fields

Each entry has five fields:

| Field | What to write |
|---|---|
| `name` | The resource's name. |
| `url` | A public `https://` link to the resource. |
| `category` | One of the categories above. |
| `when_to_use` | 1-2 sentences on when it helps a software developer -- the selection signal. |
| `example_use_case` | A short concrete scenario (2-4 sentences): the developer's situation, what the agent does with this resource, and the outcome. One good scenario beats a long capability list. |

### Worked entry

From [all-resources.yaml](all-resources.yaml):

```yaml
- name: Arm MCP Server
  url: https://github.com/arm/mcp
  category: developer-tools
  when_to_use: >-
    Gives an AI assistant Arm-specific tools -- semantic search over Arm docs and learning
    resources, x86->Arm code-migration analysis, container-architecture checks, and running Arm
    Performix profiling recipes over SSH. Reach for it when you need grounded Arm knowledge or
    want to check, port, or profile code for Arm.
  example_use_case: >-
    A developer needs grounded Arm guidance and automated checks while changing an unfamiliar
    codebase. The agent queries the Arm MCP Server to search Arm's documentation, analyze
    migration readiness and container architecture, and, when performance matters, run a
    profiling recipe over SSH. It applies and verifies targeted changes from the results.
```

## How to contribute

1. Confirm the resource is public, Arm-delivered, and within the current higher-level software
   development scope.
2. Add one entry to [all-resources.yaml](all-resources.yaml), keeping entries alphabetical by
   `name`.
3. Keep `when_to_use` and `example_use_case` focused on applicable tasks and capabilities,
   without unnecessary persona or vertical wording.
4. Validate locally: `pip install pyyaml jsonschema && python scripts/validate.py`.
5. Open a PR. Keep entries to the five fields above and avoid marketing copy.

Nominating a resource but not sure how to phrase it? Open an issue with the name + URL and a
maintainer will help shape the `when_to_use` / `example_use_case` lines.

## Maintenance

Curated and maintained by the Arm Learning Paths / developer-discoverability team. This repo is
**public**. Every entry points only at already-public, Anaqua-cleared resources (see the contribution
rules above).
