# Platform notes

Read this reference when setting up or running a radar on macOS or Windows.

## Portable defaults

- Use UTF-8 JSON and text files.
- Use Python's `pathlib` and atomic file replacement for catalog edits.
- Prefer project scripts such as `npm run content:update`, `npm run dev`, and `npm run build`; npm resolves platform-specific executable wrappers.
- Quote paths because user directories may contain spaces or non-ASCII characters.
- Keep secrets in the host platform's secret store or deployment environment, never in the catalog.

## macOS

- The usual personal Skill folders are `~/.codex/skills/` for Codex and `~/.claude/skills/` for Claude Code.
- Use `python3` when `python` is not available.
- A local-network preview may require allowing incoming connections in the macOS firewall.

## Windows

- The usual personal Skill folders are `$HOME\.codex\skills\` for Codex and `$HOME\.claude\skills\` for Claude Code.
- Use `py` or `python` depending on the Python installation.
- Use PowerShell-native commands for copying, removing, and environment variables. Do not require WSL.
- A local-network preview may require an inbound Windows Firewall rule for the selected port; ask before changing firewall settings.

## Optional tools

`yt-dlp` improves YouTube metadata and caption retrieval when it is installed and available on `PATH`. Its absence should not block title-and-description ingestion. Never download audio for transcription unless the user explicitly asks for it.

Node.js is required only when the selected radar project uses a Node-based site. Follow the project's declared engine version and lockfile rather than imposing a global version.
