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

## Editing content

Fields may contain inline HTML. Use entities for special characters so the
files stay plain ASCII: `&mdash;` for a long dash, `&ndash;` for a short one,
`&middot;` for a dot, `&amp;` for an ampersand, `&times;` for a multiplication
sign. Wrap a phrase in `<strong>...</strong>` to emphasise it on the page or
`<b>...</b>` on a CV.

**Add a project.** Open `content/projects.json`, pick a group, and append an
object to its `projects` list:

```json
{
  "when": ["JAN &mdash; APR 2027"],
  "where": ["IIT Delhi", "Prof. Someone"],
  "stack": ["Python &middot; PyTorch"],
  "title": "Project name",
  "role": "One-line subtitle (optional)",
  "points": ["First bullet.", "Second bullet with a <strong>number</strong>."],
  "source": "https://github.com/NayanRabadiya/repo  (optional)"
}
```

Each string in `when`, `where` and `stack` is one line of the left rail. The
group counts in the pill navigation update themselves.

**Change the "Currently" box.** `profile.json`, keys `currently.text` and
`currently.when`.

**Add a CV project.** Add an entry under `projects` in `content/cv.json`, then
list its key in the `projects` array of the variant that should show it. Each
variant has its own `summary`, `skills`, `thesis` bullets and section `order`.

**Education timeline.** `start` and `end` in `education.json` are decimal
years (2025.6 is roughly August 2025). The "today" marker and the hatched
remaining part are computed on each build.

## Building

```bash
pip install jinja2                        # page only
pip install playwright pymupdf            # also needed for the CVs
python -m playwright install chromium

python build.py          # writes index.html
python build.py --cv     # also rewrites assets/Nayan_Rabadiya_CV_*.pdf
```

Preview with `python -m http.server 8000` and open http://localhost:8000.

## Deploying

Push to `main`. The workflow in `.github/workflows/build.yml` installs the
tools above, runs `python build.py --cv`, and publishes the result to GitHub
Pages at https://nayanrabadiya.github.io. You can therefore edit a JSON file
directly on github.com, commit, and the live site updates in a minute or two
without running anything locally.

One-time setup on GitHub: **Settings -> Pages -> Source** must be set to
**GitHub Actions** (not "Deploy from a branch").

`index.html` and the PDFs are still committed so the repo works without the
Action, but the Action always rebuilds them from `content/`, so what you commit
there is what gets published.

## Open TODOs

See `TODO.md`.
