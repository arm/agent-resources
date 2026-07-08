# Registry

The list of already-public Arm resources. See [README](README.md) for the entry format and the
contribution rules (only already open-sourced / Anaqua-cleared codebases and public docs).

Entries are grouped by category. Within a category, keep them alphabetical by name.

## MCP servers

### Arm MCP Server

- **URL:** <https://github.com/arm/mcp>
- **When to use it:** Gives an AI assistant Arm-specific tools -- semantic search over Arm docs and learning resources, x86->Arm code-migration analysis, and container-architecture checks. Reach for it when you need grounded Arm knowledge or want to check or port code for Arm.
- **Example use case:** A team porting a Python/C++ service from x86 to Graviton is unsure which dependencies are Arm-ready. The agent queries the Arm MCP Server to semantic-search Arm's docs and run a migration and container-architecture scan across the codebase and image, gets back the specific packages that need an aarch64 build plus the recommended fixes, and applies them so the service builds and passes on Graviton.

## Knowledge bases & documentation

_None yet._

## Learning paths & tutorials

_None yet -- add learn.arm.com Learning Path repos here._

## Profiling & optimization

_None yet._

## SDKs & tools

_None yet._

## Reference implementations

_None yet._
