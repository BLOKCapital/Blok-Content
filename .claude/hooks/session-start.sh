#!/usr/bin/env bash
# Prepare a fresh session: render tooling + Composio CLI. Never fails the session.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
[ -d node_modules/playwright ] || npm install --no-audit --no-fund --silent >/dev/null 2>&1 || true
bash scripts/setup-composio.sh 2>&1 | tail -3 || true
exit 0
