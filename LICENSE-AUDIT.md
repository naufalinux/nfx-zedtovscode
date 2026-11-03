<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Audit lisensi — nfx-zedtovscode

## Ringkasan keputusan

Source code, skill, tes, dan dokumentasi original proyek ditetapkan sebagai **GPL-3.0-or-later** untuk revisi ini dan perubahan berikutnya. GPL memberikan copyleft pada penyalinan/distribusi karya turunan yang tercakup; teks GPL v3 disertakan di `LICENSE`, sedangkan pilihan “atau versi sesudahnya” dinyatakan dalam SPDX dan notice proyek.[1]

Keputusan ini mengikuti permintaan pemilik proyek Naufalinux, dengan asumsi ia berwenang melisensikan kontribusi original yang ada. Audit tidak menemukan kode library pihak ketiga yang disalin ke tiga file Python yang diperiksa. Ini bukan klaim chain-of-title yang diverifikasi secara hukum.

Revisi awal `ca20d89` telah memiliki grant MIT. Perubahan lisensi tidak mencabut hak MIT yang sudah diberikan atas salinan/revisi lama. Teks grant lama dipertahankan sebagai `LICENSES/Legacy-MIT.txt`; file itu bukan lisensi default kontribusi baru. Jangan menghapus histori untuk menyamarkan grant lama.

**Temuan terbuka:** lisensi port `vscode-dark-plus` v0.0.1 belum terkonfirmasi. Jangan menyebut seluruh dependency chain “sudah clear”, dan jangan membundel atau merelisensikan assets extension itu sebagai GPL. Installer versi ini masih mengunduhnya saat setup; penggunaan/distribusi extension tersebut perlu penilaian terpisah. Hapus/ganti komponen atau peroleh konfirmasi upstream sebelum menawarkan distribusi yang menuntut seluruh rantai lisensi terverifikasi.

## Cakupan dan metode

Baseline lokal: commit `ca20d89`, branch `main`. Audit menyapu seluruh 11 file tracked baseline menggunakan `git ls-files`, membaca import AST seluruh tiga file `.py`, memeriksa isi arsip dua extension versi yang dipatok, dan membandingkan deklarasi lisensi source upstream yang tersedia. Tidak ada file biner, archive, vendored package, dependency lockfile, atau library pihak ketiga yang dibundel pada baseline itu. Dua script setup adalah salinan identik.

Scan binary menggunakan pemeriksaan byte NUL atas semua file tracked, dilengkapi pemeriksaan tipe/path dan pembacaan source. Ini inventaris source repo, bukan audit setiap executable/library di mesin pengguna. `.git` dan untracked caches bukan distribusi source; file baru hasil audit dijelaskan pada bagian akhir.

Audit upstream dilakukan terhadap sumber yang berhasil diambil pada sesi audit. Referensi upstream `master`/`main` bisa berubah; hasilnya tidak menggantikan audit source persis dari setiap release. Snapshot manifest, hash archive yang benar-benar diperiksa, dan gap provenance dicatat di bawah.

## Inventaris dan tindakan

| Komponen | Hubungan dengan repo | Temuan lisensi | Tindakan |
|---|---|---|---|
| Script setup root + salinan dalam skill | Source original dibundel | MIT pada baseline; kini GPL-3.0-or-later | SPDX, copyright, teks GPL, dan pengakuan grant historis |
| `test_setup.py`, SKILL, README, GUIDE, SHARING | Source/dokumentasi original dibundel | Sama seperti source proyek | GPL-3.0-or-later; salinan dokumentasi disinkronkan |
| Python stdlib | Runtime imports, bukan source vendored | CPython 3.12 memakai PSF License v2 serta notices historis; source Python menyatakan 2.2+ GPL-compatible.[4] | Tidak mengubah lisensi interpreter; tidak mengklaim semua komponen CPython hanya satu lisensi |
| `curl` | Executable eksternal dipanggil sebagai subprocess | curl license, permission notice permissive; bukan sekadar nama “MIT”.[5] | Tidak dibundel; lisensi build lokal dan library TLS/transitif perlu audit jika didistribusikan |
| `vscode-icons` 13.0.0 | Extension diunduh saat setup, tidak dibundel | Repo upstream Zed menyatakan MIT; codebase asal juga MIT.[2][10] | Pertahankan notices upstream jika mendistribusikan assets; tidak merelisensikan logo/merek |
| `vscode-dark-plus` 0.0.1 | Extension diunduh saat setup, tidak dibundel | **NOASSERTION untuk lisensi port**; source yang diperiksa tidak memiliki grant lisensi tersendiri.[3] | Temuan belum selesai; jangan bundel sebagai GPL atau menyatakan cleared |
| Zed | Aplikasi target eksternal | Teks GPL v3 ada di repo upstream; ini bukan inventaris semua crate/assets atau ketentuan distribusi binary Zed.[7] | Tidak dibundel, tidak di-link; user memasang sendiri |
| Hermes Agent | Host skill opsional eksternal | Root upstream MIT.[6] | Hanya memakai format skill; runtime/binary Hermes tidak disalin |
| Git | Alat clone/development dalam panduan | COPYING upstream menegaskan GPL v2 kecuali dinyatakan lain.[8] | Bukan dependency runtime script, tidak dibundel atau di-link |
| unzip/tar shell, coreutils, journalctl | Perintah instalasi/diagnostik dalam panduan | Implementasi/versi berasal dari OS pengguna; tidak dipatok/dibundel | Di luar lisensi source proyek; tidak diasumsikan seluruhnya GPL atau MIT |

Tidak ada dependency pip/npm/Cargo, dynamic library vendored, compiled extension, atau executable binary distribusi yang ditemukan dalam tracked baseline. Fixture tes hanya metadata dan theme name sintetis, bukan source/assets extension yang disalin.

### Modul Python yang ditemukan

`argparse`, `copy`, `datetime`, `importlib`, `json`, `os`, `pathlib`, `re`, `shutil`, `subprocess`, `tarfile`, `tempfile`, `tomllib`, `unittest`.

Semua modul tersebut adalah standard library, bukan paket pip tersendiri. Lisensi interpreter tetap mengikuti distribusi Python yang dipakai; mengimpor stdlib tidak membuat file proyek otomatis berlisensi PSF.

## Bukti extension

### vscode-dark-plus 0.0.1 — unresolved

- Download: `https://api.zed.dev/extensions/vscode-dark-plus/0.0.1/download`.
- SHA-256 arsip yang diperiksa: `07d6751575eff03e0de3353456648e0a672b453be5f6af39d21ad6483cacfdfc`.
- Arsip berisi empat entry, termasuk direktori; isi file berupa `extension.json` dan JSON tema. Tidak ada `LICENSE`, `COPYING`, atau `NOTICE`.
- Source port pada commit `e64df699cf6888f15a23ef3ae8dcc3254e56c114` memiliki tiga file tracked: README, manifest, dan JSON tema; tidak ditemukan grant lisensi port.[3]
- README port merujuk `tcd/dark-plus-syntax`, yang memiliki MIT notice copyright Clay Dunston.[9] Itu bukti asal yang dirujuk, **bukan izin yang terverifikasi untuk kontribusi port d1y**, dan tidak membuktikan kesamaan seluruh isi.
- Metadata katalog extension bukan pengganti lisensi. Port tidak boleh otomatis dianggap MIT hanya karena ancestor-nya MIT.

### vscode-icons 13.0.0 — project-level MIT, asset provenance terbatas

- Download: `https://api.zed.dev/extensions/vscode-icons/13.0.0/download`.
- SHA-256 arsip yang diperiksa: `27392aebc57b5d75bd73be3d3442f7c613718dd83f9f628d9e25da4c4a6a6ae9`.
- Arsip berisi 1.669 entry; tidak memiliki file notice lisensi bernama `LICENSE`, `COPYING`, atau `NOTICE`. SVG bernama `file_type_license.svg` dan sejenisnya adalah gambar ikon, bukan teks lisensi.
- Repo Zed upstream yang diperiksa menyatakan MIT, copyright Roberto Huertas; codebase `vscode-icons` juga memuat MIT dengan copyright contributors.[2][10]
- HEAD upstream teramati: `f52dc01794c9e6571a0a077b7a87445208dce727`. Ini bukan bukti bahwa arsip v13.0.0 dibangun persis dari commit tersebut.
- Tidak dilakukan verifikasi asal/lisensi/trademark satu per satu untuk seluruh SVG. Jangan menyebut 1.669 entry telah diaudit secara individual. Izin software tidak otomatis memberi hak merek/logo.
- Bila ingin membundel assets di masa depan, sertakan notices yang sesuai, pin source release tepat, dan audit exceptions/attribution assets terlebih dahulu.

## Mengapa GPL-3.0-or-later

Copyleft GPL sesuai tujuan berbagi script lokal dengan kewajiban mempertahankan kebebasan source untuk distribusi karya turunannya.[1] Tidak ada kebutuhan copyleft layanan jaringan yang teridentifikasi pada script konfigurasi lokal ini, sehingga AGPL tidak dipilih. Lisensi original proyek tidak memperluas hak terhadap extension, trademark, atau executable eksternal.

Menjalankan executable terpisah dan mengunduh paket sebagai file terpisah tidak sama dengan menyalin source komponen tersebut ke repo. Audit ini tidak mengklaim kesimpulan universal tentang semua kemungkinan bentuk integrasi/linking; bila kelak mem-vendor dependency atau membangun binary gabungan, audit ulang komposisi dan kewajiban distribusinya.

## Aturan kontribusi dan distribusi

1. Kontribusi baru ke source/dokumentasi original menggunakan GPL-3.0-or-later, kecuali ada penetapan terpisah yang eksplisit. Jangan memasukkan karya orang lain tanpa hak yang memadai.
2. Sertakan `LICENSE` dan notice copyright/SPDX ketika mendistribusikan source proyek. Kewajiban untuk karya turunan dan bentuk non-source mengikuti GPL.[1]
3. Jangan mengubah atau menghapus notice upstream komponen pihak ketiga. Dokumen lisensi upstream di `LICENSES` tetap mengikuti ketentuannya sendiri, bukan GPL proyek.
4. Jangan membundel Python, curl, Git, Zed, Hermes, extensions, atau library OS dengan asumsi semuanya tercakup oleh GPL proyek.
5. Audit ulang setiap pin extension berubah; versi sama tidak menjamin byte archive server tidak berubah. Hash di laporan ini adalah bukti audit, **belum enforced oleh installer**.
6. Jangan memakai klaim “seluruh dependency open source terverifikasi” selama temuan port Dark Plus masih terbuka.
7. Grant MIT historis tetap diakui; penerima revisi lama dapat mengandalkan izin yang telah diterimanya.

## Hasil dan batas verifikasi

- Selesai: inventaris source tracked baseline, import stdlib, tidak adanya binary/vendor dependency dalam baseline, inspeksi kedua archive, pemilihan lisensi proyek, sinkronisasi notices dan tes source lokal.
- Terbuka: izin port Dark Plus, provenance SVG individual, mapping release archive ke commit upstream, audit transitive binary OS, dan chain-of-title hukum di luar informasi pemilik proyek.
- File hasil audit: laporan ini, policy `LICENSING.md`, salinan GPL, legacy MIT notice, dan notices MIT upstream sebagai referensi. Notice tidak berarti extension telah dibundel.
- Laporan adalah audit teknis berbasis bukti yang tersedia, bukan jaminan legal atas seluruh aset eksternal.

## Sources

[1] https://www.gnu.org/licenses/gpl-3.0.txt
[2] https://raw.githubusercontent.com/vscode-icons/vscode-icons-zed/master/LICENSE
[3] https://github.com/d1y/vscode_dark_plus.zed/tree/e64df699cf6888f15a23ef3ae8dcc3254e56c114
[4] https://raw.githubusercontent.com/python/cpython/3.12/LICENSE
[5] https://raw.githubusercontent.com/curl/curl/master/COPYING
[6] https://raw.githubusercontent.com/NousResearch/hermes-agent/main/LICENSE
[7] https://raw.githubusercontent.com/zed-industries/zed/main/LICENSE-GPL
[8] https://raw.githubusercontent.com/git/git/master/COPYING
[9] https://raw.githubusercontent.com/tcd/dark-plus-syntax/master/LICENSE.md
[10] https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/LICENSE
