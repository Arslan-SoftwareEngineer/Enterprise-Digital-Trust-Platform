"""
Realistic Forensic Sample Assets Generator
Synthesizes base64-encoded visual and spectral forensic test assets:
- Valid Official Passport (with ICAO MRZ and Holographic shimmer)
- Forged National ID (with ELA tampering splice artifacts)
- Deepfake Synthetic Portrait (with 2D FFT generative upsampling grid)
- Genuine Human Portrait (with 3D anatomical depth gradient)
- Audio Spectrogram Waveform
"""

import base64
import io
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def _to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")


def generate_passport_sample() -> str:
    """Generates synthetic high-fidelity sample passport with MRZ."""
    w, h = 600, 420
    img = Image.new("RGB", (w, h), color=(240, 243, 246))
    draw = ImageDraw.Draw(img)

    # Passport Header
    draw.rectangle([(0, 0), (w, 60)], fill=(20, 35, 60))
    draw.text((20, 18), "UNITED STATES OF AMERICA - PASSPORT", fill=(230, 235, 245))

    # Photo Box
    draw.rectangle([(30, 80), (190, 280)], fill=(200, 210, 220), outline=(50, 70, 90), width=2)
    # Portrait avatar
    draw.ellipse([(70, 110), (150, 190)], fill=(235, 195, 170))  # Head
    draw.ellipse([(50, 200), (170, 310)], fill=(40, 60, 95))     # Body

    # Guilloche decorative wavy security background lines
    for i in range(10, 320, 18):
        points = [(x, int(80 + i + 10 * math.sin(x / 25.0))) for x in range(210, 580)]
        draw.line(points, fill=(215, 225, 235), width=1)

    # Document Fields
    fields = [
        ("Type / Code", "P / USA", 210, 80),
        ("Passport No.", "E82910481", 400, 80),
        ("Surname", "MONTGOMERY", 210, 130),
        ("Given Names", "ALEXANDER DAVID", 210, 175),
        ("Nationality", "UNITED STATES OF AMERICA", 210, 220),
        ("Date of Birth", "14 MAY 1991", 210, 265),
        ("Date of Expiry", "22 OCT 2031", 400, 265),
    ]
    for lbl, val, x, y in fields:
        draw.text((x, y), lbl, fill=(110, 125, 140))
        draw.text((x, y + 16), val, fill=(20, 30, 45))

    # Holographic security emblem
    draw.polygon([(520, 140), (560, 180), (520, 220), (480, 180)], fill=(210, 230, 245), outline=(130, 180, 220))
    draw.text((505, 172), "US-SEC", fill=(70, 110, 150))

    # Machine Readable Zone (MRZ - TD3)
    draw.rectangle([(15, 325), (585, 405)], fill=(250, 250, 252), outline=(180, 190, 200), width=1)
    mrz1 = "P<USAMONTGOMERY<<ALEXANDER<DAVID<<<<<<<<<<<<<"
    mrz2 = "E829104813USA9105148M3110223<<<<<<<<<<<<<<<6"
    draw.text((25, 338), mrz1, fill=(15, 20, 30))
    draw.text((25, 368), mrz2, fill=(15, 20, 30))

    return _to_base64(img)


def generate_forged_id_sample() -> str:
    """Generates synthetic forged ID with spliced tampered birthday and photo."""
    w, h = 600, 400
    img = Image.new("RGB", (w, h), color=(245, 242, 238))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (w, 55)], fill=(120, 25, 35))
    draw.text((20, 16), "NATIONAL IDENTITY CARD - TAMPERED SPECIMEN", fill=(255, 240, 240))

    # Photo Box with obvious digital splice artifact boundary
    draw.rectangle([(30, 80), (190, 280)], fill=(180, 190, 205), outline=(220, 40, 40), width=3)
    draw.ellipse([(70, 110), (150, 190)], fill=(225, 175, 150))
    draw.ellipse([(50, 200), (170, 310)], fill=(30, 30, 50))

    # Spliced mismatch block
    draw.rectangle([(25, 75), (195, 285)], outline=(255, 0, 0), width=1)

    fields = [
        ("ID Number", "ID-908129-X", 210, 85),
        ("Full Name", "JOHN DOE SMITH", 210, 135),
        ("DOB (Altered)", "01 JAN 2004", 210, 185),
        ("Expiry", "15 DEC 2023 [EXPIRED]", 210, 235),
    ]
    for lbl, val, x, y in fields:
        draw.text((x, y), lbl, fill=(100, 100, 100))
        draw.text((x, y + 16), val, fill=(30, 30, 30))

    # ELA Tampering Highlight overlay (simulated red glow)
    draw.rectangle([(205, 180), (330, 220)], outline=(240, 50, 50), width=2)
    draw.text((340, 192), "<- ELA Splicing Anomaly", fill=(200, 30, 30))

    # Broken MRZ with checksum mismatch
    draw.rectangle([(15, 310), (585, 385)], fill=(255, 245, 245), outline=(220, 80, 80))
    draw.text((25, 325), "I<USAID908129X0<<<<<<<<<<<<<<<", fill=(20, 20, 20))
    draw.text((25, 350), "0401019M2312158USA<<<<<<<<<<<1", fill=(180, 20, 20))

    return _to_base64(img)


def generate_deepfake_face_sample() -> str:
    """Generates synthetic deepfake portrait with visible boundary seam and 2D FFT grid."""
    w, h = 400, 400
    # Create base
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    # Background gradient
    for y in range(h):
        arr[y, :, :] = [int(25 + y * 0.1), int(30 + y * 0.15), int(45 + y * 0.2)]

    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)

    # Attacker's head outline
    draw.ellipse([(100, 80), (300, 320)], fill=(210, 165, 140))
    # Blended face-swap mask (with subtle color border mismatch)
    draw.ellipse([(120, 110), (280, 290)], fill=(230, 185, 155), outline=(180, 120, 100), width=2)

    # Eyes & Mouth
    draw.ellipse([(150, 160), (180, 180)], fill=(50, 40, 40))
    draw.ellipse([(220, 160), (250, 180)], fill=(50, 40, 40))
    draw.ellipse([(170, 240), (230, 260)], fill=(160, 60, 60))

    # Add checkerboard upsampling grid typical of StyleGAN
    img_arr = np.array(img)
    y, x = np.mgrid[0:h, 0:w]
    grid = ((x % 8 == 0) & (y % 8 == 0)).astype(np.uint8) * 35
    img_arr[..., 0] = np.clip(img_arr[..., 0].astype(int) + grid, 0, 255).astype(np.uint8)

    return _to_base64(Image.fromarray(img_arr))


def generate_genuine_face_sample() -> str:
    """Generates clean authentic human portrait with natural skin gradations."""
    w, h = 400, 400
    img = Image.new("RGB", (w, h), color=(30, 38, 52))
    draw = ImageDraw.Draw(img)

    # Natural organic head
    draw.ellipse([(100, 80), (300, 320)], fill=(225, 180, 150))
    # Hair
    draw.chord([(95, 60), (305, 190)], start=180, end=360, fill=(45, 30, 25))

    # Natural organic eyes with specular reflection
    draw.ellipse([(145, 160), (185, 185)], fill=(245, 245, 245))
    draw.ellipse([(155, 165), (175, 180)], fill=(55, 40, 35))
    draw.point((160, 168), fill=(255, 255, 255))  # Corneal reflection

    draw.ellipse([(215, 160), (255, 185)], fill=(245, 245, 245))
    draw.ellipse([(225, 165), (245, 180)], fill=(55, 40, 35))
    draw.point((230, 168), fill=(255, 255, 255))  # Corneal reflection

    # Nose & Smile
    draw.line([(200, 180), (195, 215), (205, 215)], fill=(190, 140, 115), width=2)
    draw.arc([(165, 230), (235, 265)], start=10, end=170, fill=(160, 60, 60), width=3)

    return _to_base64(img)


# Pre-generate demo images
SAMPLE_PASSPORT_B64 = generate_passport_sample()
SAMPLE_FORGED_ID_B64 = generate_forged_id_sample()
SAMPLE_DEEPFAKE_FACE_B64 = generate_deepfake_face_sample()
SAMPLE_GENUINE_FACE_B64 = generate_genuine_face_sample()
