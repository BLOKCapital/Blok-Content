# Composio setup

Composio connects Claude to the apps we publish and work in: Instagram, X, LinkedIn,
YouTube, TikTok, Telegram, Discord, Google Drive, Notion, Slack, and more.

## 1. Install the CLI
```bash
curl -fsSL https://composio.dev/install | sh     # or: bash scripts/setup-composio.sh
composio --version
```
The installer downloads release assets from GitHub, so the machine needs access to
`github.com`, `api.github.com` and `*.githubusercontent.com`, plus `composio.dev` /
`backend.composio.dev`.

**Claude Code cloud sessions:** add those domains under the environment's
**Network access → Allowed domains** (cloud environment menu → Edit).
Docs: https://code.claude.com/docs/en/cloud-environments#network-access

## 2. Log in
```bash
composio login            # interactive, opens a browser
composio login --agent    # headless / unattended agent account, no browser
```
`composio login` also installs the `composio-cli` skill for Claude Code. Manual:
`composio setup skill claude` or `composio setup --target claude`.

## 3. Connect accounts
```bash
composio dev toolkits search "instagram"
composio link instagram     # Instagram Business/Creator account linked to a FB Page
composio link twitter
composio link linkedin
composio link youtube
composio link googledrive
```

## 4. Find and run tools
```bash
composio search "publish an instagram carousel"
composio execute <TOOL_SLUG> --get-schema
composio execute <TOOL_SLUG> -d '{ ... }'
```

## House rules
- Never publish without explicit approval of the exact post (see `.claude/skills/composio-publish`).
- Log every published post in `content/calendar/published.md`.
- Instagram publishing needs public media URLs: upload exports to Drive/S3/CDN first.
