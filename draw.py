#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news summary image (1024x1024 PNG).

Every story below was reported on 21 November 2026. The picture is drawn,
not photographed: flat shapes and big type that stay legible when the
judge sees the image small. Run: python3 draw.py -> writes entry.png.
Layout is measured: each block asserts it fits its box before drawing.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
PAPER = (247, 243, 234)
NAVY = (13, 32, 64)
INK = (24, 28, 38)
GOLD = (232, 178, 60)
RED = (178, 34, 52)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
GREY = (96, 104, 118)
LEAD_SUB = (196, 210, 232)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, text, fnt, fill, width, leading, max_lines):
    """Draw wrapped text; assert it fits the line budget, return end y."""
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    assert len(lines) <= max_lines, f"overflow ({len(lines)} lines): {text[:40]}"
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)

# ---- header: the day, named big ------------------------------------------
d.rectangle([0, 0, W, 158], fill=NAVY)
d.rectangle([0, 158, W, 166], fill=GOLD)
d.text((44, 22), "THE WORLD IN ONE DAY", font=font(BOLD, 29), fill=GOLD)
d.text((44, 56), "SATURDAY 21 NOVEMBER 2026", font=font(BOLD, 54), fill=WHITE)
d.text((44, 124), "The day's biggest stories, in one picture", font=font(REG, 23), fill=(178, 196, 224))

# ---- lead story: Russia's barrage, missiles land in Poland ----------------
d.rounded_rectangle([36, 182, 988, 390], radius=18, fill=NAVY)
d.rectangle([36, 182, 52, 390], fill=RED)
d.text((76, 200), "KYIV & WARSAW  •  WAR IN EUROPE", font=font(BOLD, 24), fill=GOLD)
y = block(d, (76, 230), "Russia's Biggest Barrage Yet — Missiles Land in Poland",
          font(BOLD, 39), WHITE, 876, 47, 2)
block(d, (76, y + 8), "400+ drones and 110 missiles hit Ukraine; two missiles and a suspected drone come down in Poland. PM Tusk calls it a deliberate provocation.",
      font(REG, 22), LEAD_SUB, 876, 29, 2)

# ---- story cards: two columns, three rows ----------------------------------
CARDS = [
    ("NEW YORK  •  MARKETS", RED,
     "AI Sell-Off Drags S&P 500 Into Correction",
     "Nasdaq falls 5.28%; Nvidia drops about 14%."),
    ("THE HAGUE", (0, 110, 110),
     "World Court: Myanmar Guilty of Rohingya Genocide",
     "The ICJ finds Myanmar responsible for genocide."),
    ("ANTALYA, TURKEY", (24, 122, 62),
     "COP31 Talks Run Past Deadline on Fossil Fuels",
     "Nearly 200 nations fail to agree; summit goes into overtime."),
    ("WASHINGTON", (104, 60, 160),
     "FBI Crime Database Hacked",
     "Nationwide law-enforcement database breached; US outages continue."),
    ("LONDON  •  HEALTH", (150, 40, 90),
     "Cancer Pill Makes Tumours Undetectable in 1 in 12",
     "Daraxonrasib trial brings hope for pancreatic cancer."),
    ("THE ANDES, PERU", (140, 100, 20),
     "Magnitude 6.8 Quake Shakes the Peruvian Andes",
     "Tremors felt in Lima, 320 km from the epicentre."),
]

x0, y0, cw, ch, gap = 36, 406, 466, 150, 16
for i, (kicker, colour, head, sub) in enumerate(CARDS):
    cx = x0 + (i % 2) * (cw + gap)
    cy = y0 + (i // 2) * (ch + gap)
    d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=14, fill=CARD, outline=(216, 210, 196), width=2)
    d.rectangle([cx, cy, cx + cw, cy + 9], fill=colour)
    d.text((cx + 22, cy + 18), kicker, font=font(BOLD, 19), fill=colour)
    y = block(d, (cx + 22, cy + 42), head, font(BOLD, 25), INK, cw - 44, 29, 2)
    block(d, (cx + 22, cy + 96), sub, font(REG, 19), GREY, cw - 44, 22, 2)

# ---- footer: also today ------------------------------------------------------
fy = y0 + 3 * ch + 2 * gap + 16
d.rectangle([0, fy, W, W], fill=NAVY)
d.text((44, fy + 14), "ALSO TODAY", font=font(BOLD, 21), fill=GOLD)
block(d, (44, fy + 44),
      "Trump hails Shenzhen summit as unprecedented  •  UK and EU sign biggest post-Brexit deals  •  Gen Z protests sweep 25 countries  •  Mamdani sets 2032 to close Rikers Island",
      font(REG, 21), WHITE, 936, 27, 2)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
