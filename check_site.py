#!/usr/bin/env python3
"""Standard-library checks for the generated static site."""
from __future__ import annotations
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


class PageCheck(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.resources = []
        self.image_alts = []
        self.h1_count = 0
        self.main_count = 0
        self.ids = []
        self.lang = None
        self.direction = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang, self.direction = a.get("lang"), a.get("dir")
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        if tag == "img":
            self.image_alts.append((a.get("src", ""), "alt" in a))
            if a.get("src"):
                self.resources.append(a["src"])
        if tag == "script" and a.get("src"):
            self.resources.append(a["src"])
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "canonical"):
            self.resources.append(a["href"])


def local_target(page: Path, url_path: str) -> Path:
    decoded = unquote(url_path)
    if decoded.startswith("/"):
        # A root-absolute URL is only correct for a domain-root site, so the check
        # still verifies the target inside dist and flags missing paths.
        target = (DIST / decoded.lstrip("/")).resolve()
    else:
        target = (page.parent / decoded).resolve()
    if target.is_dir() or decoded.endswith("/"):
        target = target / "index.html"
    return target


def main() -> int:
    if not DIST.exists():
        print("dist/ is missing. Run `python build.py` first.", file=sys.stderr)
        return 1
    errors = []
    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        errors.append("No HTML pages were generated.")
    for page in pages:
        parser = PageCheck()
        try:
            parser.feed(page.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            errors.append(f"{page.relative_to(DIST)} is not UTF-8.")
            continue
        relative = page.relative_to(DIST)
        if parser.h1_count != 1:
            errors.append(f"{relative}: expected exactly one h1; found {parser.h1_count}.")
        if parser.main_count != 1:
            errors.append(f"{relative}: expected exactly one main landmark; found {parser.main_count}.")
        if len(parser.ids) != len(set(parser.ids)):
            errors.append(f"{relative}: duplicate HTML id attribute.")
        if relative.parts and relative.parts[0] in ("en", "fa") and len(relative.parts) > 1:
            expected = ("ltr" if relative.parts[0] == "en" else "rtl")
            if parser.lang != relative.parts[0]:
                errors.append(f"{relative}: html lang must be {relative.parts[0]}.")
            if parser.direction != expected:
                errors.append(f"{relative}: html dir must be {expected}.")
        for src, has_alt in parser.image_alts:
            if not has_alt:
                errors.append(f"{relative}: image is missing alt text (use alt=\"\" for decorative images): {src}")
        for url in parser.links + parser.resources:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or url.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            if not parsed.path:
                continue
            target = local_target(page, parsed.path)
            try:
                target.relative_to(DIST.resolve())
            except ValueError:
                errors.append(f"{relative}: local URL escapes the generated site: {url}")
                continue
            if not target.exists():
                errors.append(f"{relative}: missing local target for {url} (expected {target.relative_to(DIST.resolve())}).")
    registry = DIST / "data" / "certificates.json"
    if not registry.exists():
        errors.append("Certificate registry dist/data/certificates.json is missing.")
    else:
        try:
            records = json.loads(registry.read_text(encoding="utf-8"))
            allowed = {"number", "holderNameEn", "holderNameFa", "issueDateEn", "issueDateFa", "descriptionEn", "descriptionFa"}
            seen = set()
            if not isinstance(records, list):
                errors.append("Certificate registry must be a JSON array.")
            else:
                for record in records:
                    extra = set(record) - allowed
                    if extra:
                        errors.append(f"Certificate record contains unsupported fields: {sorted(extra)}")
                    number = str(record.get("number", "")).strip().upper()
                    if number in seen:
                        errors.append(f"Duplicate certificate number: {number}")
                    seen.add(number)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Certificate registry is invalid JSON: {exc}")
    if errors:
        print(f"Static site checks failed: {len(errors)} issue(s)")
        for error in errors:
            print("- " + error)
        return 1
    print(f"Static site checks passed: {len(pages)} HTML pages, local links/resources resolved, language directions and image alt attributes checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
