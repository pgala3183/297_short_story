"""Render article/medium_article.md to HTML.

Two outputs:
  article/medium_article.html  - local preview, images load from ../figures
  article/medium_import.html   - for Medium: images point at the public GitHub copies and the
                                 markdown table is turned into a list (Medium has no tables).
                                 Open it in a browser, select all, copy, paste into the Medium editor,
                                 or use Medium's "Import a story" on its GitHub Pages / raw URL.
Run from the repo root: python src/render_article.py
"""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "article" / "medium_article.md"
RAW = "https://raw.githubusercontent.com/pgala3183/297_short_story/main/figures/"

CSS = """
body{max-width:760px;margin:40px auto;padding:0 20px;font:19px/1.6 Georgia,'Times New Roman',serif;color:#242424}
h1{font:700 40px/1.2 'Segoe UI',Helvetica,Arial,sans-serif;margin:0 0 8px}
h2{font:700 28px/1.25 'Segoe UI',Helvetica,Arial,sans-serif;margin:48px 0 12px}
h3{font:600 21px/1.35 'Segoe UI',Helvetica,Arial,sans-serif;color:#555;margin:28px 0 8px}
img{max-width:100%;display:block;margin:24px auto}
table{border-collapse:collapse;font:15px/1.4 'Segoe UI',Helvetica,Arial,sans-serif;margin:16px 0}
td,th{border-bottom:1px solid #e6e5e1;padding:6px 8px;vertical-align:top;text-align:left}
hr{border:0;border-top:1px solid #e6e5e1;margin:40px 0}
code{background:#f3f2ef;padding:1px 4px;border-radius:3px}
"""


def table_to_list(md: str) -> str:
    """Replace the reading-list table with a numbered list (Medium cannot show tables)."""
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("| #") and i + 1 < len(lines) and lines[i + 1].startswith("|---"):
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                num, paper, who, when, why = cells[:5]
                out.append(f"{num}. {paper}. *{who}*, {when}. {why}.")
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def render(md: str, img_prefix: str, title: str) -> str:
    md = md.replace("../figures/", img_prefix)
    body = markdown.markdown(md, extensions=["tables", "sane_lists"])
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'><style>{CSS}</style></head>"
            f"<body>{body}</body></html>")


def main():
    md = SRC.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", md, re.M).group(1)
    (ROOT / "article" / "medium_article.html").write_text(render(md, "../figures/", title), encoding="utf-8")
    (ROOT / "article" / "medium_import.html").write_text(render(table_to_list(md), RAW, title), encoding="utf-8")
    words = len(re.findall(r"[A-Za-z0-9']+", re.sub(r"!\[.*?\]\(.*?\)", "", md)))
    print(f"rendered article ({words} words)")


if __name__ == "__main__":
    main()
