#!/usr/bin/env python3
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path


class ResumeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paper_depth = 0
        self.paper_count = 0
        self.links = []
        self.current_link = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "article" and attributes.get("data-kind") == "paper":
            self.paper_depth = 1
            self.paper_count += 1
        elif self.paper_depth:
            self.paper_depth += 1
        if tag == "a" and self.paper_depth and "doi.org/" in attributes.get("href", ""):
            self.current_link = {"href": attributes["href"], "text": ""}

    def handle_endtag(self, tag):
        if tag == "a" and self.current_link is not None:
            self.links.append(self.current_link)
            self.current_link = None
        if self.paper_depth:
            self.paper_depth -= 1

    def handle_data(self, data):
        if self.current_link is not None:
            self.current_link["text"] += data


def normalize_doi(value):
    value = str(value or "").strip()
    for prefix in ("https://doi.org/", "http://dx.doi.org/", "doi:"):
        if value.lower().startswith(prefix):
            value = value[len(prefix):].strip()
    return value


def validate(data, html_text):
    papers = [item for section in data.get("sections", []) for item in section.get("items", []) if item.get("kind") == "paper"]
    parser = ResumeParser()
    parser.feed(html_text)
    errors = []
    if parser.paper_count != len(papers):
        errors.append(f"paper count mismatch: JSON={len(papers)}, HTML={parser.paper_count}")
    expected_dois = [normalize_doi(item.get("doi")) for item in papers if item.get("doi")]
    actual = {link["href"].split("doi.org/", 1)[1]: link["text"].strip() for link in parser.links}
    for doi in expected_dois:
        if doi not in actual:
            errors.append(f"missing DOI link: {doi}")
        elif actual[doi] != "DOI":
            errors.append(f"DOI link text must be DOI: {doi}")
    for index, item in enumerate(papers, 1):
        for field in ("title", "journal", "level", "author_rank", "year"):
            if not item.get(field):
                errors.append(f"paper {index} missing field: {field}")
        if item.get("doi") and not item.get("doi_source_url"):
            errors.append(f"paper {index} missing DOI verification source: doi_source_url")
    if errors:
        raise SystemExit("HTML validation failed:\n- " + "\n- ".join(errors))
    print(f"HTML validation passed: {len(papers)} papers, {len(expected_dois)} DOI links")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--html", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    validate(data, Path(args.html).read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

