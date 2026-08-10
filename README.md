# Arm Agent Resources

A curated, agent-friendly registry of **already-public Arm resources** for coding agents and
the developers who work with them. Each entry is a short pointer -- a resource that helps when
building, profiling, optimizing, or deploying software on Arm -- with just enough context for an
agent to decide whether to reach for it.

This repo is a **registry of pointers, not a mirror**. It does not host the resources; it points
to them and says, in one line, when they are useful. Keeping it small and stable lets a single
URL be referenced from agent flows while the list underneath keeps growing.

## How agents use this (progressive discovery, context-first)

An agent is handed the URL of this repo and a short description. It reads the small index in
[`registry.yaml`](registry.yaml), which lists **developer contexts** -- the situation an agent
infers from the developer's environment (cloud, performance work, ML, embedded, ...) -- and picks
the one(s) matching the task. It then loads only those [`registry/<context>.yaml`](registry/)
files. Inside a context file it matches the task against each resource's `when_to_use` and
`example_use_case` (and can use each resource's `category` to navigate), and follows the `url`
only when relevant. Loading one small index plus a context file or two -- rather than the whole
registry -- keeps the agent's context small and its choices grounded in concrete examples.

We organize **context-first** (rather than by resource type) because an agent usually starts from
the developer's situation -- "I'm porting to Graviton," "I'm optimizing a workload" -- not from
knowing which kind of resource it needs.

## What belongs here

- **Only already open-sourced or Anaqua-cleared codebases and public documentation.** No
  internal-only repos, no gated pages, no anything that is not already public. If you are unsure
  whether a resource is cleared, do not add it. (A tool can be public even when its source repo is
  not -- point at the public product page or docs, never the internal repo.)
- Resources that genuinely help a software developer building on Arm: tools, SDKs, learning
  paths, knowledge bases, MCP servers, optimization/profiling guides, reference implementations.
- One entry per resource per context. If a resource moves, update its pointer here rather than the
  URL that references this repo.

## Layout

Everything is **YAML** so it is both agent- and script-friendly and can be checked by a
deterministic validator. Every push to `main` and every pull request is validated in CI.

```
registry.yaml                    # index: the developer-context taxonomy (read this first)
registry/
  cloud-development.yaml         # resources for one context; each carries a `category`
  performance-optimization.yaml
  ...
schema/
  index.json                     # schema for registry.yaml
  entry-file.json                # schema for each registry/<context>.yaml
scripts/validate.py              # validates the whole thing (run in CI)
```

The **index** lists every developer context with a one-line description, a `count`, and (when
non-empty) the `file` that holds its resources. Counts are checked against the files, so they
cannot drift.

### Developer contexts (the files)

`cloud-development`, `compiled-languages`, `mobile-games`, `ml-developer`, `embedded-development`,
`performance-optimization`. A context's file is `registry/<key>.yaml`; the context is implied by
the filename, so entries do **not** repeat it.

### Categories (the `category` field)

Inside a context file, every resource carries a `category` -- its resource type -- so an agent can
navigate within a context: `mcp-servers`, `knowledge-bases`, `learning-paths`,
`profiling-optimization`, `sdks-tools`, `reference-implementations`.

### Entry fields

Each entry in a context file has five fields:

| Field | What to write |
|---|---|
| `name` | The resource's name. |
| `url` | A public `https://` link to the resource. |
| `category` | One of the categories above. |
| `when_to_use` | 1-2 sentences on when it helps a software developer -- the selection signal. |
| `example_use_case` | A short concrete scenario (2-4 sentences): the developer's situation, what the agent does with this resource, and the outcome. One good scenario beats a long capability list. |

### Resources in more than one context

A resource relevant to several contexts (e.g. Arm Performix -> `cloud-development`, `ml-developer`,
`performance-optimization`) is listed in **each** of those context files, with identical content,
so an agent gets the same entry whichever context it enters from. The validator fails CI if the
copies drift apart -- see [Maintaining multi-context resources](#maintaining-multi-context-resources).

### Worked entry

From [`registry/performance-optimization.yaml`](registry/performance-optimization.yaml):

```yaml
- name: Arm MCP Server
  url: https://github.com/arm/mcp
  category: mcp-servers
  when_to_use: >-
    Gives an AI assistant Arm-specific tools -- semantic search over Arm docs and learning
    resources, x86->Arm code-migration analysis, container-architecture checks, and running Arm
    Performix profiling recipes over SSH. Reach for it when you need grounded Arm knowledge or
    want to check, port, or profile code for Arm.
  example_use_case: >-
    A team porting a Python/C++ service from x86 to Graviton is unsure which dependencies are
    Arm-ready. The agent queries the Arm MCP Server to semantic-search Arm's docs and run a
    migration and container-architecture scan across the codebase and image, gets back the
    specific packages that need an aarch64 build plus the recommended fixes, and applies them so
    the service builds and passes on Graviton.
```

## How to contribute

1. Confirm the resource is **already public** (open-sourced or Anaqua-cleared). This is a hard rule.
2. Decide which developer contexts it helps in. Add an **identical** entry to each
   `registry/<context>.yaml`, keeping entries alphabetical by `name`. Create the file if that
   context has none yet.
3. Bump each of those contexts' `count` in [`registry.yaml`](registry.yaml) (add the `file`
   pointer for a context's first entry).
4. Validate locally: `pip install pyyaml jsonschema && python scripts/validate.py`.
5. Open a PR. Keep it to the five fields -- no marketing copy. CI runs the validator.

Nominating a resource but not sure how to phrase it? Open an issue with the name + URL and a
maintainer will help shape the `when_to_use` / `example_use_case` lines.

## Maintaining multi-context resources

Context-first matches how agents work, but a resource that spans several contexts lives in several
files. To keep that cheap and safe:

- The validator fails CI if the copies of a resource drift apart (different `url`, `category`,
  `when_to_use`, or `example_use_case`), so inconsistencies can't merge.
- **Planned tooling (`scripts/add_resource.py`).** Takes one resource plus the contexts it serves,
  inserts the identical entry into each file, keeps entries sorted, updates the counts, and runs
  the validator -- so adding or editing a multi-context resource stays a single action. Until it
  lands, edit the copies together and let CI catch any slip.

## Maintenance

Curated and maintained by the Arm Learning Paths / developer-discoverability team. This repo is
**public**. Every entry points only at already-public, Anaqua-cleared resources (see the contribution
rules above).
