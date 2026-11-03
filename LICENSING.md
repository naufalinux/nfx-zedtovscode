<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Licensing policy

Copyright (c) 2026 Naufalinux.

Except for separately identified third-party license texts and the historical MIT grant, original source code, tests, Hermes skill instructions, and documentation in this revision are licensed under **GNU General Public License version 3 or, at your option, any later version** (`GPL-3.0-or-later`). See `LICENSE` for GPL v3 and `LICENSE-AUDIT.md` for scope and findings.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for details.

## Scope

- `zed-to-vscode.py`, `skills/zed-to-vscode/scripts/*.py`, project Markdown, skill metadata, and original sharing instructions: GPL-3.0-or-later.
- `.gitignore` and other original project configuration: GPL-3.0-or-later where copyright applies.
- `LICENSE` and `skills/zed-to-vscode/references/LICENSE.txt`: unmodified GPL v3 license document; its own verbatim-copy conditions apply. The “or later” choice is established by the source notices and this policy.
- `LICENSES/Legacy-MIT.txt`: original MIT grant for the prior revision, retained as legal history, not the default license for new material.
- `LICENSES/VSCode-Icons-MIT.txt`, `LICENSES/VSCode-Icons-Base-MIT.txt`, `LICENSES/Dark-Plus-Ancestor-MIT.txt`: verbatim third-party MIT notices used as audit evidence. These documents do not license the original project under MIT and do not establish permission for an unlicensed port.

Third-party software is **not relicensed** by this repository. Python, curl, Zed, Hermes, Git, downloaded themes/icons, and their dependencies retain their upstream terms. They are not bundled as executable/library/assets in this source repository.

## Historical MIT grant

Commit `ca20d89` was supplied under MIT. Rights previously granted under MIT are not revoked by this change. A recipient may continue using the old revision under its MIT terms. New changes are offered under GPL-3.0-or-later; this is not a retroactive removal of permissions already granted.

## Open licensing issue

The `vscode-dark-plus` 0.0.1 port has no confirmed license grant in the audited upstream snapshot/archive. Its referenced ancestor has MIT terms, but that alone does not establish rights over the port's contributions. The current installer still downloads this separately. Do not redistribute that extension as GPL or advertise the whole dependency chain as license-cleared. Resolve permission or replace the component before bundling or claiming complete clearance.

Project-level MIT notices were found for VSCode Icons, but individual artwork/trademark provenance was not exhaustively verified. Re-distribution of downloaded extension assets requires its own review and notices.

## Contributions

Submit original contributions under GPL-3.0-or-later unless an explicit, separately reviewed license statement says otherwise. Preserve third-party attribution and do not introduce code/assets without adequate permission. Re-audit whenever extensions or dependency distribution changes.
