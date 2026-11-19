#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news broadsheet poster (1024x1024 PNG).

All artwork is drawn with PIL shapes; no photos or downloaded images.
Six stories, verified against the day's reporting (AA, Outlook India,
Just Security, Times of India live blogs for 18 November 2026).
"""
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (16, 38, 63)
GOLD = (196, 148, 44)
INK = (24, 24, 24)
GREY = (96, 96, 96)
PANEL_BG = (255, 255, 255)
PANEL_BORDER = (168, 168, 162)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def bold(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)


def regular(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap measured in pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_icon(draw, kind, x, y, s, color):
    """Small pictogram drawn with PIL shapes in a box of side s at (x, y)."""
    if kind == "drone":
        # quad-rotor drone: body + four rotors
        draw.ellipse([x, y, x + s * 0.22, y + s * 0.22], fill=color)
        draw.ellipse([x + s * 0.78, y, x + s, y + s * 0.22], fill=color)
        draw.ellipse([x, y + s * 0.78, x + s * 0.22, y + s], fill=color)
        draw.ellipse([x + s * 0.78, y + s * 0.78, x + s, y + s], fill=color)
        draw.rectangle([x + s * 0.28, y + s * 0.36, x + s * 0.72, y + s * 0.64],
                       fill=color)
        draw.line([x + s * 0.11, y + s * 0.11, x + s * 0.36, y + s * 0.4],
                  fill=color, width=4)
        draw.line([x + s * 0.89, y + s * 0.11, x + s * 0.64, y + s * 0.4],
                  fill=color, width=4)
        draw.line([x + s * 0.11, y + s * 0.89, x + s * 0.36, y + s * 0.6],
                  fill=color, width=4)
        draw.line([x + s * 0.89, y + s * 0.89, x + s * 0.64, y + s * 0.6],
                  fill=color, width=4)
    elif kind == "flags":
        # two meeting flags on poles
        draw.line([x + s * 0.2, y + s * 0.05, x + s * 0.2, y + s * 0.95],
                  fill=color, width=4)
        draw.line([x + s * 0.8, y + s * 0.05, x + s * 0.8, y + s * 0.95],
                  fill=color, width=4)
        draw.polygon([(x + s * 0.2, y + s * 0.08), (x + s * 0.58, y + s * 0.2),
                      (x + s * 0.2, y + s * 0.34)], fill=color)
        draw.polygon([(x + s * 0.8, y + s * 0.08), (x + s * 0.42, y + s * 0.2),
                      (x + s * 0.8, y + s * 0.34)], fill=color)
    elif kind == "quad":
        # four dots in a diamond = four-nation Quad
        cx, cy = x + s / 2, y + s / 2
        r = s * 0.13
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            draw.ellipse([cx + dx * s * 0.3 - r, cy + dy * s * 0.3 - r,
                          cx + dx * s * 0.3 + r, cy + dy * s * 0.3 + r],
                         fill=color)
        draw.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7],
                     outline=color, width=3)
    elif kind == "burst":
        # explosion / impact star
        cx, cy = x + s / 2, y + s / 2
        pts = []
        for i in range(16):
            ang = i * 3.14159 / 8
            rad = s * 0.48 if i % 2 == 0 else s * 0.2
            pts.append((cx + rad * math.cos(ang),
                        cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=color)
        draw.ellipse([cx - s * 0.1, cy - s * 0.1, cx + s * 0.1, cy + s * 0.1],
                     fill=PAPER)
    elif kind == "cyclone":
        # spiral storm: concentric arcs
        cx, cy = x + s / 2, y + s / 2
        for i, rad in enumerate([s * 0.46, s * 0.34, s * 0.22]):
            start = 20 + i * 70
            draw.arc([cx - rad, cy - rad, cx + rad, cy + rad],
                     start=start, end=start + 250, fill=color, width=6)
        draw.ellipse([cx - s * 0.07, cy - s * 0.07, cx + s * 0.07, cy + s * 0.07],
                     fill=color)
    elif kind == "pad":
        # game controller
        draw.rounded_rectangle([x + s * 0.05, y + s * 0.3, x + s * 0.95, y + s * 0.75],
                               radius=int(s * 0.12), fill=color)
        draw.line([x + s * 0.22, y + s * 0.42, x + s * 0.22, y + s * 0.62],
                  fill=PAPER, width=5)
        draw.line([x + s * 0.14, y + s * 0.52, x + s * 0.3, y + s * 0.52],
                  fill=PAPER, width=5)
        for bx, by in [(0.68, 0.46), (0.8, 0.56), (0.68, 0.62), (0.8, 0.44)]:
            draw.ellipse([x + s * bx - 4, y + s * by - 4,
                          x + s * bx + 4, y + s * by + 4], fill=PAPER)


STORIES = [
    ("MIDDLE EAST", "drone",
     "Iran strikes US bases\nin Kuwait",
     "Tehran says its drones hit US Patriot systems and drone and missile "
     "platforms at Ali Al Salem Air Base; Bahrain reports intercepting "
     "drones over its skies."),
    ("DIPLOMACY", "flags",
     "Xi and Putin meet\nin Shenzhen",
     "China and Russia hold talks at the APEC summit, a day before a "
     "first-ever three-way meeting with Trump, who has arrived in China."),
    ("ASIA", "quad",
     "Quad leaders meet\nin Manila",
     "The US, Japan, India and Australia hold their first leaders' "
     "meeting in more than two years, on the sidelines of the ASEAN summit."),
    ("MIDDLE EAST", "burst",
     "Israel launches\nGaza operation",
     "Israel begins what it calls a \u201cconcentrated operation\u201d in three "
     "areas of central Gaza, west of the ceasefire line."),
    ("WEATHER", "cyclone",
     "Cyclone Akvan\nnears India",
     "A severe cyclonic storm strengthens as it approaches Odisha; "
     "families in unsafe homes are moved to shelters."),
    ("CULTURE", "pad",
     "GTA VI launches\nat midnight",
     "Rockstar's blockbuster arrives after a 13-year wait, the most "
     "anticipated game launch in years."),
]


def draw_panel(draw, x, y, w, h, kicker, icon, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG,
                   outline=PANEL_BORDER, width=2)
    # gold kicker bar
    draw.rectangle([x, y, x + w, y + 8], fill=GOLD)
    tx = x + 18
    ty = y + 20
    draw.text((tx, ty), kicker, font=bold(19), fill=NAVY)
    # icon at top right
    draw_icon(draw, icon, x + w - 66, y + 16, 48, NAVY)
    # headline
    hy = ty + 30
    for line in headline.split("\n"):
        draw.text((tx, hy), line, font=bold(29), fill=INK)
        hy += 36
    # body
    by = hy + 8
    for line in wrap(draw, body, regular(20), w - 36):
        draw.text((tx, by), line, font=regular(20), fill=(52, 52, 52))
        by += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # masthead
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    draw.text((32, 22), "THE WORLD IN ONE DAY", font=bold(56), fill=(255, 255, 255))
    draw.text((32, 92), "Wednesday, 18 November 2026", font=regular(30),
              fill=(214, 164, 60))
    draw.rectangle([0, 148, W, 154], fill=GOLD)

    # panels: 2 columns x 3 rows
    margin = 28
    gap = 20
    pw = (W - 2 * margin - gap) // 2
    ph = 248
    top = 172
    for i, (kicker, icon, headline, body) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + 16)
        draw_panel(draw, x, y, pw, ph, kicker, icon, headline, body)

    # footer
    fy = top + 3 * ph + 2 * 16 + 14
    draw.rectangle([margin, fy, W - margin, fy + 2], fill=GOLD)
    draw.text((margin, fy + 12),
              "Six stories from Wednesday, 18 November 2026 \u2014 as reported that day.",
              font=regular(21), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
