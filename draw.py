#!/usr/bin/env python3
"""The World in One Day — Saturday 21 November 2026.

One 1024x1024 picture that sums up the day's world news, drawn with
Pillow from flat shapes and type. Twenty-eight stories are named below
— one lead, eight cards and nineteen one-line briefs — and every one
was reported on 21 November 2026; nothing here is photographed and
nothing is AI-generated. The layout is checked as it draws: each text
block asserts it fits its box, so a too-long headline fails loudly
instead of spilling over the edge.

Run:  python3 draw.py        -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 44
GUTTER = 16

PAPER = (246, 241, 231)     # warm newsprint
NAVY = (15, 34, 66)         # masthead / lead / footer
INK = (22, 26, 36)          # body headlines
SLATE = (98, 106, 120)      # decks and captions
CARD_BG = (255, 255, 255)
CARD_RULE = (214, 208, 194)
GOLD = (217, 164, 65)
CRIMSON = (176, 42, 60)
PALE = (196, 210, 232)      # light text on navy
WHITE = (255, 255, 255)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, font, fill, max_width, leading, max_lines):
    """Draw wrapped text inside a box; assert it fits; return bottom y."""
    x, y = xy
    lines = wrap_text(draw, text, font, max_width)
    assert len(lines) <= max_lines, f"text overflows ({len(lines)} lines): {text[:48]!r}"
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---- the day's stories -------------------------------------------------
LEAD = {
    "kicker": "KYIV & WARSAW  •  WAR IN EUROPE",
    "headline": "Russia's Biggest Barrage Yet — Missiles Land in Poland",
    "deck": "400+ drones and 110 missiles hit Ukraine; two missiles and a "
            "suspected drone come down in Poland. PM Tusk calls it a "
            "deliberate provocation.",
}

STORIES = [
    {
        "kicker": "NEW YORK  •  MARKETS",
        "accent": CRIMSON,
        "headline": "AI Sell-Off Drags S&P 500 Into Correction",
        "deck": "Nasdaq falls 5.28%; Nvidia drops about 14%.",
    },
    {
        "kicker": "THE HAGUE",
        "accent": (0, 108, 108),
        "headline": "World Court: Myanmar Guilty of Rohingya Genocide",
        "deck": "The ICJ finds Myanmar responsible for genocide.",
    },
    {
        "kicker": "ANTALYA, TURKEY",
        "accent": (26, 120, 60),
        "headline": "COP31 Talks Run Past Deadline on Fossil Fuels",
        "deck": "Nearly 200 nations fail to agree; summit in overtime.",
    },
    {
        "kicker": "WASHINGTON",
        "accent": (104, 60, 160),
        "headline": "FBI Crime Database Hacked",
        "deck": "Law-enforcement database breached; outages continue.",
    },
    {
        "kicker": "LONDON  •  HEALTH",
        "accent": (150, 40, 90),
        "headline": "Cancer Pill Makes Tumours Undetectable in 1 in 12",
        "deck": "Daraxonrasib trial brings hope for pancreatic cancer.",
    },
    {
        "kicker": "THE ANDES, PERU",
        "accent": (140, 100, 20),
        "headline": "Magnitude 6.8 Quake Shakes the Peruvian Andes",
        "deck": "Tremors felt in Lima, 320 km from the epicentre.",
    },
    {
        "kicker": "SAN FRANCISCO  •  SCIENCE",
        "accent": (30, 90, 170),
        "headline": "Anthropic: Claude Solved Maths' Greatest Riddle",
        "deck": "Riemann riddle stood 160 years; experts check proof.",
    },
    {
        "kicker": "TEHRAN  •  DIPLOMACY",
        "accent": (170, 90, 20),
        "headline": "Iran Seeks Diplomacy; Trump Rejects Its Terms",
        "deck": "Tehran seeks talks; Trump weighs new strikes.",
    },
]

# One-line briefs for the footer band: (place, headline).
BRIEFS = [
    ("SHENZHEN", "Trump hails summit with Xi, Putin"),
    ("BRUSSELS", "UK and EU sign biggest post-Brexit deals"),
    ("BERLIN", "Gen Z protests sweep 25 countries"),
    ("NEW YORK", "Mamdani sets 2032 to close Rikers Island"),
    ("GENEVA", "Nations open path to a 'killer robots' pact"),
    ("WASHINGTON", "Trump ousts cyber chief over outages"),
    ("TOYOTA CITY", "Honda, Toyota recall 1.6m vehicles"),
    ("TOKYO", "Japan core inflation rises to 2.2% in October"),
    ("LOS ANGELES", "Man convicted in deadly Palisades fire"),
    ("HAITI", "Salvadoran soldiers killed by explosives"),
    ("GAZA", "Israeli strikes kill more Palestinians"),
    ("PARIS", "Senate approves 'licence to kill' police law"),
    ("TALLINN", "Estonia to shut Russia border crossings Dec 1"),
    ("MADRID", "Spain votes Nov 29 as conservatives gain"),
    ("NEW DELHI", "Pakistan minister in India for SCO dialogue"),
    ("MUNICH", "Kane out for months with torn ankle ligament"),
    ("LAS VEGAS", "Russell on pole for Las Vegas Grand Prix"),
    ("TURIN", "Alcaraz unbeaten into ATP Finals semi-finals"),
    ("WELLINGTON", "Rahul ton puts India in charge vs NZ"),
]

assert 1 + len(STORIES) + len(BRIEFS) == 28, "the edition must hold 28 stories"


def draw_masthead(draw):
    """Navy band, gold rule, title, date and tagline."""
    draw.rectangle([0, 0, SIZE, 132], fill=NAVY)
    draw.rectangle([0, 132, SIZE, 138], fill=GOLD)
    draw.text((MARGIN, 14), "THE WORLD IN ONE DAY",
              font=load_font(BOLD_PATH, 24), fill=GOLD)
    draw.text((MARGIN, 40), "SATURDAY 21 NOVEMBER 2026",
              font=load_font(BOLD_PATH, 46), fill=WHITE)
    draw.text((MARGIN, 100), "The day's biggest stories, in one picture — 28 reports",
              font=load_font(REG_PATH, 19), fill=PALE)


def draw_lead(draw):
    """The big navy panel for the day's top story."""
    top, bottom = 146, 330
    draw.rounded_rectangle([36, top, 988, bottom], radius=18, fill=NAVY)
    draw.rectangle([36, top, 52, bottom], fill=CRIMSON)
    draw.text((72, 160), LEAD["kicker"],
              font=load_font(BOLD_PATH, 19), fill=GOLD)
    draw.rectangle([72, 186, 172, 190], fill=GOLD)
    end_y = draw_wrapped(draw, (72, 198), LEAD["headline"],
                         load_font(BOLD_PATH, 32), WHITE, 880, 39, 2)
    draw_wrapped(draw, (72, end_y + 8), LEAD["deck"],
                 load_font(REG_PATH, 18), PALE, 880, 23, 2)


def draw_card(draw, box, index, story):
    """One white story card: numbered, accent strip, kicker, headline, deck."""
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12,
                           fill=CARD_BG, outline=CARD_RULE, width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=story["accent"])
    draw.text((x + 20, y + 12), f"{index:02d}  •  {story['kicker']}",
              font=load_font(BOLD_PATH, 14), fill=story["accent"])
    draw_wrapped(draw, (x + 20, y + 30), story["headline"],
                 load_font(BOLD_PATH, 20), INK, w - 40, 23, 2)
    draw_wrapped(draw, (x + 20, y + 76), story["deck"],
                 load_font(REG_PATH, 14), SLATE, w - 40, 17, 1)


def draw_grid(draw):
    """Two columns, four rows of story cards."""
    card_w, card_h = 466, 98
    x0, y0 = 36, 344
    for i, story in enumerate(STORIES):
        cx = x0 + (i % 2) * (card_w + GUTTER)
        cy = y0 + (i // 2) * (card_h + 12)
        draw_card(draw, (cx, cy, card_w, card_h), i + 1, story)
    return y0 + 4 * card_h + 3 * 12


def draw_briefs(draw, top):
    """Navy strip: the rest of the day as two columns of one-line briefs."""
    draw.rectangle([0, top, SIZE, SIZE], fill=NAVY)
    draw.text((MARGIN, top + 12), "ALSO TODAY — IN BRIEF",
              font=load_font(BOLD_PATH, 17), fill=GOLD)
    place_font = load_font(BOLD_PATH, 15)
    text_font = load_font(REG_PATH, 15)
    col_x = (MARGIN, 528)
    col_w = 452
    rows_y = top + 42
    half = (len(BRIEFS) + 1) // 2
    for col, chunk in enumerate((BRIEFS[:half], BRIEFS[half:])):
        for row, (place, headline) in enumerate(chunk):
            y = rows_y + row * 18.5
            label = place + "  —  "
            draw.text((col_x[col], y), label, font=place_font, fill=GOLD)
            label_w = draw.textlength(label, font=place_font)
            draw.text((col_x[col] + label_w, y), headline,
                      font=text_font, fill=WHITE)
            total = label_w + draw.textlength(headline, font=text_font)
            assert total <= col_w, f"brief overflows: {place} {headline!r}"


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    grid_bottom = draw_grid(draw)
    draw_briefs(draw, grid_bottom + 16)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
