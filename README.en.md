# Hera Content Radar Skill

[简体中文](README.md) · English

Turn scattered YouTube, podcast, AI news, newsletter, and X sources into a daily, source-backed Chinese reading radar.

![Hera Content Radar overview](docs/images/overview.jpg)

## What it is

Hera Content Radar is an Agent Skill for Codex, Claude Code, and other Agent-Skills-compatible tools. It is not a fixed aggregation service. It is a reusable workflow for creating a radar, changing its sources, refreshing it over time, and connecting it to an existing publishing setup.

It helps an agent:

- Check both today and yesterday to recover late or missed publications.
- Prefer YouTube captions, podcast show notes, and public transcripts.
- Write evidence-aware Chinese summaries while preserving original titles and links.
- Produce sourced Daily Highlights and content ideas across all modules.
- Normalize and deduplicate sources without erasing existing data after one failed fetch.
- Cache public X profile images locally so a generated page does not depend on X image servers on every visit.

## Quick start

### 1. Install with an agent (recommended)

Paste this into Codex, Claude Code, or another compatible agent:

```text
Install the Hera Content Radar Skill from
https://github.com/hihera/hera-content-radar-skill
into this agent's personal Skills directory. Keep SKILL.md at the root of the
hera-content-radar folder. Tell me whether I need to start a new session, and
do not create a site yet.
```

The agent can use its Skill installer or clone the repository into the correct directory. A new session is usually needed for Skill discovery.

### 2. Create your first radar

```text
Use $hera-content-radar and the public starter sources to create a daily
content radar, then show me a local preview.
```

For an existing radar:

```text
Use $hera-content-radar to refresh today and yesterday, preserve older data,
run the checks, and open the latest page.
```

## Change many sources at once

You do not need to edit JSON one record at a time or look up YouTube channel IDs and podcast RSS URLs yourself. The easiest approach is to give the agent all links together.

### Option 1: Paste a list of links

```text
Use $hera-content-radar to add all links below to my sources. Detect whether
each one is YouTube, a podcast, news, a newsletter, an X profile, or a web
directory. Resolve stable IDs or RSS feeds, deduplicate the catalog, and report
anything that cannot be verified:

https://x.com/OpenAI
https://www.youtube.com/@AndrejKarpathy
https://example.com/podcast
https://example.com/newsletter
```

Links may be one per line or include a name and short note. The agent normalizes them before updating content.

### Option 2: Upload a simple source inbox

Copy [source-inbox.example.txt](assets/source-inbox.example.txt), replace its examples, and attach it to your agent:

```text
Use $hera-content-radar to import the attached source inbox. Detect each type,
resolve stable IDs or RSS feeds, deduplicate it, and list unresolved entries.
```

The file is intentionally loose-formatted:

```text
https://x.com/OpenAI
YouTube | Andrej Karpathy | https://www.youtube.com/@AndrejKarpathy
Newsletter | Example | https://example.com/newsletter
```

### Option 3: Edit configuration directly

For advanced users:

- Current radar sources: `data/sources.json`
- Starter sources for new radars: `assets/default-sources.json`
- X creator list: `assets/default-x-creators.json`

Ask the agent to validate and deduplicate after editing. `scripts/catalog.py` is an optional helper, not a prerequisite for using the Skill.

## Manual installation

macOS, Windows, and Linux use the same files and installation flow. Only home-directory path notation differs.

1. Open the agent's personal Skills directory:

| Agent | Personal Skills directory |
| --- | --- |
| Codex | `.codex/skills` under your user home directory |
| Claude Code | `.claude/skills` under your user home directory |

2. Open a terminal in that directory and run:

```bash
git clone https://github.com/hihera/hera-content-radar-skill.git hera-content-radar
```

3. Start a new agent session.

Without Git, download the repository ZIP and extract it as `hera-content-radar`. `SKILL.md` must be directly inside that folder.

To update later, run this inside the installed Skill folder:

```bash
git pull --ff-only
```

## Starter sources

The repository includes an editable public starter catalog, including:

- YouTube: How I AI, The Pragmatic Engineer, IBM Technology, Andrej Karpathy, and Lenny's Podcast.
- Podcasts: public Chinese technology, business, culture, and AI RSS feeds.
- AI and technology news: TechCrunch AI, The Verge AI, Google Blog, and Hugging Face Blog.
- Newsletters: Lenny's Newsletter, The Rundown AI, TLDR, Every, and Stratechery.
- Directory: AIHOT, GitHub Trending, model directories, and AI tool directories.
- X: public profiles across AI research, products, engineering, investing, and creative work.

These sources are editable starting points, not endorsements or mandatory dependencies.

## Preview

<p align="center">
  <img src="docs/images/highlights.jpg" alt="Daily Highlights with supporting sources" width="49%">
  <img src="docs/images/x-creators.jpg" alt="X creator directory with visible profile images" width="49%">
</p>

## Content principles

- Prefer manual YouTube captions, then automatic captions; do not download audio for transcription by default.
- State the evidence limitation when only a title or description is available.
- Daily Highlights must be conclusions with supporting links, not a renamed article list.
- Private X Lists, authenticated timelines, and paid content may not be publicly readable; public profile links can still be used for navigation.

## Repository structure

```text
hera-content-radar-skill/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── default-sources.json
│   ├── default-x-creators.json
│   └── source-inbox.example.txt
├── references/
├── scripts/catalog.py
└── docs/images/
```

## License and content boundary

[MIT](LICENSE) applies to this repository's Skill instructions, scripts, and original assets. Third-party articles, feeds, videos, podcasts, profile images, names, and trademarks remain the property of their respective owners. Do not commit cookies, tokens, paid-feed keys, or other credentials to a public repository.
