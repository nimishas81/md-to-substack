#!/usr/bin/env python3
"""Convert a markdown file to rich text on the macOS clipboard.

Usage:
    python3 convert.py path/to/post.md
    python3 convert.py path/to/post.md --print   # also echo HTML to stdout
"""

import argparse
import subprocess
import sys
from pathlib import Path

import markdown


SUBSTACK_EXTENSIONS = [
    "extra",         # tables, fenced code, footnotes, abbr, def lists
    "smarty",        # smart quotes / dashes
    "sane_lists",    # predictable list behavior
]


def md_to_html(md_text: str) -> str:
    html = markdown.markdown(md_text, extensions=SUBSTACK_EXTENSIONS, output_format="html5")
    return f"<html><body>{html}</body></html>"


def copy_html_to_clipboard(html: str) -> None:
    hex_data = html.encode("utf-8").hex()
    script = f'set the clipboard to «data HTML{hex_data}»'
    subprocess.run(["osascript", "-e", script], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown → Substack-ready clipboard rich text")
    parser.add_argument("path", type=Path, help="Path to the .md file")
    parser.add_argument("--print", dest="print_html", action="store_true", help="Also print HTML to stdout")
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"error: {args.path} is not a file", file=sys.stderr)
        return 1

    md_text = args.path.read_text(encoding="utf-8")
    html = md_to_html(md_text)
    copy_html_to_clipboard(html)

    if args.print_html:
        print(html)

    word_count = len(md_text.split())
    print(f"copied to clipboard — {word_count} words — paste into Substack editor")
    return 0


if __name__ == "__main__":
    sys.exit(main())
