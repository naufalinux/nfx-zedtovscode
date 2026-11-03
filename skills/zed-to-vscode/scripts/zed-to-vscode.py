#!/usr/bin/env python3
"""Configure Zed with a VS Code-like layout without GUI automation.

Usage: python3 zed-to-vscode.py [--config-dir PATH] [--data-dir PATH] [--dry-run]
Requires Python 3.12+ and curl. Downloads theme-only extensions from api.zed.dev.
No editor launch, service restart, git init, or desktop interaction.
"""
import argparse
import copy
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import tarfile
import tempfile
import tomllib
import subprocess

EXTENSIONS = (("vscode-dark-plus", "0.0.1"), ("vscode-icons", "13.0.0"))
UPDATES = {
    "base_keymap": "VSCode",
    "theme": {"mode": "dark", "dark": "VScode Dark Plus"},
    "icon_theme": "VSCode Icons for Zed (Dark)",
    "ui_font_size": 13,
    "buffer_font_size": 14,
    "buffer_line_height": {"custom": 1.35},
    "soft_wrap": "editor_width",
    "project_panel": {"dock": "left", "default_width": 260, "starts_open": True,
                      "entry_spacing": "standard", "file_icons": True, "git_status": True},
    "outline_panel": {"dock": "left"},
    "git_panel": {"dock": "left", "default_width": 300, "button": True},
    "terminal": {"dock": "bottom", "default_height": 260, "font_size": 14},
    "agent": {"dock": "bottom", "default_height": 320},
    "bottom_dock_layout": "contained",
    "tab_bar": {"show": True, "show_nav_history_buttons": False},
    "tabs": {"file_icons": True, "git_status": True, "close_position": "right",
             "show_close_button": "hover"},
    "toolbar": {"breadcrumbs": True},
    "title_bar": {"show_menus": True, "show_onboarding_banner": False,
                  "show_branch_name": True, "show_branch_status_icon": True,
                  "show_worktree_name": True, "show_project_items": True},
    "status_bar": {"line_endings_button": True, "active_encoding_button": "enabled"},
    "minimap": {"show": "always"},
    "gutter": {"line_numbers": True, "folds": True},
    "indent_guides": {"enabled": True},
    "preview_tabs": {"enabled": True},
}

def parse_jsonc(text):
    # Strip comments and trailing commas only outside quoted strings.
    token = r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/'
    text = re.sub(token, lambda m: "" if m[0].startswith(("//", "/*")) else m[0], text)
    text = re.sub(r'"(?:\\.|[^"\\])*"|,(\s*[}\]])',
                  lambda m: m[1] if m[1] is not None else m[0], text)
    result = json.loads(text)
    if not isinstance(result, dict):
        raise ValueError("settings.json must contain an object")
    return result


def merge(target, updates):
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            merge(target[key], value)
        else:
            target[key] = copy.deepcopy(value)
    return target


def validate_extension(folder, extension_id, version):
    if (folder / "extension.toml").exists():
        meta = tomllib.loads((folder / "extension.toml").read_text())
        if meta.get("id") != extension_id:
            raise ValueError("Extension ID mismatch")
    else:
        meta = json.loads((folder / "extension.json").read_text())
    if meta.get("version") != version:
        raise ValueError(f"Unexpected installed version for {extension_id}; refusing overwrite")
    if extension_id == "vscode-dark-plus":
        theme = json.loads((folder / "themes/vscode_dark_plus.json").read_text())
        assert any(t["name"] == "VScode Dark Plus" for t in theme["themes"])
    else:
        theme = json.loads((folder / "icon_themes/vsicons-icon-theme-zed.json").read_text())
        assert any(t["name"] == "VSCode Icons for Zed (Dark)" for t in theme["themes"])


def install_extension(root, extension_id, version, scratch):
    dest = root / "installed" / extension_id
    if dest.exists():
        validate_extension(dest, extension_id, version)
        print(f"Verified installed: {extension_id} {version}")
        return
    with tempfile.TemporaryDirectory(prefix="zed-vscode-", dir=scratch) as temp:
        temp = Path(temp)
        archive = temp / "extension.tar.gz"
        url = f"https://api.zed.dev/extensions/{extension_id}/{version}/download"
        subprocess.run(["curl", "--fail", "--location", "--silent", "--show-error",
                        "--retry", "2", "--connect-timeout", "15", "--max-time", "90",
                        "--proto", "=https", "--proto-redir", "=https",
                        "--output", str(archive), url], check=True)
        stage = temp / "unpacked"
        stage.mkdir()
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            if sum(m.size for m in members) > 150 * 1024 * 1024:
                raise ValueError("Extension archive exceeds extraction size limit")
            for member in members:
                if not (member.isfile() or member.isdir()):
                    raise ValueError("Links and special archive files are not allowed")
                resolved = (stage / member.name).resolve()
                if not resolved.is_relative_to(stage.resolve()):
                    raise ValueError("Unsafe archive path")
            tar.extractall(stage, filter="data")
        validate_extension(stage, extension_id, version)
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Keep staging on target filesystem so publishing uses an atomic rename.
        staged = Path(tempfile.mkdtemp(prefix=f".{extension_id}-", dir=dest.parent))
        try:
            shutil.copytree(stage, staged, dirs_exist_ok=True)
            staged.rename(dest)
        finally:
            if staged.exists():
                shutil.rmtree(staged)
        validate_extension(dest, extension_id, version)
        print(f"Installed and verified: {extension_id} {version}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home()/".config")))/"zed")
    parser.add_argument("--data-dir", type=Path, default=Path(os.environ.get("XDG_DATA_HOME", str(Path.home()/".local/share")))/"zed")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes without writing or downloading")
    args = parser.parse_args()
    settings_path = args.config_dir / "settings.json"
    original = settings_path.read_bytes() if settings_path.exists() else None
    settings = parse_jsonc(original.decode()) if original is not None else {}
    desired = merge(copy.deepcopy(settings), UPDATES)
    if args.dry_run:
        print("Settings:", settings_path)
        print("Extensions:", args.data_dir / "extensions/installed")
        print("Planned settings (existing credentials are not printed):")
        print(json.dumps(UPDATES, indent=2))
        print("No changes made.")
        return
    scratch = Path(os.environ.get("TMPDIR", str(Path.home()/".cache/zed-to-vscode")))
    scratch.mkdir(parents=True, exist_ok=True)
    for extension_id, version in EXTENSIONS:
        install_extension(args.data_dir / "extensions", extension_id, version, scratch)
    # Refuse to overwrite settings edited concurrently by the user or Zed.
    current = settings_path.read_bytes() if settings_path.exists() else None
    if current != original:
        raise RuntimeError("Settings changed during setup. Rerun to merge the latest settings.")
    backup = None
    if desired != settings:
        args.config_dir.mkdir(parents=True, exist_ok=True)
        if original is not None:
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            backup = settings_path.with_name(f"settings.json.before-vscode-{stamp}.bak")
            backup.write_bytes(original)
            backup.chmod(0o600)
        content = "// Zed: VS Code-like layout (existing settings preserved)\n" + json.dumps(desired, indent=2) + "\n"
        fd, filename = tempfile.mkstemp(prefix=".settings-", dir=args.config_dir)
        try:
            with os.fdopen(fd, "w") as out:
                out.write(content)
                out.flush()
                os.fsync(out.fileno())
            os.replace(filename, settings_path)
        finally:
            if Path(filename).exists():
                Path(filename).unlink()
    assert parse_jsonc(settings_path.read_text()) == desired
    print("Settings verified:", settings_path)
    if backup:
        print("Backup:", backup)
        print("Restore: copy this backup over settings.json with Zed closed.")
    else:
        print("Settings already match; no rewrite needed.")
    print("No GUI input, editor launch, service restart, or Git changes performed.")
    print("Open/reopen Zed manually to load extensions. Branch indicators require a Git repository.")

if __name__ == "__main__":
    main()
