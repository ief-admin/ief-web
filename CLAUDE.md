# CLAUDE.md — IEF Global Website

Guidance for AI agents (Claude Code / Cowork) working in this repository.
Official website for the **International Educational Foundation (IEF)**, a 501(c)(3)
nonprofit. Live at **https://ief-global.org**.

## What this is

A **static, bilingual (English / Tamil) website**. No backend, no framework build
step beyond a small Python compiler. Pages are authored as HTML with SSI-style
`<!--#include virtual="...">` directives that get inlined at build time.

| Layer | Tech |
|---|---|
| Markup | HTML5 with SSI includes (compiled by `compile_site.py`) |
| Styling | Tailwind CSS (CDN, no build) |
| Interactivity | Alpine.js (CDN) |
| Fonts | Noto Sans (Latin) + Noto Sans Tamil (Tamil), Google Fonts — one shared `body` stack across `en/` and `ta/` |
| Build | `html/compile_site.py` (Python 3) |
| Hosting | Cloudflare Pages |

## Layout (source lives under `html/`)

```
html/
  en/        index.html, gallery.html      ← English pages (edit these)
  ta/        index.html, gallery.html      ← Tamil pages   (edit these)
  parts/     nav-en, nav-ta, footer-en, footer-ta, donate-modal   ← shared SSI includes
  index.html                                ← (legacy root; build emits its own redirect)
  assets/    *.webp media (committed to git)
  compile_site.py                           ← the build script
dist/        ← GENERATED OUTPUT — do not edit, gitignored
deploy.sh    docker-compose.yml  nginx.conf  wrangler.toml
.github/workflows/deploy.yml                ← CI build + deploy
```

> The README's "Repository Structure" section is partly stale — trust this file and
> the actual tree. Source is under `html/`, not the repo root.

## Build

```bash
python3 html/compile_site.py
```

This **wipes and regenerates `dist/`**: compiles `en/index`, `ta/index`, `en/gallery`,
`ta/gallery`, resolves `<!--#include virtual="...">` includes (recursively, from
`html/parts/`), writes a root `/` → `/en/` redirect, and copies `html/assets/` into
`dist/assets/`. On Windows use `python` if `python3` isn't on PATH.

Preview locally after building: `cd dist && python -m http.server 8080` → http://localhost:8080/en/

(Alternative: the `docker-compose.yml` + `nginx.conf` setup serves `html/` directly
with nginx SSI `on`, plus a Tailscale sidecar — used for a LAN/tailnet dev preview.)

## Deploy

**CI is the normal path.** `.github/workflows/deploy.yml` runs on push:

| Branch | Target |
|---|---|
| `main` | Production → **ief-global.org** |
| `develop` | Preview → **develop.ief-site.pages.dev** |

Manual deploy (needs a local `.env` with `CLOUDFLARE_*` creds, gitignored):
`./deploy.sh` (build + deploy) · `./deploy.sh --build` · `./deploy.sh --deploy`.

## Working rules — read before editing

- **Edit source in `html/`, never `dist/`.** `dist/` is generated and wiped on every build.
- **Bilingual parity:** content lives in BOTH `en/` and `ta/`. When you add/change a
  page, photo, video, or nav/footer item, update the Tamil side too. Tamil captions
  must be real Tamil, not English placeholders.
- **Shared chrome (nav, footer, donate modal)** is in `html/parts/` — edit once there,
  it propagates to every page on the next build.
- **Photos/videos** are JS arrays (`photoItems` / `videoItems`) inside the gallery and
  index pages — update the array entries in both languages (see README "Adding Content").
- **Don't hand-edit `wrangler.toml` project/output fields in the Cloudflare dashboard** —
  this file is the source of truth (`name = ief-site`, output `./dist`).
- **Always build before previewing/deploying** — raw `<!--#include-->` directives are not
  rendered by a plain browser; you'll see broken pages if you skip the compile step.

## Branches

`develop` is the active working branch (deploys to the preview URL). Merge to `main`
for production. The README mentions a `dev` branch — the real integration branch is
`develop`.

## Secrets & ignored files

`.env`, `.dev.vars`, `ts-state/`, `dist/`, and Cowork scratch files
(`IEF-HANDOFF.md`, `PROJECT-*.md`) are gitignored. Never commit Cloudflare/Tailscale
credentials.
