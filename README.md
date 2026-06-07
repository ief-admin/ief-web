# IEF Global — Website

Official website for the **International Educational Foundation (IEF)**, a 501(c)(3) nonprofit organization dedicated to empowering K–12 students through native-language education.

🌐 **Live site:** [https://ief-global.org](https://ief-global.org)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Markup | HTML5 with SSI-style includes (compiled) |
| Styling | [Tailwind CSS](https://tailwindcss.com/) (CDN) |
| Interactivity | [Alpine.js](https://alpinejs.dev/) (CDN) |
| Tamil Font | [IBM Plex Sans Tamil](https://fonts.google.com/specimen/IBM+Plex+Sans+Tamil) (Google Fonts) |
| Build | Python compile script (`compile_site.py`) |
| Hosting | [Cloudflare Pages](https://pages.cloudflare.com/) |
| DNS | Cloudflare |

---

## Repository Structure

```
ief-web/
├── assets/                  # Static assets (images, logos, QR codes)
│   ├── logo.webp
│   ├── hero-bg.webp
│   ├── picture-00.webp      # Community photos (picture-00 through picture-11)
│   ├── ...
│   ├── headshot-sm.webp     # Board member headshots
│   └── zelle-qr.webp        # Donation QR code
│
├── parts/                   # Shared HTML components (SSI includes)
│   ├── nav-en.html          # English navigation bar
│   ├── nav-ta.html          # Tamil navigation bar
│   ├── donate-modal.html    # Donation modal (Stripe + Zelle)
│   └── footer.html          # Site-wide footer
│
├── en/                      # English pages
│   ├── index.html
│   └── gallery.html
│
├── ta/                      # Tamil pages
│   ├── index.html
│   └── gallery.html
│
├── compile_site.py               # SSI include compiler / build script
├── wrangler.toml            # Cloudflare Wrangler configuration
├── .gitignore
├── LICENSE
└── README.md
```

---

## Languages & Localization

The site is fully bilingual. Every page exists in two versions:

| Path | Language |
|---|---|
| `/en/` | English |
| `/ta/` | Tamil (தமிழ்) |

- Shared components (nav, footer, donate modal) live in `/parts/` and are compiled into each page at build time.
- The donate modal uses Alpine.js `lang` state (`'en'` or `'ta'`) to switch label text dynamically at runtime.
- The Tamil version uses the **IBM Plex Sans Tamil** font for correct rendering.

---

## Local Development

### Prerequisites

- Python 3.x
- A local web server that supports static files (e.g. VS Code Live Server, `python -m http.server`, or similar)

### Setup

```bash
# Clone the repo
git clone https://github.com/ief-admin/ief-web.git
cd ief-web

# Run the SSI compile step to resolve <!--#include virtual="..."--> directives
python compile_site.py

# Serve the output locally
python -m http.server 8080
# Then open http://localhost:8080/en/ in your browser
```

> **Note:** The raw source files use `<!--#include virtual="...">` directives for shared components. These are **not** processed by browsers directly — always run `compile_site.py` first to produce the final HTML before previewing or deploying.

---

## Build & Deployment

The site is deployed via **Cloudflare Pages**, connected directly to this GitHub repository.

| Setting | Value |
|---|---|
| Build command | `python compile_site.py` |
| Output directory | `dist/` *(or as configured in compile_site.py)* |
| Production branch | `main` |
| Node version | N/A (Python only) |

Every push to `main` triggers an automatic build and deployment on Cloudflare Pages. Pull requests generate isolated preview deployments with a unique URL for review before merging.

### Manual deploy (Wrangler CLI)

```bash
# Install Wrangler if not already installed
npm install -g wrangler

# Authenticate
wrangler login

# Deploy
wrangler pages deploy dist/
```

---

## Adding Content

### Adding a new photo

1. Convert your image to `.webp` format (use [Squoosh](https://squoosh.app/) or `cwebp` CLI for best results).
2. Name it sequentially: `picture-12.webp`, `picture-13.webp`, etc.
3. Place it in `/assets/`.
4. Add an entry to the `photoItems` array in **both** `en/gallery.html` and `ta/gallery.html`:

```js
// en/gallery.html
{ url: '/assets/picture-12.webp', title: 'Your English Caption' }

// ta/gallery.html
{ url: '/assets/picture-12.webp', title: 'உங்கள் தமிழ் தலைப்பு' }
```

5. If the photo should also appear on the home page, add it to `photoItems` in `en/index.html` and `ta/index.html` as well.

### Adding a new video

1. Upload the video to the [IEF YouTube channel](https://www.youtube.com/) and copy its video ID (the part after `?v=` in the URL).
2. Add an entry to `videoItems` in **both** the gallery files and the home page files:

```js
// en/gallery.html & en/index.html
{ type: 'video', url: 'YOUR_VIDEO_ID', title: 'Your English Title' }

// ta/gallery.html & ta/index.html
{ type: 'video', url: 'YOUR_VIDEO_ID', title: 'உங்கள் தமிழ் தலைப்பு' }
```

---

## Collaboration

Contributors are managed via GitHub repository access. Contact the repository admin to request access.

| Role | Permission level |
|---|---|
| Core developer | `Maintain` |
| Contributor | `Write` |
| Read-only reviewer | `Read` |

### Branching convention

```
main          ← production (auto-deploys to ief-global.org)
dev           ← integration branch for ongoing work
feature/<name> ← individual feature branches
fix/<name>    ← bug fix branches
```

Always open a **Pull Request** into `main` and get at least one review before merging.

---

## Organization Details

| Field | Value |
|---|---|
| Legal Name | International Educational Foundation, Inc. |
| Tax Status | 501(c)(3) Non-Profit, Tax-Exempt |
| EIN | 32-0103781 |
| General Contact | info@ief-global.org |
| Website Admin | admin@ief-global.org |

---

## License

This codebase is proprietary and maintained by the International Educational Foundation, Inc. All rights reserved. Content, images, and branding may not be reproduced without written permission.
