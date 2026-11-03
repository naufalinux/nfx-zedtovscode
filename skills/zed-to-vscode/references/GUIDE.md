# Zed to VS Code — Dokumentasi dan Panduan

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

Copyright (c) 2026 Naufalinux. Source, skill, dan dokumentasi original revisi ini: GPL-3.0-or-later. Grant MIT revisi lama tetap diakui. Komponen eksternal tidak ikut direlisensikan. Lisensi port Dark Plus 0.0.1 belum terkonfirmasi; jangan membundel assets atau menganggap seluruh dependency chain telah clear. Lihat `LICENSING.md` dan `LICENSE-AUDIT.md` di root repository untuk temuan, cakupan, dan notices.

Skill/script versi 0.1.0 • Linux • Bahasa Indonesia

Panduan ini menjelaskan pemakaian script mandiri, pemasangan skill Hermes dari ZIP/TAR atau clone Git, verifikasi, rollback, dan troubleshooting. Script menata Zed agar menyerupai VS Code; bukan mengubah Zed menjadi VS Code atau menjamin tampilan identik.

## 1. Fitur dan batasan

| Area | Pengaturan |
|---|---|
| Color theme | `VScode Dark Plus`, extension `vscode-dark-plus` v0.0.1 |
| File icon theme | `VSCode Icons for Zed (Dark)`, extension `vscode-icons` v13.0.0 |
| Keybindings | Preset `VSCode` |
| Sidebar | Explorer, Git, Outline di kiri |
| Panel bawah | Terminal dan agent |
| Branch/worktree | Nama branch, ikon status branch, dan nama worktree di title bar |
| Word wrap | `soft_wrap: editor_width` untuk membungkus tampilan sesuai lebar editor |
| Navigasi | Ikon tab, breadcrumbs, minimap, nomor baris, indent guides |
| Ukuran font | UI 13, editor dan terminal 14 |

Yang tidak dilakukan:

- Tidak menginstal Zed atau Hermes.
- Tidak menyalin extensions VS Code selain dua tema khusus Zed di atas.
- Tidak mengubah repository Git, melakukan `git init`, fetch, atau pull.
- Tidak mengontrol mouse/keyboard, mengambil screenshot, membuka Zed, atau merestart desktop/layanan.
- Tidak mengubah pengaturan autosave atau font family; nilai yang sudah ada dipertahankan.
- Tidak menyalin credentials ke komputer lain. Nilai existing dalam settings lokal dipertahankan, termasuk permissions agent.

Pengaturan yang menjadi target script akan diganti sesuai tabel, sementara key lain digabung dan dipertahankan. Komentar JSONC akan hilang dari file hasil rewrite, tetapi file aslinya dibackup utuh.

## 2. Prasyarat

- Linux dengan Zed terpasang.
- Python 3.12 atau lebih baru.
- `curl`; `unzip` untuk ZIP atau `tar` untuk TAR.GZ; `git` hanya untuk metode clone.
- Internet ke `https://api.zed.dev` ketika extension belum terpasang.
- Akses tulis ke konfigurasi dan data Zed milik user sendiri. Jangan menjalankan setup memakai `sudo`.

Cek dari terminal:

```bash
python3 --version
curl --version
zed --version
hermes --version
```

`hermes` tidak diperlukan untuk pemakaian script mandiri. Pada sebagian instalasi, executable Zed dapat bernama lain; versi diperiksa melalui executable yang benar di sistem tersebut.

Tutup Zed secara manual sebelum menerapkan setup, lalu buka kembali secara manual setelah selesai. Tidak perlu logout atau restart Plasma.

## 3. Isi paket

```text
zed-to-vscode/
├── SKILL.md
├── scripts/
│   ├── zed-to-vscode.py
│   └── test_setup.py
└── references/
    ├── GUIDE.md
    ├── SHARING.txt
    └── LICENSE.txt
```

File distribusi:

- `zed-to-vscode-0.1.0.zip`: paket yang paling mudah dibagikan.
- `zed-to-vscode-0.1.0.tar.gz`: alternatif arsip.
- `zed-to-vscode-0.1.0.SHA256SUMS`: checksum kedua arsip.
- `ZED-TO-VSCODE-GUIDE.md`: panduan mandiri ini, juga disertakan sebagai `references/GUIDE.md` dalam paket.

Paket hanya berisi instruksi dan source code reusable. Theme/icon assets diunduh saat setup dan tetap mengikuti lisensi upstream.

## 4. Periksa paket sebelum menjalankan

Simpan checksum dan kedua arsip dalam direktori yang sama:

```bash
sha256sum -c zed-to-vscode-0.1.0.SHA256SUMS
```

Jika hanya mengunduh ZIP, verifikasi arsip itu saja:

```bash
sha256sum zed-to-vscode-0.1.0.zip
```

Bandingkan dengan baris ZIP dalam file checksum. Checksum mendeteksi perubahan file, bukan menjamin keaslian penerbit jika checksum berasal dari pihak yang sama-sama tidak dipercaya.

Lihat isi arsip:

```bash
unzip -l zed-to-vscode-0.1.0.zip
```

Baca `SKILL.md` dan script setelah ekstraksi. Jangan menjalankan paket yang menyertakan credentials, konfigurasi pribadi, path arsip yang keluar dari direktori skill, atau source code yang tidak kamu percaya.

## 5. Menjalankan script tanpa Hermes

### Langkah 1 — Ekstrak

Jalankan di direktori tempat ZIP disimpan. Jika folder `zed-to-vscode` sudah ada, pilih direktori kosong lain agar tidak mencampur versi.

```bash
unzip -n zed-to-vscode-0.1.0.zip
cd zed-to-vscode
```

### Langkah 2 — Preview tanpa perubahan

```bash
python3 scripts/zed-to-vscode.py --dry-run
```

Dry-run menunjukkan lokasi target dan nilai yang direncanakan. Tidak mengunduh extension, menulis settings, atau mencetak credentials existing. Dry-run bukan tes jaringan maupun validasi pengenalan tema oleh Zed.

### Langkah 3 — Jalankan tes offline

```bash
python3 scripts/test_setup.py
```

Tes memakai direktori sementara dan manifest fixture, bukan konfigurasi editor asli. Tes memeriksa parsing JSONC, preservation key existing, dry-run, backup, dan idempotensi. Hasil sukses ditandai exit code 0 dan ringkasan `OK`.

### Langkah 4 — Terapkan

Dengan Zed sudah ditutup manual:

```bash
python3 scripts/zed-to-vscode.py
```

Script akan:

1. Membaca settings existing dan menggabungkan pengaturan target.
2. Memvalidasi extension yang sudah ada atau mengunduh paket versi yang dipatok.
3. Menolak archive path tidak aman, link/special file, dan ukuran ekstraksi berlebihan.
4. Menolak menimpa settings yang berubah selama proses setup.
5. Membackup settings asli sebelum perubahan, jika file existing dan nilainya perlu berubah.
6. Menulis settings secara atomic dan membaca balik hasilnya.

Catat path backup yang dicetak. Bila settings sudah cocok, script tidak menulis ulang atau membuat backup tambahan. Extension yang sudah cocok tetap diverifikasi. Jika download kedua extension gagal, extension pertama mungkin sudah terpasang; settings belum tentu berubah. Baca output, jangan menganggap proses sebagai transaksi rollback menyeluruh.

### Langkah 5 — Verifikasi di Zed

Buka Zed secara manual. Periksa tema, ikon Explorer, word wrap, posisi panel, dan nama branch pada project Git sungguhan.

Verifikasi file oleh script bukan verifikasi visual. Workspace state yang sudah tersimpan dapat mempertahankan ukuran panel lama walaupun default baru sudah ditulis.

### Script mandiri di komputer pembuat

Di komputer tempat paket ini dibuat, salinan script juga tersedia di:

```bash
python3 "$HOME/zed-to-vscode.py" --dry-run
python3 "$HOME/zed-to-vscode.py"
```

Path tersebut bukan prasyarat untuk komputer penerima; gunakan script dalam paket.

## 6. Install/import skill Hermes dari ZIP atau TAR.GZ

“Import ZIP” di sini berarti mengekstrak direktori skill ke direktori skills Hermes. Bukan `snapshot import`, karena format dan tujuannya berbeda.

### Langkah 1 — Pilih profil tujuan

```bash
HERMES_SKILLS_HOME="${HERMES_HOME:-$HOME/.hermes}"
SKILL_PARENT="$HERMES_SKILLS_HOME/skills/software-development"
SKILL_DIR="$SKILL_PARENT/zed-to-vscode"
printf '%s\n' "$SKILL_DIR"
```

Pastikan path itu profil yang ingin dipasangi skill. Jika menggunakan profil lain, tentukan home profil yang benar secara eksplisit; jangan mengubah profil lain tanpa sengaja.

### Langkah 2 — Pastikan tidak mencampur versi

```bash
test ! -e "$SKILL_DIR" && printf 'Target belum ada\n'
```

Jika target sudah ada, berhenti dulu, bandingkan versi, dan backup direktori lama sebelum upgrade. `unzip -n` tidak mengganti file existing, tetapi dapat mencampurkan file lama/baru; bukan mekanisme upgrade.

### Langkah 3 — Ekstrak salah satu format

Untuk ZIP:

```bash
mkdir -p "$SKILL_PARENT"
unzip -n zed-to-vscode-0.1.0.zip -d "$SKILL_PARENT"
```

Atau TAR.GZ, hanya ke target yang belum ada:

```bash
mkdir -p "$SKILL_PARENT"
tar -xzf zed-to-vscode-0.1.0.tar.gz -C "$SKILL_PARENT"
```

### Langkah 4 — Uji hasil import

```bash
python3 "$SKILL_DIR/scripts/test_setup.py"
python3 "$SKILL_DIR/scripts/zed-to-vscode.py" --dry-run
hermes skills list --source local
```

Mulai sesi Hermes baru agar indeks skill dimuat ulang. Minta:

> Pakai skill zed-to-vscode. Preview dulu, lalu setup Zed seperti VS Code tanpa kontrol GUI atau restart desktop.

Pemasangan skill sendiri belum menerapkan settings Zed; script perlu dijalankan setelah itu.

## 7. Install melalui clone Git

Repository proyek: `https://github.com/naufalinux/nfx-zedtovscode.git`. Skill berada di subdirektori `skills/zed-to-vscode/`, bukan root repo. Untuk proyek ini, ikuti quick start dan instalasi skill pada `README.md`, atau metode repo multi-skill pada bagian B. Bagian A di bawah adalah contoh untuk repository khusus yang menaruh satu skill di root.

### A. Repo khusus berisi satu skill di root

Struktur root repo harus memuat `SKILL.md`, `scripts/`, dan `references/`.

Setelah memiliki URL yang benar, ganti placeholder berikut:

```bash
REPO_URL='GANTI_DENGAN_URL_REPO_SKILL'
HERMES_SKILLS_HOME="${HERMES_HOME:-$HOME/.hermes}"
SKILL_PARENT="$HERMES_SKILLS_HOME/skills/software-development"
SKILL_DIR="$SKILL_PARENT/zed-to-vscode"
mkdir -p "$SKILL_PARENT"
git clone "$REPO_URL" "$SKILL_DIR"
```

`git clone` menolak direktori tujuan yang sudah berisi file. Jangan menghapus skill existing secara otomatis untuk mengatasi penolakan itu.

Baca source, lalu:

```bash
python3 "$SKILL_DIR/scripts/test_setup.py"
python3 "$SKILL_DIR/scripts/zed-to-vscode.py" --dry-run
```

Mulai sesi Hermes baru dan gunakan skill seperti bagian sebelumnya.

### B. Repo berisi banyak skill

Clone ke direktori kerja terpisah. Setelah memastikan lokasi `SKILL.md` yang benar, salin seluruh direktori `zed-to-vscode`, bukan hanya file `SKILL.md`, ke direktori skills profil tujuan. Jangan menaruh keseluruhan repo secara buta sehingga struktur skill menjadi bersarang salah.

### C. Install dari registry/GitHub dengan CLI Hermes

Jika skill sudah dihosting dalam sumber yang didukung Hermes, cek sintaks versi terpasang:

```bash
hermes skills install --help
```

Bentuk identifier GitHub yang didukung CLI:

```bash
hermes skills install OWNER/REPO/PATH_TO_SKILL
```

`OWNER/REPO/PATH_TO_SKILL` adalah placeholder, bukan repo yang sudah tersedia. Tinjau scan/konfirmasi installer; jangan memakai `--force` untuk melewati peringatan tanpa memahami penyebabnya. Sesudah install, pastikan kedua script dan references ikut terpasang. Memasang URL langsung ke satu `SKILL.md` tidak boleh diasumsikan ikut membawa seluruh supporting files.

## 8. Snapshot Hermes bukan pengganti arsip skill ini

Hermes menyediakan:

```bash
hermes skills snapshot export --help
hermes skills snapshot import --help
```

Sintaks CLI yang terpasang saat panduan dibuat:

```bash
hermes skills snapshot export skills-snapshot.json
hermes skills snapshot import skills-snapshot.json
```

Snapshot mengekspor/mengimpor konfigurasi installed skills melalui JSON, bukan menerima ZIP/TAR paket ini. Jangan mengasumsikan snapshot memuat source code skill lokal lengkap. Untuk berbagi skill lokal beserta script, gunakan arsip atau repo Git pada bagian 6–7. Preview JSON dan cek versi CLI sebelum berbagi snapshot yang dapat memuat referensi skill lain.

## 9. Lokasi konfigurasi dan custom path

Default Linux:

```text
${XDG_CONFIG_HOME:-$HOME/.config}/zed/settings.json
${XDG_DATA_HOME:-$HOME/.local/share}/zed/extensions/installed/
```

Custom target:

```bash
python3 scripts/zed-to-vscode.py \
  --config-dir "$HOME/zed-test/config" \
  --data-dir "$HOME/zed-test/data" \
  --dry-run
```

Hilangkan `--dry-run` untuk benar-benar menerapkan ke lokasi custom. Opsi ini menentukan direktori `zed`, bukan parent-nya; script menambahkan `settings.json` dan `extensions/installed` sendiri. Menulis ke direktori custom tidak otomatis membuat Zed membaca direktori itu.

Direktori sementara mengikuti `TMPDIR`, atau fallback `~/.cache/zed-to-vscode`. Tes menggunakan `TMPDIR` atau `~/.cache/zed-to-vscode-tests`.

## 10. Backup dan rollback

Backup settings dibuat di samping settings.json:

```text
settings.json.before-vscode-YYYYMMDD-HHMMSS-microseconds.bak
```

Hak akses backup dibatasi ke user pemilik. Backup mungkin mengandung credentials existing; jangan bagikan.

Untuk rollback:

1. Tutup Zed secara manual.
2. Pilih path backup persis dari output setup, bukan menebak file terbaru.
3. Pulihkan dengan path milikmu sendiri:

```bash
BACKUP='/GANTI/DENGAN/PATH/BACKUP-YANG-BENAR.bak'
ZED_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/zed"
cp -- "$BACKUP" "$ZED_CONFIG/settings.json"
chmod 600 "$ZED_CONFIG/settings.json"
```

4. Buka Zed kembali secara manual.

Rollback settings tidak menghapus extension tema yang terpasang. Hapus extension melalui pengelola extension Zed bila memang tidak diperlukan. Jika setup dimulai tanpa settings existing, tidak ada backup asli yang dapat dipulihkan.

## 11. Troubleshooting

### Skill tidak muncul di Hermes

- Periksa profil aktif dan `HERMES_HOME`.
- Struktur harus berakhir pada `zed-to-vscode/SKILL.md`, bukan `zed-to-vscode/zed-to-vscode/SKILL.md` akibat salah ekstraksi.
- Pastikan skill tidak dinonaktifkan, gunakan `hermes skills list --source local`.
- Mulai sesi baru; sesi lama dapat menyimpan indeks skill sebelumnya.
- Pastikan semua supporting files ikut disalin.

### `python3: command not found`, `tomllib` hilang, atau error `filter` pada tarfile

Gunakan Python 3.12+. Periksa interpreter yang benar dengan `python3 --version`. Jangan mengganti Python sistem secara paksa. Bila memakai interpreter lain yang sesuai, gunakan interpreter itu konsisten untuk setup dan tes. Instalasi Python bergantung distro dan berada di luar script ini.

### `curl` tidak ditemukan atau permission denied

Instal curl melalui package manager distro. Jalankan script sebagai user pemilik konfigurasi Zed. Periksa kepemilikan direktori jika pernah menjalankan editor memakai sudo; jangan menyelesaikannya dengan menjalankan seluruh setup sebagai root.

### HTTP 403, timeout, TLS, atau download gagal

Script sudah memakai curl, retries terbatas, dan timeout. Tes endpoint dengan:

```bash
curl --fail --location --head --connect-timeout 15 --max-time 30 \
  https://api.zed.dev/extensions/vscode-icons/13.0.0/download
```

Respons HEAD dapat berbeda dari GET; keberhasilan/penolakannya bukan bukti tunggal bahwa download GET akan berhasil. Periksa koneksi, proxy, DNS, dan CA. Jangan mematikan verifikasi TLS dengan `-k`. Jika endpoint versi dipatok berubah, periksa katalog Zed dan review pembaruan script sebelum mengganti nomor versi.

### `Unexpected installed version ... refusing overwrite`

Extension existing berbeda dari versi yang dipatok. Script sengaja menolak downgrade/overwrite otomatis. Cek versi extension di Zed. Pilih mempertahankan versi itu dengan memperbarui pin dan menguji kompatibilitas script, atau backup/hapus extension tersebut secara sadar sebelum pemasangan ulang. Jangan menghapus seluruh direktori extensions.

### Tema/icon tidak muncul walau file sudah terpasang

- Tutup-buka Zed manual.
- Periksa apakah `--config-dir`/`--data-dir` mengarah ke instalasi yang sedang digunakan.
- Pilih `VScode Dark Plus` dan `VSCode Icons for Zed (Dark)` melalui selector Zed bila perlu.
- Periksa daftar extensions dan log Zed. Instalasi arsip langsung memverifikasi file, bukan menjamin editor sudah mengindeksnya.
- Jika Zed menolak paket, gunakan pengelola extensions bawaan secara manual untuk memasang nama yang sama; jangan mereset semua settings.

### Word wrap masih tidak aktif

Global settings harus berisi `"soft_wrap": "editor_width"`. Periksa override per bahasa, project `.zed/settings.json`, dan toggle wrap pada editor aktif. Soft wrap hanya mengubah tampilan, bukan menambahkan newline permanen. Baris hasil formatter adalah persoalan berbeda.

### Indikator branch tidak muncul

Di Zed indikator branch/worktree berada di title bar atas, bukan status bar kiri bawah seperti VS Code. Cek project asli:

```bash
git -C /path/ke/project rev-parse --show-toplevel
git -C /path/ke/project status --short --branch
```

Jika `not a git repository`, membuka folder source saja tidak cukup: metadata Git harus tersedia. Jangan otomatis `git init` atau menghapus file untuk memulihkan clone. `.git` juga bisa berupa file pada Git worktree; gunakan hasil Git, bukan asumsi bahwa `.git` selalu direktori. Detached HEAD atau repo tanpa commit awal juga tidak sama dengan branch normal.

### Panel tetap di posisi/ukuran lama

Ukuran pada script adalah default; workspace state dapat menyimpan ukuran sebelumnya. Atur posisi/ukuran manual di Zed bila diperlukan. Jangan menghapus database workspace pengguna tanpa persetujuan. Activity bar dan beberapa kontrol native memang tidak identik dengan VS Code.

### `Settings changed during setup`

Script mendeteksi settings diedit saat download berlangsung. Tutup Zed dan hentikan penyuntingan settings sementara, lalu jalankan ulang. Ini mencegah menimpa perubahan terbaru. Extension yang sudah terpasang pada percobaan pertama akan diverifikasi saat rerun.

### `JSONDecodeError` atau settings invalid

Script mendukung JSONC umum: komentar dan trailing comma. Sintaks rusak tetap ditolak. Perbaiki bagian yang dilaporkan dengan backup tersedia; jangan mengganti keseluruhan settings dengan contoh minimal karena dapat menghilangkan koneksi dan credentials.

### Desktop Plasma logout/crash

Hentikan seluruh GUI automation dan jangan mencoba mengulang crash. Script ini tidak memakai GUI input atau restart desktop. Ada pengamatan sebelumnya tentang CUA pointer hotplug yang bertepatan dengan crash Plasma X11; korelasi itu bukan bukti akar penyebab.

Diagnostik read-only, sesuaikan waktu kejadian:

```bash
journalctl --user --since '10 minutes ago' --no-pager
journalctl -k --since '10 minutes ago' --no-pager
```

Periksa juga `/var/log/Xorg.0.log.old` bila menggunakan X11; log itu mungkin tidak ada pada Wayland. Akses journal kernel/sistem bisa dibatasi. Bedakan SIGSEGV awal dari rentetan error display/Qt setelah sesi putus. Jangan restart display manager atau reboot hanya untuk menerapkan tema.

## 12. Verifikasi akhir

- [ ] Tes offline lolos dengan exit code 0.
- [ ] Script setup melaporkan verifikasi extension dan settings tanpa error.
- [ ] Backup asli tersedia jika ada perubahan pada settings existing.
- [ ] Zed dibuka ulang manual, tema dan ikon terlihat benar.
- [ ] Baris panjang membungkus sesuai lebar editor.
- [ ] Branch/worktree muncul ketika membuka repo Git yang valid.
- [ ] Pengaturan existing di luar target tetap tersedia.
- [ ] Paket yang dibagikan tidak memuat data pribadi.

Tes offline memakai fixture; tes itu tidak membuktikan jaringan atau render GUI. Script dasar juga telah diuji sebelumnya dengan download extension sungguhan dan eksekusi ulang idempotent di direktori terisolasi. Kesesuaian visual pada komputer penerima tetap perlu diperiksa di Zed.

## 13. Referensi

- [Hermes: Work with Skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)
- [Hermes: Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
- [Zed: Configuration](https://zed.dev/docs/configuring-zed)
- [Vscode Dark Plus Theme](https://zed.dev/extensions/vscode-dark-plus)
- [VSCode Icons](https://zed.dev/extensions/vscode-icons)
- [Source Dark Plus](https://github.com/d1y/vscode_dark_plus.zed)
- [Source VSCode Icons](https://github.com/vscode-icons/vscode-icons-zed)

Sintaks Hermes dapat berkembang. Gunakan `hermes skills --help` dan help subcommand versi terpasang sebelum memakai opsi yang tidak didokumentasikan di sini.
