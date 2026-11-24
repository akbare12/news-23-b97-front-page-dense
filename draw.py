#!/usr/bin/env python3
"""THE WORLD TODAY — Monday 23 November 2026 (31 stories). Front-page-dense.
Draws entry.png 1024x1024 with PIL. Run: python3 draw.py  (writes entry.png next to this file)
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
BG = (247, 243, 234)
INK = (17, 17, 17)
RED = (184, 16, 46)
DARKRED = (150, 10, 35)
GOLD = (201, 162, 39)
NAVY = (27, 42, 74)
GREEN = (30, 91, 58)
TEAL = (14, 116, 116)
PURPLE = (90, 50, 140)
BLUE = (30, 80, 160)
CREAM = (250, 246, 238)
GREY = (90, 90, 90)
LIGHTGREEN = (190, 220, 180)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"

def f_serif_b(sz): return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", sz)
def f_sans(sz): return ImageFont.truetype(FD + "DejaVuSans.ttf", sz)
def f_sans_b(sz): return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", sz)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def rect(x0, y0, x1, y1, fill, outline=None, width=1):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)

def center_text(cx, y, s, font, fill=INK):
    d.text((cx, y), s, font=font, fill=fill, anchor="ma")

# ---------- MASTHEAD ----------
rect(0, 0, W, 58, INK)
text(14, 8, "THE WORLD TODAY", f_serif_b(40), fill=(255, 255, 255))
text(W - 14, 20, "MONDAY 23 NOVEMBER 2026", f_sans_b(17), fill=GOLD, anchor="ra")

# ---------- KICKER ----------
rect(0, 58, W, 84, RED)
center_text(W // 2, 63, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
            f_sans_b(14), fill=(255, 255, 255))

# ---------- NUMBER STRIP (2 rows x 5) ----------
NUMS = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", INK), ("10T won", "SEOUL STABILISATION FUND", (150, 110, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", GREEN),
    ("$450M", "SKUBAL DEAL", NAVY), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", INK), ("264 kg", "EXPLOSIVES SEIZED", INK),
    ("$107.3B", "ANTHROPIC IPO", GREEN),
]
colw = W // 5
for i, (val, lab, col) in enumerate(NUMS):
    r, c = divmod(i, 5)
    x0 = c * colw + 12
    yv = 90 + r * 38
    text(x0, yv, val, f_sans_b(19), fill=col)
    text(x0, yv + 21, lab, f_sans_b(8), fill=GREY)

# ---------- REGION BAR ----------
REGIONS = [("ASIA-PACIFIC 7", NAVY), ("AMERICAS 8", RED), ("MIDDLE EAST 6", (150, 110, 0)),
           ("EUROPE 5", BLUE), ("AFRICA 3", GREEN), ("WORLD 2", GREY)]
rx = 0
for name, col in REGIONS:
    wseg = W // 6
    rect(rx, 166, rx + wseg - 1, 182, col)
    center_text(rx + wseg // 2, 169, name, f_sans_b(11), fill=(255, 255, 255))
    rx += wseg

# ---------- UTC STRIP ----------
text(10, 186, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     f_sans(10), fill=GREY)
text(W - 10, 186, "~ APPROX", f_sans(9), fill=GREY, anchor="ra")

# ---------- HEROES ----------
HY = 202          # scene top
HSCENE = 92       # scene height
HCAP = 204 + 92   # caption strip top = 296
heroes = [
    dict(x=10, w=330, kind="kospi"),
    dict(x=347, w=330, kind="guterres"),
    dict(x=684, w=330, kind="power"),
]
for h in heroes:
    x, w, kind = h["x"], h["w"], h["kind"]
    if kind == "kospi":
        rect(x, HY, x + w, HY + HSCENE, NAVY)
        # buildings with lit windows
        import random
        rnd = random.Random(7)
        bx = x + 8
        while bx < x + w - 30:
            bw = rnd.randint(22, 34)
            bh = rnd.randint(34, 66)
            by = HY + HSCENE - bh
            rect(bx, by, bx + bw, HY + HSCENE, (24, 36, 66))
            for wy in range(by + 5, HY + HSCENE - 6, 9):
                for wx in range(bx + 4, bx + bw - 4, 8):
                    if rnd.random() < 0.55:
                        rect(wx, wy, wx + 3, wy + 4, (255, 210, 90))
            bx += bw + 4
        # orange chart line
        pts = [(x + 8, HY + 62), (x + 55, HY + 44), (x + 105, HY + 58), (x + 160, HY + 30),
               (x + 215, HY + 48), (x + 270, HY + 20), (x + w - 8, HY + 34)]
        d.line(pts, fill=(255, 140, 40), width=3)
        for px, py in pts:
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255), outline=(255, 140, 40))
        text(x + 10, HY + 6, "-3.3%", f_sans_b(24), fill=(255, 255, 255))
        rect(x, HY + HSCENE, x + w, HY + HSCENE + 16, INK)
        text(x + 8, HY + HSCENE + 2, "KOSPI 4,708.54   \u00b7   -161 PTS", f_sans_b(11), fill=(255, 255, 255))
    elif kind == "guterres":
        rect(x, HY, x + w, HY + HSCENE, GREEN)
        text(x + 12, HY + 8, "150 DELEGATES", f_sans_b(22), fill=(255, 215, 90))
        text(x + 12, HY + 34, "BACK A RISK", f_sans_b(22), fill=(255, 215, 90))
        text(x + 12, HY + 60, "FRAMEWORK", f_sans_b(22), fill=(255, 215, 90))
        # globe
        cx, cy, r = x + w - 52, HY + 46, 34
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 230, 200), outline=(255, 255, 255), width=2)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(120, 160, 120), width=1)
        d.line([cx - r, cy, cx + r, cy], fill=(120, 160, 120), width=1)
        d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(120, 160, 120), width=1)
        rect(x, HY + HSCENE, x + w, HY + HSCENE + 16, INK)
        text(x + 8, HY + HSCENE + 2, "UN   \u00b7   BRIDGETOWN", f_sans_b(11), fill=(255, 255, 255))
    else:
        rect(x, HY, x + w, HY + HSCENE, CREAM, outline=(200, 200, 190))
        text(x + 10, HY + 4, "NARROWEST SINCE 2018", f_sans_b(10), fill=INK)
        text(x + w - 10, HY + 4, "GAP 5.3", f_sans_b(10), fill=RED, anchor="ra")
        # bars: scaled to fit scene (max 52px tall)
        base = HY + HSCENE - 8
        vals = [("78.9", "US", NAVY, 52), ("73.6", "CHINA", RED, 49), ("40.5", "INDIA", GOLD, 27)]
        bx = x + 16
        for val, lab, col, bh in vals:
            rect(bx, base - bh, bx + 88, base, col)
            if col == GOLD:
                # short gold bar: value ABOVE bar (dark on cream), label inside bar
                center_text(bx + 44, base - bh - 17, val, f_sans_b(15), fill=INK)
                center_text(bx + 44, base - bh + 6, lab, f_sans_b(10), fill=INK)
            else:
                center_text(bx + 44, base - bh + 6, val, f_sans_b(15), fill=(255, 255, 255))
                center_text(bx + 44, base - bh + 26, lab, f_sans_b(10), fill=(255, 255, 255))
            bx += 100
        rect(x, HY + HSCENE, x + w, HY + HSCENE + 16, INK)
        text(x + 8, HY + HSCENE + 2, "ASIA POWER INDEX 2026", f_sans_b(11), fill=(255, 255, 255))

# hero headlines + body (below caption strip, with clear gap)
HHEAD_Y = HY + HSCENE + 22   # 316
hero_text = [
    (10, 330, "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    (347, 330, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    (684, 330, "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for x, w, head, body, src in hero_text:
    lines = wrap(head, f_sans_b(20), w - 4)
    y = HHEAD_Y
    for ln in lines:
        text(x, y, ln, f_sans_b(20), fill=INK)
        y += 23
    blines = wrap(body, f_sans(11), w - 4)
    for ln in blines:
        text(x, y, ln, f_sans(11), fill=INK)
        y += 14
    # source + chip row
    text(x, y + 2, src, f_sans(9), fill=GREY)
    d.rounded_rectangle([x + w - 78, y, x + w, y + 15], radius=3, fill=BLUE)
    center_text(x + w - 39, y + 2, "REPORTED", f_sans_b(8), fill=(255, 255, 255))

# ---------- CARDS ----------
CY = 420
rect(0, CY, W, CY + 18, INK)
text(10, CY + 2, "MORE OF THE DAY  \u2014  10 STORIES", f_sans_b(12), fill=(255, 255, 255))
CARDS = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", False),
    ("FBI", NAVY, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", False),
    ("WHITE HOUSE", (150, 110, 0), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", False),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", False),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", False),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", False),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", False),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", False),
    ("EUROPE", BLUE, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", True),
    ("SPACE", PURPLE, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", True),
]
cw, ch = 200, 72
gapx = (W - 5 * cw - 20) // 4
for i, (cat, col, head, body, src, claim) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x0 = 10 + c * (cw + gapx)
    y0 = CY + 24 + r * (ch + 6)
    rect(x0, y0, x0 + cw, y0 + ch, (255, 255, 255), outline=(210, 205, 195))
    rect(x0, y0, x0 + cw, y0 + 15, col)
    text(x0 + 5, y0 + 2, cat, f_sans_b(9), fill=(255, 255, 255))
    text(x0 + cw - 5, y0 + 2, str(i + 1), f_sans_b(9), fill=(255, 255, 255), anchor="ra")
    hlines = wrap(head, f_sans_b(11), cw - 10)
    y = y0 + 18
    for ln in hlines[:2]:
        text(x0 + 5, y, ln, f_sans_b(11), fill=INK)
        y += 13
    text(x0 + 5, y0 + 46, body, f_sans(9), fill=GREY)
    text(x0 + 5, y0 + ch - 15, src, f_sans(8), fill=GREY)
    chip = "CLAIM" if claim else "REPORTED"
    chipcol = RED if claim else BLUE
    d.rounded_rectangle([x0 + cw - 62, y0 + ch - 17, x0 + cw - 4, y0 + ch - 4], radius=3, fill=chipcol)
    center_text(x0 + cw - 33, y0 + ch - 15, chip, f_sans_b(7), fill=(255, 255, 255))

# ---------- MAP + ALSO ----------
MY = 600
rect(0, MY, 330, MY + 18, INK)
text(10, MY + 2, "WHERE IT HAPPENED", f_sans_b(12), fill=(255, 255, 255))
rect(340, MY, W, MY + 18, INK)
text(350, MY + 2, "ALSO ON MONDAY", f_sans_b(12), fill=(255, 255, 255))
# map blobs (stylised continents)
rect(10, MY + 18, 330, MY + 198, (255, 255, 255), outline=(210, 205, 195))
d.polygon([(30, 648), (90, 633), (130, 648), (120, 708), (80, 738), (40, 708)], fill=LIGHTGREEN)
d.polygon([(150, 648), (230, 638), (260, 668), (240, 718), (180, 728), (155, 688)], fill=LIGHTGREEN)
d.polygon([(270, 653), (315, 648), (320, 688), (290, 708), (268, 683)], fill=LIGHTGREEN)
d.polygon([(150, 748), (210, 743), (225, 778), (180, 798), (155, 773)], fill=LIGHTGREEN)
PINS = [(60, 673), (95, 743), (285, 663), (70, 723), (105, 708), (200, 673),
        (225, 693), (170, 698), (250, 708), (85, 768), (215, 753), (245, 668), (275, 688)]
for n, (px, py) in enumerate(PINS, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    center_text(px, py - 6, str(n), f_sans_b(8), fill=(255, 255, 255))
text(14, MY + 168, "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", f_sans(8), fill=GREY)
text(14, MY + 178, "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", f_sans(8), fill=GREY)
text(14, MY + 188, "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", f_sans(8), fill=GREY)
# ALSO list, 2 columns x 9
ALSO = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: the day after Antalya pact rejected",
    "Benghazi: UN demands probe [CLAIM]",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Sudan: defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row",
    "SK Telecom -7.3% as hype cools",
    "China eases margin rules",
    "Seoul readies 10T-won fund",
]
for i, item in enumerate(ALSO):
    col = i // 9
    row = i % 9
    x0 = 350 + col * 340
    y0 = MY + 24 + row * 19
    text(x0, y0, f"{14 + i}. {item}", f_sans(11), fill=INK)

# ---------- DATE CHECK ----------
DY = 812
rect(10, DY, W - 10, DY + 52, (255, 255, 255), outline=RED, width=2)
text(16, DY + 4, "DATE CHECK", f_sans_b(13), fill=RED)
text(W - 16, DY + 4, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
     f_sans_b(10), fill=RED, anchor="ra")
text(16, DY + 22, "LEFT OUT \u2014 NOT 23 NOV:   Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
     f_sans(10), fill=INK)
text(16, DY + 37, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
     f_sans(10), fill=INK)

# ---------- FOOTER ----------
FY = 872
text(10, FY, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     f_sans(9), fill=GREY)
text(10, FY + 14, "CHIPS: REPORTED = confirmed by wires.  CLAIM = one side's claim, not independently confirmed.  ONGOING = still developing.",
     f_sans(9), fill=GREY)
text(10, FY + 28, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     f_sans(9), fill=GREY)
d.line([10, 930, W - 10, 930], fill=GOLD, width=2)
center_text(W // 2, 940, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
            f_sans_b(12), fill=(150, 110, 0))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
