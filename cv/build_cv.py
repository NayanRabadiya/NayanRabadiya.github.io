"""Build the role-specific CV PDFs from content/*.json.

Shared facts (name, links, education) come from content/profile.json and
content/education.json. Everything CV-specific - internship wording, thesis
summary, project bullets and the role variants - lives in content/cv.json.

usage:
    python cv/build_cv.py assets        # or: python build.py --cv

Each CV is rendered as A4 with Playwright's Chromium. The type size starts at
10.6pt and steps down 0.2pt at a time until the CV fits on one page.
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


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: Calibri, Carlito, 'Segoe UI', Arial, sans-serif;
  font-size: __FS__pt;
  line-height: 1.27;
  color: #111;
  width: 210mm;
  min-height: 297mm;
  padding: 8mm 12mm 7mm;
}
a { color: inherit; text-decoration: none; }
b { font-weight: 700; }
.head { display: flex; justify-content: space-between; align-items: flex-end; gap: 8mm; border-bottom: 1.5pt solid #1f3b31; padding-bottom: 2.2mm; }
.head h1 { margin: 0; font-size: 1.95em; letter-spacing: .01em; font-weight: 700; line-height: 1; }
.head .title { margin: 1.4mm 0 0; font-size: 1.05em; color: #1f3b31; font-weight: 600; }
.head .sub { margin: .8mm 0 0; color: #444; }
.links { text-align: right; line-height: 1.45; color: #333; white-space: nowrap; }
h2 {
  margin: 2.6mm 0 1mm;
  font-size: .86em;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: #1f3b31;
  border-bottom: .6pt solid #b9c2bd;
  padding-bottom: .6mm;
}
p { margin: 0; }
.summary { color: #222; }
.row { display: flex; justify-content: space-between; gap: 6mm; align-items: baseline; }
.row .r { color: #333; white-space: nowrap; }
.item { margin-top: 1.1mm; }
.item:first-of-type { margin-top: 0; }
.item .t { font-weight: 700; }
.item .m { color: #555; font-weight: 400; }
ul { margin: .5mm 0 0; padding-left: 4.2mm; }
li { margin: 0 0 .2mm; padding-left: .3mm; }
li::marker { color: #1f3b31; }
.skills div { display: flex; gap: 3mm; margin-bottom: .6mm; }
.skills dt { flex: 0 0 34mm; font-weight: 700; margin: 0; }
.skills dd { margin: 0; }
.edu .row { margin-bottom: .7mm; }
.edu .deg { color: #333; }
"""


def item(title, meta, when, bullets):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return (f'<div class="item"><div class="row"><div><span class="t">{title}</span> '
            f'<span class="m">&middot; {meta}</span></div><div class="r">{when}</div></div><ul>{lis}</ul></div>')


def build_html(profile, education, cv, variant, font_size):
    name = profile["name"]
    c = profile["contact"]
    site = profile["site_url"].rstrip("/")
    links = [
        ("mailto:" + c["email"], c["email"]),
        (c["linkedin"], c["linkedin"].replace("https://www.", "")),
        (c["github"], c["github"].replace("https://", "")),
        (site, site.replace("https://", "")),
    ]
    link_html = "<br/>".join(f'<a href="{h}">{t}</a>' for h, t in links)
    top = education["entries"][0]

    parts = [f'''<div class="head">
      <div>
        <h1>{name}</h1>
        <p class="title">{variant["title"]}</p>
        <p class="sub">M.Tech Computer Science &amp; Engineering, IIT Delhi &middot; {top["result"].replace("department rank", "Department rank")}</p>
      </div>
      <div class="links">{link_html}</div>
    </div>''']

    for sec in variant["order"]:
        if sec == "summary":
            parts.append(f'<h2>Profile</h2><p class="summary">{variant["summary"]}</p>')
        elif sec == "education":
            rows = []
            for e in education["entries"]:
                rows.append(f'<div class="row"><div><b>{e.get("cv_institution", e["institution"])}</b> <span class="deg">&mdash; {e["cv_degree"]}</span></div>'
                            f'<div class="r">{e["cv_years"]} &nbsp;&middot;&nbsp; {e["cv_result"]}</div></div>')
            parts.append('<h2>Education</h2><div class="edu">' + "".join(rows) + "</div>")
        elif sec == "thesis":
            parts.append("<h2>Research</h2>" + item(cv["thesis"]["title"], cv["thesis"]["meta"], "", variant["thesis"]))
        elif sec == "projects":
            parts.append("<h2>Projects</h2>" + "".join(
                item(p["title"], p["stack"], p["when"], p["bullets"])
                for p in (cv["projects"][k] for k in variant["projects"])))
        elif sec == "skills":
            dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in variant["skills"])
            parts.append(f'<h2>Technical skills</h2><dl class="skills">{dl}</dl>')
        elif sec == "experience":
            i = cv["intern"]
            parts.append("<h2>Experience</h2>" + item(i["org"], i["role"] + " &middot; " + i["stack"], i["when"], i["bullets"]))
        elif sec == "extras":
            parts.append("<h2>Teaching</h2><p>" + cv["teaching"] + "</p>")

    body = "".join(parts)
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{name} CV</title>'
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
            font_size = 10.6
            while True:
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(build_html(profile, education, cv, variant, font_size))
                page.goto("file:///" + os.path.abspath(html_path).replace("\\", "/"))
                page.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
                n = pages_of(out)
                if n == 1 or font_size <= 9.0:
                    break
                font_size = round(font_size - 0.2, 2)
            os.remove(html_path)
            print(f"wrote {os.path.relpath(out, ROOT)}: {n} page(s) at {font_size}pt")
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets"))
