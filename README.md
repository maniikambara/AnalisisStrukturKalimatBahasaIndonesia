# Analisis Struktur Kalimat Bahasa Indonesia Dengan Metode Parser & Context-Free Grammar

Repositori ini berisi program untuk melakukan analisis struktur kalimat sederhana dalam Bahasa Indonesia menggunakan metode Parser dan Context-Free Grammar (CFG). Program ini juga melibatkan proses scraping data dari basis data KBBI dengan kategori kata (verba, nomina, adjektiva, dsb.) yang disimpan dalam sebuah file JSON (`output.json`).

## Daftar Isi
- [Tentang Proyek](#tentang-proyek)
- [Struktur Folder dan File](#struktur-folder-dan-file)
- [Kebutuhan Sistem](#kebutuhan-sistem)
- [Panduan Instalasi & Penggunaan](#panduan-instalasi--penggunaan)
- [Deskripsi Singkat Tiap Program](#deskripsi-singkat-tiap-program)
- [Skema Database MySQL](#skema-database-mysql)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## Tentang Proyek
Proyek ini bertujuan untuk:

1. Membangun aplikasi berbasis Python yang dapat mengenali struktur kalimat bahasa Indonesia.
2. Mengkategorikan kata berdasarkan data hasil scraping dari website KBBI, lalu menyimpannya pada database MySQL dan mengeluarkannya dalam bentuk file JSON.
3. Menganalisis suatu kalimat sesuai dengan CFG (Context-Free Grammar) yang telah didefinisikan, dan menampilkan hasil strukturnya di antarmuka GUI.

## Struktur Folder dan File
```
├── CFG.py
├── Database.py
├── Main.py
├── Parser.py
├── scrapSQL.py
├── kbbi_dictionary.sql
├── output.json
└── README.md  <-- (file ini)
```

- **CFG.py**: Berisi definisi grammar (aturan CFG) dan fungsi untuk validasi struktur kalimat.
- **Database.py**: Berisi pengolahan data file `output.json` untuk disiapkan sebagai dictionary kata (kategori kata, dsb.).
- **Main.py**: Berisi implementasi GUI berbasis `tkinter` untuk memasukkan kalimat yang akan dianalisis serta menampilkan hasil analisis.
- **Parser.py**: Berisi lexer dan parser engine yang menggunakan `ply` (Python Lex-Yacc) untuk memeriksa token/kategori kata.
- **scrapSQL.py**: Berisi skrip untuk scraping data dari database MySQL (tabel dictionary) dan menghasilkan file `output.json` sesuai kategori kata.
- **kbbi_dictionary.sql**: Berisi skema dan data tabel dictionary (schema KBBI) sebagai hasil scraping dari KBBI.
- **output.json**: Berisi data hasil scraping (tiap kategori kata).

## Kebutuhan Sistem
- Python 3.x
- Library Python:
  - `ply`
  - `tkinter` (biasanya sudah terpasang untuk versi standar Python Windows/macOS, di Linux perlu disesuaikan)
  - `mysql-connector-python` (untuk mengakses database MySQL)
- MySQL (untuk menjalankan file `kbbi_dictionary.sql`)

## Panduan Instalasi & Penggunaan

### Clone atau Unduh Repositori
```bash
git clone https://github.com/username/analisis-struktur-kalimat-Bahasa-Indonesia.git
cd analisis-struktur-kalimat-Bahasa-Indonesia
```

### Install Library yang Dibutuhkan
Gunakan `pip` atau manajer paket lain:
```bash
pip install ply mysql-connector-python
```
(Tambahkan library lain jika dibutuhkan, misalnya `tkinter` di Linux: `sudo apt-get install python3-tk`.)

### Setup Database MySQL
1. Buat database MySQL bernama `kbbi` (atau sesuaikan nama database di `scrapSQL.py`).
2. Impor file `kbbi_dictionary.sql` ke MySQL:
```sql
CREATE DATABASE kbbi;
USE kbbi;
SOURCE /path/to/kbbi_dictionary.sql;
```
3. Pastikan kredensial (host, user, password, dan database) di dalam `scrapSQL.py` sesuai dengan instalasi lokal Anda.

### Menjalankan Scraping Data untuk Membuat `output.json`
Jalankan:
```bash
python scrapSQL.py
```
Script ini akan mengambil data dari tabel `dictionary` di database MySQL dan menyimpannya dalam file `output.json`.

### Menjalankan Program GUI (`Main.py`)
Jalankan perintah:
```bash
python Main.py
```
- Masukkan kalimat pada kotak input untuk dianalisis.
- Klik tombol **Analisis**.
- Hasil struktur kalimat akan ditampilkan pada area teks di bawahnya.

## Deskripsi Singkat Tiap Program

### CFG.py
- **Class CFG**: Mendefinisikan grammar (aturan CFG) untuk beberapa bentuk kalimat (kalimat sederhana, majemuk setara, dan majemuk bertingkat).
- **Fungsi validate_sentence_structure(words)**: Memeriksa apakah rangkaian kata sesuai dengan salah satu pola CFG yang ditetapkan.

### Database.py
- **Class SPOKDatabase**: Memuat data kategori kata dari file JSON (`output.json`), serta menyediakan fungsi `get_word_categories()` untuk mengakses data kategori tersebut.
- **Fungsi get_word_categories()**: Dapat diimpor secara langsung untuk digunakan di modul lain.

### Main.py
- Berisi antarmuka GUI menggunakan `tkinter`.
- **Class SPOKParserGUI**: Menyediakan seluruh elemen GUI, seperti input teks, tombol analisis, dan output area.
- **Fungsi analyze_sentence()**: Memanggil `ParserEngine` (dari `Parser.py`) untuk memvalidasi kalimat dan menampilkan hasil analisis.

### Parser.py
- Menggunakan `ply` (Python Lex-Yacc) untuk mendefinisikan token-token lexer berdasarkan data kategori kata (adjektiva, verba, nomina, dsb.).
- **Class ParserEngine**: Menggabungkan hasil tokenisasi dengan modul CFG untuk menentukan apakah kalimat valid serta mengembalikan struktur SPOK.

### scrapSQL.py
- Menghubungkan ke database MySQL, membaca tabel `dictionary`, lalu memfilter record berdasarkan kategori (misal: verba, nomina, dsb.).
- Menyimpan hasil penyaringan kata ke dalam `output.json` untuk digunakan oleh modul lain.

## Skema Database MySQL
Dalam file `kbbi_dictionary.sql`, terdapat skema `kbbi` dengan tabel `dictionary` dan struktur sebagai berikut:

| Nama Field | Tipe Data | Nullable | Keterangan              |
|------------|-----------|----------|-------------------------|
| _id        | INT(11)   | NO       | Primary Key, Auto Increment |
| word       | TEXT      | NO       | Kata                    |
| arti       | TEXT      | NO       | Arti atau penjelasan    |
| type       | INT(11)   | NO       | Tipe atau kategori      |

## Kontribusi
1. Fork repositori ini.
2. Buat branch baru untuk fitur atau perbaikan (`git checkout -b nama-fitur`).
3. Lakukan commit perubahan Anda (`git commit -m 'Menambahkan fitur XYZ'`).
4. Push ke branch milik Anda (`git push origin nama-fitur`).
5. Buat Pull Request ke branch utama repositori ini.

## Lisensi
Proyek ini menggunakan lisensi MIT. Silakan gunakan, modifikasi, dan distribusikan secara bebas dengan tetap menyertakan hak cipta aslinya.
