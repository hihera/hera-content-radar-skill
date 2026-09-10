#!/usr/bin/env python3
"""Safely list, add, and deduplicate Hera Content Radar sources."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


SECTIONS = ("youtube", "podcasts", "editorialFeeds", "directory")
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def canonical_url(value: str) -> str:
    parts = urlsplit(value.strip())
    query = [(key, val) for key, val in parse_qsl(parts.query, keep_blank_values=True)
             if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS]
    path = parts.path if parts.path == "/" else parts.path.rstrip("/")
    return urlunsplit((parts.scheme.lower() or "https", parts.netloc.lower(), path, urlencode(query), ""))


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    for section in SECTIONS:
        data.setdefault(section, [])
        if not isinstance(data[section], list):
            raise ValueError(f"{section} must be a list")
    return data


def key_for(section: str, item: dict) -> tuple:
    if section == "youtube":
        return (item.get("channelId", "").strip().lower() or item.get("handle", "").strip().lower(),)
    if section == "podcasts":
        return (canonical_url(item.get("rss", "")) or item.get("appleId", "").strip(),)
    if section == "editorialFeeds":
        return (canonical_url(item.get("url", "")),)
    return (canonical_url(item.get("url", "")),)


def dedupe(data: dict) -> tuple[dict, dict[str, int]]:
    removed = {}
    for section in SECTIONS:
        seen = set()
        clean = []
        count = 0
        for item in data[section]:
            key = key_for(section, item)
            if not key[0] or key in seen:
                count += 1
                continue
            seen.add(key)
            clean.append(item)
        data[section] = clean
        removed[section] = count
    return data, removed


def atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def item_from_args(args: argparse.Namespace) -> tuple[str, dict]:
    if args.command == "add-youtube":
        return "youtube", {"name": args.name, "handle": args.handle, "channelId": args.channel_id, "category": args.category}
    if args.command == "add-podcast":
        item = {"category": args.category, "name": args.name, "rss": canonical_url(args.rss)}
        if args.apple_id:
            item["appleId"] = args.apple_id
        if args.apple_url:
            item["appleUrl"] = canonical_url(args.apple_url)
        return "podcasts", item
    if args.command == "add-feed":
        return "editorialFeeds", {"kind": args.kind, "name": args.name, "url": canonical_url(args.url), "siteUrl": canonical_url(args.site_url), "priority": args.priority}
    if args.command == "add-directory":
        url = canonical_url(args.url)
        return "directory", {"category": args.category, "name": args.name, "url": url, "domain": urlsplit(url).netloc, "description": args.description}
    raise ValueError(f"unsupported command: {args.command}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--catalog", required=True, type=Path)
    root.add_argument("--dry-run", action="store_true")
    sub = root.add_subparsers(dest="command", required=True)
    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--section", choices=SECTIONS)
    sub.add_parser("dedupe")

    yt = sub.add_parser("add-youtube")
    yt.add_argument("--name", required=True)
    yt.add_argument("--handle", required=True)
    yt.add_argument("--channel-id", required=True)
    yt.add_argument("--category", required=True)

    podcast = sub.add_parser("add-podcast")
    podcast.add_argument("--name", required=True)
    podcast.add_argument("--rss", required=True)
    podcast.add_argument("--category", required=True)
    podcast.add_argument("--apple-id")
    podcast.add_argument("--apple-url")

    feed = sub.add_parser("add-feed")
    feed.add_argument("--kind", required=True, choices=("ai", "newsletter"))
    feed.add_argument("--name", required=True)
    feed.add_argument("--url", required=True)
    feed.add_argument("--site-url", required=True)
    feed.add_argument("--priority", type=int, default=5)

    directory = sub.add_parser("add-directory")
    directory.add_argument("--name", required=True)
    directory.add_argument("--url", required=True)
    directory.add_argument("--category", required=True)
    directory.add_argument("--description", required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    data = load(args.catalog)
    if args.command == "list":
        payload = data[args.section] if args.section else {key: len(data[key]) for key in SECTIONS}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command != "dedupe":
        section, item = item_from_args(args)
        new_key = key_for(section, item)
        if any(key_for(section, current) == new_key for current in data[section]):
            print(json.dumps({"status": "duplicate", "section": section, "key": new_key[0]}, ensure_ascii=False))
            return 0
        data[section].append(item)

    data, removed = dedupe(data)
    if not args.dry_run:
        atomic_write(args.catalog, data)
    print(json.dumps({"status": "dry-run" if args.dry_run else "updated", "counts": {key: len(data[key]) for key in SECTIONS}, "duplicates_removed": removed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
