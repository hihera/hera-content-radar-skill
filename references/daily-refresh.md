# Daily refresh

Read this reference when the radar fetches recent content, updates editorial output, or publishes the site.

## Time window

Resolve today and yesterday in the configured timezone, defaulting to Asia/Shanghai. Fetch both days on every scheduled run because feeds, captions, and publication timestamps can arrive late or be corrected. Preserve older history and manual editorial data.

## Ingestion order

1. Read the project catalog and existing content before fetching.
2. YouTube: fetch channel feed metadata; use `yt-dlp` for already available manual captions, then automatic captions. Do not download audio by default.
3. Podcasts: read RSS or Atom. Prefer publisher transcripts when the feed exposes them; otherwise use show notes and mark the summary basis accordingly.
4. AI news and newsletters: use official feeds first. Hydrate article metadata and representative images only when needed, with bounded concurrency and timeouts.
5. X: use public profile or List links and official embeds for navigation. Do not promise reliable scraping of authenticated or private timelines.
6. Isolate failures per source. Keep the previous successful record when one source is unavailable.

Inspect and use the project's established content command, commonly `npm run content:update`, rather than reimplementing a working fetcher. On Windows, run the same npm script from PowerShell or Command Prompt; do not translate it into a Bash-only wrapper.

## Editorial processing

For every new or corrected item:

- Keep the original title.
- Write a Chinese summary of two to four useful sentences from the strongest available evidence.
- Do not pad a thin feed description into a false detailed summary.
- Preserve the original link, source, time, module, tags, image, and summary provenance.
- Translate English descriptions, while preserving model and product names.

For each date, create exactly ten “今日看点” entries when the day has enough meaningful evidence. These are conclusions derived after reading across modules, not ranked source cards. Each entry needs:

- a concise conclusion title;
- a two-to-four-sentence explanation of why it matters;
- a useful category label;
- one or more supporting source links, with module, publisher, and original title;
- no claim broader than the cited material supports.

If fewer than ten defensible insights exist, use fewer and state the limitation; never split one weak point merely to reach ten. Generate four to six “今日选题” ideas from the strongest cross-module insights, each with a clear angle and a source link.

## Quality checks

Before publishing, verify:

- today and yesterday were both considered;
- duplicate URLs and duplicate cross-posts are removed;
- English titles may remain original, but the summary beneath them is Chinese;
- every insight source resolves to a content record for the same date;
- every insight is a conclusion rather than an article recommendation;
- images use lazy loading and failures do not block text;
- no private tokens or browser data entered public assets;
- the project build succeeds.

Compare the generated files with the previous state. If nothing material changed, do not create a new site version.

## Local preview and publishing

Start with the project's documented local preview command and report whether the link is loopback-only, local-network, or public. A local-network address is temporary: it requires the host computer to stay awake and the process to keep running.

If the project contains `.openai/hosting.json` and Sites tools are available, reuse its project ID and existing slug. Commit and push the exact validated state, package the validated build, save one version, and preserve the existing access level unless the user asks to change it.

For projects without Sites, use the existing deployment configuration or a hosting provider explicitly selected by the user. Do not create accounts, change DNS, publish publicly, or replace a production address without the required authorization. A failed refresh or deployment must not replace the last working deployment.

Report new and corrected item counts, failed sources, the dates refreshed, insight coverage, and the working local or public page link.
