---
name: hera-content-radar
description: Build, refresh, and extend a daily content radar from YouTube channels, podcast RSS feeds, AI/news sites, newsletters, public X profiles or lists, and a link directory. Use when the user asks to manage sources, fetch recent content, use available captions or transcripts without audio transcription, produce Chinese summaries and sourced cross-content insights, or maintain a content-radar site on macOS or Windows. Do not use for an unrelated one-off transcript request.
---

# Hera Content Radar

Maintain a source-backed daily reading site while keeping its catalog easy to extend and safe to share.

## Choose the mode

- For adding, removing, importing, validating, or deduplicating information sources, read [references/source-catalog.md](references/source-catalog.md).
- For fetching today and yesterday, updating summaries and insights, or publishing the site, read [references/daily-refresh.md](references/daily-refresh.md).
- For operating-system commands, local prerequisites, or cross-platform project setup, read [references/platforms.md](references/platforms.md).
- When both are requested, update and validate the catalog first, then refresh the affected date window and publish once.

## Locate or initialize the project

For an existing radar, use the project path supplied by the user or locate the nearest project containing `data/sources.json` or an equivalent source catalog. Inspect its scripts, data schema, and hosting configuration before editing. Preserve its framework, source history, manual editorial overrides, and live address.

For a new radar, create a responsive local site that can run on the user's operating system and initialize its catalog from [assets/default-sources.json](assets/default-sources.json). Set `trackingStart` to the current local date when the template value is `null`. The bundled defaults are public information sources curated by Hera; users may retain, remove, or extend them. [assets/default-x-creators.json](assets/default-x-creators.json) is an optional public-profile navigation starter, not authorization to scrape authenticated or private timelines.

Use an existing deployment integration when the project already has one. OpenAI Sites is appropriate when `.openai/hosting.json` and Sites tools are available. Otherwise keep the project locally runnable and use only a hosting provider the user selected or authorized.

## Non-negotiable content rules

- Preserve original titles, canonical links, publishers, publication times, and available cover images.
- Treat Asia/Shanghai as the default editorial day unless the user specifies another timezone.
- Produce Chinese card summaries. Keep product names and proper nouns in their established form.
- Do not present a feed description, page metadata, or title paraphrase as a deep summary. Label limitations internally and state them when they affect the result.
- For YouTube, prefer existing manual captions, then automatic captions. Do not download audio for transcription unless the user explicitly authorizes it.
- Keep raw content in its original module. “今日看点” must contain ten conclusion-level insights synthesized across available modules, not ten recommended links. Every insight must show one or more clickable source records that support it.
- Generate “今日选题” from the strongest cross-module evidence, not from AI news alone.
- Deduplicate by stable channel ID, feed URL, canonical content URL, and normalized title where necessary.
- Never include cookies, session tokens, credentials, private browser data, or personal visit timestamps in a shareable catalog.
- Use OS-native commands and paths. Do not assume Bash exists on Windows or PowerShell exists on macOS.

## Update behavior

When the user supplies a new creator or site, resolve its stable identifier or feed, validate it, classify it, deduplicate it, update the catalog, fetch the affected recent window, rebuild, and publish the existing site. If a source cannot be verified, record the unresolved item separately instead of inventing an ID or RSS URL.

Only publish after the project’s own validation succeeds and publication is within the user's request. Preserve an existing public URL and access level unless the user explicitly asks to change them. A failed refresh or deployment must not replace the last working version.
