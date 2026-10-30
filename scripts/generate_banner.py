# -*- coding: utf-8 -*-
"""Render a GitHub-safe PNG banner (SVG often fails on profile pages)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "banner.png"

W, H = 1600, 460
BG = (7, 12, 22)
ACCENT = (34, 211, 238)
ACCENT_2 = (59, 130, 246)
WHITE = (248, 250, 252)
MUTED = (148, 163, 184)
SUB = (203, 213, 225)
CHIP_BG = (15, 39, 68)
CHIP_BORDER = (34, 211, 238)


def font(size, bold=False):
    names = (
        ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"]
        if bold
        else ["segoeui.ttf", "arial.ttf", "calibri.ttf"]
    )
    for name in names:
        path = Path(r"C:\Windows\Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def chip(draw, xy, text, font_obj):
    x, y = xy
    pad_x, pad_y = 22, 10
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    w, h = tw + pad_x * 2, th + pad_y * 2
    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=20,
        fill=CHIP_BG,
        outline=CHIP_BORDER,
        width=2,
    )
    draw.text((x + pad_x, y + pad_y - 2), text, font=font_obj, fill=WHITE)
    return w + 16


def main():
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw = ImageDraw.Draw(img, "RGBA")

    for x in range(0, W, 120):
        draw.line((x, 0, x, H), fill=(30, 58, 95, 70), width=1)
    for y in range(0, H, 80):
        draw.line((0, y, W, y), fill=(30, 58, 95, 70), width=1)

    draw.ellipse((1140, -30, 1500, 330), fill=(34, 211, 238, 28))
    draw.ellipse((1340, 220, 1580, 460), fill=(59, 130, 246, 32))
    draw.rectangle((0, 0, 10, H), fill=ACCENT)

    nodes = [(1180, 120), (1288, 168), (1410, 128), (1488, 210), (1380, 268), (1270, 236)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 4)]
    for a, b in edges:
        draw.line((nodes[a], nodes[b]), fill=ACCENT, width=2)
    for i, (nx, ny) in enumerate(nodes):
        r = 8 if i == 1 else 6
        draw.ellipse((nx - r, ny - r, nx + r, ny + r), fill=ACCENT)

    for i, sx in enumerate((1238, 1340, 1442)):
        sy = 300 if i != 1 else 318
        draw.rounded_rectangle(
            (sx, sy, sx + 86, sy + 54),
            radius=8,
            fill=(11, 18, 32),
            outline=ACCENT_2,
            width=2,
        )
        draw.rounded_rectangle((sx + 14, sy + 14, sx + 72, sy + 20), radius=3, fill=ACCENT)
        draw.rounded_rectangle((sx + 14, sy + 28, sx + 54, sy + 34), radius=3, fill=ACCENT)

    title = font(72, bold=True)
    kicker = font(18, bold=True)
    subtitle = font(26)
    body = font(20)
    chip_font = font(16)

    draw.text((64, 68), "DHAKA, BANGLADESH  |  12+ YEARS", font=kicker, fill=ACCENT)
    draw.text((64, 108), "Nur Islam", font=title, fill=WHITE)
    draw.rounded_rectangle((68, 202, 288, 208), radius=3, fill=ACCENT)
    draw.text((64, 224), "CTO at SOFT HAB  |  Founder & CEO of HOST HAB", font=subtitle, fill=SUB)
    draw.text(
        (64, 270),
        "Linux SysAdmin  |  DevOps  |  Cloud  |  WHMCS  |  Full-Stack Engineering",
        font=body,
        fill=MUTED,
    )

    x = 64
    for label in ("cPanel / WHM", "AWS", "WHMCS", "WordPress", "Laravel", "SSL"):
        x += chip(draw, (x, 340), label, chip_font)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print("wrote %s (%s bytes)" % (OUT, OUT.stat().st_size))


if __name__ == "__main__":
    main()
