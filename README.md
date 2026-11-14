# NayanRabadiya.github.io

Personal site. The page and both CVs are generated from a handful of JSON
files, so updating content never means editing HTML.

```
content/         what the site says - edit these
  profile.json      name, headline, lede, intro, "currently", contact, CV links
  research.json     thesis entry
  experience.json   internship, TA work
  projects.json     project groups and their cards (the Projects section)
  education.json    degrees (page rows, timeline chart and CV rows)
  recognition.json  awards
  skills.json       the Technical section
  cv.json           CV-only wording: internship, thesis, project bullets, role variants
templates/
  index.html.j2     page layout (Jinja2)
site.css            styling (light theme, responsive)
build.py            content + template -> index.html  (add --cv for the PDFs)
cv/build_cv.py      content -> assets/*.pdf
assets/             generated CV PDFs, portrait
index.html          generated - do not edit by hand
```

## Where to look next

- `EDITING.md` - where every piece of text lives and how to add a project,
  a CV entry, an award or a course.
- `DEPLOY.md` - how a change gets online, how to check a deploy, how to undo
  one.

## Quick start

```bash
pip install jinja2                        # page only
pip install playwright pymupdf            # also needed for the CVs
python -m playwright install chromium

python build.py          # writes index.html
python build.py --cv     # also rewrites assets/Nayan_Rabadiya_CV_*.pdf
python -m http.server 8000   # preview at http://localhost:8000
```

Push to `main` and the GitHub Actions workflow rebuilds and publishes the
site at https://nayanrabadiya.github.io.
