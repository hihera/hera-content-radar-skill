# Cross-platform notes

Read this reference when setting up or running a radar on macOS or Windows.

## Shared behavior

The Skill package, manual installation flow, agent-assisted installation prompt, source schema, and daily workflow are the same across supported desktop systems. Do not create separate operating-system instructions unless a command or path actually differs.

- Use UTF-8 JSON and text files.
- Use Python's `pathlib` and atomic file replacement for catalog edits.
- Prefer project scripts such as `npm run content:update`, `npm run dev`, and `npm run build`; npm resolves platform-specific executable wrappers.
- Quote paths because user directories may contain spaces or non-ASCII characters.
- Keep secrets in the host platform's secret store or deployment environment, never in the catalog.

## Small environment differences

- Personal Skill folders live under the user's home directory: `.codex/skills` for Codex and `.claude/skills` for Claude Code. Path notation varies by shell and file manager.
- Invoke Python as `python3`, `python`, or `py`, depending on the installation.
- Use PowerShell-native commands for copying, removing, and environment variables. Do not require WSL.
- A local-network preview may require an operating-system firewall exception; ask before changing firewall settings.

## Optional tools

`yt-dlp` improves YouTube metadata and caption retrieval when it is installed and available on `PATH`. Its absence should not block title-and-description ingestion. Never download audio for transcription unless the user explicitly asks for it.

Node.js is required only when the selected radar project uses a Node-based site. Follow the project's declared engine version and lockfile rather than imposing a global version.
