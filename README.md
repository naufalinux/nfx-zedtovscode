# nfx-zedtovscode

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

Script dan skill Hermes untuk menata Zed di Linux agar menyerupai VS Code—tanpa GUI automation atau restart desktop.

## Prasyarat

- Zed sudah terpasang.
- Python 3.12+, curl, dan internet untuk download awal extensions.
- Hermes hanya diperlukan jika menggunakan skill; script dapat dipakai mandiri.

## Quick start

```bash
git clone https://github.com/naufalinux/nfx-zedtovscode.git
cd nfx-zedtovscode
python3 zed-to-vscode.py --dry-run
python3 skills/zed-to-vscode/scripts/test_setup.py
# Tutup Zed secara manual, lalu terapkan:
python3 zed-to-vscode.py
```

Buka Zed kembali secara manual. Script membackup settings existing sebelum mengubahnya, mempertahankan key lain, dan memverifikasi hasil penulisan.

## Pengaturan

- VScode Dark Plus dan VSCode Icons varian Dark.
- Preset shortcut VSCode.
- Explorer/Git/Outline di kiri; terminal/agent di bawah.
- Indikator branch/worktree di title bar atas, membutuhkan repo Git valid.
- Word wrap mengikuti lebar editor, minimap, breadcrumbs, ikon tab, nomor baris, dan indent guides.
- Font UI 13 dan editor/terminal 14; font family existing dipertahankan.

Bukan pixel-perfect VS Code. Pengaturan target ditimpa sesuai preset; key unrelated dipertahankan. Komentar JSONC hilang saat rewrite, tetapi backup asli utuh. Script tidak melakukan `git init`, fetch/pull, membuka editor, atau restart layanan.

## Install skill Hermes dari clone ini

Jalankan dari root repo. Pastikan direktori tujuan belum ada; jangan mencampur versi.

```bash
SKILL_PARENT="${HERMES_HOME:-$HOME/.hermes}/skills/software-development"
mkdir -p "$SKILL_PARENT"
if [ -e "$SKILL_PARENT/zed-to-vscode" ]; then
  printf 'Skill sudah ada. Backup dan bandingkan versi sebelum upgrade.\n'
else
  cp -R skills/zed-to-vscode "$SKILL_PARENT/zed-to-vscode"
fi
```

Pastikan `HERMES_HOME` menunjuk profil yang benar. Mulai sesi Hermes baru, lalu minta:

> Pakai skill zed-to-vscode. Preview dulu, lalu setup Zed tanpa GUI automation atau restart desktop.

Alternatif installer Hermes untuk sumber GitHub yang didukung:

```bash
hermes skills install naufalinux/nfx-zedtovscode/skills/zed-to-vscode
```

Periksa `hermes skills install --help` sesuai versi Hermes dan pastikan supporting files ikut terpasang. Jangan melewati warning installer secara buta.

## Struktur

```text
README.md
GUIDE.md
LICENSE
zed-to-vscode.py
skills/zed-to-vscode/
  SKILL.md
  scripts/zed-to-vscode.py
  scripts/test_setup.py
  references/GUIDE.md
  references/SHARING.txt
  references/LICENSE.txt
```

Script root dan script dalam skill merupakan salinan identik; saat mengubah implementasi, sinkronkan keduanya. GUIDE root dan panduan dalam skill juga harus tetap sinkron.

## Dokumentasi dan troubleshooting

Baca [GUIDE.md](GUIDE.md) untuk langkah lengkap, import ZIP/TAR, clone, snapshot Hermes, custom path, rollback, dan troubleshooting.

Catatan untuk contoh repo di GUIDE: repo publik proyek ini adalah `https://github.com/naufalinux/nfx-zedtovscode.git`, dengan skill berada di `skills/zed-to-vscode/`, bukan root repo. Gunakan metode multi-skill/copy pada GUIDE atau instruksi README ini.

## Pengujian

```bash
python3 skills/zed-to-vscode/scripts/test_setup.py
```

Tes offline memakai direktori terisolasi dan fixture extension, bukan settings pengguna. Tes tidak membuktikan render GUI atau koneksi download. Setup dasar juga telah diuji dengan download extension sungguhan di direktori terisolasi.

## Keamanan dan lisensi

Tidak menyertakan credentials, konfigurasi pribadi Zed/Hermes, session, logs, atau backup settings. Jangan commit file tersebut saat berkontribusi.

Source, skill, tes, dan dokumentasi original revisi ini: **GPL-3.0-or-later**. Lihat [LICENSE](LICENSE), [LICENSING.md](LICENSING.md), dan [LICENSE-AUDIT.md](LICENSE-AUDIT.md). Grant MIT revisi awal tetap berlaku bagi salinan/revisi lama; komponen pihak ketiga tidak ikut direlisensikan.

**Temuan terbuka:** lisensi port `vscode-dark-plus` 0.0.1 belum terkonfirmasi. Installer masih mengunduhnya terpisah; jangan membundel atau menyatakan extension tersebut sudah license-cleared. VSCode Icons memiliki notice MIT upstream, tetapi artwork/trademark individual belum diaudit menyeluruh.
