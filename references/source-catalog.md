# Source catalog

Read this reference when sources are added, removed, imported, validated, or deduplicated.

## Public default catalog

`assets/default-sources.json` contains public YouTube channels, podcast feeds, editorial feeds, newsletters, and navigation sites. `assets/default-x-creators.json` contains public X profile links without personal follow-state or private List metadata. They are starter data, not immutable requirements: a user may delete defaults and add their own sources.

Do not put account cookies, private list identifiers, browser-history timestamps, email addresses, paid-feed tokens, or other credentials in a shareable catalog. Keep user-specific secrets in the platform’s secret store when a supported integration truly requires them.

## Project schema

The standard project catalog is `data/sources.json`.

### Bulk source inbox

Treat a pasted block of links or an attached `.txt`, `.md`, `.csv`, or `.json` file as a source inbox. The user may provide bare URLs or loose rows such as `type | name | URL | note`; strict formatting is not required.

1. Extract all candidate URLs and any nearby names or notes.
2. Detect the likely source type from the URL and page metadata.
3. Resolve stable YouTube channel IDs, podcast RSS feeds, canonical editorial feeds, public X handles or Lists, and directory URLs.
4. Deduplicate the complete batch against the existing catalog.
5. Apply verified additions together and return unresolved items with a short reason.

Do not make the user add records one by one or manually construct the normalized JSON. [The source-inbox example](../assets/source-inbox.example.txt) is an optional convenience, not a required input format.

### YouTube

Required fields:

```json
{
  "name": "Channel name",
  "handle": "@channel",
  "channelId": "UC...",
  "category": "AI、产品与创业"
}
```

Use the stable `channelId` as the primary key and the normalized handle as a secondary key. Resolve IDs from the channel page or a reliable YouTube metadata tool. A display name alone is insufficient.

### Podcasts

```json
{
  "category": "科技、AI、创业与投资",
  "name": "Podcast name",
  "appleId": "1234567890",
  "rss": "https://example.com/feed.xml",
  "appleUrl": "https://podcasts.apple.com/..."
}
```

Use the canonical RSS URL as the primary key and Apple podcast ID as a secondary key. Validate that the endpoint is parseable RSS or Atom and contains episode entries. Redirects are allowed; store the stable final feed when appropriate.

### AI news and newsletters

```json
{
  "kind": "ai",
  "name": "Publisher",
  "url": "https://example.com/feed.xml",
  "siteUrl": "https://example.com/",
  "priority": 10
}
```

`kind` is `ai` or `newsletter`. Deduplicate by canonical feed URL. Prefer official first-party feeds. A website without a feed can remain in the directory but must not be treated as an automatically refreshable source.

### Navigation directory

```json
{
  "category": "Newsletter／科技",
  "name": "Site name",
  "url": "https://example.com/",
  "domain": "example.com",
  "description": "Short purpose"
}
```

Deduplicate by canonical URL, then domain and purpose. Directory entries are jump links; they do not imply permission or technical ability to ingest the site.

### Public X profiles and lists

Use public profile records for navigation:

```json
{
  "handle": "OpenAI",
  "name": "OpenAI",
  "category": "AI 公司 / 产品",
  "profileUrl": "https://x.com/OpenAI"
}
```

Public List URLs may be added when the user supplies them and wants them shared. Never export private List IDs, cookies, login state, or a user's personal following flags into a reusable default catalog. Following an account and adding it to a List are separate actions; do not infer permission for either.

When a user deletes a List and moves its members into “Following,” remove the obsolete List URL from the source catalog, generated directory data, and rendered embeds. Keep the public profile directory as the reusable view. Do not replace the List with a supposed public “Following feed”: X home and following timelines depend on the signed-in viewer and are not a shareable equivalent to a List. An optional `https://x.com/home` link may open X for the current viewer, while profile cards should continue to use stable public profile URLs.

For a rendered profile directory, avoid loading every avatar directly from X on each visit. Cache public profile images into bounded local static assets, keep the original public image URL as refresh provenance, use lazy loading, and provide a text or local-image fallback. Refresh the cache when creators or avatars change rather than during every daily content update. Validate that every local avatar exists before publishing.

## Validation sequence

1. Normalize redirects, scheme, hostname casing, trailing slashes, and tracking parameters.
2. Resolve stable channel or feed identifiers.
3. Confirm the source responds and contains at least one plausible item.
4. Classify it without changing the user’s editorial intent.
5. Check primary and secondary dedupe keys.
6. Update the catalog with `scripts/catalog.py` or a focused equivalent.
7. Refresh today and yesterday so the new source appears immediately when it has recent content.

Do not remove a source only because one fetch fails. Report temporary failures and preserve the last successful data.
