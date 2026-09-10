# Source catalog

Read this reference when sources are added, removed, imported, validated, or deduplicated.

## Public default catalog

`assets/default-sources.json` contains public YouTube channels, podcast feeds, editorial feeds, newsletters, and navigation sites. `assets/default-x-creators.json` contains public X profile links without personal follow-state or private List metadata. They are starter data, not immutable requirements: a user may delete defaults and add their own sources.

Do not put account cookies, private list identifiers, browser-history timestamps, email addresses, paid-feed tokens, or other credentials in a shareable catalog. Keep user-specific secrets in the platform’s secret store when a supported integration truly requires them.

## Project schema

The standard project catalog is `data/sources.json`.

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

## Validation sequence

1. Normalize redirects, scheme, hostname casing, trailing slashes, and tracking parameters.
2. Resolve stable channel or feed identifiers.
3. Confirm the source responds and contains at least one plausible item.
4. Classify it without changing the user’s editorial intent.
5. Check primary and secondary dedupe keys.
6. Update the catalog with `scripts/catalog.py` or a focused equivalent.
7. Refresh today and yesterday so the new source appears immediately when it has recent content.

Do not remove a source only because one fetch fails. Report temporary failures and preserve the last successful data.
