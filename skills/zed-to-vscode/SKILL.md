---
name: zed-to-vscode
description: "Use when styling Zed like VS Code on Linux."
version: 0.1.0
author: Naufalinux, Hermes Agent
license: GPL-3.0-or-later
platforms: [linux]
metadata:
  hermes:
    tags: [zed, vscode, editor, themes, icons, layout]
---

# Zed to VS Code

Copyright (c) 2026 Naufalinux. Original skill/source/documentation: GPL-3.0-or-later. See `references/LICENSE.txt`. External extensions retain upstream terms; the Dark Plus port's license is unresolved. The GPL label does not clear or relicense external assets.

Configure a VS Code-like Zed layout using file edits and theme-only extensions. Do not automate the desktop, launch Zed, or restart any session or service.

## When to Use

- Set up Zed like VS Code, including dark theme, file icons, word wrap, and branch/worktree indicators.
- Reapply or share a reproducible Linux editor setup.
- Do not use for installing Zed itself, Git recovery, or importing credentials.

## Documentation

Read `references/GUIDE.md` for the Indonesian step-by-step script guide, ZIP/TAR import, Git clone installation, sharing, rollback, and troubleshooting. The guide distinguishes local skill archives from Hermes snapshot JSON and does not assume a public Git repository already exists.

## Prerequisites

- Zed already installed; Python 3.12+ and curl available.
- Network access to https://api.zed.dev for first-time extension downloads.
- Resolve this skill directory from the path returned by `skill_view`; never hardcode a user's home.
- Prefer having the user close Zed manually before applying settings to avoid concurrent edits.

## Procedure

1. Use `terminal` to check `python3 --version`, `curl --version`, and `zed --version` when available. Read the bundled script with `read_file` before execution.
2. Use `terminal` to preview: `python3 <skill-dir>/scripts/zed-to-vscode.py --dry-run`. This performs no writes or downloads and prints only planned values, not existing secrets.
3. After the user has requested setup, use `terminal` to apply: `python3 <skill-dir>/scripts/zed-to-vscode.py`. Allow up to 300 seconds for network downloads. Capture the output and exact backup path.
4. The script validates installed extension versions, safely downloads/extracts missing themes, merges nested settings, backs up the original settings with restricted permissions, writes atomically, and reads the result back. A nonzero exit is not success; inspect the error before retrying.
5. Report what was verified and ask the user to reopen Zed manually if necessary. Do not claim visual verification from file checks alone.

## Configuration

The script installs pinned theme-only extensions `vscode-dark-plus` 0.0.1 and `vscode-icons` 13.0.0. It selects `VScode Dark Plus` and `VSCode Icons for Zed (Dark)`.

It enables VSCode keybindings; left Explorer/Git/Outline; bottom terminal/agent; tabs with icons; breadcrumbs; minimap; line numbers; indent guides; and `soft_wrap: editor_width`. UI font size is 13 and editor font size is 14. Existing font families, unrelated configuration, credentials, and agent permissions remain unchanged. JSONC comments are removed when settings are rewritten, but the original file is backed up exactly.

The `title_bar` settings explicitly enable `show_branch_name`, `show_branch_status_icon`, `show_worktree_name`, and `show_project_items`. Git indicators are at the top in Zed, not at VS Code's bottom-left position.

Defaults respect `XDG_CONFIG_HOME` and `XDG_DATA_HOME`. Override safely with `--config-dir PATH --data-dir PATH`. Existing extensions at another version cause refusal, not an automatic downgrade.

## Pitfalls and Safety

- Do not use CUA, synthetic input, or GUI captures for this workflow. Plasma X11 session crashes have coincided with CUA pointer hotplug; never reproduce that on a user's live desktop.
- Branch indicators require an actual Git repository. Use `terminal` with `git -C <project> status --short --branch` to diagnose. Missing `.git` is not repaired by creating a fresh repository; do not run `git init` without explicit authorization.
- Layout is similar, not pixel-identical. Native Zed panel controls differ from VS Code's activity bar.
- Language/project overrides or workspace state can override global preferences. Investigate those separately rather than resetting them blindly.
- Never export personal Zed settings, backups, API keys, logs, memories, or sessions with this skill. Export only this directory's reusable files.
- If downloading via Python encounters HTTP 403, use the bundled curl-based path; do not fabricate successful installation.

## Verification and Rollback

- Run `python3 <skill-dir>/scripts/test_setup.py` through `terminal` for isolated offline tests. Tests must not touch the real editor configuration.
- Confirm script output verifies extension manifests and merged settings. GUI recognition after restart remains a separate user-visible check.
- Backups are named `settings.json.before-vscode-<timestamp>.bak` beside settings.json. To roll back, have the user close Zed, then restore the exact reported backup over settings.json; do not choose an arbitrary older backup.
- Re-running identical settings is idempotent: no settings rewrite or extra backup.
