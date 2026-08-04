#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

TEXT_EXTENSIONS = {".md", ".py", ".html", ".css", ".js", ".json", ".yaml", ".yml", ".txt"}
PATTERNS = {
    "mainland_phone": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "windows_user_path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.I),
    "id_number": re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
}
ALLOWLIST = {"example@example.com"}

def main():
    parser = argparse.ArgumentParser(description="Scan a skill or output directory for common personal data.")
    parser.add_argument("path")
    args = parser.parse_args()
    root = Path(args.path)
    findings = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                value = match.group(0)
                if value in ALLOWLIST:
                    continue
                findings.append((str(path.relative_to(root)), label, value))
    if findings:
        for item in findings:
            print("\t".join(item))
        raise SystemExit(1)
    print("Privacy scan passed")

if __name__ == "__main__":
    main()


