#!/usr/bin/env python3
"""Validate the public Hera Content Radar Skill package."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "agents/openai.yaml",
    "assets/default-sources.json",
    "assets/default-x-creators.json",
    "references/daily-refresh.md",
    "references/platforms.md",
    "references/source-catalog.md",
    "scripts/catalog.py",
    "docs/images/overview.jpg",
    "docs/images/highlights.jpg",
    "docs/images/directory.jpg",
)

PRIVATE_PATTERNS = {
    "absolute macOS user path": re.compile(r"/Users/[^/\s]+/"),
    "absolute Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
    "private IPv4 range": re.compile(r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))(?:\.\d{1,3}){2}\b"),
    "OpenAI Sites project id": re.compile(r"\bappgprj_[A-Za-z0-9]+\b"),
    "GitHub OAuth token": re.compile(r"\bgh[opusr]_[A-Za-z0-9_]{20,}\b"),
}


def fail(message: str) -> None:
    raise SystemExit(message)


def text_files() -> list[Path]:
    allowed = {".md", ".json", ".py", ".yaml", ".yml", ".txt"}
    return [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in allowed]


def main() -> int:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail(f"Missing required files: {', '.join(missing)}")

    for path in text_files():
        if path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                fail(f"Potential {label} in {path.relative_to(ROOT)}")

    prohibited_files = [path for path in ROOT.rglob(".env*") if path.name != ".env.example"]
    if prohibited_files:
        fail("Environment file found in release")

    sources = json.loads((ROOT / "assets/default-sources.json").read_text(encoding="utf-8"))
    creators = json.loads((ROOT / "assets/default-x-creators.json").read_text(encoding="utf-8"))

    if sources.get("trackingStart") is not None:
        fail("trackingStart must be null in the reusable public template")
    if any("/lists/" in item.get("url", "") for item in sources.get("directory", [])):
        fail("Default directory must not contain personal X List URLs")

    creator_items = creators.get("creators")
    if not isinstance(creator_items, list) or not creator_items:
        fail("Public X creator starter is empty or invalid")
    expected_keys = {"handle", "name", "category", "profileUrl"}
    if any(set(item) != expected_keys for item in creator_items):
        fail("Public X creator records contain unexpected or personal-state fields")

    print("Public release validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
