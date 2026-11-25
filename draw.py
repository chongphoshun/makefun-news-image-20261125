#!/usr/bin/env python3
"""Render the news-image-20261125 front page: 1024x1024 PNG.

50 stories that happened or were first reported on Wednesday,
25 November 2026, across 7 regions. Build-time only (Pillow);
the submitted main.py is stdlib-only and copies the PNG.

Run:  python3 draw.py   -> writes entry.png next to this script.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (24, 24, 24)
PAPER = (253, 251, 244)
RED = (166, 24, 28)
GREY = (96, 96, 96)
FAINT = (168, 168, 168)
RULE = (150, 148, 140)
BOX = (244, 242, 234)
DARK = (28, 28, 34)
LAND = (206, 202, 188)
SEA = (238, 240, 236)

SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

W, H = 1024, 1024
MARGIN = 26
CW = W - 2 * MARGIN  # 972 content width

# kind: D = event dated 25 Nov, R = first REPORTED 25 Nov, C = CLAIMED 25 Nov
HEROES = [
    ("ASIA-PACIFIC", "China flies first Pakistani astronaut",
     "Shenzhou-24 lifts off 08:18 CST; Zeeshan Ali, first foreigner aboard Tiangong.", "D"),
    ("OCEANIA", "Solomons picks Australia over China",
     "Canberra signs an A$740m security treaty; no foreign bases, China pact lapses.", "D"),
    ("ASIA-PACIFIC", "Asian stocks dive on tariff threat",
     "Kospi falls 5.3%, Taiwan 5.1%, Nikkei 2.9% as US readies tariffs.", "D"),
]

MAINS = [
    ("EUROPE", "Russia's own figures show 500,000 war dead",
     "Leaked records: 490,334 Russian soldiers dead since 2022.", "D"),
    ("AFRICA", "Sahel rebels wage war with cheap drones",
     "Reuters: 187 drone attacks by Mali insurgents since 2023.", "D"),
    ("EUROPE", "Russian strike kills two in Odesa",
     "Two killed, three hurt; Kyiv also hit by drones.", "D"),
    ("EUROPE", "US shelves Russia business-deal incentives",
     "Deal offers dropped after the Kremlin balks.", "D"),
    ("EUROPE", "EU meets Western Balkans in Brussels",
     "Leaders talk membership, migration, security and reforms.", "D"),
    ("MIDDLE EAST", "Israeli strike kills four in Gaza",
     "Four of one family killed in an apartment in al-Shati, west Gaza City.", "D"),
    ("MIDDLE EAST", "Houthis threaten Jeddah after port strikes",
     "Houthis vow Saudi Red Sea ports are targets.", "D"),
    ("LATIN AMERICA", "Cartagena siege: ten hostages freed",
     "Ten of 30 hostages released by Wednesday morning.", "D"),
    ("OCEANIA", "Australia inflation jumps to 4.9%",
     "October CPI up 4.9% yearly, core 3.8%; rate-hike talk grows.", "D"),
    ("ASIA-PACIFIC", "Seoul subway strike called off",
     "Dawn deal shelves 2,212 job cuts; 500 hires and a 3.5% pay rise.", "D"),
    ("ASIA-PACIFIC", "Rescuers hunt dozens trapped in mine",
     "Search under way in West Java; miners stuck since Monday.", "D"),
    ("OCEANIA", "Ex-officer guilty of Sydney double murder",
     "Jury convicts Beau Lamarre-Condon over the 2024 killings.", "D"),
]

BRIEFS = [
    ("ASIA-PACIFIC", "India condemns Riyadh attack",
     "Statement 25 Nov.", "D"),
    ("AFRICA", "Pete Edochie dies aged 79",
     "Died 00:30 Wed.", "D"),
    ("AFRICA", "Nigerian monarch, 92, suspended",
     "Emir of Daura, 92.", "D"),
    ("OCEANIA", "Fiji drought may run into 2027",
     "Rain below normal.", "D"),
    ("OCEANIA", "El Nino raises Guam drought risk",
     "Risk rises in 2027.", "D"),
    ("NORTH AMERICA", "Nor'easter threatens Thanksgiving",
     "Gusts 50-70 mph.", "D"),
    ("NORTH AMERICA", "Florida river crests at Sanford",
     "Crest 8.4 ft Wed.", "D"),
    ("NORTH AMERICA", "Trump pardons two turkeys",
     "Thanksgiving rite.", "D"),
    ("ASIA-PACIFIC", "Hasina plans 16 Dec return",
     "Return 16 Dec.", "D"),
    ("AFRICA", "Convicted over Ukraine bid",
     "Ukraine bid fails.", "D"),
    ("ASIA-PACIFIC", "N. Koreans jailed for faith",
     "Beatings and jail.", "D"),
    ("AFRICA", "Cameroon war scars children",
     "Shot at 15.", "D"),
    ("ASIA-PACIFIC", "India food prices squeeze budgets",
     "Budgets squeezed.", "D"),
    ("EUROPE", "Spain divided ahead of election",
     "Split ahead of vote.", "D"),
    ("NORTH AMERICA", "Iowa braces for explosives blast",
     "Blast set for Wed.", "D"),
    ("NORTH AMERICA", "Omar search records unsealed",
     "Redacted files out.", "D"),
    ("ASIA-PACIFIC", "Afghan women lose UK visas",
     "Visas stopped.", "D"),
    ("NORTH AMERICA", "Thomas Markle indicted in the US",
     "BBC reports.", "R"),
    ("EUROPE", "Pochettino fumes at Yoro red card",
     "Fury at ruling.", "D"),
    ("NORTH AMERICA", "US poised to unveil new tariffs",
     "16 partners named.", "R"),
    ("NORTH AMERICA", "Huawei guilty on 10 of 12 counts",
     "Fraud, sanctions.", "R"),
    ("AFRICA", "Senegal AFCON winners again",
     "CAS overturns CAF.", "R"),
    ("ASIA-PACIFIC", "Vaibhav, 15, hits 204 off 53",
     "28 sixes.", "R"),
    ("EUROPE", "Sinner knee surgery, out months",
     "Misses Aus Open.", "R"),
    ("EUROPE", "Sarkozy and Bruni face trial",
     "Trial ordered.", "R"),
    ("NORTH AMERICA", "Abrego Garcia leaves US for Spain",
     "Saga ends.", "R"),
    ("NORTH AMERICA", "GPT-6 designs proteins in the lab",
     "35 of 322 bound.", "R"),
    ("NORTH AMERICA", "Tidal to delete 29m AI songs",
     "From 9 December.", "R"),
    ("MIDDLE EAST", "Israel claims Iran chemical arms",
     "Tehran denies.", "C"),
    ("MIDDLE EAST", "Iran claims tankers mined",
     "Unconfirmed.", "C"),
    ("LATIN AMERICA", "US pauses operations with Ecuador",
     "Probe into killing.", "R"),
    ("ASIA-PACIFIC", "China AI fakes target Taiwan vote",
     "500-plus videos.", "D"),
    ("NORTH AMERICA", "US AG dodges Nvidia queries",
     "Sidesteps queries.", "D"),
    ("MIDDLE EAST", "Gaza truce near collapse",
     "Ceasefire failing.", "D"),
    ("AFRICA", "349 Russians killed in Mali",
     "Toll since 2023.", "D"),
]

NUMBERS = [
    ("50", "STORIES"),
    ("7", "REGIONS"),
    ("-5.3%", "KOSPI"),
    ("4.9%", "AUSTRALIA CPI"),
    ("490,334", "RUSSIAN WAR DEAD*"),
    ("187", "SAHEL DRONE ATTACKS"),
]

REGIONS = ["NORTH AMERICA", "LATIN AMERICA", "EUROPE", "AFRICA",
           "MIDDLE EAST", "ASIA-PACIFIC", "OCEANIA"]

# Schematic continent blobs, in map-band coordinates (x 0..972, y 0..92).
LAND_POLYS = [
    [(48, 16), (150, 8), (214, 20), (206, 46), (150, 58), (88, 50), (50, 34)],
    [(206, 56), (252, 54), (268, 74), (238, 90), (208, 74)],
    [(428, 14), (482, 8), (502, 24), (472, 38), (434, 32)],
    [(438, 42), (502, 40), (522, 60), (496, 84), (454, 72), (432, 56)],
    [(512, 12), (700, 6), (762, 24), (722, 56), (640, 62), (558, 50), (510, 34)],
    [(762, 62), (822, 60), (842, 76), (792, 84), (760, 72)],
]
# (label, badge x, badge y) per continent, matching LAND_POLYS order.
MAP_LABELS = [
    ("N. AMERICA", 128, 34), ("S. AMERICA", 232, 72), ("EUROPE", 462, 24),
    ("AFRICA", 476, 62), ("ASIA", 632, 34), ("OCEANIA", 800, 72),
]


def f(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def trunc(draw, s, font, max_w):
    """Shorten s with an ellipsis until it fits max_w. Returns (text, cut)."""
    if text_w(draw, s, font) <= max_w:
        return s, False
    ell = "…"
    while s and text_w(draw, s + ell, font) > max_w:
        s = s[:-1]
    return s + ell, True


def wrap(draw, s, font, max_w):
    """Greedy word wrap. Returns list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tag_text(kind):
    return {"D": "25 NOV", "R": "REPORTED 25 NOV", "C": "CLAIMED 25 NOV"}[kind]


def tag_color(kind):
    return RED if kind == "D" else (GREY if kind == "R" else (168, 90, 20))


def region_counts():
    counts = {r: 0 for r in REGIONS}
    for group in (HEROES, MAINS, BRIEFS):
        for item in group:
            counts[item[0]] += 1
    return counts


def draw_masthead(d, y):
    title = f(SERIF_B, 42)
    sub = f(SANS_B, 16)
    d.text((MARGIN, y), "THE WORLD IN ONE DAY", font=title, fill=INK)
    d.text((MARGIN, y + 54),
           "WEDNESDAY, 25 NOVEMBER 2026  ·  50 STORIES  ·  7 REGIONS  ·  ALL DATED 25 NOV 2026",
           font=sub, fill=RED)
    d.line([(MARGIN, y + 78), (W - MARGIN, y + 78)], fill=INK, width=3)
    return y + 86


def draw_heroes(d, y):
    gap = 14
    bw = (CW - 2 * gap) // 3
    bh = 148
    cuts = []
    for i, (region, head, deck, kind) in enumerate(HEROES):
        x = MARGIN + i * (bw + gap)
        d.rectangle([x, y, x + bw, y + bh], fill=BOX, outline=RULE, width=1)
        d.rectangle([x, y, x + bw, y + 5], fill=RED)
        d.text((x + 12, y + 14), "LEAD  ·  " + region, font=f(SANS_B, 12), fill=RED)
        lines = wrap(d, head, f(SERIF_B, 23), bw - 24)
        ly = y + 34
        for ln in lines[:2]:
            d.text((x + 12, ly), ln, font=f(SERIF_B, 23), fill=INK)
            ly += 27
        dlines = wrap(d, deck, f(SANS, 14), bw - 24)
        for ln in dlines[:2]:
            d.text((x + 12, ly), ln, font=f(SANS, 14), fill=(52, 52, 52))
            ly += 18
        d.text((x + 12, y + bh - 18), tag_text(kind), font=f(SANS_B, 11),
               fill=tag_color(kind))
    return y + bh + 6


def draw_numbers(d, y):
    bh = 46
    d.rectangle([MARGIN, y, W - MARGIN, y + bh], fill=DARK)
    seg = CW // len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        cx = MARGIN + i * seg + seg // 2
        nw = text_w(d, num, f(SANS_B, 24))
        d.text((cx - nw / 2, y + 5), num, font=f(SANS_B, 24), fill=(255, 255, 255))
        lw = text_w(d, label, f(SANS_B, 10))
        d.text((cx - lw / 2, y + 30), label, font=f(SANS_B, 10), fill=(190, 190, 190))
        if i:
            d.line([(MARGIN + i * seg, y + 7), (MARGIN + i * seg, y + bh - 7)],
                   fill=(90, 90, 96), width=1)
    return y + bh + 6


def draw_map(d, y, counts):
    """Region strip: seven cells, one per region, count on top."""
    bh = 64
    d.rectangle([MARGIN, y, W - MARGIN, y + bh], fill=SEA, outline=RULE, width=1)
    d.text((MARGIN + 10, y + 6), "AROUND THE WORLD — STORIES BY REGION", font=f(SANS_B, 11), fill=GREY)
    seg = CW // 7
    for i, region in enumerate(REGIONS):
        cx = MARGIN + i * seg + seg // 2
        num = str(counts[region])
        nw = text_w(d, num, f(SANS_B, 22))
        d.text((cx - nw / 2, y + 20), num, font=f(SANS_B, 22), fill=RED)
        short = {"NORTH AMERICA": "N. AMERICA", "LATIN AMERICA": "LATIN AMERICA",
                 "ASIA-PACIFIC": "ASIA-PACIFIC"}.get(region, region)
        lw = text_w(d, short, f(SANS_B, 10))
        d.text((cx - lw / 2, y + 46), short, font=f(SANS_B, 10), fill=INK)
        if i:
            d.line([(MARGIN + i * seg, y + 20), (MARGIN + i * seg, y + bh - 6)],
                   fill=RULE, width=1)
    return y + bh + 6


def draw_mains(d, y, cuts):
    d.text((MARGIN, y), "THE DAY'S NEWS", font=f(SANS_B, 13), fill=RED)
    y += 20
    gap = 16
    bw = (CW - gap) // 2
    rows = (len(MAINS) + 1) // 2
    rh = 46
    for i, (region, head, brief, kind) in enumerate(MAINS):
        col, row = i % 2, i // 2
        x = MARGIN + col * (bw + gap)
        yy = y + row * rh
        d.text((x, yy), region, font=f(SANS_B, 11), fill=RED)
        tw = text_w(d, tag_text(kind), f(SANS_B, 11))
        d.text((x + bw - tw, yy), tag_text(kind), font=f(SANS_B, 11),
               fill=tag_color(kind))
        h, cut = trunc(d, head, f(SANS_B, 17), bw)
        cuts.append(("main-head", head) if cut else None)
        d.text((x, yy + 14), h, font=f(SANS_B, 17), fill=INK)
        b, cut = trunc(d, brief, f(SANS, 14), bw)
        cuts.append(("main-brief", brief) if cut else None)
        d.text((x, yy + 32), b, font=f(SANS, 14), fill=(52, 52, 52))
    return y + rows * rh + 6


def draw_briefs(d, y, cuts):
    d.text((MARGIN, y), "IN BRIEF — EVERY ITEM DATED 25 NOVEMBER 2026",
           font=f(SANS_B, 13), fill=RED)
    y += 20
    gap = 14
    bw = (CW - 2 * gap) // 3
    rows = (len(BRIEFS) + 2) // 3
    rh = 21
    for i, (region, head, brief, kind) in enumerate(BRIEFS):
        col, row = i % 3, i // 3
        x = MARGIN + col * (bw + gap)
        yy = y + row * rh
        d.text((x, yy), "•", font=f(SANS_B, 13), fill=RED)
        # Bold headline, then regular " — brief", all on one line.
        hx = x + 12
        h, cut = trunc(d, head, f(SANS_B, 13), bw - 12)
        cuts.append(("brief-head", head) if cut else None)
        d.text((hx, yy), h, font=f(SANS_B, 13), fill=INK)
        rest_w = bw - 12 - text_w(d, h, f(SANS_B, 13))
        sep = " — "
        # Reported/claimed items show their dating first; dated items
        # show the short detail tail. Drawn only when it fits whole.
        tail_brief = brief
        if kind == "R":
            tail_brief = "reported 25 Nov"
        elif kind == "C":
            tail_brief = "claimed 25 Nov"
        tail = sep + tail_brief
        if text_w(d, tail, f(SANS, 13)) <= rest_w:
            d.text((hx + text_w(d, h, f(SANS_B, 13)), yy), tail,
                   font=f(SANS, 13), fill=(80, 80, 80))
    return y + rows * rh + 4


def draw_footer(d, y):
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    d.text((MARGIN, y + 7),
           "Every story happened or was first reported on Wednesday, 25 November 2026. "
           "REPORTED = first reported that day; CLAIMED = unverified claim.",
           font=f(SANS, 12), fill=GREY)
    d.text((MARGIN, y + 24),
           "Sources: Reuters · BBC · AP · Al Jazeera · ABC · The Guardian · ABS · Yonhap.  "
           "*BBC analysis of leaked Russian records, reported 25 Nov.",
           font=f(SANS, 12), fill=GREY)
    return y + 42


def render():
    counts = region_counts()
    total = len(HEROES) + len(MAINS) + len(BRIEFS)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cuts = []
    y = 20
    y = draw_masthead(d, y)
    y = draw_heroes(d, y)
    y = draw_numbers(d, y)
    y = draw_map(d, y, counts)
    y = draw_mains(d, y, cuts)
    y = draw_briefs(d, y, cuts)
    y = draw_footer(d, y)
    cuts = [c for c in cuts if c]
    return img, total, counts, y, cuts


def main():
    img, total, counts, bottom, cuts = render()
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    size = os.path.getsize(out)
    with open(out, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print(f"stories={total} counts={counts}")
    print(f"bottom_y={bottom} (canvas {H})")
    print(f"wrote {out}: {size} bytes, sha256 {digest}")
    print(f"truncated_lines={len(cuts)}")
    for kind, text in cuts:
        print(f"  CUT {kind}: {text}")
    if bottom > H:
        raise SystemExit(f"OVERFLOW: content ends at y={bottom}, canvas is {H}")
    if size > 1048576:
        raise SystemExit(f"TOO BIG: {size} bytes > 1 MiB")
    if total != 50:
        raise SystemExit(f"WRONG COUNT: {total} stories, want 50")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
