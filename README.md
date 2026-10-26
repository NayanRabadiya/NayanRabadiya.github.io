# NayanRabadiya.github.io

Personal site — single static page, no build step.

```
index.html   the whole page (content lives here)
site.css     styling (light + dark, responsive)
assets/      CV PDF, portrait
```

## Local preview

```bash
python -m http.server 8000
# open http://localhost:8000
```

## Deploy

Commit and push to `main`. GitHub Pages serves it at
https://nayanrabadiya.github.io — give it a minute after the push.

```bash
git add -A
git commit -m "Rebuild portfolio"
git push origin main
```

If the site does not appear, check **Settings → Pages** on the repo:
source should be *Deploy from a branch*, branch `main`, folder `/ (root)`.

## Updating the CV

Replace `assets/Nayan_Rabadiya_CV.pdf` and push. The filename is linked from
the masthead nav, the sticky bar and the contact section — keep it the same and
nothing else needs editing.

## Open TODOs

Search the HTML for `TODO` — see `TODO.md` for the list.
