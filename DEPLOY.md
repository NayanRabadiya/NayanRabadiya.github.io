# Deploying the site

How a change on your computer becomes the live page at
https://nayanrabadiya.github.io. For *what* to change, see `EDITING.md`.

## The short version

```bash
cd portfolio
# ... edit files in content/ ...
python build.py            # regenerate index.html and preview it
git add -A
git commit -m "Describe the change"
git push origin main
```

GitHub rebuilds and publishes the site about two minutes after the push.
Nothing else is required.

## What happens on push

1. GitHub notices a push to `main` and starts the workflow in
   `.github/workflows/build.yml`.
2. The workflow installs Python, Jinja2, Playwright and Chromium.
3. It runs `python build.py --cv`, which regenerates `index.html` from
   `content/` and `templates/`, and the two CV PDFs from `content/`.
4. It copies `index.html`, `site.css` and `assets/` into a folder and uploads
   that folder to GitHub Pages.
5. Pages serves it at https://nayanrabadiya.github.io.

Because the workflow rebuilds everything, the `index.html` and PDFs you commit
are only a convenience for local preview. The live site always reflects
`content/`.

## Checking a deploy

- Repo page -> **Actions** tab. The newest "Build and deploy" run should show
  two green ticks (build, deploy). Click a red one to read the log.
- Or from the terminal: `gh run list --limit 3` and `gh run watch`.
- Browsers cache the page. If a change does not appear, hard-refresh
  (Ctrl+Shift+R) or open the site in a private window.

## Previewing locally before you push

```bash
python build.py             # page only, needs: pip install jinja2
python build.py --cv        # page and both CV PDFs, needs: pip install playwright pymupdf
                            #                              python -m playwright install chromium
python -m http.server 8000  # then open http://localhost:8000
```

Opening `index.html` directly from the file system also works for a quick look.
The web fonts need an internet connection either way.

## One-time settings (already done, for reference)

- Repository is **public**. GitHub Pages on the free plan does not serve
  private repositories.
- **Settings -> Pages -> Build and deployment -> Source** is **GitHub Actions**.
  If it is ever switched back to "Deploy from a branch", the workflow's deploy
  step fails with "Creating Pages deployment failed".
- The workflow has `pages: write` and `id-token: write` permissions; these are
  declared in the workflow file, nothing to set in the UI.

## Editing from a phone or any browser

Open the file on github.com, click the pencil icon, edit, and choose
"Commit changes" to `main`. The workflow runs exactly as for a local push. Use
this for small text fixes; for anything larger, edit locally so you can
preview first.

## Undoing a bad deploy

Every deploy corresponds to a commit. To go back:

```bash
git log --oneline            # find the last good commit
git revert <bad-commit>      # makes a new commit that undoes it
git push origin main
```

Never force-push `main` for this; a revert keeps the history readable.

## Files you should not edit by hand

- `index.html` - overwritten on every build. Edit `content/` or
  `templates/index.html.j2` instead.
- `assets/Nayan_Rabadiya_CV_*.pdf` - overwritten by `python build.py --cv`.
  Edit `content/cv.json` instead.

## Files kept out of the repo

`.gitignore` excludes `TODO.md` (personal checklist), `_site/` (workflow
output) and Python caches. Anything else you add to the folder will be
committed and therefore visible on the public repo.
