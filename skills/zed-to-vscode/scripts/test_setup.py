#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Naufalinux
"""Offline tests: run only in isolated temporary directories."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('zed-to-vscode.py')
spec = importlib.util.spec_from_file_location('zed_setup', SCRIPT)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)

class SetupTests(unittest.TestCase):
    def test_jsonc(self):
        self.assertEqual(setup.parse_jsonc('{"url":"https://example.org/a,}",// comment\n"a":[1,],}'), {'url':'https://example.org/a,}', 'a':[1]})

    def test_setup_and_rerun(self):
        root = Path(os.environ.get('TMPDIR', str(Path.home()/'.cache/zed-to-vscode-tests')))
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as temp:
            base = Path(temp)
            config = base/'config'
            config.mkdir()
            p = config/'settings.json'
            original = '// original\n{"agent":{"enabled":false},"keep":true,}\n'
            p.write_text(original)
            installed = base/'data/extensions/installed'
            for extension_id, version in setup.EXTENSIONS:
                folder = installed/extension_id
                folder.mkdir(parents=True)
                if extension_id == 'vscode-dark-plus':
                    (folder/'extension.json').write_text(json.dumps({'version':version}))
                    theme_path = folder/'themes/vscode_dark_plus.json'
                    name = 'VScode Dark Plus'
                else:
                    (folder/'extension.toml').write_text(f'id = "{extension_id}"\nversion = "{version}"\n')
                    theme_path = folder/'icon_themes/vsicons-icon-theme-zed.json'
                    name = 'VSCode Icons for Zed (Dark)'
                theme_path.parent.mkdir()
                theme_path.write_text(json.dumps({'themes':[{'name':name}]}))
            command = ['python3', str(SCRIPT), '--config-dir', str(config), '--data-dir', str(base/'data')]
            subprocess.run(command+['--dry-run'], check=True, capture_output=True)
            self.assertEqual(p.read_text(), original)
            self.assertEqual(list(config.glob('*.bak')), [])
            subprocess.run(command, check=True, capture_output=True)
            actual = setup.parse_jsonc(p.read_text())
            self.assertTrue(actual['keep'])
            self.assertFalse(actual['agent']['enabled'])
            self.assertEqual(actual['soft_wrap'], 'editor_width')
            self.assertEqual(actual['ui_font_size'], 12)
            self.assertEqual(actual['buffer_font_size'], 12)
            self.assertEqual(actual['terminal']['font_size'], 12)
            self.assertTrue(actual['title_bar']['show_branch_name'])
            backups = list(config.glob('*.bak'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), original)
            self.assertEqual(backups[0].stat().st_mode & 0o777, 0o600)
            before = p.read_bytes()
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(p.read_bytes(), before)
            self.assertEqual(len(list(config.glob('*.bak'))), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
