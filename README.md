# 📸 Image EXIF Location - Batch Processor

Script Python untuk otomatis menambahkan informasi lokasi (GPS, alamat, timestamp, QR code maps) ke foto dalam batch mode.

## 👁️ Preview

### Sebelum (Before)
![Before](images/WhatsApp%20Image%202026-05-21%20at%2014.49.31.jpeg)

### Sesudah (After)
![After](output/WhatsApp%20Image%202026-05-21%20at%2014.49.31.jpeg)

*Hasil processing dengan informasi lokasi, timestamp, dan QR code Google Maps*

## ✨ Fitur

- ✅ **Batch Processing**: Proses semua foto di folder `images/` secara otomatis
- ✅ **Input Koordinat**: Prompt interaktif untuk memasukkan Latitude & Longitude
- ✅ **Format Fleksibel**: Support input comma-separated (e.g., `3.886561, 98.47930`)
- ✅ **QR Code Maps**: QR code untuk akses langsung ke Google Maps (kiri bawah)
- ✅ **Responsive Font**: Ukuran font otomatis 3% dari lebar gambar
- ✅ **Posisi Tetap**: Teks di kanan bawah, QR code di kiri bawah
- ✅ **Align Right**: Text align ke kanan untuk tampilan profesional
- ✅ **Metadata GPS**: Tambahan GPS EXIF data ke setiap foto
- ✅ **Geocoding**: Konversi koordinat ke alamat (OpenStreetMap)
- ✅ **Tanggal Indonesia**: Format tanggal dalam bahasa Indonesia
- ✅ **Auto Output**: Hasil otomatis tersimpan ke folder `output/`

## 📋 Requirements

- Python 3.7+
- Pillow (PIL)
- piexif
- requests

## 🚀 Instalasi

### 1. Clone atau Download Project
```bash
git clone <repository-url>
cd image-exif-location
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install Pillow piexif requests qrcode
```

## 📁 Struktur Folder

```
image-exif-location/
├── script.py           # Main script
├── requirements.txt    # Dependencies
├── README.md          # Dokumentasi
├── images/            # Folder input (tempat letakkan foto)
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── ...
└── output/            # Folder output (hasil processing otomatis)
    ├── photo1.jpg
    ├── photo2.jpg
    └── ...
```

## 💻 Cara Menggunakan

### 1. Siapkan Foto
Letakkan semua foto yang ingin diproses di folder `images/`

### 2. Jalankan Script
```bash
python script.py
```

### 3. Input Koordinat
Script akan meminta input dalam format:
```
Masukan Koordinat (format: latitude, longitude)
Contoh: 3.886561111111111, 98.47930555555556
> 
```

Masukkan koordinat dengan format: `latitude, longitude`

Contoh:
```
3.886561111111111, 98.47930555555556
```

### 4. Tunggu Proses Selesai
Script akan memproses semua foto satu per satu:
```
🖼 Ditemukan 6 foto
📂 Output akan disimpan ke folder 'output'

⏳ Processing: photo1.jpg... ✓ Selesai
⏳ Processing: photo2.jpg... ✓ Selesai
...
```

### 5. Cek Hasil
Semua foto hasil processing ada di folder `output/`

## 📝 Output Informasi

Setiap foto akan ditambahkan dengan:

```
21 Mei 2026 14.30.45
Nama Desa/Kelurahan
Kecamatan [District]
Kabupaten [City]
[Province]
```

- **Timestamp**: Tanggal & waktu dalam bahasa Indonesia
- **Alamat**: Diambil dari koordinat (via OpenStreetMap)
- **QR Code**: Scannable QR code untuk akses Google Maps (di kiri bawah)
- **GPS Data**: Koordinat disimpan di EXIF metadata

## ⚙️ Konfigurasi

Edit `script.py` untuk mengubah:

```python
IMAGES_FOLDER = "images"        # Folder input
OUTPUT_FOLDER = "output"        # Folder output
```

## 🔧 Troubleshooting

### Font tidak ditemukan
Jika melihat warning font, install font Arial atau gunakan font lain:
```python
font = ImageFont.truetype("/path/to/font.ttf", font_size)
```

### API Rate Limit
Jika mendapat error dari OpenStreetMap API, script otomatis menambah delay 1 detik antar foto.

### Foto tidak terproses
- Pastikan format foto: `.jpg`, `.jpeg`, atau `.png`
- Pastikan foto ada di folder `images/`
- Check apakah foto valid dan tidak corrupt

## 📊 Contoh Output

Foto akan memiliki:
- Text overlay dengan timestamp & alamat (kanan bawah)
- QR code untuk Google Maps (kiri bawah)
- GPS metadata di EXIF

## 📄 File yang Dihasilkan

Hasil di folder `output/`:
- Foto dengan overlay text
- GPS metadata di EXIF
- Nama file sama dengan file asli

## 🤝 Support

Jika ada masalah:
1. Pastikan Python 3.7+ terinstall
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Check folder `images/` ada dan berisi foto
4. Jalankan script dengan output penuh untuk debugging

## 📜 License

Free to use

---

**Dibuat dengan ❤️ untuk dokumentasi lokasi foto**
