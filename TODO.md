# To do

Checklist for publishing and finishing the site. Tick items off as you go.

## Publish (done 14 Nov 2026)

- [x] Pushed to `main`.
- [x] Repo made public (GitHub Pages on the free plan needs a public repo).
- [x] Pages source set to GitHub Actions; "Build and deploy" workflow green.
- [x] https://nayanrabadiya.github.io serves the page, both CVs, the portrait
      and the stylesheet (all checked with HTTP 200).
- [ ] Open the site on your phone and scroll through the Projects section.

## Content you can fill in (edit the JSON, commit, push)

- [ ] **Repo links.** For each project you are allowed to publish, create or
      make public the GitHub repo, then add `"source": "https://github.com/..."`
      to that project in `content/projects.json`. A "Source" link appears in
      its rail automatically. Course assignments usually must stay private
      under the honour code; safe candidates are the thesis sync code,
      Minutes Away, the speech translator and the expense tracker.
- [ ] **Dates to confirm** in `content/projects.json` and `content/research.json`:
      - [ ] Cornerstone runtime: "2025 - 2026" (which months?)
      - [ ] Speech translation: "2026" (which months?)
      - [ ] Thesis start: "2026 - present" (which month?)
- [ ] **M.Tech completion month.** In `content/education.json` set `end` for
      the IIT Delhi entry (2027.5 = July 2027) and update
      `chart.remaining_label` if it is no longer "mid-2027".
- [ ] **Recognition** in `content/recognition.json`: add GATE rank,
      scholarships, hackathons, B.E.-era awards. It currently has two rows.
- [ ] **Sharper portrait.** The current one is the 175 px photo from the CV
      PDF. Replace `assets/portrait.jpg` with a square photo of about 600 px.
      No other change needed.
- [ ] **CV numbers.** The ML-from-scratch bullets in `content/cv.json` quote no
      accuracy figures on purpose. If you want one quoted, decide which and
      add it to the bullet.

## Keep current (every semester)

- [ ] Update `currently.text` and `currently.when` in `content/profile.json`.
- [ ] Add new projects to the right group in `content/projects.json`.
- [ ] Add CV-worthy projects to `content/cv.json` and list their keys in the
      `projects` array of the AI_ML or SDE variant (keep four per CV; swap one
      out rather than adding a fifth, or the CV will shrink below 10 pt).
- [ ] Add new courses to `coursework` in `content/education.json`.
- [ ] Run `python build.py --cv` locally once to check the CVs still fit on
      one page, then commit and push.

## Optional

- [ ] Custom domain: add a `CNAME` file with the domain, point DNS at GitHub
      Pages, and set the domain under Settings -> Pages.
- [ ] Forms-based editor: Decap or Sveltia CMS can sit at `/admin` and edit the
      same JSON files through a login with your GitHub account. Only worth it
      if editing JSON by hand becomes a chore.
