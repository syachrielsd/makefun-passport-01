#!/usr/bin/env python3
"""Render an invented passport spread: Republic of Vessalia.

Draws a two-page passport open on a desk, with PIL only, one font family
(DejaVu Sans / DejaVu Sans Mono) throughout. Saves passport.png next to
this file. Deterministic, no network.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FDIR = "/usr/share/fonts/truetype/dejavu"
SANS = f"{FDIR}/DejaVuSans.ttf"
BOLD = f"{FDIR}/DejaVuSans-Bold.ttf"
MONO = f"{FDIR}/DejaVuSansMono.ttf"

W, H = 1024, 724

DESK = (99, 101, 103)
PAGE = (243, 236, 217)
TEAL = (14, 70, 78)
TEAL_DARK = (10, 54, 62)
GUILLOCHE = (168, 199, 192)
GOLD = (196, 164, 96)
CREAM = (246, 242, 231)
LABEL_ON_TEAL = (148, 199, 192)
INK_BLUE = (58, 84, 158)
INK_RED = (168, 52, 48)
INK_DARKRED = (128, 30, 34)


def font(path, size):
    return ImageFont.truetype(path, size)


def ctext(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def guilloche(d, box):
    """Thin repeated wave lines + concentric corner arcs, pale teal."""
    x0, y0, x1, y1 = box
    for yy in range(y0 + 14, y1 - 8, 24):
        pts = []
        for xx in range(x0 + 6, x1 - 5, 6):
            pts.append((xx, yy + 3.2 * math.sin((xx - x0) / 34.0 + yy / 47.0)))
        d.line(pts, fill=GUILLOCHE, width=1)
    for cx, cy in ((x0 + 26, y0 + 26), (x1 - 26, y1 - 26)):
        for r in range(10, 74, 9):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GUILLOCHE, width=1)


def round_stamp(size, lines, ink, angle, ring_text=None):
    """A round ink stamp on a transparent layer, rotated."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = size // 2
    r = c - 8
    col = ink + (168,)
    d.ellipse([c - r, c - r, c + r, c + r], outline=col, width=4)
    d.ellipse([c - r + 11, c - r + 11, c + r - 11, c + r - 11], outline=col, width=2)
    f1 = font(BOLD, 25)
    f2 = font(BOLD, 19)
    f3 = font(BOLD, 23)
    ctext(d, c, c - 46, lines[0], f1, col)
    ctext(d, c, c - 12, lines[1], f2, col)
    ctext(d, c, c + 22, lines[2], f3, col)
    return layer.rotate(angle, resample=Image.BICUBIC)


def rect_stamp(w, h, lines, ink, angle):
    layer = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    col = ink + (185,)
    d.rectangle([6, 6, w + 9, h + 9], outline=col, width=4)
    d.rectangle([13, 13, w + 2, h + 2], outline=col, width=1)
    f = font(BOLD, 21)
    total = len(lines) * 27
    y = (h + 16 - total) // 2 + 2
    for ln in lines:
        ctext(d, (w + 16) // 2, y, ln, f, col)
        y += 27
    return layer.rotate(angle, resample=Image.BICUBIC)


def emblem(d, cx, cy, r):
    """Anchor over waves inside a circle."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], outline=GOLD, width=1)
    # ring + shank
    d.ellipse([cx - 5, cy - r + 12, cx + 5, cy - r + 22], outline=GOLD, width=3)
    d.line([cx, cy - r + 22, cx, cy + r - 20], fill=GOLD, width=3)
    # crossbar
    d.line([cx - 13, cy - r + 32, cx + 13, cy - r + 32], fill=GOLD, width=3)
    # flukes
    d.arc([cx - 16, cy - 2, cx, cy + r - 12], start=270, end=360, fill=GOLD, width=3)
    d.arc([cx, cy - 2, cx + 16, cy + r - 12], start=180, end=270, fill=GOLD, width=3)
    # waves
    for k, wy in enumerate((cy + r - 14, cy + r - 8)):
        pts = [(x, wy + 2.2 * math.sin((x - cx) / 6.0 + k * 1.7))
               for x in range(cx - 17, cx + 18, 2)]
        d.line(pts, fill=GOLD, width=2)


def portrait(d, box):
    """Flat illustrated portrait: dignified harbour pilot."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(186, 196, 198))
    cx = (x0 + x1) // 2
    # shoulders / jacket
    d.polygon([(x0 + 12, y1), (x0 + 30, y0 + 118), (cx - 16, y0 + 104),
               (cx + 16, y0 + 104), (x1 - 30, y0 + 118), (x1 - 12, y1)],
              fill=(34, 39, 54))
    # shirt + tie
    d.polygon([(cx - 15, y0 + 106), (cx + 15, y0 + 106), (cx, y1)], fill=(238, 236, 228))
    d.polygon([(cx - 5, y0 + 112), (cx + 5, y0 + 112), (cx + 3, y0 + 150),
               (cx, y0 + 158), (cx - 3, y0 + 150)], fill=(120, 32, 36))
    # neck + head
    d.rectangle([cx - 11, y0 + 82, cx + 11, y0 + 110], fill=(214, 172, 138))
    d.ellipse([cx - 30, y0 + 22, cx + 30, y0 + 96], fill=(226, 182, 148))
    # hair
    d.pieslice([cx - 31, y0 + 12, cx + 31, y0 + 66], start=180, end=360,
               fill=(74, 62, 54))
    d.rectangle([cx - 31, y0 + 38, cx - 25, y0 + 58], fill=(74, 62, 54))
    d.rectangle([cx + 25, y0 + 38, cx + 31, y0 + 58], fill=(74, 62, 54))
    # calm face: brows, eyes, nose, straight mouth
    d.line([cx - 19, y0 + 56, cx - 7, y0 + 55], fill=(60, 48, 40), width=2)
    d.line([cx + 7, y0 + 55, cx + 19, y0 + 56], fill=(60, 48, 40), width=2)
    d.line([cx - 17, y0 + 63, cx - 9, y0 + 63], fill=(40, 36, 34), width=2)
    d.line([cx + 9, y0 + 63, cx + 17, y0 + 63], fill=(40, 36, 34), width=2)
    d.line([cx, y0 + 64, cx - 2, y0 + 74], fill=(196, 150, 116), width=2)
    d.line([cx - 10, y0 + 84, cx + 10, y0 + 84], fill=(150, 92, 84), width=2)
    d.rectangle(box, outline=GOLD, width=2)


def field(d, x, y, label, value, lab_f, val_f, lab_col, val_col):
    d.text((x, y), label, font=lab_f, fill=lab_col)
    d.text((x, y + 13), value, font=val_f, fill=val_col)


def main():
    img = Image.new("RGB", (W, H), DESK)
    d = ImageDraw.Draw(img, "RGBA")

    # book shadow + pages
    d.rounded_rectangle([24, 30, 1000, 696], radius=10, fill=(58, 59, 61))
    d.rectangle([32, 36, 512, 688], fill=PAGE)
    d.rectangle([512, 36, 992, 688], fill=PAGE)

    guilloche(d, (32, 36, 512, 688))
    guilloche(d, (512, 36, 992, 688))

    # centre spine shadow
    for i in range(26):
        a = int(105 * (1 - i / 26))
        d.line([512 - 26 + i, 36, 512 - 26 + i, 688], fill=(70, 66, 58, a))
        d.line([512 + 26 - i, 36, 512 + 26 - i, 688], fill=(70, 66, 58, a))

    # ---------- LEFT PAGE: teal data panel ----------
    d.rounded_rectangle([50, 54, 494, 670], radius=8, fill=TEAL)
    d.rounded_rectangle([50, 54, 494, 670], radius=8, outline=TEAL_DARK, width=2)

    emblem(d, 96, 104, 31)
    d.text((140, 78), "REPUBLIC OF VESSALIA", font=font(BOLD, 20), fill=CREAM)
    d.text((141, 106), "PASSPORT / PASSEPORT", font=font(SANS, 12),
           fill=LABEL_ON_TEAL)
    d.text((141, 124), "Maritime Republic — Est. 1911", font=font(SANS, 10),
           fill=LABEL_ON_TEAL)
    d.line([66, 142, 478, 142], fill=GOLD, width=2)

    portrait(d, (66, 152, 216, 342))

    lab_f = font(SANS, 10)
    val_f = font(BOLD, 15)
    rows = [
        ("SURNAME", "MARIN"),
        ("GIVEN NAMES", "ELIO TOMAS"),
        ("NATIONALITY", "VESSALIAN"),
        ("DATE OF BIRTH", "02 MAY 1984"),
        ("PLACE OF BIRTH", "PORT SEREIN"),
        ("PROFESSION", "HARBOUR PILOT"),
    ]
    y = 154
    for lab, val in rows:
        field(d, 232, y, lab, val, lab_f, val_f, LABEL_ON_TEAL, CREAM)
        y += 32

    d.line([66, 356, 478, 356], fill=(LABEL_ON_TEAL + (120,)), width=1)
    field(d, 66, 366, "DATE OF ISSUE", "14 MAR 2021", lab_f, val_f,
          LABEL_ON_TEAL, CREAM)
    field(d, 282, 366, "DATE OF EXPIRY", "14 MAR 2031", lab_f, val_f,
          LABEL_ON_TEAL, CREAM)
    field(d, 66, 404, "PASSPORT No", "VS 0044171", lab_f, font(BOLD, 17),
          LABEL_ON_TEAL, CREAM)
    field(d, 282, 404, "LANGUAGES", "Vessalian / English", lab_f,
          font(SANS, 13), LABEL_ON_TEAL, CREAM)

    # bearer signature squiggle
    d.text((66, 448), "SIGNATURE OF BEARER", font=lab_f, fill=LABEL_ON_TEAL)
    pts = [(x, 486 + 7 * math.sin((x - 66) / 9.0) * math.exp(-(x - 66) / 190.0))
           for x in range(66, 300, 3)]
    d.line(pts, fill=CREAM, width=2)
    d.line([66, 500, 300, 500], fill=(LABEL_ON_TEAL + (120,)), width=1)

    # machine-readable zone
    d.rectangle([62, 540, 482, 652], fill=(238, 232, 210))
    line1 = "P<VESMARIN<<ELIO<TOMAS<<<<<<<<<<<<<<<<<<<"
    line2 = "VS0044171<2VES840502M3103142<<<<<<<<<<<<04"
    n = max(len(line1), len(line2))
    line1 = line1.ljust(n, "<")[:n]
    line2 = line2.ljust(n, "<")[:n]
    mrz_f = font(MONO, 15)
    d.text((72, 562), line1, font=mrz_f, fill=(38, 38, 38))
    d.text((72, 606), line2, font=mrz_f, fill=(38, 38, 38))

    # ---------- RIGHT PAGE: visas ----------
    d.text((540, 58), "VISAS", font=font(BOLD, 23), fill=TEAL)
    d.text((541, 90), "Vessalian Consular Service", font=font(SANS, 11),
           fill=(110, 104, 92))
    d.line([540, 112, 964, 112], fill=TEAL, width=2)
    d.text((946, 648), "24", font=font(SANS, 12), fill=(110, 104, 92))

    rect = rect_stamp(360, 52, ["BEARER MAY REMAIN UNTIL", "THE TIDE RETURNS"],
                      INK_DARKRED, -3)
    img.paste(rect, (592, 128), rect)

    s1 = round_stamp(210, ["ARRIVED", "PORT SEREIN", "03 JUN 2023"], INK_BLUE, -8)
    img.paste(s1, (548, 218), s1)

    s3 = round_stamp(226, ["ALDOVIA", "KINGDOM · ENTRY", "04 JUN 2023"],
                     (84, 66, 148), 4)
    img.paste(s3, (742, 232), s3)

    s2 = round_stamp(210, ["DEPARTED", "PORT SEREIN", "18 JUN 2023"], INK_RED, 6)
    img.paste(s2, (636, 442), s2)

    d.text((540, 648), "This page is reserved for visas and endorsements.",
           font=font(SANS, 10), fill=(110, 104, 92))

    img.save(HERE / "passport.png")
    print("passport.png", (HERE / "passport.png").stat().st_size, "bytes")


if __name__ == "__main__":
    main()
