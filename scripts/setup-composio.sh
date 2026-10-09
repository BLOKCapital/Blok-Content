#!/usr/bin/env bash
# Install the Composio CLI (idempotent) and, if already logged in, install its Claude Code skill.
# Usage: bash scripts/setup-composio.sh
# Login is a separate, interactive step: `composio login` (or `composio login --agent` headless).
set -u

export PATH="$HOME/.local/bin:$HOME/.composio/bin:$PATH"

if ! command -v composio >/dev/null 2>&1; then
  echo "Installing Composio CLI..."
  if ! curl -fsSL https://composio.dev/install | sh; then
    cat >&2 <<'MSG'
Composio CLI install failed.
In Claude Code cloud sessions this is usually the network policy: the installer downloads
from github.com / api.github.com (release assets), which must be on the environment's
allowed domains. See docs/composio.md.
MSG
    exit 0   # never block the session
  fi
fi

composio --version 2>/dev/null || true

if composio whoami >/dev/null 2>&1; then
  composio setup skill claude --yes >/dev/null 2>&1 || true
  echo "Composio: logged in and Claude skill installed."
else
  echo "Composio: CLI installed but not logged in. Run 'composio login' (interactive) or 'composio login --agent'."
fi
