#!/usr/bin/env bash
# =============================================================================
# deploy.sh — IEF Website Build & Deploy Script
# Location: ~/docker/ief-dev/deploy.sh
#
# Usage:
#   ./deploy.sh            → full build + deploy (default)
#   ./deploy.sh --build    → build only (no deploy)
#   ./deploy.sh --deploy   → deploy only (skip rebuild)
#
# Requires: python3, wrangler (npx), .env file with Cloudflare credentials
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPILE_SCRIPT="$SCRIPT_DIR/html/compile_site.py"
DIST_DIR="$SCRIPT_DIR/dist"
ENV_FILE="$SCRIPT_DIR/.env"

# ── Load Cloudflare credentials from .env ──────────────────────────────────
if [[ -f "$ENV_FILE" ]]; then
    # Export only CLOUDFLARE_* and WRANGLER_* vars, ignore comments and blanks
    set -a
    # shellcheck source=/dev/null
    source <(grep -E '^(CLOUDFLARE_|WRANGLER_)' "$ENV_FILE")
    set +a
else
    echo "⚠️  Warning: .env file not found at $ENV_FILE"
    echo "   Wrangler will fall back to system-level auth (wrangler login)."
fi

# ── Parse arguments ────────────────────────────────────────────────────────
DO_BUILD=true
DO_DEPLOY=true

if [[ "${1:-}" == "--build" ]]; then
    DO_DEPLOY=false
elif [[ "${1:-}" == "--deploy" ]]; then
    DO_BUILD=false
fi

# ── Build ──────────────────────────────────────────────────────────────────
if [[ "$DO_BUILD" == true ]]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🔨 BUILD"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python3 "$COMPILE_SCRIPT"
fi

# ── Deploy ─────────────────────────────────────────────────────────────────
if [[ "$DO_DEPLOY" == true ]]; then
    if [[ ! -d "$DIST_DIR" ]]; then
        echo ""
        echo "❌ ERROR: dist/ not found at $DIST_DIR"
        echo "   Run './deploy.sh --build' first."
        exit 1
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🚀 DEPLOY → Cloudflare Pages"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    npx wrangler pages deploy "$DIST_DIR" \
        --project-name=ief-site \
        --commit-dirty=true

    echo ""
    echo "✅ Deployed! Check https://ief-global.org"
fi

