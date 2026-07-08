# Arm Agent Resources

A curated, agent-friendly registry of **already-public Arm resources** for coding agents and
the developers who work with them. Each entry is a short pointer -- a resource that helps when
building, profiling, optimizing, or deploying software on Arm -- with just enough context for an
agent to decide whether to reach for it.

This repo is a **registry of pointers, not a mirror**. It does not host the resources; it points
to them and says, in one line, when they are useful. Keeping it small and stable lets a single
URL be referenced from agent flows while the list underneath keeps growing.

## How agents use this (progressive discovery)

An agent is handed the URL of this repo and a short description. It reads the small index in
[`registry.yaml`](registry.yaml), which lists the categories and what each is for, picks the ones
relevant to the developer's task, and loads only those [`registry/<category>.yaml`](registry/)
files. Within a file it matches the task against each entry's `when_to_use` and `example_use_case`
and follows the resource `url` only when relevant. Loading one small index plus a couple of
category files -- rather than the whole registry -- keeps the agent's context small and its
choices grounded in concrete examples.

## What belongs here

- **Only already open-sourced or Anaqua-cleared codebases and public documentation.** No
  internal-only repos, no gated pages, no anything that is not already public. If you are unsure
  whether a resource is cleared, do not add it. (A tool can be public even when its source repo is
  not -- point at the public product page or docs, never the internal repo.)
- Resources that genuinely help a software developer building on Arm: tools, SDKs, learning
  paths, knowledge bases, MCP servers, optimization/profiling guides, reference implementations.
- One entry per resource. If a resource moves, update its pointer here rather than the URL that
  references this repo.

## Layout

Everything is **YAML** so it is both agent- and script-friendly and can be checked by a
deterministic validator. Every push and pull request is validated in CI.

```
registry.yaml              # index: the category taxonomy + counts (read this first)
registry/
  mcp-servers.yaml         # entries for one category, one file per category
  profiling-optimization.yaml
  ...
schema/
  index.json               # schema for registry.yaml
  entry-file.json          # schema for each registry/<category>.yaml
scripts/validate.py        # validates the whole thing (run in CI)
```

The **index** lists every category with a one-line description, a `count`, and (when non-empty) the
`file` that holds its entries. Counts are checked against the files, so they cannot drift.

### Categories

`mcp-servers`, `knowledge-bases`, `learning-paths`, `profiling-optimization`, `sdks-tools`,
`reference-implementations`. A category's file is `registry/<key>.yaml`; the category is implied by
the filename, so entries do **not** repeat it.

### Entry fields

Each entry in a category file has five fields:

| Field | What to write |
|---|---|
| `name` | The resource's name. |
| `url` | A public `https://` link to the resource. |
| `contexts` | One or more developer contexts it is relevant to (see below). |
| `when_to_use` | 1-2 sentences on when it helps a software developer -- the selection signal. |
| `example_use_case` | A short concrete scenario (2-4 sentences): the developer's situation, what the agent does with this resource, and the outcome. One good scenario beats a long capability list. |

### Developer contexts

The context(s) an incoming agent would infer from the developer's coding environment. Tagging
entries lets us later serve a smaller, context-specific slice of the registry without duplicating
any source content (see [Scaling](#scaling)):

`cloud-development`, `compiled-languages`, `mobile-games`, `ml-developer`, `embedded-development`,
`performance-optimization`.

### Worked entry

From [`registry/mcp-servers.yaml`](registry/mcp-servers.yaml):

```yaml
- name: Arm MCP Server
  url: https://github.com/arm/mcp
  contexts: [cloud-development, compiled-languages, performance-optimization]
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
2. Add an entry to the right `registry/<category>.yaml`, keeping entries alphabetical by `name`.
   If the category has no file yet, create `registry/<category>.yaml` from the template above.
3. Bump that category's `count` in [`registry.yaml`](registry.yaml) (add the `file` pointer if it
   is the category's first entry).
4. Validate locally: `pip install pyyaml jsonschema && python scripts/validate.py`.
5. Open a PR. Keep it to the five fields -- no marketing copy. CI runs the validator.

Nominating a resource but not sure how to phrase it? Open an issue with the name + URL and a
maintainer will help shape the `when_to_use` / `example_use_case` lines.

## Scaling

The split above is the first scaling step (progressive discovery by category). The remaining move
is designed in and adds no duplicated content:

- **Per-developer-context views.** Every entry carries `contexts`, so smaller, context-specific
  views (e.g. `developer-contexts/performance-optimization.yaml`) can be **generated** from the
  category files rather than hand-maintained -- an agent loads only the slice matching the
  developer's environment, and there is still exactly one place to edit a resource.

## Maintenance

Curated and maintained by the Arm Learning Paths / developer-discoverability team. This repo is
currently **Internal** while the initial set is reviewed, and will be made **public** when ready.
