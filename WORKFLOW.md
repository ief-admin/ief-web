# IEF Website — Development & Deployment Workflow

How code moves from an edit to the live site, in the Cowork-based setup.

## Source of truth

The laptop folder `E:\COWORK\PROJECTS\IEF-WEB` is the single source of truth. It is a
git clone of `ief-admin/ief-web`. Cowork edits files here; you commit and push from here.

`minnaham` is out of the loop. With media now committed to the repo, there's no Linux
dependency: one Windows box edits, commits, and pushes; GitHub Actions builds and deploys
to Cloudflare. Don't edit code on `minnaham`. Editing in two places is the one thing that
breaks this model.

## Branches

- `develop` — integration / preview branch. Pushing here deploys to the preview URL.
- `main` — production. Merging `develop` into `main` deploys to the live site.

Work on `develop`. Promote to `main` only after the preview looks right.

## The loop

1. **Edit (Cowork).** You tell Cowork what to change; it edits the files in this folder.
   For `parts/` partials (nav, footer, donate modal), remember the change affects every
   page that includes it.
2. **Review + commit + push (laptop).** Open GitHub Desktop, review the diff, commit to
   `develop`, push.
3. **CI deploys.** GitHub Actions runs `compile_site.py` (flattens the SSI includes) and
   deploys HTML to Cloudflare Pages. Push to `develop` -> preview; push/merge to `main`
   -> production.
4. **Validate on preview.** Check `https://develop.ief-site.pages.dev`. This is the
   validation surface — there is no local preview server in this setup.
5. **Promote.** When the preview is good, merge `develop` into `main` (GitHub Desktop or a
   PR). CI deploys production at `https://ief-global.org`.

## Media (images / assets)

Media lives in the repo at `html/assets/` and is committed to git. `compile_site.py`
copies it into `dist/assets/`, so CI deploys the full site (HTML + images) to both preview
and production. No separate media deploy, no minnaham. If the image set grows large later,
the plan is to move media to Cloudflare R2 and out of git.

## What Cowork can and can't do

- **Can:** read and edit every file in this folder; check correctness with its host-side
  Read tool.
- **Can't:** reach GitHub or Cloudflare from its Linux sandbox, and can't run `wrangler`,
  `gh`, or `docker` there. So Cowork never pushes or deploys — that all happens on the
  laptop. (A GitHub connector exists and can be authenticated later to let Cowork read CI
  status and open PRs; not enabled yet.)

## Gotchas (hard-won — don't relearn these)

- **Don't run `git` from the Cowork sandbox on this repo.** Git writes over the Windows
  mount fail and leave a stale `.git/index.lock` that blocks GitHub Desktop. If GitHub
  Desktop complains about a lock, delete `.git\index.lock` and retry. All git stays on the
  laptop.
- **Sandbox reads truncate multibyte files** (Tamil, em-dashes, emoji). A file can look
  cut off when the sandbox or a sandbox `compile_site.py` run reads it, while the real file
  on the laptop and in git is complete. Trust the host-side Read tool and GitHub Desktop's
  diff, not a sandbox compile.
- **`compile_site.py` paths derive from `__file__`, never `~`** (CI runs as
  `/home/runner`). Don't regress this.
- **A malformed Alpine `x-data` silently breaks all Alpine on the page.** If interactivity
  dies, check `x-data` syntax first.
- **Cloudflare auth is an API token from `.env` / GitHub Actions secrets, not OAuth.**
  OAuth fails headless.

## Local files not in the repo

`IEF-HANDOFF.md` and `PROJECT-STATE.md` are git-ignored working notes. `PROJECT-STATE.md`
is the current source of truth for project decisions; `IEF-HANDOFF.md` is migration history.
