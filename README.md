# Hera Content Radar Skill

[简体中文](README.zh-CN.md) · English

An Agent Skill for building and maintaining a source-backed daily content radar from YouTube, podcasts, AI/news feeds, newsletters, public X profiles or Lists, and useful web directories.

The Skill helps an agent manage sources, refresh today and yesterday, use available captions or transcripts without downloading audio by default, write Chinese summaries, synthesize cited daily insights, generate content ideas, validate the site, and publish only after checks pass.

> This repository contains the Skill and public starter catalogs, not a hosted service. The screenshots below show an example radar generated with the Skill.

## Preview

![Daily radar overview](docs/images/overview.jpg)

<p align="center">
  <img src="docs/images/highlights.jpg" alt="Sourced daily highlights" width="49%">
  <img src="docs/images/directory.jpg" alt="Source directory" width="49%">
</p>

## What it does

- Maintains normalized YouTube channel IDs, podcast RSS feeds, editorial/newsletter feeds, public X links, and a navigation directory.
- Refreshes both today and yesterday in the configured timezone so late publications and corrections can be recovered.
- Prefers manual YouTube captions, then automatic captions; it does not download audio for transcription unless the user explicitly asks.
- Uses podcast show notes, chapters, and publisher transcript links when available.
- Produces Chinese summaries with clear provenance and avoids pretending that title-only evidence is a deep summary.
- Creates up to ten conclusion-level “Daily Highlights,” each backed by clickable sources, plus four to six content ideas.
- Preserves older history and manual editorial overrides when a source fails.
- Supports local projects on macOS and Windows and can use an existing deployment workflow when one is available.

## Requirements

- An agent that supports `SKILL.md`-style Agent Skills, such as Codex or Claude Code.
- Git for the command-line installation method.
- Python 3 for the optional cross-platform source catalog helper.
- Project-specific tools only when needed. For example, `yt-dlp` improves YouTube caption retrieval, and Node.js is needed when the generated radar uses a Node-based site.

The Skill does not require a public domain. A radar can run locally. A LAN link only works while the host computer is awake, connected, and running the preview process.

## Manual installation

### Codex — macOS or Linux

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/hihera/hera-content-radar-skill.git ~/.codex/skills/hera-content-radar
```

### Codex — Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
git clone https://github.com/hihera/hera-content-radar-skill.git "$HOME\.codex\skills\hera-content-radar"
```

### Claude Code — macOS or Linux

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/hihera/hera-content-radar-skill.git ~/.claude/skills/hera-content-radar
```

### Claude Code — Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/hihera/hera-content-radar-skill.git "$HOME\.claude\skills\hera-content-radar"
```

Start a new agent session after installation so the Skill can be discovered. If Git is unavailable, download the repository ZIP and extract it to the matching `hera-content-radar` folder. `SKILL.md` must be directly inside that folder.

To update later:

```bash
git -C ~/.codex/skills/hera-content-radar pull --ff-only
```

On Windows, replace the path with `$HOME\.codex\skills\hera-content-radar` or the Claude Code equivalent.

## Install with an agent

Paste this into Codex, Claude Code, or another Agent-Skills-compatible agent:

```text
Install the Hera Content Radar Skill from
https://github.com/hihera/hera-content-radar-skill
into this agent's personal skills directory. Read the repository README, keep
SKILL.md at the root of the installed skill folder, do not run the Skill yet,
and tell me whether I need to start a new session.
```

The agent should use its supported Skill installer when available. Otherwise it can clone or copy the repository into the correct personal skills directory.

## Basic use

Examples:

```text
Use $hera-content-radar to create a local daily content radar with the public starter sources.
```

```text
Use $hera-content-radar to refresh today and yesterday, preserve older data, run the existing quality checks, and report failed sources. Do not publish yet.
```

```text
Use $hera-content-radar to add this YouTube channel and this podcast RSS feed, deduplicate the catalog, refresh recent content, and show me a local preview.
```

Publication is not implied by a refresh. Ask the agent to publish only when you want it to use the project's existing authorized hosting workflow.

## Default sources

The starter catalog reflects Hera's public reading mix and is intentionally editable. Examples include:

- YouTube: How I AI, The Pragmatic Engineer, IBM Technology, Andrej Karpathy, Lenny's Podcast, and selected Chinese technology channels.
- Podcasts: 硅谷101, 疯投圈, 声动早咖啡, 文化有限, and other public RSS feeds.
- AI/news: TechCrunch AI, The Verge AI, Google Blog, and Hugging Face Blog.
- Newsletters: Lenny's Newsletter, The Rundown AI, TLDR, Every, and Stratechery.
- Directory: AIHOT, GitHub Trending, model directories, and publication home pages.
- X navigation: public profiles across AI research, products, engineering, investing, and creative work.

These are examples, not endorsements or mandatory dependencies. Availability, feed terms, and redistribution rights remain with each publisher.

## Change your sources

For a generated radar, edit `data/sources.json`. For the defaults used by future new radars, edit:

- `assets/default-sources.json`
- `assets/default-x-creators.json`

You can edit the UTF-8 JSON directly or use the portable helper:

```bash
python3 scripts/catalog.py --catalog /path/to/radar/data/sources.json list
python3 scripts/catalog.py --catalog /path/to/radar/data/sources.json dedupe
```

Windows PowerShell:

```powershell
py scripts/catalog.py --catalog "C:\path\to\radar\data\sources.json" list
py scripts/catalog.py --catalog "C:\path\to\radar\data\sources.json" dedupe
```

Add examples:

```bash
python3 scripts/catalog.py --catalog /path/to/data/sources.json add-youtube \
  --name "Channel name" --handle "@channel" --channel-id "UC..." \
  --category "AI and engineering"

python3 scripts/catalog.py --catalog /path/to/data/sources.json add-podcast \
  --name "Podcast name" --rss "https://example.com/feed.xml" \
  --category "Technology"

python3 scripts/catalog.py --catalog /path/to/data/sources.json add-feed \
  --kind ai --name "Publisher" --url "https://example.com/feed.xml" \
  --site-url "https://example.com/" --priority 8

python3 scripts/catalog.py --catalog /path/to/data/sources.json add-directory \
  --name "Useful site" --url "https://example.com/" \
  --category "AI tools" --description "Short description"
```

Use `py` instead of `python3` on Windows when appropriate. After changing sources, ask the agent to validate and deduplicate the catalog before refreshing.

## Privacy and safety

The public starter files intentionally exclude personal account URLs, private X List IDs, cookies, tokens, email addresses, local IPs, browser history, and personal following-state flags.

Before publishing your own radar:

- keep paid-feed tokens and API keys in a secret store;
- review public X Lists before sharing their IDs;
- do not commit `.env` files, browser exports, cookies, or deployment credentials;
- treat summaries as secondary material and verify important numbers, policies, and quotes against the original source;
- check publisher terms before mirroring or redistributing content.

## Repository structure

```text
hera-content-radar-skill/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── default-sources.json
│   └── default-x-creators.json
├── references/
│   ├── daily-refresh.md
│   ├── platforms.md
│   └── source-catalog.md
└── scripts/catalog.py
```

## License

[MIT](LICENSE). The license applies to this Skill's instructions, scripts, and repository assets. Third-party articles, feeds, videos, podcasts, profile images, names, and trademarks remain the property of their respective owners.
