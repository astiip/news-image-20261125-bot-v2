"""The Wednesday Herald -- news-image-20261125 (v2).

Draws one 1024x1024 newspaper front page for Wednesday 25 November
2026 with PIL only. No network, no randomness, no timestamps: the same
code always writes the same bytes.

Layout (top to bottom): navy masthead, ticker, three illustrated
leads, six-number stat strip, Saturday-to-Wednesday timeline, eight
cards (4-11) each with a small coded scene, a 21-item index (12-32),
a dotted world map with 11 numbered pins, a DATE CHECK box and a
footer. All 32 stories carry a date; the DATE CHECK box groups every
non-Wednesday story by day and is generated from STORIES, so the
counts can never drift from the story list.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 16

PAPER = (247, 241, 222)
PANEL = (255, 253, 244)
INK = (28, 36, 54)
NAVY = (20, 33, 61)
NAVY2 = (27, 42, 74)
GOLD = (217, 164, 65)
RED = (179, 39, 30)
GREEN = (30, 122, 76)
TEAL = (23, 122, 82)
MUTED = (90, 90, 82)
LINE = (120, 110, 90)
YELLOW_BOX = (253, 243, 192)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


# ---------------------------------------------------------------- data

# day codes: WED 25 NOV, TUE 24 NOV, MON 23 NOV, SUN 22 NOV, SAT 21 NOV,
# FRI 20 NOV. "short" is the label used in the DATE CHECK box.
STORIES = [
    {"n": 1, "title": "Hormuz mines lift oil past $91", "date": "WED 25 NOV",
     "day": "WED", "short": "Hormuz mines lift oil",
     "pill": "REPORTED", "source": "Reuters · DeepDraft",
     "deck": "Iran says a container ship hit a mine near the strait; Brent "
             "settles $91.40, up $2.03. UKMTO logged a three-ship strike on "
             "23 Nov; no authority confirms the mine claims."},
    {"n": 2, "title": "700,000 Russian soldiers killed, new count says",
     "date": "WED 25 NOV", "day": "WED", "short": "700,000 Russian dead",
     "pill": "REPORTED", "source": "RFE/RL",
     "deck": "A new analysis puts Russian soldiers killed above 700,000, "
             "nearly five years in. No official toll confirms it."},
    {"n": 3, "title": "Banten toll hits 26 as search goes on",
     "date": "TUE 24 NOV", "day": "TUE", "short": "Banten toll 26",
     "pill": "CONFIRMED", "source": "AP · Xinhua",
     "deck": "26 candy-factory workers confirmed dead Tuesday; most died "
             "on the second floor, trying to reach the exit. 8 still missing."},
    {"n": 4, "title": "Houthi drone hits Riyadh tower", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Riyadh drone, 11 hurt",
     "body": "Drone strike wounds 11 in the capital; TUE 24 NOV · "
             "Saudi civil defence", "scene": "riyadh"},
    {"n": 5, "title": "Huawei convicted in US trial", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Huawei convicted",
     "body": "Guilty on trade-secret counts over Iran business; "
             "racketeering cleared. TUE 24 NOV", "scene": "court"},
    {"n": 6, "title": "Zelenskyy confirms ship strikes", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Zelenskyy ship strikes",
     "body": "Kyiv hit a cargo ship off Finland and sank a warship off "
             "Benghazi. TUE 24 NOV", "scene": "ship"},
    {"n": 7, "title": "Trump gives Giuliani top medal", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Giuliani medal",
     "body": "Medal of Freedom for the ex-mayor; TUE 24 NOV · "
             "ex-lawyer 'very humbled'", "scene": "medal"},
    {"n": 8, "title": "Sarkozy case goes to trial", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Sarkozy trial",
     "body": "Ex-president and wife Carla Bruni face trial; TUE 24 NOV · "
             "first hearing 1 Apr 2027", "scene": "scales"},
    {"n": 9, "title": "COP31 collapses, no deal", "date": "SUN 22 NOV",
     "day": "SUN", "short": "COP31",
     "body": "Two weeks of talks end with no final text. SUN 22 NOV · "
             "text silent on fossil fuels", "scene": "hall"},
    {"n": 10, "title": "Nvidia jumps 31.5% on Huang", "date": "MON 23 NOV",
     "day": "MON", "short": "Nvidia +31.5%",
     "body": "Best day in 23 years as the CEO returns; MON 23 NOV · "
             "~$1tn in value regained", "scene": "chipchart"},
    {"n": 11, "title": "NATO sends jets to Poland", "date": "TUE 24 NOV",
     "day": "TUE", "short": "NATO jets",
     "body": "Early-warning aircraft after Russian missiles land in "
             "Poland. TUE 24 NOV", "scene": "jets"},
    {"n": 12, "title": "Fort Hood shooter seeks stay of execution",
     "date": "TUE 24 NOV", "day": "TUE", "short": "Fort Hood stay"},
    {"n": 13, "title": "CIA, ODNI hit in cyber breach", "date": "TUE 24 NOV",
     "day": "TUE", "short": "CIA breach"},
    {"n": 14, "title": "Trump pardons turkeys Freedom, Feathers",
     "date": "TUE 24 NOV", "day": "TUE", "short": "turkeys pardoned"},
    {"n": 15, "title": "US envoy: Israel aid may run on", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Israel aid may run on"},
    {"n": 16, "title": "24 civilians killed in S. Sudan attack",
     "date": "TUE 24 NOV", "day": "TUE", "short": "S. Sudan"},
    {"n": 17, "title": "UN flags Gaza aid hardship", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Gaza aid"},
    {"n": 18, "title": "EU adds sanctions on Russia", "date": "TUE 24 NOV",
     "day": "TUE", "short": "EU sanctions"},
    {"n": 19, "title": "US sanctions Iran shadow banks", "date": "TUE 24 NOV",
     "day": "TUE", "short": "Iran sanctions"},
    {"n": 20, "title": "England level T20I series, win by 8 wickets",
     "date": "TUE 24 NOV", "day": "TUE", "short": "England win"},
    {"n": 21, "title": "Tajikistan quits ICC, out in 2027",
     "date": "MON 23 NOV", "day": "MON", "short": "Tajikistan"},
    {"n": 22, "title": "India–NZ Test ends in draw", "date": "MON 23 NOV",
     "day": "MON", "short": "India–NZ draw"},
    {"n": 23, "title": "Kushner floats NATO-like Ukraine vow",
     "date": "SUN 22 NOV", "day": "SUN", "short": "Kushner vow"},
    {"n": 24, "title": "Verstappen wins Las Vegas GP", "date": "SAT 21 NOV",
     "day": "SAT", "short": "Verstappen"},
    {"n": 25, "title": "Alcaraz wins ATP Finals, beats Zverev",
     "date": "SUN 22 NOV", "day": "SUN", "short": "Alcaraz"},
    {"n": 26, "title": "Miley Cyrus marries Maxx Morando",
     "date": "SUN 22 NOV", "day": "SUN", "short": "Miley"},
    {"n": 27, "title": "Istanbul protests over media closures",
     "date": "SUN 22 NOV", "day": "SUN", "short": "Istanbul"},
    {"n": 28, "title": "El Chapo Isidro captured in Jalisco",
     "date": "FRI 20 NOV", "day": "FRI", "short": "El Chapo"},
    {"n": 29, "title": "US jobless rate falls to 4.4%", "date": "FRI 20 NOV",
     "day": "FRI", "short": "US jobless 4.4%"},
    {"n": 30, "title": "Anthropic makes record IPO debut",
     "date": "FRI 20 NOV", "day": "FRI", "short": "Anthropic IPO"},
    {"n": 31, "title": "Sunrise on the Reaping tops box office",
     "date": "SUN 22 NOV", "day": "SUN", "short": "Sunrise box office"},
    {"n": 32, "title": "Liverpool 4–0 Man Utd", "date": "SUN 22 NOV",
     "day": "SUN", "short": "Liverpool"},
]

STATS = [
    ("$91.40", "BRENT CRUDE"),
    ("700,000", "RUSSIAN DEAD"),
    ("26", "BANTEN DEAD"),
    ("11", "HURT IN RIYADH"),
    ("+31.5%", "NVIDIA MONDAY"),
    ("185", "ENGLAND CHASE"),
]

TIMELINE = [
    ("SAT 21 NOV", ["Banten fire breaks out", "Verstappen wins Las Vegas GP",
                    "Lisbon marches over living costs"]),
    ("SUN 22 NOV", ["COP31 collapses, no deal", "Alcaraz wins ATP Finals",
                    "Liverpool 4–0 Man Utd", "Kushner floats NATO-like vow"]),
    ("MON 23 NOV", ["Huang returns to Nvidia", "Russian missiles enter Poland",
                    "India, NZ draw Test"]),
    ("WED 25 NOV", ["Hormuz mines lift oil past $91",
                    "700,000 Russian dead in new count",
                    "Banten toll confirmed at 26",
                    "Houthi drone hits Riyadh tower"]),
]

# Pins: (story number, place, lon, lat). London/Paris nudged a little
# apart on the map so the two pins do not sit on top of each other.
PINS = [
    (1, "Hormuz", 56.5, 26.5, 209, 41),
    (6, "Kyiv", 30.5, 50.5, 185, 21),
    (6, "Benghazi", 20.1, 32.1, 175, 36),
    (4, "Riyadh", 46.7, 24.7, 200, 43),
    (3, "Banten", 106.1, -6.1, 255, 69),
    (22, "Delhi", 77.2, 28.6, 228, 39),
    (8, "Paris", 2.35, 48.85, 164, 26),
    (7, "Washington", -77.0, 38.9, 86, 31),
    (24, "Las Vegas", -115.1, 36.2, 51, 33),
    (9, "Antalya", 30.7, 36.9, 185, 32),
    (20, "London", -0.1, 51.5, 150, 14),
]

# Day order used by the DATE CHECK box (newest first, Wednesday excluded).
DAY_ORDER = ["TUE", "MON", "SUN", "SAT", "FRI"]
DAY_LABEL = {"TUE": "TUE 24 NOV", "MON": "MON 23 NOV", "SUN": "SUN 22 NOV",
             "SAT": "SAT 21 NOV", "FRI": "FRI 20 NOV"}


def date_check_groups():
    """Non-Wednesday stories grouped by day, in story order."""
    groups = {d: [] for d in DAY_ORDER}
    for s in STORIES:
        if s["day"] != "WED":
            groups[s["day"]].append(s["short"])
    return groups


def date_check_lines():
    """Text lines for the DATE CHECK box (TUE may wrap to two lines)."""
    groups = date_check_groups()
    lines = []
    tue = "TUE: " + " · ".join(groups["TUE"])
    lines.append(tue)
    lines.append("MON: " + " · ".join(groups["MON"]) + "   ·   SUN: "
                 + " · ".join(groups["SUN"]))
    lines.append("SAT: " + " · ".join(groups["SAT"]) + "   ·   FRI: "
                 + " · ".join(groups["FRI"]))
    return lines


# ---------------------------------------------------------------- helpers

def wrap(d, text, font, max_w, max_lines=None):
    """Greedy word wrap; truncate with an ellipsis past max_lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "…", font=font) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def pill(d, x, y, text, fill):
    f = F(SANS_B, 11)
    w = int(d.textlength(text, font=f)) + 16
    h = 17
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=fill)
    d.text((x + w / 2, y + h / 2), text, font=f, fill=(255, 255, 255),
           anchor="mm")
    return w


def num_badge(d, x, y, n, r=9):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    d.text((x, y), str(n), font=F(SANS_B, 11), fill=(255, 255, 255),
           anchor="mm")


def rule(d, x, y, w, color=LINE, width=1):
    d.line([x, y, x + w, y], fill=color, width=width)

# ---------------------------------------------------------------- scenes
# Every scene is flat, bold shapes with hard edges: no gradients, no
# glyph icons. Coordinates are relative to the scene box (x, y, w, h).

def scene_hormuz(d, x, y, w, h):
    """Night strait, container ship, one BIG burning flame."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 27, 46))
    for sx, sy, r in [(24, 14, 2), (70, 26, 1), (120, 10, 2), (180, 22, 1),
                      (250, 12, 2), (310, 24, 1), (360, 12, 2), (150, 34, 1),
                      (330, 40, 1), (48, 44, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 255))
    # sea
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(10, 36, 54))
    d.line([x + 8, y + h - 22, x + w - 8, y + h - 22], fill=(46, 90, 110),
           width=2)
    d.line([x + 30, y + h - 12, x + w - 40, y + h - 12], fill=(46, 90, 110),
           width=2)
    # orange glow behind the fire
    d.ellipse([x + 218, y + 8, x + 330, y + 108], fill=(214, 110, 20))
    # container stacks (left of the fire)
    cols = [(196, 58, 44), (44, 92, 140), (220, 122, 40), (34, 122, 62)]
    for i, (r, g, b) in enumerate(cols):
        cx = x + 36 + i * 52
        d.rectangle([cx, y + 78, cx + 48, y + 96], fill=(r, g, b))
        d.rectangle([cx, y + 60, cx + 48, y + 76], fill=(r, g, b))
    # hull
    d.rectangle([x + 28, y + 96, x + 340, y + 118], fill=(8, 8, 10))
    d.polygon([(x + 340, y + 96), (x + 368, y + 96), (x + 352, y + 118),
               (x + 340, y + 118)], fill=(8, 8, 10))
    # THE FIRE: three stacked flame tongues, tall enough to read at a glance
    fx = x + 252
    d.polygon([(fx - 42, y + 100), (fx - 30, y + 52), (fx - 12, y + 78),
               (fx - 2, y + 30), (fx + 14, y + 66), (fx + 26, y + 44),
               (fx + 40, y + 100)], fill=(232, 90, 12))
    d.polygon([(fx - 26, y + 100), (fx - 16, y + 60), (fx - 4, y + 80),
               (fx + 6, y + 48), (fx + 18, y + 76), (fx + 26, y + 100)],
              fill=(250, 190, 30))
    d.polygon([(fx - 12, y + 100), (fx - 6, y + 72), (fx + 2, y + 58),
               (fx + 10, y + 76), (fx + 13, y + 100)], fill=(255, 240, 160))
    # smoke
    for sx, sy, r in [(238, 26, 12), (262, 14, 14), (286, 26, 11),
                      (250, 6, 9)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(70, 70, 74))
    # fire reflection on the water
    for i in range(5):
        d.rectangle([x + 246 + i * 12, y + h - 30, x + 254 + i * 12,
                     y + h - 6], fill=(232, 120, 20))
    d.text((x + 10, y + 8), "$91.40", font=F(SANS_B, 22), fill=(120, 220, 130))


def scene_banten(d, x, y, w, h):
    """Factory at dusk with two searchlight beams."""
    d.rectangle([x, y, x + w, y + 22], fill=(214, 110, 44))
    d.rectangle([x, y + 22, x + w, y + 40], fill=(122, 62, 96))
    d.rectangle([x, y + 40, x + w, y + h], fill=(52, 32, 54))
    # searchlight beams from the ground, sweeping up
    d.polygon([(x + 60, y + h), (x + 150, y + 6), (x + 178, y + 6),
               (x + 96, y + h)], fill=(255, 244, 190))
    d.polygon([(x + w - 60, y + h), (x + w - 190, y + 10),
               (x + w - 164, y + 10), (x + w - 96, y + h)],
              fill=(255, 244, 190))
    # factory block with sawtooth roof and lit windows
    d.rectangle([x + 30, y + 26, x + w - 30, y + h], fill=(24, 20, 26))
    for i in range(6):
        wx = x + 44 + i * 68
        d.rectangle([wx, y + 34, wx + 34, y + 46], fill=(250, 200, 60))
    d.rectangle([x + w - 78, y + 12, x + w - 62, y + 30], fill=(24, 20, 26))
    for sx, sy, r in [(380, 8, 9), (398, 4, 11), (416, 10, 8)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(120, 110, 116))


def scene_card(d, kind, x, y, w, h):
    """Small flat scene for cards 4-11. Box is about 226x60."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if kind == "riyadh":
        d.rectangle([x, y, x + w, y + h], fill=(16, 30, 58))
        for sx, sy in [(14, 10), (52, 18), (120, 8), (190, 14), (210, 26)]:
            d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                      fill=(255, 255, 255))
        d.rectangle([x + 96, y + 14, x + 128, y + h], fill=(40, 60, 96))
        d.polygon([(x + 96, y + 14), (x + 112, y + 2), (x + 128, y + 14)],
                  fill=(40, 60, 96))
        for wy in range(20, h - 4, 9):
            d.rectangle([x + 104, y + wy, x + 120, y + wy + 4],
                        fill=(250, 200, 60))
        # drone, upper right
        dx, dy = x + 168, y + 14
        d.ellipse([dx - 12, dy - 3, dx + 12, dy + 3], fill=(220, 220, 220))
        d.line([dx - 18, dy - 6, dx + 18, dy - 6], fill=(220, 220, 220),
               width=2)
        d.ellipse([dx + 8, dy + 2, dx + 12, dy + 6], fill=RED)
    elif kind == "court":
        d.rectangle([x, y, x + w, y + h], fill=(233, 226, 200))
        d.polygon([(x + 30, y + 12), (x + 100, y + 12), (x + 65, y + 2)],
                  fill=(70, 60, 50))
        for cx in (38, 60, 82):
            d.rectangle([x + cx, y + 14, x + cx + 8, y + 40],
                        fill=(70, 60, 50))
        d.rectangle([x + 30, y + 40, x + 108, y + 46], fill=(70, 60, 50))
        d.rectangle([x + 24, y + 46, x + 114, y + h], fill=(96, 86, 74))
        # chip, foreground right
        d.rectangle([x + 150, y + 14, x + 198, y + 50], fill=(20, 90, 60))
        d.rectangle([x + 162, y + 24, x + 186, y + 40], fill=(247, 241, 222))
        for px in (154, 172, 190):
            d.line([x + px, y + 8, x + px, y + 14], fill=(20, 90, 60),
                   width=3)
            d.line([x + px, y + 50, x + px, y + 56], fill=(20, 90, 60),
                   width=3)
    elif kind == "ship":
        d.rectangle([x, y, x + w, y + 26], fill=(150, 160, 168))
        d.rectangle([x, y + 26, x + w, y + h], fill=(52, 96, 128))
        for wy in (34, 44, 54):
            for wx in range(0, w, 26):
                d.arc([x + wx, y + wy, x + wx + 22, y + wy + 10], 180, 360,
                      fill=(200, 225, 235), width=2)
        d.rectangle([x + 40, y + 34, x + 190, y + 48], fill=(20, 20, 24))
        for i, c in enumerate([(196, 58, 44), (44, 92, 140), (220, 122, 40)]):
            cx = x + 52 + i * 44
            d.rectangle([cx, y + 16, cx + 40, y + 34], fill=c)
        d.rectangle([x + 184, y + 8, x + 196, y + 34], fill=(20, 20, 24))
    elif kind == "medal":
        d.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
        d.polygon([(x + 96, y + 2), (x + 116, y + 2), (x + 108, y + 34)],
                  fill=(179, 39, 30))
        d.polygon([(x + 116, y + 2), (x + 136, y + 2), (x + 124, y + 34)],
                  fill=(255, 255, 255))
        d.ellipse([x + 84, y + 26, x + 148, y + 58], fill=GOLD)
        d.ellipse([x + 94, y + 32, x + 138, y + 52], fill=(240, 190, 80))
        d.text((x + 116, y + 42), "★", font=F(SANS_B, 18), fill=NAVY,
               anchor="mm")

    elif kind == "scales":
        d.rectangle([x, y, x + w, y + h], fill=(233, 226, 200))
        for i in range(4):
            d.rectangle([x, y + h - 8 - i * 8, x + 120 + i * 26, y + h - i * 8],
                        fill=(96, 86, 74))
        bx = x + 168
        d.line([bx, y + 8, bx, y + 44], fill=INK, width=3)
        d.line([bx - 34, y + 12, bx + 34, y + 12], fill=INK, width=3)
        d.polygon([(bx - 44, y + 26), (bx - 24, y + 26), (bx - 34, y + 40)],
                  fill=GOLD)
        d.polygon([(bx + 24, y + 26), (bx + 44, y + 26), (bx + 34, y + 40)],
                  fill=GOLD)
        d.line([bx - 34, y + 12, bx - 44, y + 26], fill=INK, width=2)
        d.line([bx - 34, y + 12, bx - 24, y + 26], fill=INK, width=2)
        d.line([bx + 34, y + 12, bx + 24, y + 26], fill=INK, width=2)
        d.line([bx + 34, y + 12, bx + 44, y + 26], fill=INK, width=2)
    elif kind == "hall":
        d.rectangle([x, y, x + w, y + h], fill=(214, 205, 180))
        d.rectangle([x + 10, y + 34, x + w - 10, y + 44], fill=(96, 70, 50))
        for cx in (30, 80, 130, 180):
            d.rectangle([x + cx, y + 46, x + cx + 18, y + 56],
                        fill=(60, 50, 44))
        for i, c in enumerate([(179, 39, 30), (30, 90, 160), (30, 122, 76),
                               (220, 160, 40), (120, 60, 140), (200, 100, 30),
                               (40, 120, 120)]):
            fx = x + 16 + i * 30
            d.line([fx, y + 4, fx, y + 22], fill=INK, width=2)
            d.rectangle([fx, y + 6, fx + 20, y + 16], fill=c)
    elif kind == "chipchart":
        d.rectangle([x, y, x + w, y + h], fill=(16, 30, 26))
        d.rectangle([x + 14, y + 18, x + 62, y + 54], fill=(30, 122, 76))
        d.rectangle([x + 26, y + 28, x + 50, y + 44], fill=(16, 30, 26))
        for px in (20, 34, 48):
            d.line([x + px, y + 12, x + px, y + 18], fill=(30, 122, 76),
                   width=3)
            d.line([x + px, y + 54, x + px, y + 60], fill=(30, 122, 76),
                   width=3)
        pts = [(70, 50), (100, 46), (120, 48), (150, 34), (170, 36),
               (200, 14), (220, 6)]
        pts = [(x + px, y + py) for px, py in pts]
        d.line(pts, fill=(120, 220, 130), width=4, joint="curve")
        d.polygon([(x + 220, y + 6), (x + 206, y + 6), (x + 220, y + 18)], fill=(120, 220, 130))
        d.text((x + 76, y + 8), "+31.5%", font=F(SANS_B, 13),
               fill=(120, 220, 130))
    elif kind == "jets":
        d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
        for cx in (20, 90, 160):
            d.ellipse([x + cx - 2, y + 44, x + cx + 2, y + 48],
                      fill=(255, 255, 255))
        for jx, jy, s in [(60, 16, 1.0), (130, 30, 0.8), (190, 12, 0.65)]:
            d.polygon([(x + jx, y + jy), (x + jx + int(34 * s), y + jy + 6),
                       (x + jx + int(30 * s), y + jy + 10),
                       (x + jx + 4, y + jy + 10)], fill=(40, 48, 64))
            d.polygon([(x + jx + 12, y + jy - 6), (x + jx + 20, y + jy),
                       (x + jx + 12, y + jy + 4)], fill=(40, 48, 64))
            d.line([x + jx, y + jy + 5, x + jx - 34, y + jy + 12],
                   fill=(255, 255, 255), width=2)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


# ---------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    by_num = {s["n"]: s for s in STORIES}

    # ---- masthead (0-62) + red rule + ticker
    d.rectangle([0, 0, W, 62], fill=NAVY)
    d.text((MARGIN, 7), "THE WEDNESDAY HERALD", font=F(SANS_B, 14),
           fill=GOLD)
    d.text((W - MARGIN, 9), "32 STORIES · 7 REGIONS · ALL DATED TO THE DAY",
           font=F(SANS_B, 11), fill=GOLD, anchor="ra")
    d.text((W / 2, 20), "WEDNESDAY 25 NOVEMBER 2026",
           font=F(SERIF_B, 42), fill=(255, 255, 255), anchor="ma")
    d.rectangle([0, 62, W, 65], fill=RED)
    d.text((W / 2, 72), "Hormuz mines lift oil past $91 · 700,000 Russian "
           "dead, new count says · Banten toll hits 26 — Wednesday's news, "
           "dated as it happened", font=F(SANS, 12), fill=NAVY, anchor="mm")

    # ---- lead 1: Hormuz (y 83-235), text left, big fire scene right
    s1 = by_num[1]
    d.rectangle([MARGIN, 83, W - MARGIN, 235], fill=PANEL, outline=LINE)
    num_badge(d, MARGIN + 10, 94, 1)
    pw = pill(d, MARGIN + 26, 87, s1["pill"], TEAL)
    d.text((MARGIN + 26 + pw + 8, 95), s1["date"], font=F(SANS_B, 12),
           fill=INK, anchor="lm")
    d.text((600, 95), "Source: " + s1["source"], font=F(SANS, 10),
           fill=MUTED, anchor="rm")
    d.text((MARGIN, 108), "Hormuz mines lift oil", font=F(SERIF_B, 46),
           fill=INK)
    d.text((MARGIN, 156), "past $91", font=F(SERIF_B, 46), fill=INK)
    for i, ln in enumerate(wrap(d, s1["deck"], F(SERIF, 13), 584, 2)):
        d.text((MARGIN, 206 + i * 13), ln, font=F(SERIF, 13), fill=INK)
    scene_hormuz(d, 612, 83, 396, 152)

    # ---- lead 2 (left) + lead 3 (right), y 239-471
    # lead 2: giant figure + dot field (1 dot = 2,000 lives)
    s2 = by_num[2]
    d.rectangle([MARGIN, 239, 500, 471], fill=PANEL, outline=LINE)
    d.text((MARGIN + 10, 247), "700,000", font=F(SERIF_B, 52), fill=INK)
    d.text((MARGIN + 10, 303), "Russian soldiers killed — each dot = 2,000 "
           "lives", font=F(SANS, 10), fill=MUTED)
    for r in range(7):
        for c in range(50):
            cx = MARGIN + 10 + c * 8.6
            cy = 321 + r * 7.3
            d.ellipse([cx - 1.8, cy - 1.8, cx + 1.8, cy + 1.8], fill=RED)
    num_badge(d, MARGIN + 10, 380, 2)
    pw = pill(d, MARGIN + 26, 373, s2["pill"], TEAL)
    d.text((MARGIN + 26 + pw + 8, 381), s2["date"], font=F(SANS_B, 12),
           fill=INK, anchor="lm")
    d.text((492, 381), "Source: " + s2["source"], font=F(SANS, 10),
           fill=MUTED, anchor="rm")
    d.text((MARGIN + 10, 389), "Russian soldiers killed,", font=F(SERIF_B, 28),
           fill=INK)
    d.text((MARGIN + 10, 417), "new count says", font=F(SERIF_B, 28),
           fill=INK)
    for i, ln in enumerate(wrap(d, s2["deck"], F(SERIF, 11), 464, 2)):
        d.text((MARGIN + 10, 449 + i * 11), ln, font=F(SERIF, 11), fill=INK)

    # lead 3: Banten, dusk factory + searchlights on top
    s3 = by_num[3]
    d.rectangle([516, 239, W - MARGIN, 471], fill=PANEL, outline=LINE)
    scene_banten(d, 516, 239, 492, 60)
    num_badge(d, 526, 314, 3)
    pw = pill(d, 542, 307, s3["pill"], RED)
    d.text((542 + pw + 8, 315), s3["date"], font=F(SANS_B, 12), fill=INK,
           anchor="lm")
    d.text((1000, 315), "Source: " + s3["source"], font=F(SANS, 10),
           fill=MUTED, anchor="rm")
    d.text((526, 325), "Banten toll hits 26", font=F(SERIF_B, 44), fill=INK)
    d.text((526, 371), "as search goes on", font=F(SERIF_B, 44), fill=INK)
    for i, ln in enumerate(wrap(d, s3["deck"], F(SERIF, 13), 472, 2)):
        d.text((526, 423 + i * 13), ln, font=F(SERIF, 13), fill=INK)

    # ---- stat strip (y 475-515)
    d.rectangle([MARGIN, 475, W - MARGIN, 515], fill=NAVY2)
    cell = (W - 2 * MARGIN) / 6
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + cell * (i + 0.5)
        d.text((cx, 479), num, font=F(SANS_B, 27), fill=(255, 255, 255),
               anchor="ma")
        d.text((cx, 505), label, font=F(SANS_B, 9), fill=GOLD, anchor="ma")
        if i:
            d.line([MARGIN + cell * i, 480, MARGIN + cell * i, 510],
                   fill=(90, 110, 150), width=1)

    # ---- timeline SATURDAY -> WEDNESDAY (y 519-595)
    d.text((MARGIN, 521), "SATURDAY → WEDNESDAY", font=F(SANS_B, 12),
           fill=NAVY)
    rule(d, MARGIN, 535, W - 2 * MARGIN)
    col_w = (W - 2 * MARGIN) / 4
    for ci, (day, items) in enumerate(TIMELINE):
        cx = MARGIN + col_w * ci
        color = RED if day.startswith("WED") else NAVY
        d.text((cx, 540), day, font=F(SANS_B, 11), fill=color)
        for j, item in enumerate(items):
            d.text((cx, 554 + j * 11), "· " + item, font=F(SANS, 10),
                   fill=INK)

    # ---- cards 4-11: 4 columns x 2 rows, scene above the text
    card_w, card_h, gap = 242, 110, 8
    for idx, n in enumerate(range(4, 12)):
        s = by_num[n]
        row, col = divmod(idx, 4)
        cx = MARGIN + col * (card_w + gap)
        cy = 599 + row * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=PANEL,
                    outline=LINE)
        scene_card(d, s["scene"], cx + 8, cy + 6, card_w - 16, 60)
        num_badge(d, cx + 18, cy + 16, n)
        d.text((cx + 8, cy + 70), s["title"], font=F(SANS_B, 12), fill=INK)
        for i, ln in enumerate(wrap(d, s["body"], F(SANS, 10),
                                    card_w - 16, 2)):
            d.text((cx + 8, cy + 86 + i * 11), ln, font=F(SANS, 10),
                   fill=INK)

    # ---- index 12-32 (left) + world map (right), y 831-957
    d.text((MARGIN, 833), "ALSO ON — 21 MORE STORIES · 32 STORIES",
           font=F(SANS_B, 11), fill=NAVY)
    d.text((676, 833), "WHERE IT HAPPENED · 11 PLACES PINNED",
           font=F(SANS_B, 11), fill=NAVY)
    rule(d, MARGIN, 847, W - 2 * MARGIN)
    idx_items = [by_num[n] for n in range(12, 33)]
    for i, s in enumerate(idx_items):
        col, row = divmod(i, 11)
        ix = MARGIN + col * 330
        iy = 850 + row * 9.5
        d.text((ix, iy), f"{s['n']}  {s['title']} — {s['date']}",
               font=F(SANS, 9), fill=INK)
    # dotted world map
    mx, my, mw, mh = 676, 850, 332, 106
    continents = [(60, 32, 46, 20), (95, 78, 18, 22), (165, 25, 16, 11),
                  (170, 62, 20, 26), (235, 32, 56, 22), (255, 70, 22, 9),
                  (285, 86, 18, 10)]
    gx, gy = 4, 851
    while gy < my + mh:
        while gx < mx + mw:
            lx, ly = gx - mx, gy - my
            inside = any(((lx - ex) / erx) ** 2 + ((ly - ey) / ery) ** 2 <= 1
                         for ex, ey, erx, ery in continents)
            if inside:
                d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6],
                          fill=(168, 159, 141))
            gx += 7
        gx = mx + 4
        gy += 7
    for n, _place, _lon, _lat, px, py in PINS:
        d.ellipse([mx + px - 8, my + py - 8, mx + px + 8, my + py + 8],
                  fill=RED, outline=(255, 255, 255), width=1)
        d.text((mx + px, my + py), str(n), font=F(SANS_B, 9),
               fill=(255, 255, 255), anchor="mm")

    # ---- DATE CHECK box (y 957-1007)
    d.rectangle([MARGIN, 957, W - MARGIN, 1007], fill=YELLOW_BOX,
                outline=INK)
    d.text((MARGIN + 8, 960),
           "DATE CHECK — This page is WEDNESDAY 25 NOVEMBER 2026.",
           font=F(SANS_B, 10), fill=INK)
    check_font = F(SANS, 8)
    lines = date_check_lines()
    # TUE line may need a second row; wrap it to the box width.
    tue_wrapped = wrap(d, lines[0], check_font, W - 2 * MARGIN - 16, 2)
    ly = 971
    for ln in tue_wrapped:
        d.text((MARGIN + 8, ly), ln, font=check_font, fill=INK)
        ly += 9
    for ln in lines[1:]:
        d.text((MARGIN + 8, ly), ln, font=check_font, fill=INK)
        ly += 9

    # ---- footer
    d.text((W / 2, 1013),
           "Sources: Reuters · AP · AFP · RFE/RL · Xinhua · DeepDraft · "
           "UKMTO — CONFIRMED: verified by two or more sources. REPORTED: "
           "one source, or a claim, labelled in the text.",
           font=F(SANS, 8), fill=MUTED, anchor="ma")
    return img


def main():
    img = build()
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG")
    return out


if __name__ == "__main__":
    main()
