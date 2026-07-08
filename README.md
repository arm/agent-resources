# Arm Agent Resources

A curated, agent-friendly registry of **already-public Arm resources** for coding agents and
the developers who work with them. Each entry is a short pointer -- a resource that helps when
building, profiling, optimizing, or deploying software on Arm -- with just enough context for an
agent to decide whether to reach for it.

This repo is a **registry of pointers, not a mirror**. It does not host the resources; it points
to them and says, in one line, when they are useful. Keeping it small and stable lets a single
URL be referenced from agent flows while the list underneath keeps growing.

## How agents use this

An agent is handed the URL of this repo and a short description. It reads the registry, matches a
developer's task against each entry's **When to use it** and **Example use case**, and follows the
resource URL only when relevant. That keeps the agent's context small and its choices grounded in
concrete examples rather than long descriptions.

## What belongs here

- **Only already open-sourced or Anaqua-cleared codebases and public documentation.** No
  internal-only repos, no gated pages, no anything that is not already public. If you are unsure
  whether a resource is cleared, do not add it.
- Resources that genuinely help a software developer building on Arm: tools, SDKs, learning
  paths, knowledge bases, MCP servers, optimization/profiling guides, reference implementations.
- One entry per resource. If a resource moves, update its pointer here rather than the URL that
  references this repo.

## Entry format

Every entry provides four things, so an agent gets concise selection context plus one exemplar:

| Field | What to write |
|---|---|
| **Name** | The resource's name. |
| **URL** | A public link to the resource. |
| **When to use it** | 1-2 sentences on when it is useful for software developers -- the selection signal. |
| **Example use case** | One realistic, one-line scenario in the developer's own words -- the request or situation that should trigger this resource. Concrete beats comprehensive; one example is enough. |

### Worked example

> **Arm MCP Server**
> https://github.com/arm/mcp
> **When to use it:** Gives an AI assistant Arm-specific tools -- semantic search over Arm docs and learning resources, x86->Arm code-migration analysis, and container-architecture checks. Reach for it when you need grounded Arm knowledge or want to check or port code for Arm.
> **Example use case:** "Is my Docker image Arm-compatible, and what would it take to migrate my x86 service to Graviton?"

### Copy-paste template

```markdown
### <Name>

- **URL:** <https://...>
- **When to use it:** <1-2 sentences on when it helps a software developer>
- **Example use case:** "<one-line developer-voice scenario that should trigger this resource>"
```

## How to contribute

1. Confirm the resource is **already public** (open-sourced or Anaqua-cleared). This is a hard rule.
2. Add an entry to [`registry.md`](registry.md) using the template above, filed under the right
   category.
3. Open a PR. Keep the description to the four fields -- no marketing copy.

Nominating a resource but not sure how to phrase it? Open an issue with the name + URL and a
maintainer will help shape the **When to use it** / **Example use case** lines.

## Maintenance

Curated and maintained by the Arm Learning Paths / developer-discoverability team. This repo is
currently **Internal** while the initial set is reviewed, and will be made **public** when ready.
