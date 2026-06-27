# IEF Website — Development & Deployment Workflow

How code moves from an edit to the live site.

## Environments

**Claude Code on the Windows laptop is the primary development environment** for this repo.
It does the whole pipeline end-to-end: edit, build, local preview, git commit/push, promote
`develop`→`main`, and check CI. All code development for ief-global.org happens here (git
steps can also be done in GitHub Desktop).

**Claude Cowork is for non-code work only** (content drafting, planning). Its Linux sandbox
can read/edit files over the Windows mount but cannot run git, build, or deploy reliably —
see Gotchas. Don't do code development for this project in Cowork; keeping development in one
place is what stops the two environments from drifting.

## Source of truth

The laptop folder `E:\COWORK\PROJECTS\IEF\WEB` is the single source of truth. It is a git
clone of `ief-admin/ief-web`. Edit, build, and push from here.

`minnaham` is out of the loop. With media committed to the repo, there's no Linux
dependency: one Windows box edits, builds, commits, and pushes; GitHub Actions builds and
deploys to Cloudflare. Editing in two places is the one thing that breaks this model.

Two repo files are canonical and are read by any AI agent that opens the project — keep them
current: **`CLAUDE.md`** (what the site is + working rules) and this **`WORKFLOW.md`**.

## Branches

- `develop` — integration / preview branch. Pushing here deploys to the preview URL.
- `main` — production. Merging `develop` into `main` deploys to the live site.

Work on `develop`. Promote to `main` only after the preview looks right.

## The loop

1. **Edit (Claude Code).** Change files in `html/`. For `parts/` partials (nav, footer,
   donate modal), remember the change affects every page that includes it. Keep bilingual
   parity — update EN and TA together.
2. **Build + preview locally (Claude Code).** `python html/compile_site.py` regenerates
   `dist/`, then `cd dist && python -m http.server 8080` → http://localhost:8080/en/.
   (Prepend `PYTHONUTF8=1` on Windows if the console chokes on the build script's emoji.)
3. **Commit + push `develop`.** From Claude Code (git creds are cached in Git Credential
   Manager) or GitHub Desktop. Never commit `dist/` (it is gitignored).
4. **CI deploys.** GitHub Actions runs `compile_site.py` and deploys to Cloudflare Pages.
   Push to `develop` → preview `https://develop.ief-site.pages.dev`; push/merge to `main`
   → production `https://ief-global.org`.
5. **Validate on preview**, then **promote** (next section).

## Promote develop → main (and keep them in sync)

Merging `develop` → `main` creates a merge commit on `main` only, which leaves `develop`
showing as "N commits behind." After every promotion, fast-forward `develop` back up so both
branches point to the same commit (`0 ahead, 0 behind`):

1. Merge `develop` → `main` (PR or `git merge --no-ff develop`), push `main` → prod deploy.
2. Switch to `develop`, `git merge main` (this fast-forwards, no new commit), push `develop`.

## Media (images / assets)

Media lives in the repo at `html/assets/` and is committed to git. `compile_site.py` copies
it into `dist/assets/`, so CI deploys the full site (HTML + images) to both preview and
production. If the image set grows large later, the plan is to move media to Cloudflare R2.

## Current site state (2026-06-27)

Detail lives in `CLAUDE.md` / `README.md`; the highlights:

- **Fonts:** one shared stack `'Noto Sans', 'Noto Sans Tamil', sans-serif` on `body` of
  every page (replaced IBM Plex Sans Tamil). Latin renders in Noto Sans, Tamil in Noto Sans
  Tamil via per-glyph fallback.
- **Pages:** `index`, `gallery`, `privacy`, `terms` under each of `html/en/` and `html/ta/`
  — 8 pages total. `compile_site.py` has a hardcoded page list; ADD new pages to it.
- **Footer:** dark (`bg-slate-950`) in `parts/footer-en.html` / `footer-ta.html`.
- **Favicon:** `html/assets/favicon.ico` + PNG/Apple/PWA icons, declared in every head;
  `compile_site.py` also copies `favicon.ico` to the dist root.

## Gotchas (hard-won — don't relearn these)

- **Don't run `git` from the Cowork sandbox on this repo.** Git writes over the Windows
  mount fail and leave a stale `.git/index.lock`. If GitHub Desktop complains about a lock,
  delete `.git\index.lock` and retry. Git happens in Claude Code or GitHub Desktop.
- **Cowork sandbox reads truncate multibyte files** (Tamil, em-dashes, emoji). A file can
  look cut off in the sandbox while the real file on the laptop and in git is complete.
- **`compile_site.py` paths derive from `__file__`, never `~`** (CI runs as `/home/runner`).
  Don't regress this.
- **A malformed Alpine `x-data` silently breaks all Alpine on the page.** If interactivity
  dies, check `x-data` syntax first.
- **Cloudflare auth is an API token from `.env` / GitHub Actions secrets, not OAuth.** OAuth
  fails headless.
- **`gh` (GitHub CLI) is not yet installed.** CI status is checked via the GitHub REST API
  for now; install `gh` later for scriptable PR/CI work.

## Local files not in the repo

`IEF-HANDOFF.md` and `PROJECT-STATE.md` are git-ignored working notes. `PROJECT-STATE.md` is
the current source of truth for project decisions; `IEF-HANDOFF.md` is migration history.
