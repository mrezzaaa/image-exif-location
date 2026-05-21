from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import piexif
from datetime import datetime
import os
from pathlib import Path
import time
import qrcode

# =========================================
# CONFIG
# =========================================

IMAGES_FOLDER = "images"
OUTPUT_FOLDER = "output"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================================
# INPUT COORDINATES
# =========================================

print("=" * 50)
print("IMAGE EXIF LOCATION - BATCH PROCESSOR")
print("=" * 50)

while True:
    try:
        coords_input = input("\nMasukan Koordinat (format: latitude, longitude)\nContoh: 3.886561111111111, 98.47930555555556\n> ").strip()
        
        # Split by comma and parse
        coords = coords_input.split(",")
        if len(coords) != 2:
            raise ValueError("Gunakan format: latitude, longitude")
        
        LATITUDE = float(coords[0].strip())
        LONGITUDE = float(coords[1].strip())
        
        print(f"\n✓ Koordinat: {LATITUDE}, {LONGITUDE}")
        break
    except ValueError as e:
        print(f"❌ Error: {e} (gunakan titik untuk desimal)")
    except Exception as e:
        print(f"❌ Error: Masukan koordinat yang valid")

# =========================================
# FUNCTION TO PROCESS SINGLE IMAGE
# =========================================

def process_image(input_path, output_path):
    """Process a single image with coordinates and save to output"""
    
    # OpenStreetMap Reverse Geocoding
    GEOCODE_URL = (
        f"https://nominatim.openstreetmap.org/reverse"
        f"?format=jsonv2"
        f"&lat={LATITUDE}"
        f"&lon={LONGITUDE}"
    )
    
    # Google Maps URL for QR code
    MAPS_URL = f"https://www.google.com/maps?q={LATITUDE},{LONGITUDE}"
    
    # =========================================
    # GET ADDRESS FROM COORDINATE
    # =========================================
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    formatted_address = "Alamat tidak tersedia"
    
    try:
        geo_response = requests.get(GEOCODE_URL, headers=headers, timeout=5)
        if geo_response.status_code == 200:
            try:
                geo_json = geo_response.json()
                address = geo_json.get("address", {})
                
                village = (
                    address.get("village")
                    or address.get("hamlet")
                    or address.get("suburb")
                    or ""
                )
                
                district = (
                    address.get("county")
                    or address.get("city_district")
                    or ""
                )
                
                city = (
                    address.get("city")
                    or address.get("town")
                    or address.get("municipality")
                    or address.get("state_district")
                    or ""
                )
                
                province = address.get("state", "")
                
                formatted_address = f"""
{village}
{district}
{city}
{province}
""".strip()
            except Exception as e:
                pass
    except Exception as e:
        pass
    
    # =========================================
    # GENERATE QR CODE
    # =========================================
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(MAPS_URL)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # =========================================
    # OPEN MAIN IMAGE
    # =========================================
    
    img = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # =========================================
    # PASTE QR CODE AT LEFT BOTTOM
    # =========================================
    
    try:
        qr_size = 280
        qr_image = qr_image.resize((qr_size, qr_size))
        
        qr_x = 40
        qr_y = img.height - qr_size - 40
        
        img.paste(qr_image, (qr_x, qr_y))
    except:
        pass
    
    # =========================================
    # TIMESTAMP
    # =========================================
    
    # Indonesian month names
    months_id = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    
    now = datetime.now()
    month_id = months_id[now.month]
    timestamp = f"{now.day} {month_id} {now.year} {now.strftime('%H.%M.%S')}"
    
    # =========================================
    # FONT
    # =========================================
    
    # Calculate font size as 4% of image width
    font_size = int(img.width * 0.03)
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        print("⚠️ Font 'arial.ttf' not found")
        font = ImageFont.load_default(font_size)
    
    # =========================================
    # DRAW TEXT
    # =========================================
    
    text = f"{timestamp}\n{formatted_address}"
    
    # Calculate text position at RIGHT BOTTOM
    # Get text bounding box to calculate width and height
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=8)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Position at right bottom with padding
    padding = 40
    text_x = img.width - text_width - padding
    text_y = img.height - text_height - padding
    
    # shadow
    draw.multiline_text(
        (text_x + 2, text_y + 2),
        text,
        font=font,
        fill=(0, 0, 0),
        spacing=8,
        align="right"
    )
    
    # main text
    draw.multiline_text(
        (text_x, text_y),
        text,
        font=font,
        fill=(255, 255, 255),
        spacing=8,
        align="right"
    )
    
    # =========================================
    # SAVE IMAGE
    # =========================================
    
    img.save(output_path)
    
    # =========================================
    # ADD GPS EXIF
    # =========================================
    
    def to_deg(value):
        abs_value = abs(value)
        
        deg = int(abs_value)
        min_float = (abs_value - deg) * 60
        minute = int(min_float)
        sec = round((min_float - minute) * 60 * 100)
        
        return (
            (deg, 1),
            (minute, 1),
            (sec, 100)
        )
    
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef:
            "N" if LATITUDE >= 0 else "S",
        
        piexif.GPSIFD.GPSLatitude:
            to_deg(LATITUDE),
        
        piexif.GPSIFD.GPSLongitudeRef:
            "E" if LONGITUDE >= 0 else "W",
        
        piexif.GPSIFD.GPSLongitude:
            to_deg(LONGITUDE),
    }
    
    exif_dict = {
        "GPS": gps_ifd
    }
    
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, output_path)
    
    return True

# =========================================
# PROCESS ALL IMAGES
# =========================================

if not os.path.exists(IMAGES_FOLDER):
    print(f"\n❌ Folder '{IMAGES_FOLDER}' tidak ditemukan!")
else:
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(Path(IMAGES_FOLDER).glob(ext))
    
    if not image_files:
        print(f"❌ Tidak ada foto di folder '{IMAGES_FOLDER}'")
    else:
        print(f"\n🖼 Ditemukan {len(image_files)} foto")
        print(f"📂 Output akan disimpan ke folder '{OUTPUT_FOLDER}'\n")
        
        successful = 0
        failed = 0
        
        for image_path in sorted(image_files):
            try:
                output_filename = image_path.name
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                
                print(f"⏳ Processing: {image_path.name}...", end=" ", flush=True)
                
                if process_image(str(image_path), output_path):
                    print("✓ Selesai")
                    successful += 1
                
                # Delay untuk menghindari rate limit
                time.sleep(1)
                    
            except Exception as e:
                print(f"✗ Error: {str(e)[:50]}")
                failed += 1
        
        print("\n" + "=" * 50)
        print(f"✓ Berhasil: {successful}")
        print(f"✗ Gagal: {failed}")
        print(f"📂 Output tersimpan di folder: {OUTPUT_FOLDER}")
        print("=" * 50)