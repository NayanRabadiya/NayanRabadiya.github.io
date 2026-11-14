# Editing the site

Where every piece of text lives and how to change it. For getting a change
online, see `DEPLOY.md`.

## How the pieces fit together

```
content/*.json  --+
                  |--> build.py --> index.html         (the page)
templates/        |
  index.html.j2 --+

content/profile.json  --+
content/education.json  |--> cv/build_cv.py --> assets/Nayan_Rabadiya_CV_AI_ML.pdf
content/cv.json       --+                       assets/Nayan_Rabadiya_CV_SDE.pdf

site.css  --> colours, fonts, spacing, responsive rules (no content)
```

Rule of thumb: if you want to change **words or facts**, edit a file in
`content/`. If you want to change **how something looks**, edit `site.css`
or `templates/index.html.j2`. You should almost never need the template.

After editing, run `python build.py` (or `python build.py --cv` if you touched
anything the CVs use) and reload the page.

## Writing rules for every JSON file

- Strings may contain HTML. `<strong>text</strong>` emphasises on the page,
  `<b>text</b>` on a CV. `<code>ptrace</code>` renders in monospace.
- Keep files plain ASCII. Write special characters as entities:

  | You want | Write      |
  |----------|------------|
  | long dash (em dash) | `&mdash;` |
  | short dash in a range | `&ndash;` |
  | middle dot separator | `&middot;` |
  | & | `&amp;` |
  | multiplication sign (2.18x) | `&times;` |
  | non-breaking space (64 MB) | `&nbsp;` |
  | arrow (north-east) | `&#8599;` |

- JSON is strict: double quotes only, a comma between items, **no** comma
  after the last item, and no comments. If the build fails with a
  `JSONDecodeError`, the message names the file and line.
- A quick validity check for one file:
  `python -c "import json; json.load(open('content/projects.json'))"`

## The page, section by section

### Masthead (name, headline, lede, intro, Currently box)

File: `content/profile.json`

| Key | What it is |
|-----|------------|
| `name` | Your name, used in the title, header, sticky bar and footer |
| `descriptor` | List of 2-4 short phrases shown under the name, separated by dots |
| `affiliation` | The small uppercase line (degree, institute, city) |
| `portrait` | Path to the photo, or `null` to hide the photo entirely |
| `lede` | The large serif sentence |
| `intro` | List of paragraphs under the lede (one string per paragraph) |
| `currently.text` | Text inside the "Currently" box |
| `currently.when` | The small date under it, for example `November 2026` |
| `meta_description`, `og_description` | What search engines and link previews show; plain text, no HTML |
| `site_url` | Canonical URL |
| `contact.blurb` | Paragraph in the Contact section |
| `contact.email`, `contact.github`, `contact.linkedin` | Links in the Contact section; email is also the mailto link |
| `cvs` | List of CV download links: `label` (nav), `contact_label` (Contact section) and `file` |
| `colophon` | Right-hand text in the footer |

To update the Currently box each term, change `currently.text` and
`currently.when`. Nothing else.

To change the photo, replace `assets/portrait.jpg` with a square image
(about 600 px). No JSON change needed unless you rename the file.

### 01 Research

File: `content/research.json` (a single entry)

| Key | What it is |
|-----|------------|
| `when`, `where`, `sup`, `stack` | Lines in the left rail; each list item is one line |
| `title` | Heading |
| `role` | One-line subtitle |
| `paragraphs` | List of body paragraphs |
| `specs` | The three big numbers: each has `n` (the number) and `l` (the caption; `<br />` forces a line break) |

### 02 Experience

File: `content/experience.json` (a list of entries, newest first)

Each entry:

```json
{
  "when": ["JAN &mdash; APR 2025"],
  "where": ["Ahmedabad"],
  "stack": ["FastAPI &middot; MongoDB", "React &middot; Python"],
  "title": "Company or activity",
  "role": "Your title there",
  "points": ["Bullet one.", "Bullet two."],
  "source": "https://github.com/... (optional)"
}
```

`stack` is optional. `role` is optional. Each string in `when`, `where`
and `stack` is one rail line on desktop; on phones they run together with a
dot between them.

### 03 Projects

File: `content/projects.json` (a list of groups; each group holds projects)

```json
{
  "id": "ml-ai",
  "letter": "A",
  "title": "Machine learning &amp; AI",
  "blurb": "One sentence describing the group.",
  "projects": [ ...entries with the same shape as Experience... ]
}
```

- **Add a project**: append an entry to the `projects` list of the right
  group. The count in the pill navigation updates by itself.
- **Reorder**: move entries within the list; the page follows the file.
- **Add a group**: append a group object with a new `id` (lowercase, hyphens,
  used in the URL as `#id`), the next `letter`, and at least one project.
- **Add a repo link**: add `"source": "https://github.com/..."` to the entry.
  A "Source" link appears in its rail.
- **Remove a project**: delete its object (watch the commas).

### 04 Education

File: `content/education.json`

`entries` is a list, newest first. Each entry feeds three places:

| Keys | Used by |
|------|---------|
| `institution`, `degree`, `years`, `result` | The text rows shown on phones and when printing |
| `start`, `end`, `expected`, `chart_label`, `chart_degree`, `chart_value`, `chart_title` | The timeline chart shown on desktop |
| `cv_institution` (optional), `cv_degree`, `cv_years`, `cv_result` | The Education table on both CVs |

`start` and `end` are decimal years: `.0` is January, `.5` is July, `.6` is
roughly August. `expected: true` draws the part after today hatched. The
"today" line is computed on every build, so it moves by itself.

`chart.year_from` and `chart.year_to` set the axis. `chart.remaining_label`
is the legend text for the hatched part. `chart.desc` is the text read out by
screen readers; update it when the facts change.

`coursework` is the comma-separated course list under the entries.

### 05 Recognition

File: `content/recognition.json`, a list of `{ "text": "...", "where": "IIT DELHI" }`.
Add a row per award. `where` is shown small and uppercase.

### 06 Technical

File: `content/skills.json`, a list of `{ "group": "Languages", "list": "C, C++, Python, SQL" }`.
Order in the file is order on the page.

### 07 Contact and footer

All in `content/profile.json` (see the Masthead table above). The copyright
year is the build year, computed automatically.

## The CVs

File: `content/cv.json`. Shared facts (name, links, education rows) are read
from `profile.json` and `education.json` so they cannot drift.

| Key | What it is |
|-----|------------|
| `intern` | The Experience entry: `org`, `role`, `when`, `stack`, `bullets` |
| `thesis.title`, `thesis.meta` | Heading and grey meta line of the Research entry |
| `teaching` | One sentence for the Teaching section |
| `projects` | A dictionary of reusable project blocks keyed by a short name (`tpch`, `nn`, ...), each with `title`, `stack`, `when`, `bullets` |
| `variants` | One object per CV, keyed `AI_ML` and `SDE` |

Each variant:

| Key | What it is |
|-----|------------|
| `file` | Output filename inside `assets/` (must match `cvs[].file` in `profile.json`) |
| `title` | The coloured line under your name, e.g. `Machine Learning &middot; Data Science` |
| `summary` | The Profile paragraph |
| `skills` | List of `[label, text]` pairs for the skills table |
| `thesis` | List of bullets for the Research entry (worded for this role) |
| `projects` | List of keys from the shared `projects` dictionary, in display order |
| `order` | Section order: any arrangement of `summary`, `education`, `experience`, `thesis`, `projects`, `skills`, `extras` |

- **Add a project to a CV**: write it once under `projects` with a new key,
  then put that key into the `projects` list of the variant(s) that should
  show it. Keep four per CV; swap one out rather than adding a fifth. The
  builder shrinks the type until the CV fits one page, and stops at 9 pt; if
  it reports 2 pages, cut text.
- **Add a third CV** (for example research): copy a variant under a new key,
  give it a new `file`, and add a matching object to `cvs` in `profile.json`
  so the page links to it.
- Rebuild with `python build.py --cv` and open the PDFs from `assets/`.

## Look and feel

`site.css` starts with a block of variables: page background, ink colour,
accent green, fonts, column widths. Changing `--accent` recolours every
accent on the page. Section spacing, the pill navigation and the responsive
breakpoints (1040 px and 820 px) are all in this file and commented.

`templates/index.html.j2` is the page skeleton. Edit it only to add a new
section or change markup. It uses Jinja2: `{{ x }}` prints a value,
`{% for %}` loops, and the `entry` macro at the top renders every card in
Experience and Projects.

## Common mistakes

- Edited `index.html` directly: the next build overwrites it. Move the change
  into `content/` or the template.
- Build says `jinja2 not found`: `pip install jinja2`.
- CV build says `playwright` or `pymupdf` not found: `pip install playwright pymupdf`
  then `python -m playwright install chromium`.
- Page shows `&amp;mdash;` literally: you double-escaped. Write `&mdash;`.
- A project vanished: a missing comma made JSON swallow it, or the build
  failed and you are looking at the old page. Check the terminal output.
