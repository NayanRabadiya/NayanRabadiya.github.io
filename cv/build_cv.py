"""Build the role-specific CV PDFs from content/*.json.

Layout follows the widely used "Jake's Resume" format: centred name and
contact line, small-caps section headers with a rule, bold title on the left
with the date on the right, an italic subline, and tight bullets. Type is
Source Serif 4 (fetched from Google Fonts at build time, falling back to
Georgia if offline).

Shared facts (name, links, education) come from content/profile.json and
content/education.json. Everything CV-specific - internship wording, thesis
summary, project bullets and the role variants - lives in content/cv.json.

usage:
    python cv/build_cv.py assets        # or: python build.py --cv

Each CV is rendered as A4 with Playwright's Chromium. The type size starts at
10.8pt and steps down 0.2pt at a time until the CV fits on one page.
"""
import json
import os
import sys

import pymupdf
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")


def load(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as f:
        return json.load(f)


FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@'
    '0,8..60,400;0,8..60,600;1,8..60,400&display=block" rel="stylesheet">'
)


# Inline SVG icons (24x24 viewBox) so the PDF needs no icon font.
# GitHub and LinkedIn marks are the Simple Icons paths; envelope and globe are plain strokes.
ICONS = {
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">'
            '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M3 6.5l9 6.5 9-6.5"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
    "github": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">'
             '<circle cx="12" cy="12" r="9.5"/><ellipse cx="12" cy="12" rx="4" ry="9.5"/><path d="M2.5 12h19M4 7.5h16M4 16.5h16"/></svg>',
}

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: 'Source Serif 4', Charter, Georgia, 'Times New Roman', serif;
  font-size: __FS__pt;
  line-height: 1.22;
  color: #111;
  width: 210mm;
  min-height: 297mm;
  padding: 8mm 12mm 7mm;
}
a { color: inherit; text-decoration: none; }
b { font-weight: 600; }
i { font-style: italic; }
p { margin: 0; }

/* ---- header: centred name, role line, contact line ---- */
.head { text-align: center; }
.head h1 { margin: 0; font-size: 2.3em; font-weight: 600; letter-spacing: .02em; line-height: 1.05; }
.head .title { margin: 1.1mm 0 0; font-size: 1.02em; font-style: italic; color: #333; }
.head .contact { margin: 1.3mm 0 0; font-size: .95em; color: #222; }
.head .contact a { white-space: nowrap; display: inline-flex; align-items: center; gap: .35em; }
.head .contact svg { width: 1.05em; height: 1.05em; flex: none; position: relative; top: .02em; }
.head .contact .sep { margin: 0 .5em; color: #888; }

/* ---- sections ---- */
h2 {
  margin: 2.5mm 0 1mm;
  padding-bottom: .5mm;
  font-size: 1.02em;
  font-weight: 600;
  font-variant: small-caps;
  letter-spacing: .06em;
  border-bottom: .8pt solid #222;
}
.summary { text-align: justify; }

/* ---- entries: bold title left / date right, italic subline ---- */
.item { margin-top: 1.1mm; }
.item:first-of-type { margin-top: 0; }
.row { display: flex; justify-content: space-between; gap: 5mm; align-items: baseline; }
.row .r { white-space: nowrap; }
.item .t { font-weight: 600; }
.item .t .stack { font-weight: 400; font-style: italic; color: #333; }
.item .t .bar { font-weight: 400; color: #888; margin: 0 .35em; }
.item .sub { font-style: italic; color: #333; font-size: .97em; }
ul { margin: .5mm 0 0; padding-left: 4.5mm; }
li { margin: 0 0 .15mm; padding-left: .4mm; }
li::marker { font-size: .8em; }

/* ---- education rows ---- */
.edu .row { margin-bottom: .5mm; }
.edu .inst { font-weight: 600; }
.edu .deg { font-style: italic; color: #333; font-size: .97em; }
.edu .r { text-align: right; }
.edu .r i { color: #333; }

/* ---- skills: inline label: text ---- */
.skills p { margin: 0 0 .5mm; }
"""


def item(title, right_top, sub_left, sub_right, bullets):
    """One entry: bold title with the date on the right, an italic subline, bullets."""
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    sub = ""
    if sub_left or sub_right:
        sub = f'<div class="row sub"><div>{sub_left}</div><div class="r">{sub_right}</div></div>'
    return (f'<div class="item"><div class="row"><div class="t">{title}</div><div class="r">{right_top}</div></div>'
            f"{sub}<ul>{lis}</ul></div>")


def build_html(profile, education, cv, variant, font_size):
    name = profile["name"]
    c = profile["contact"]
    site = profile["site_url"].rstrip("/")
    # icon + short label; the full URL is the link target
    links = [
        ("mailto:" + c["email"], "mail", c["email"]),
        (c["linkedin"], "linkedin", "LinkedIn"),
        (c["github"], "github", "GitHub"),
        (site, "globe", "Portfolio"),
    ]
    contact = '<span class="sep">|</span>'.join(
        f'<a href="{h}">{ICONS[icon]}<span>{t}</span></a>' for h, icon, t in links)

    parts = [
        '<div class="head">'
        f"<h1>{name}</h1>"
        f'<p class="title">{variant["title"]}</p>'
        f'<p class="contact">{contact}</p>'
        "</div>"
    ]

    for sec in variant["order"]:
        if sec == "summary":
            parts.append(f'<h2>Summary</h2><p class="summary">{variant["summary"]}</p>')
        elif sec == "education":
            rows = []
            for e in education["entries"]:
                inst = e.get("cv_institution", e["institution"])
                rows.append(
                    f'<div class="row"><div><span class="inst">{inst}</span> '
                    f'<span class="deg">&mdash; {e["cv_degree"]}</span></div>'
                    f'<div class="r">{e["cv_years"]} &nbsp;&middot;&nbsp; <i>{e["cv_result"]}</i></div></div>'
                )
            parts.append('<h2>Education</h2><div class="edu">' + "".join(rows) + "</div>")
        elif sec == "thesis":
            t = cv["thesis"]
            parts.append("<h2>Research</h2>" + item(t["title"], t.get("when", ""), t["meta"], "", variant["thesis"]))
        elif sec == "projects":
            blocks = [cv["projects"][k] for k in variant["projects"]]
            parts.append("<h2>Projects</h2>" + "".join(
                item(p["title"] + '<span class="bar">|</span><span class="stack">' + p["stack"] + "</span>",
                     p["when"], "", "", p["bullets"]) for p in blocks))
        elif sec == "skills":
            lines = "".join(f"<p><b>{k}:</b> {v}</p>" for k, v in variant["skills"])
            parts.append(f'<h2>Technical Skills</h2><div class="skills">{lines}</div>')
        elif sec == "experience":
            parts.append("<h2>Experience</h2>" + "".join(
                item(x["role"], x["when"], x["org"], x["stack"], x["bullets"])
                for x in (cv["intern"], cv["teaching"])))

    body = "".join(parts)
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{name} CV</title>{FONT_LINK}'
            f'<style>{CSS.replace("__FS__", str(font_size))}</style></head><body>{body}</body></html>')


def pages_of(pdf):
    with pymupdf.open(pdf) as d:
        return len(d)


def main(out_dir):
    profile, education, cv = load("profile.json"), load("education.json"), load("cv.json")
    os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        for key, variant in cv["variants"].items():
            out = os.path.join(out_dir, variant["file"])
            html_path = os.path.join(out_dir, f"_cv_{key}.html")
            font_size = 10.8
            while True:
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(build_html(profile, education, cv, variant, font_size))
                page.goto("file:///" + os.path.abspath(html_path).replace("\\", "/"), wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                page.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
                n = pages_of(out)
                if n == 1 or font_size <= 9.4:
                    break
                font_size = round(font_size - 0.2, 2)
            os.remove(html_path)
            print(f"wrote {os.path.relpath(out, ROOT)}: {n} page(s) at {font_size}pt")
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets"))
