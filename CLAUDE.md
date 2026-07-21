# CLAUDE.md

## README.md conventions

- Keep it a brief, high-level intro — not detailed technical documentation (no step-by-step "how this feature works" sections).
- Features section: plain sentences, not a checklist. Only list things that actually work today — skip stubs/unimplemented items entirely.
- No internal file paths, command syntax, or function/tool names in feature descriptions — describe behavior in plain English.
- Project Structure tree: top-level `src/` entries only (max depth 1), except `adapters/` and `extensions/`, which expand one level deeper to list their immediate subfolders.
- Keep "How to run the project" in sync whenever a new setup/install method is added.
- The Description should accurately reflect all extension mechanisms mentioned (skills, tools, MCP servers), not just one.
