# build_image.py -- draws the news-image-20261124 front page.
#
# A code-drawn newspaper front page summing up the world news of
# Tuesday 24 November 2026. Everything on the page is drawn with
# Pillow primitives (no photographs, no network): three large
# headline scenes, twelve smaller illustrated stories, a world map
# with numbered pins, a by-the-numbers bar and 27 one-line stories.
#
# Run:  python3 build_image.py   ->  writes entry.png (1024x1024)
# The drawing is deterministic: fixed geometry, fixed seed.

import math
import random
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor; final image is 1024x1024
W = H = 1024 * S
rng = random.Random(20261124)

PAPER = (247, 242, 231)
PAPER2 = (255, 253, 246)
INK = (26, 24, 20)
MUTE = (104, 95, 82)
RED = (179, 35, 27)
BLUE = (29, 78, 137)
GOLD = (176, 132, 26)
RULE = (60, 55, 48)

FDIR = "/usr/share/fonts/truetype/noto/"


def F(name, size):
    return ImageFont.truetype(FDIR + name, size * S)


SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SERIF = "NotoSerif-Regular.ttf"
SANS = "NotoSans-Regular.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS_BLACK = "NotoSans-Black.ttf"
SANS_COND = "NotoSans-CondensedBold.ttf"


def img_new():
    im = Image.new("RGB", (W, H), PAPER)
    return im, ImageDraw.Draw(im, "RGBA")


def xy(box):
    return [v * S for v in box]


def rect(d, box, fill=None, outline=None, width=1):
    d.rectangle(xy(box), fill=fill, outline=outline, width=max(1, int(width * S)))


def rectwh(d, b, fill=None, outline=None, width=1):
    """Rectangle from an (x, y, w, h) box."""
    x, y, w, h = b
    rect(d, [x, y, x + w, y + h], fill=fill, outline=outline, width=width)


def line(d, pts, fill=INK, width=1):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=max(1, int(width * S)))


def poly(d, pts, fill=None, outline=None):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)


def ellipse(d, box, fill=None, outline=None, width=1):
    d.ellipse(xy(box), fill=fill, outline=outline, width=max(1, int(width * S)))


def txt(d, pos, s, font, fill=INK, anchor="la", spacing=4):
    d.text((pos[0] * S, pos[1] * S), s, font=font, fill=fill, anchor=anchor,
           spacing=spacing * S)


def tw(d, s, font):
    return d.textlength(s, font=font) / S


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def person(d, cx, by, h, coat, skin=(232, 190, 150)):
    """Tiny standing figure: head + body, feet at (cx, by), height h."""
    hr = h * 0.16
    ellipse(d, [cx - hr, by - h, cx + hr, by - h + 2 * hr], fill=skin)
    poly(d, [(cx - h * 0.20, by), (cx + h * 0.20, by), (cx + h * 0.13, by - h * 0.62),
             (cx - h * 0.13, by - h * 0.62)], fill=coat)


def smoke(d, cx, cy, r, n=7, tone=70):
    for i in range(n):
        dx = rng.uniform(-r, r) * 0.6
        dy = rng.uniform(-r, r) * 0.38 - i * r * 0.13
        rr_ = r * rng.uniform(0.38, 0.78)
        g = tone + rng.randint(0, 45)
        ellipse(d, [cx + dx - rr_, cy + dy - rr_, cx + dx + rr_, cy + dy + rr_],
                fill=(g, g, g - 4, 105))


def sun(d, cx, cy, r, col=(244, 178, 62)):
    ellipse(d, [cx - r, cy - r, cx + r, cy + r], fill=col)


# ---------------------------------------------------------------- stories
# cred: 2 = multi-outlet confirmed, 1 = single source, 0 = developing
BIG = [
    dict(n=1, place="RIYADH, SAUDI ARABIA", lon=46.68, lat=24.71, scene="tower",
         head="HOUTHI MISSILE HITS RIYADH'S TALLEST TOWER AGAIN",
         body="Yemen's Houthis struck the PIF Tower, the capital's tallest "
              "building, a second time in five days; 11 were injured.",
         big="11", bigcap="injured · 2nd hit in 5 days", cred=2),
    dict(n=2, place="BENGHAZI, LIBYA", lon=20.07, lat=32.12, scene="ship",
         head="UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         body="Naval drones sank the Russian corvette Merkury in Benghazi "
              "port and hit a cargo ship — far beyond the Black Sea.",
         big="7", bigcap="naval drones · 1 corvette sunk", cred=2),
    dict(n=3, place="BROOKLYN, NEW YORK", lon=-73.99, lat=40.69, scene="court",
         head="HUAWEI GUILTY: JURY CONVICTS ON 10 OF 12 COUNTS",
         body="A US federal jury convicted Huawei of conspiracy to steal "
              "trade secrets and of bank fraud over its Iran business, "
              "ending a sprawling criminal trial in Brooklyn.",
         big="10/12", bigcap="counts proven in Brooklyn", cred=2),
]

MED = [
    dict(n=4, place="ZAPORIZHZHIA, UKRAINE", lon=35.18, lat=47.84, scene="apartment",
         head="Strike on flats: 2 dead, 40+ hurt", cred=2),
    dict(n=5, place="GAZA CITY", lon=34.45, lat=31.50, scene="gaza",
         head="Israeli strike kills Hamas security chief", cred=2),
    dict(n=6, place="STRAIT OF HORMUZ", lon=56.45, lat=26.57, scene="tanker",
         head="3 tankers hit mines and burn", cred=1),
    dict(n=7, place="SANTA CLARA, USA", lon=-122.03, lat=37.37, scene="chip",
         head="Nvidia -7% as Huang rally fades", cred=2),
    dict(n=8, place="DAKAR, SENEGAL", lon=-17.45, lat=14.72, scene="trophy",
         head="Senegal restored as AFCON champions", cred=2),
    dict(n=9, place="VILLAVICENCIO, COLOMBIA", lon=-73.64, lat=4.14, scene="carbomb",
         head="100 kg car bomb injures 25", cred=1),
    dict(n=10, place="GUASAVE, MEXICO", lon=-108.47, lat=25.57, scene="convoy",
         head="16 killed capturing 'El Chapo Isidro'", cred=1),
    dict(n=11, place="ORBIT OF MERCURY", lon=None, lat=None, scene="mercury",
         head="BepiColombo arrives after 8 years", cred=2),
    dict(n=12, place="BRUSSELS, BELGIUM", lon=4.35, lat=50.85, scene="airport",
         head="National strike shuts airports", cred=2),
    dict(n=13, place="TALLINN, ESTONIA", lon=24.75, lat=59.44, scene="border",
         head="Moscow warns Estonia of 'open war'", cred=2),
    dict(n=14, place="ATLANTIC, OFF DAKAR", lon=-19.5, lat=15.6, scene="boat",
         head="175 migrants missing at sea", cred=2),
    dict(n=15, place="MADRID, SPAIN", lon=-3.70, lat=40.42, scene="stadium",
         head="Real Madrid fight back, beat PSV 5–1", cred=2),
]

TEXTS = [
    (16, "KYIV", 30.52, 50.45, "Ukraine hits oil plants; Putin vows payback", 2),
    (17, "MOSCOW", 37.62, 55.76, "Leaked data: up to 700,000 Russian war dead", 1),
    (18, "ADEN", 45.03, 12.79, "Houthi fighters close to 60 km from Aden", 2),
    (19, "WASHINGTON", -77.04, 38.90, "Democrats win House by largest margin in decades", 1),
    (20, "WASHINGTON", -77.30, 38.80, "New US tariffs on China, EU loom after capacity probe", 2),
    (21, "SHANGHAI", 121.47, 31.23, "Politburo member Chen Jining under graft probe", 2),
    (22, "DHAKA", 90.41, 23.81, "Ousted PM Sheikh Hasina plans Dec 16 return home", 2),
    (23, "JERUSALEM", 35.21, 31.78, "Eisenkot signs first coalition deal in Israel", 2),
    (24, "THE HAGUE", 4.30, 52.08, "UK sanctions 5 Myanmar generals over Rohingya ruling", 2),
    (25, "BERLIN", 13.40, 52.52, "Germany first to gain Ukraine's Delta battle system", 1),
    (26, "SEOUL", 126.98, 37.57, "Russian jets enter Korea's air-defence zone", 2),
    (27, "SEOUL", 127.30, 37.30, "$375,000 reward to catch AI exam cheating", 1),
    (28, "ITURI, DR CONGO", 29.30, 1.40, "Fighting traps Ebola responders inside hospital", 2),
    (29, "INDONESIA", 106.85, -6.21, "Factory fire kills 26, dozens still missing", 1),
    (30, "LONDON", -0.13, 51.51, "UK records 5,258 heat-linked deaths in 2026", 1),
    (31, "NORFOLK, UK", 1.30, 52.63, "Masked men break into Prince William's home", 1),
    (32, "PARIS", 2.35, 48.86, "Sanofi-Insmed: biggest pharma deal since 2023", 1),
    (33, "PARIS", 2.60, 48.70, "Sarkozy and Carla Bruni to stand trial", 1),
    (34, "BRUSSELS", 4.60, 50.70, "NATO vows space defence after satellite reports", 2),
    (35, "WARSAW", 21.01, 52.23, "Poland: Russian drone came in on purpose", 1),
    (36, "STRASBOURG", 7.75, 48.58, "Court allows pushbacks as migration pressure", 1),
    (37, "OTTAWA", -75.70, 45.42, "Pentagon rebukes Canada as a defence partner", 1),
    (38, "HAVANA", -82.37, 23.11, "Cuban life expectancy falls, first time since 1950", 1),
    (39, "INDIA", 78.96, 21.15, "Sooryavanshi, 14, smashes 204 off just 53 balls", 1),
    (40, "BRASILIA", -47.88, -15.79, "Brazil trims 2027 growth forecast to 1.8%", 1),
    (41, "BEIJING", 116.40, 39.90, "Pakistani astronaut to fly on Shenzhou-24", 1),
    (42, "CANBERRA", 149.13, -35.28, "Australia lets users sue tech giants, fines 5%", 1),
    (43, "BAGHDAD", 44.37, 33.31, "Iraq PM orders takeover of Kurdish-area oilfields", 1),
    (44, "WASHINGTON ST.", -120.50, 47.40, "WHO told of 3 human bird-flu cases in US", 0),
]

NUMBERS = [
    ("700,000", "Russian war dead in leaked data"),
    ("-7%", "Nvidia a day after Huang's return"),
    ("$88.50", "Brent crude, little changed"),
    ("175", "migrants missing off Senegal"),
    ("26", "killed in Indonesia factory fire"),
    ("5,258", "UK heat-linked deaths in 2026"),
    ("60 km", "Houthi advance short of Aden"),
    ("204", "runs off 53 balls, age 14"),
]

CRED_MARK = {2: "●", 1: "◐", 0: "○"}


# ---------------------------------------------------------------- scenes
# Each painter draws inside box (x, y, w, h) in final-image coordinates.

def sky(d, b, top, bot):
    x, y, w, h = b
    steps = 24
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        rect(d, [x, y + h * i / steps, x + w, y + h * (i + 1) / steps + 1], fill=c)


def sc_tower(d, b):
    x, y, w, h = b
    sky(d, b, (38, 44, 66), (196, 120, 84))
    sun(d, x + w * 0.80, y + h * 0.30, w * 0.07, (250, 190, 90))
    # skyline
    for i, (bx, bh, bw) in enumerate([(0.02, 0.42, 0.10), (0.13, 0.55, 0.09),
                                      (0.66, 0.48, 0.10), (0.78, 0.62, 0.09),
                                      (0.89, 0.40, 0.09)]):
        rect(d, [x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(52, 52, 66))
    # PIF tower: tapered, centre
    tx0, tx1 = x + w * 0.36, x + w * 0.60
    poly(d, [(tx0 + w * 0.03, y + h), (tx1 - w * 0.03, y + h),
             (tx1 - w * 0.075, y + h * 0.10), (tx0 + w * 0.075, y + h * 0.10)],
         fill=(70, 78, 104))
    for i in range(6):
        yy = y + h * (0.18 + i * 0.13)
        line(d, [(tx0 + w * 0.085, yy), (tx1 - w * 0.085, yy)], fill=(150, 170, 205), width=2)
    # missile trail + impact flash
    line(d, [(x + w * 0.06, y + h * 0.06), (x + w * 0.44, y + h * 0.30)], fill=(255, 226, 160), width=3)
    cx, cy = x + w * 0.47, y + h * 0.32
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        line(d, [(cx, cy), (cx + math.cos(a) * w * 0.085, cy + math.sin(a) * w * 0.085)],
             fill=(255, 170, 60), width=3)
    ellipse(d, [cx - w * 0.045, cy - w * 0.045, cx + w * 0.045, cy + w * 0.045], fill=(255, 214, 110))
    smoke(d, cx + w * 0.05, cy - h * 0.05, w * 0.075)
    rect(d, [x, y + h * 0.94, x + w, y + h], fill=(30, 28, 34))


def sc_ship(d, b):
    x, y, w, h = b
    sky(d, b, (52, 74, 104), (168, 178, 178))
    rect(d, [x, y + h * 0.58, x + w, y + h], fill=(36, 74, 104))
    for i in range(9):  # waves
        wx = x + w * (0.05 + 0.11 * i)
        line(d, [(wx, y + h * (0.70 + 0.07 * (i % 3))), (wx + w * 0.05, y + h * (0.70 + 0.07 * (i % 3)))],
             fill=(120, 170, 200), width=2)
    # warship hull + superstructure, listing
    hx, hy = x + w * 0.16, y + h * 0.52
    poly(d, [(hx, hy), (hx + w * 0.62, hy), (hx + w * 0.55, hy + h * 0.12),
             (hx + w * 0.08, hy + h * 0.12)], fill=(58, 62, 70))
    rect(d, [hx + w * 0.20, hy - h * 0.16, hx + w * 0.34, hy], fill=(74, 78, 88))
    rect(d, [hx + w * 0.38, hy - h * 0.10, hx + w * 0.47, hy], fill=(74, 78, 88))
    line(d, [(hx + w * 0.27, hy - h * 0.16), (hx + w * 0.27, hy - h * 0.30)], fill=INK, width=2)
    # drones
    for (dx, dy) in [(0.70, 0.14), (0.80, 0.08), (0.60, 0.05)]:
        cx, cy = x + w * dx, y + h * dy
        line(d, [(cx - w * 0.035, cy), (cx + w * 0.035, cy)], fill=INK, width=3)
        line(d, [(cx, cy - h * 0.05), (cx, cy + h * 0.05)], fill=INK, width=2)
        line(d, [(cx, cy), (hx + w * 0.42, hy - h * 0.05)], fill=(200, 60, 40), width=1)
    # explosion at stern
    cx, cy = hx + w * 0.52, hy - h * 0.06
    for ang in range(0, 360, 36):
        a = math.radians(ang)
        line(d, [(cx, cy), (cx + math.cos(a) * w * 0.07, cy + math.sin(a) * w * 0.07)],
             fill=(246, 130, 40), width=3)
    ellipse(d, [cx - w * 0.035, cy - w * 0.035, cx + w * 0.035, cy + w * 0.035], fill=(250, 190, 80))
    smoke(d, cx + w * 0.03, cy - h * 0.10, w * 0.085)


def sc_court(d, b):
    x, y, w, h = b
    sky(d, b, (214, 206, 188), (238, 232, 214))
    # courthouse: pediment + columns
    poly(d, [(x + w * 0.10, y + h * 0.26), (x + w * 0.90, y + h * 0.26),
             (x + w * 0.50, y + h * 0.06)], fill=(150, 138, 116))
    rect(d, [x + w * 0.10, y + h * 0.26, x + w * 0.90, y + h * 0.32], fill=(120, 108, 88))
    for i in range(6):
        cx = x + w * (0.16 + i * 0.125)
        rect(d, [cx, y + h * 0.32, cx + w * 0.055, y + h * 0.78], fill=(216, 206, 184),
             outline=(110, 100, 82), width=2)
    rect(d, [x + w * 0.06, y + h * 0.78, x + w * 0.94, y + h * 0.84], fill=(120, 108, 88))
    rect(d, [x, y + h * 0.92, x + w, y + h], fill=(96, 88, 72))
    for i in range(4):
        rect(d, [x + w * (0.08 + i * 0.24), y + h * 0.84, x + w * (0.92 - (3 - i) * 0.24), y + h * 0.86],
             fill=(140, 130, 108))
    # gavel, front right: handle + head + sound block
    gx, gy = x + w * 0.70, y + h * 0.64
    line(d, [(gx, gy), (gx + w * 0.13, gy - h * 0.13)], fill=(110, 72, 34), width=6)
    rect(d, [gx + w * 0.085, gy - h * 0.215, gx + w * 0.205, gy - h * 0.125], fill=(140, 94, 44),
         outline=(90, 58, 24), width=2)
    rect(d, [gx - w * 0.02, gy + h * 0.13, gx + w * 0.20, gy + h * 0.18], fill=(110, 72, 34))
    # scales, front left
    sx, sy = x + w * 0.22, y + h * 0.52
    line(d, [(sx, sy), (sx, sy + h * 0.30)], fill=(90, 74, 40), width=4)
    line(d, [(sx - w * 0.11, sy + h * 0.05), (sx + w * 0.11, sy + h * 0.05)], fill=(90, 74, 40), width=4)
    for sgn in (-1, 1):
        px = sx + sgn * w * 0.11
        line(d, [(px, sy + h * 0.05), (px - w * 0.045, sy + h * 0.20)], fill=(90, 74, 40), width=2)
        line(d, [(px, sy + h * 0.05), (px + w * 0.045, sy + h * 0.20)], fill=(90, 74, 40), width=2)
        poly(d, [(px - w * 0.055, sy + h * 0.20), (px + w * 0.055, sy + h * 0.20),
                 (px, sy + h * 0.27)], fill=GOLD)


def sc_apartment(d, b):
    x, y, w, h = b
    sky(d, b, (70, 66, 78), (150, 120, 105))
    bx, bw = x + w * 0.30, w * 0.42
    rect(d, [bx, y + h * 0.10, bx + bw, y + h], fill=(104, 96, 92))
    for r in range(5):
        for c in range(4):
            wx, wy = bx + bw * (0.08 + c * 0.24), y + h * (0.17 + r * 0.16)
            col = (250, 200, 90) if (r * 4 + c) % 3 else (60, 58, 66)
            if r == 1 and c >= 2:
                col = (30, 28, 30)
            rect(d, [wx, wy, wx + bw * 0.15, wy + h * 0.10], fill=col)
    smoke(d, bx + bw * 0.78, y + h * 0.10, w * 0.13, tone=45)
    rect(d, [bx + bw * 0.55, y + h * 0.08, bx + bw * 1.0, y + h * 0.30], fill=(40, 36, 38))
    rect(d, [x, y + h * 0.93, x + w, y + h], fill=(44, 40, 44))
    person(d, x + w * 0.16, y + h * 0.97, h * 0.20, (70, 90, 140))
    person(d, x + w * 0.22, y + h * 0.97, h * 0.17, (150, 60, 50))


def sc_gaza(d, b):
    x, y, w, h = b
    sky(d, b, (96, 84, 84), (196, 156, 120))
    sun(d, x + w * 0.16, y + h * 0.24, w * 0.06, (246, 196, 110))
    for i, (bx, bh, bw) in enumerate([(0.04, 0.52, 0.16), (0.22, 0.66, 0.13), (0.37, 0.45, 0.15),
                                      (0.54, 0.60, 0.12), (0.68, 0.50, 0.14), (0.84, 0.64, 0.13)]):
        rect(d, [x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(88, 78, 74))
        for r in range(int(bh * 5)):
            for c in range(2):
                if (i + r + c) % 3:
                    rect(d, [x + w * (bx + 0.02 + c * bw * 0.45), y + h - h * bh + h * (0.06 + r * 0.17),
                             x + w * (bx + 0.05 + c * bw * 0.45), y + h - h * bh + h * (0.12 + r * 0.17)],
                         fill=(240, 205, 120))
    smoke(d, x + w * 0.60, y + h * 0.28, w * 0.13, tone=55)
    smoke(d, x + w * 0.30, y + h * 0.20, w * 0.09, tone=80)
    rect(d, [x, y + h * 0.95, x + w, y + h], fill=(52, 46, 44))


def sc_tanker(d, b):
    x, y, w, h = b
    sky(d, b, (58, 80, 108), (170, 168, 150))
    rect(d, [x, y + h * 0.55, x + w, y + h], fill=(30, 62, 92))
    hx, hy = x + w * 0.10, y + h * 0.47
    poly(d, [(hx, hy), (hx + w * 0.78, hy), (hx + w * 0.70, hy + h * 0.14),
             (hx + w * 0.06, hy + h * 0.14)], fill=(150, 44, 36))
    rect(d, [hx + w * 0.06, hy - h * 0.07, hx + w * 0.68, hy], fill=(70, 70, 76))
    rect(d, [hx + w * 0.62, hy - h * 0.20, hx + w * 0.72, hy - h * 0.07], fill=(210, 205, 195))
    # flames on deck
    for fx in (0.24, 0.36, 0.48):
        cx = hx + w * fx
        poly(d, [(cx - w * 0.035, hy - h * 0.07), (cx + w * 0.035, hy - h * 0.07),
                 (cx, hy - h * 0.30)], fill=(244, 120, 36))
        poly(d, [(cx - w * 0.018, hy - h * 0.07), (cx + w * 0.018, hy - h * 0.07),
                 (cx, hy - h * 0.20)], fill=(250, 196, 84))
    smoke(d, hx + w * 0.40, hy - h * 0.40, w * 0.09, tone=50)
    for i in range(7):
        wx = x + w * (0.06 + 0.14 * i)
        line(d, [(wx, y + h * (0.78 + 0.06 * (i % 2))), (wx + w * 0.06, y + h * (0.78 + 0.06 * (i % 2)))],
             fill=(130, 180, 210), width=2)


def sc_chip(d, b):
    x, y, w, h = b
    rectwh(d, b, fill=(24, 34, 30))
    # circuit traces
    for i in range(5):
        yy = y + h * (0.12 + i * 0.19)
        line(d, [(x + w * 0.04, yy), (x + w * 0.30, yy), (x + w * 0.38, yy + h * 0.08)], fill=(46, 92, 70), width=2)
        line(d, [(x + w * 0.96, yy), (x + w * 0.70, yy), (x + w * 0.62, yy + h * 0.08)], fill=(46, 92, 70), width=2)
    # chip
    rect(d, [x + w * 0.36, y + h * 0.26, x + w * 0.64, y + h * 0.66], fill=(38, 48, 44),
         outline=(120, 200, 150), width=2)
    txt(d, (x + w * 0.50, y + h * 0.46), "AI", F(SANS_BLACK, 26), fill=(150, 230, 170), anchor="ma")
    # plunging chart across the bottom
    pts = [(0.04, 0.70), (0.20, 0.66), (0.34, 0.72), (0.50, 0.68), (0.64, 0.80), (0.80, 0.86), (0.96, 0.95)]
    line(d, [(x + w * px, y + h * py) for px, py in pts], fill=(255, 92, 74), width=4)
    poly(d, [(x + w * 0.96, y + h * 0.95), (x + w * 0.90, y + h * 0.90), (x + w * 0.915, y + h * 0.99)],
         fill=(255, 92, 74))
    txt(d, (x + w * 0.06, y + h * 0.06), "NVDA -7%", F(SANS_BLACK, 17), fill=(255, 120, 100), anchor="la")


def sc_trophy(d, b):
    x, y, w, h = b
    sky(d, b, (30, 110, 62), (120, 190, 110))
    rect(d, [x, y + h * 0.78, x + w, y + h], fill=(26, 96, 54))
    line(d, [(x, y + h * 0.78), (x + w, y + h * 0.78)], fill=(230, 240, 220), width=2)
    cx, cy = x + w * 0.50, y + h * 0.34
    ellipse(d, [cx - w * 0.10, cy - w * 0.10, cx + w * 0.10, cy + w * 0.10], fill=GOLD,
            outline=(120, 88, 16), width=2)
    poly(d, [(cx - w * 0.035, cy + w * 0.09), (cx + w * 0.035, cy + w * 0.09),
             (cx + w * 0.02, cy + w * 0.20), (cx - w * 0.02, cy + w * 0.20)], fill=GOLD)
    rect(d, [cx - w * 0.09, cy + w * 0.20, cx + w * 0.09, cy + w * 0.26], fill=(110, 78, 20))
    for sgn in (-1, 1):
        ellipse(d, [cx + sgn * w * 0.16 - w * 0.05, cy - w * 0.06, cx + sgn * w * 0.16 + w * 0.05,
                    cy + w * 0.06], outline=(230, 190, 70), width=3)
    # football
    fx, fy = x + w * 0.20, y + h * 0.86
    ellipse(d, [fx - w * 0.06, fy - w * 0.06, fx + w * 0.06, fy + w * 0.06], fill=(245, 245, 245),
            outline=INK, width=2)
    poly(d, [(fx - w * 0.02, fy - w * 0.02), (fx + w * 0.02, fy - w * 0.02), (fx + w * 0.03, fy + w * 0.015),
             (fx, fy + w * 0.03), (fx - w * 0.03, fy + w * 0.015)], fill=INK)
    person(d, x + w * 0.78, y + h * 0.97, h * 0.30, (20, 140, 70))
    person(d, x + w * 0.86, y + h * 0.97, h * 0.30, (250, 205, 40))


def sc_carbomb(d, b):
    x, y, w, h = b
    sky(d, b, (120, 104, 96), (206, 178, 150))
    rect(d, [x, y + h * 0.80, x + w, y + h], fill=(80, 74, 70))
    for i, (bx, bh, bw) in enumerate([(0.04, 0.44, 0.16), (0.70, 0.50, 0.14), (0.86, 0.38, 0.12)]):
        rect(d, [x + w * bx, y + h * 0.80 - h * bh, x + w * (bx + bw), y + h * 0.80], fill=(110, 98, 90))
    # car + blast
    cx, cy = x + w * 0.44, y + h * 0.76
    rect(d, [cx - w * 0.11, cy - h * 0.07, cx + w * 0.11, cy + h * 0.03], fill=(60, 60, 66))
    for ang in range(0, 360, 28):
        a = math.radians(ang)
        r1 = w * (0.10 + 0.05 * math.sin(ang * 2.3))
        line(d, [(cx, cy - h * 0.10), (cx + math.cos(a) * r1, cy - h * 0.10 + math.sin(a) * r1 * 0.8)],
             fill=(246, 140, 44), width=3)
    ellipse(d, [cx - w * 0.05, cy - h * 0.10 - w * 0.05, cx + w * 0.05, cy - h * 0.10 + w * 0.05],
            fill=(250, 200, 90))
    smoke(d, cx, cy - h * 0.34, w * 0.13, tone=60)
    person(d, x + w * 0.14, y + h * 0.97, h * 0.22, (60, 80, 130))


def sc_convoy(d, b):
    x, y, w, h = b
    sky(d, b, (214, 168, 96), (238, 205, 140))
    sun(d, x + w * 0.14, y + h * 0.20, w * 0.06)
    poly(d, [(x, y + h * 0.62), (x + w * 0.35, y + h * 0.40), (x + w * 0.62, y + h * 0.62)],
         fill=(186, 138, 84))
    poly(d, [(x + w * 0.55, y + h * 0.62), (x + w * 0.85, y + h * 0.44), (x + w, y + h * 0.62)],
         fill=(196, 148, 92))
    rect(d, [x, y + h * 0.62, x + w, y + h], fill=(206, 164, 104))
    # cactus
    gx = x + w * 0.88
    line(d, [(gx, y + h * 0.86), (gx, y + h * 0.60)], fill=(52, 110, 60), width=5)
    line(d, [(gx, y + h * 0.70), (gx - w * 0.05, y + h * 0.70), (gx - w * 0.05, y + h * 0.63)],
         fill=(52, 110, 60), width=4)
    line(d, [(gx, y + h * 0.74), (gx + w * 0.05, y + h * 0.74), (gx + w * 0.05, y + h * 0.66)],
         fill=(52, 110, 60), width=4)
    # two trucks
    for i, tx in enumerate((0.14, 0.48)):
        ty = y + h * (0.72 + i * 0.07)
        rect(d, [x + w * tx, ty, x + w * (tx + 0.24), ty + h * 0.10], fill=(84, 88, 74))
        rect(d, [x + w * (tx + 0.24), ty + h * 0.03, x + w * (tx + 0.31), ty + h * 0.10], fill=(70, 74, 62))
        for wx in (tx + 0.05, tx + 0.22):
            ellipse(d, [x + w * wx, ty + h * 0.09, x + w * (wx + 0.055), ty + h * 0.09 + w * 0.055],
                    fill=(30, 30, 30))
    # dust
    for i in range(5):
        ellipse(d, [x + w * (0.06 + i * 0.03), y + h * (0.78 + 0.03 * (i % 2)),
                    x + w * (0.11 + i * 0.03), y + h * (0.84 + 0.03 * (i % 2))],
                fill=(226, 190, 130, 150))


def sc_mercury(d, b):
    x, y, w, h = b
    rectwh(d, b, fill=(10, 12, 24))
    for i in range(40):
        sx, sy = x + rng.uniform(0, w), y + rng.uniform(0, h)
        r = rng.uniform(0.6, 1.6)
        ellipse(d, [sx - r, sy - r, sx + r, sy + r], fill=(230, 230, 240))
    # Mercury
    cx, cy, r = x + w * 0.70, y + h * 0.55, w * 0.20
    ellipse(d, [cx - r, cy - r, cx + r, cy + r], fill=(168, 148, 128))
    for (ox, oy, orr) in [(-0.08, -0.05, 0.045), (0.06, 0.07, 0.06), (0.02, -0.11, 0.035), (-0.11, 0.08, 0.03)]:
        ellipse(d, [cx + w * ox - w * orr, cy + w * oy - w * orr, cx + w * ox + w * orr, cy + w * oy + w * orr],
                fill=(140, 122, 102))
    poly(d, [(cx - r * 0.98, cy - r), (cx - r * 0.35, cy - r), (cx - r * 0.35, cy + r), (cx - r * 0.98, cy + r)],
         fill=(10, 12, 24, 90))
    # BepiColombo: bus + two panels + boom
    bx, by = x + w * 0.26, y + h * 0.34
    rect(d, [bx - w * 0.045, by - h * 0.07, bx + w * 0.045, by + h * 0.07], fill=(200, 200, 210),
         outline=(120, 120, 140), width=1)
    rect(d, [bx - w * 0.20, by - h * 0.045, bx - w * 0.06, by + h * 0.045], fill=(52, 74, 160))
    rect(d, [bx + w * 0.06, by - h * 0.045, bx + w * 0.20, by + h * 0.045], fill=(52, 74, 160))
    line(d, [(bx, by + h * 0.07), (bx + w * 0.10, by + h * 0.20)], fill=(190, 190, 200), width=2)
    ellipse(d, [bx + w * 0.085, by + h * 0.185, bx + w * 0.125, by + h * 0.225], outline=(220, 220, 230), width=2)
    line(d, [(bx + w * 0.10, by + h * 0.22), (cx - r * 0.8, cy - r * 0.3)], fill=(250, 210, 90), width=1)


def sc_airport(d, b):
    x, y, w, h = b
    sky(d, b, (120, 150, 190), (205, 214, 220))
    rect(d, [x, y + h * 0.80, x + w, y + h], fill=(140, 146, 150))
    # terminal
    rect(d, [x + w * 0.06, y + h * 0.42, x + w * 0.62, y + h * 0.80], fill=(168, 176, 184))
    for i in range(6):
        rect(d, [x + w * (0.10 + i * 0.085), y + h * 0.50, x + w * (0.155 + i * 0.085), y + h * 0.62],
             fill=(90, 120, 150))
    rect(d, [x + w * 0.68, y + h * 0.18, x + w * 0.76, y + h * 0.80], fill=(150, 156, 164))
    rect(d, [x + w * 0.665, y + h * 0.14, x + w * 0.775, y + h * 0.20], fill=(110, 116, 124))
    # parked plane
    px, py = x + w * 0.60, y + h * 0.70
    ellipse(d, [px, py, px + w * 0.30, py + h * 0.07], fill=(235, 238, 240))
    poly(d, [(px + w * 0.27, py - h * 0.02), (px + w * 0.33, py - h * 0.12), (px + w * 0.33, py + h * 0.03)],
         fill=(52, 92, 160))
    poly(d, [(px + w * 0.10, py + h * 0.05), (px + w * 0.20, py + h * 0.13), (px + w * 0.22, py + h * 0.05)],
         fill=(200, 204, 208))
    # CLOSED sign
    rect(d, [x + w * 0.10, y + h * 0.06, x + w * 0.44, y + h * 0.20], fill=(250, 248, 240),
         outline=RED, width=3)
    txt(d, (x + w * 0.27, y + h * 0.13), "CLOSED", F(SANS_BLACK, 15), fill=RED, anchor="ma")
    person(d, x + w * 0.52, y + h * 0.97, h * 0.20, (70, 70, 80))
    person(d, x + w * 0.57, y + h * 0.97, h * 0.20, (150, 60, 50))


def sc_border(d, b):
    x, y, w, h = b
    sky(d, b, (140, 160, 180), (210, 208, 190))
    rect(d, [x, y + h * 0.66, x + w, y + h], fill=(120, 140, 96))
    # forest line
    for i in range(9):
        fx = x + w * (0.03 + i * 0.11)
        poly(d, [(fx, y + h * 0.66), (fx + w * 0.05, y + h * 0.44), (fx + w * 0.10, y + h * 0.66)],
             fill=(52, 92, 58))
    # fence posts + wire
    for i in range(7):
        fx = x + w * (0.05 + i * 0.15)
        line(d, [(fx, y + h * 0.60), (fx, y + h * 0.92)], fill=(70, 60, 50), width=4)
    for fy in (0.66, 0.76, 0.86):
        line(d, [(x, y + h * fy), (x + w, y + h * fy)], fill=(90, 84, 76), width=2)
    # warning sign
    rect(d, [x + w * 0.58, y + h * 0.10, x + w * 0.96, y + h * 0.26], fill=(250, 248, 240),
         outline=INK, width=2)
    txt(d, (x + w * 0.77, y + h * 0.145), "BORDER", F(SANS_BLACK, 13), fill=INK, anchor="ma")
    txt(d, (x + w * 0.77, y + h * 0.205), "CLOSES DEC 1", F(SANS_BOLD, 9), fill=RED, anchor="ma")
    line(d, [(x + w * 0.77, y + h * 0.26), (x + w * 0.77, y + h * 0.60)], fill=(70, 60, 50), width=4)


def sc_boat(d, b):
    x, y, w, h = b
    sky(d, b, (70, 96, 128), (168, 172, 160))
    sun(d, x + w * 0.82, y + h * 0.18, w * 0.055, (240, 200, 110))
    rect(d, [x, y + h * 0.52, x + w, y + h], fill=(28, 66, 100))
    for i in range(10):
        wx = x + w * (0.03 + 0.10 * i)
        yy = y + h * (0.60 + 0.09 * (i % 3))
        line(d, [(wx, yy), (wx + w * 0.055, yy)], fill=(130, 180, 210), width=2)
    # small overloaded boat
    bx, by = x + w * 0.30, y + h * 0.55
    poly(d, [(bx, by), (bx + w * 0.42, by), (bx + w * 0.35, by + h * 0.11), (bx + w * 0.07, by + h * 0.11)],
         fill=(120, 84, 50))
    for i in range(6):
        person(d, bx + w * (0.08 + i * 0.055), by + h * 0.015, h * 0.17,
               [(180, 80, 60), (60, 100, 160), (220, 180, 60), (90, 140, 90), (160, 60, 120), (240, 240, 240)][i])
    line(d, [(bx + w * 0.21, by), (bx + w * 0.21, by - h * 0.16)], fill=(90, 70, 46), width=3)
    poly(d, [(bx + w * 0.21, by - h * 0.16), (bx + w * 0.30, by - h * 0.05), (bx + w * 0.21, by - h * 0.03)],
         fill=(235, 230, 215))


def sc_stadium(d, b):
    x, y, w, h = b
    sky(d, b, (24, 34, 64), (70, 90, 130))
    # floodlights
    for fx in (0.10, 0.90):
        line(d, [(x + w * fx, y + h * 0.42), (x + w * fx, y + h * 0.10)], fill=(200, 205, 215), width=3)
        for r in range(2):
            for c in range(3):
                rect(d, [x + w * (fx - 0.045 + c * 0.032), y + h * (0.045 + r * 0.05),
                         x + w * (fx - 0.022 + c * 0.032), y + h * (0.085 + r * 0.05)],
                     fill=(255, 246, 190))
    # stands
    poly(d, [(x + w * 0.04, y + h * 0.66), (x + w * 0.16, y + h * 0.40), (x + w * 0.84, y + h * 0.40),
             (x + w * 0.96, y + h * 0.66)], fill=(88, 60, 60))
    for i in range(160):
        px, py = rng.uniform(0.08, 0.92), rng.uniform(0.44, 0.62)
        c = [(230, 80, 70), (240, 240, 240), (240, 190, 80), (120, 160, 230)][i % 4]
        ellipse(d, [x + w * px, y + h * py, x + w * px + 3 * S, y + h * py + 3 * S], fill=c)
    # pitch
    poly(d, [(x + w * 0.04, y + h * 0.66), (x + w * 0.96, y + h * 0.66), (x + w, y + h), (x, y + h)],
         fill=(34, 120, 56))
    ellipse(d, [x + w * 0.42, y + h * 0.76, x + w * 0.58, y + h * 0.90], outline=(235, 240, 230), width=2)
    person(d, x + w * 0.38, y + h * 0.90, h * 0.16, (240, 240, 240))
    person(d, x + w * 0.60, y + h * 0.92, h * 0.16, (200, 40, 40))
    # scoreboard
    rect(d, [x + w * 0.36, y + h * 0.07, x + w * 0.64, y + h * 0.19], fill=(16, 18, 26),
         outline=(200, 205, 215), width=2)
    txt(d, (x + w * 0.50, y + h * 0.095), "RMA 5-1 PSV", F(SANS_BLACK, 13), fill=(255, 220, 90), anchor="ma")

SCENES = {
    "tower": sc_tower, "ship": sc_ship, "court": sc_court, "apartment": sc_apartment,
    "gaza": sc_gaza, "tanker": sc_tanker, "chip": sc_chip, "trophy": sc_trophy,
    "carbomb": sc_carbomb, "convoy": sc_convoy, "mercury": sc_mercury,
    "airport": sc_airport, "border": sc_border, "boat": sc_boat, "stadium": sc_stadium,
}


# ---------------------------------------------------------------- world map
# Coarse hand-drawn continent outlines in (lon, lat). Stylised on purpose:
# at poster scale the silhouettes read as the world, and the numbered pins
# carry the geography.
LAND = [
    # North America
    [(-166, 68), (-158, 71), (-148, 70), (-140, 70), (-132, 69), (-125, 71), (-115, 72),
     (-105, 72), (-98, 76), (-92, 78), (-88, 76), (-86, 72), (-90, 69), (-95, 67), (-93, 64),
     (-86, 62), (-80, 62), (-79, 58), (-77, 56), (-72, 54), (-66, 51), (-60, 47), (-65, 44),
     (-69, 42), (-72, 40), (-75, 38), (-76, 35), (-79, 33), (-81, 30), (-81, 25), (-84, 28),
     (-86, 30), (-90, 29), (-95, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 15), (-86, 13),
     (-83, 9), (-79, 9), (-82, 8), (-85, 11), (-89, 14), (-94, 16), (-97, 16), (-101, 18),
     (-104, 20), (-107, 23), (-110, 24), (-111, 28), (-114, 31), (-117, 33), (-121, 34),
     (-123, 38), (-124, 43), (-124, 47), (-129, 52), (-134, 56), (-141, 60), (-152, 59),
     (-158, 56), (-162, 58), (-166, 60), (-168, 65)],
    # Greenland
    [(-46, 60), (-40, 63), (-32, 68), (-22, 70), (-20, 74), (-26, 78), (-40, 80), (-55, 78),
     (-58, 73), (-54, 66), (-52, 61)],
    # South America
    [(-78, 7), (-75, 10), (-71, 12), (-66, 10), (-61, 9), (-55, 6), (-51, 4), (-50, 0),
     (-44, -3), (-38, -5), (-35, -8), (-39, -13), (-40, -20), (-42, -23), (-48, -27),
     (-52, -33), (-57, -38), (-58, -41), (-62, -43), (-65, -46), (-67, -50), (-68, -54),
     (-71, -54), (-72, -50), (-73, -44), (-73, -37), (-72, -31), (-70, -24), (-70, -18),
     (-75, -15), (-78, -8), (-80, -4), (-80, 1), (-78, 4)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (19, 32), (28, 31), (32, 31), (34, 28),
     (37, 23), (39, 20), (41, 15), (43, 12), (47, 11), (51, 12), (49, 6), (44, 0),
     (41, -6), (40, -12), (39, -18), (37, -22), (35, -26), (32, -29), (29, -32), (26, -34),
     (20, -35), (18, -33), (16, -28), (14, -22), (13, -16), (12, -10), (13, -5), (9, -1),
     (9, 4), (5, 6), (-1, 5), (-7, 4), (-12, 8), (-16, 12), (-17, 15), (-16, 20),
     (-15, 25), (-13, 28), (-10, 31), (-6, 35)],
    # Madagascar
    [(44, -16), (47, -14), (50, -17), (49, -21), (47, -24), (45, -25), (44, -22), (43, -19)],
    # Europe
    [(-9, 37), (-2, 37), (0, 39), (3, 42), (6, 43), (8, 44), (10, 44), (13, 41), (15, 38),
     (18, 40), (19, 42), (15, 44), (13, 45), (18, 46), (20, 45), (23, 40), (24, 38),
     (23, 36), (26, 38), (28, 41), (27, 44), (30, 46), (32, 46), (33, 45), (30, 46),
     (28, 45), (24, 44), (22, 45), (20, 46), (16, 47), (12, 47), (9, 47), (6, 48),
     (3, 49), (1, 50), (-1, 50), (-4, 48), (-2, 49), (-5, 48), (-1, 46), (-2, 44),
     (-9, 44), (-9, 37)],
    # Scandinavia + Baltic
    [(5, 58), (5, 60), (7, 62), (11, 64), (15, 66), (19, 69), (25, 71), (31, 70),
     (35, 67), (33, 64), (30, 61), (27, 60), (23, 59), (21, 59), (18, 59), (17, 57),
     (14, 56), (11, 57), (8, 57), (5, 58)],
    # Britain
    [(-5, 50), (-3, 52), (-2, 54), (-3, 56), (-5, 58), (-7, 57), (-6, 55), (-5, 53), (-5, 50)],
    # Asia (incl. Siberia, Arabia, India handled below, SE Asia)
    [(30, 41), (36, 42), (41, 43), (45, 42), (48, 41), (50, 39), (53, 37), (57, 37),
     (61, 35), (65, 35), (69, 34), (72, 33), (75, 31), (78, 29), (80, 26), (79, 21),
     (77, 12), (78, 8), (80, 13), (83, 17), (86, 20), (88, 22), (91, 22), (92, 16),
     (94, 17), (97, 15), (98, 10), (99, 6), (100, 3), (102, 1), (104, 3), (106, 8),
     (107, 12), (108, 16), (109, 19), (110, 21), (113, 22), (116, 23), (119, 25),
     (121, 28), (122, 31), (121, 33), (120, 35), (122, 37), (124, 39), (126, 40),
     (128, 41), (130, 42), (132, 43), (135, 45), (138, 46), (140, 48), (142, 50),
     (142, 53), (140, 56), (142, 59), (146, 60), (151, 60), (156, 59), (159, 55),
     (161, 57), (163, 60), (166, 61), (169, 63), (172, 65), (176, 66), (178, 67),
     (178, 69), (172, 69), (164, 69), (156, 70), (148, 70), (140, 71), (132, 71),
     (124, 72), (116, 72), (108, 73), (100, 74), (94, 76), (88, 74), (82, 73),
     (76, 72), (70, 72), (66, 70), (60, 69), (54, 69), (48, 68), (43, 68), (38, 67),
     (35, 65), (33, 63), (31, 59), (29, 53), (30, 47), (30, 41)],
    # Arabia (fills the notch under Asia's west edge)
    [(35, 28), (38, 24), (40, 20), (42, 15), (45, 12), (49, 12), (53, 13), (56, 16),
     (58, 19), (59, 22), (57, 25), (54, 26), (51, 27), (49, 28), (48, 29), (46, 28),
     (42, 29), (38, 29), (35, 28)],
    # Korea
    [(126, 38), (128, 39), (129, 41), (130, 42), (128, 40), (127, 37), (126, 36), (126, 38)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 37), (141, 39),
     (141, 42), (142, 44), (143, 43), (142, 40), (140, 38), (138, 36), (135, 34),
     (133, 34), (131, 32), (130, 31)],
    # Sumatra / Borneo / Java / New Guinea
    [(95, 5), (99, 2), (103, -2), (106, -6), (104, -5), (100, 0), (96, 4), (95, 5)],
    [(109, 1), (112, 3), (116, 5), (119, 2), (118, -1), (115, -3), (112, -2), (109, 1)],
    [(106, -6), (110, -7), (114, -8), (114, -9), (108, -8), (106, -7)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9), (142, -8),
     (137, -6), (132, -4), (131, -1)],
    # Australia
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32), (132, -32),
     (135, -35), (137, -35), (139, -37), (141, -38), (145, -38), (147, -39), (150, -37),
     (153, -32), (153, -27), (151, -24), (149, -20), (146, -19), (143, -15), (142, -11),
     (142, -14), (145, -15), (143, -18), (142, -21), (140, -25), (138, -29), (136, -32),
     (133, -32), (130, -31), (126, -32), (121, -34), (117, -35), (115, -33), (113, -26),
     (113, -22)],
    # New Zealand
    [(167, -46), (169, -44), (171, -42), (173, -40), (175, -38), (177, -38), (176, -40),
     (174, -42), (172, -44), (169, -46), (167, -46)],
    [(173, -35), (175, -36), (177, -37), (176, -39), (174, -40), (173, -39), (172, -36),
     (173, -35)],
]


def project(lon, lat, b):
    x, y, w, h = b
    return (x + (lon + 180) / 360 * w, y + (78 - lat) / 140 * h)


def pin(d, cx, cy, n, r=10):
    ellipse(d, [cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 250, 240), width=2)
    f = F(SANS_BLACK, 11 if n < 10 else 10)
    txt(d, (cx, cy - 1), str(n), f, fill=(255, 250, 240), anchor="ma")


def draw_map(d, b):
    x, y, w, h = b
    rectwh(d, b, fill=(196, 216, 228))
    for i in range(7):  # graticule
        gx = x + w * i / 6
        line(d, [(gx, y), (gx, y + h)], fill=(170, 196, 214), width=1)
        gy = y + h * i / 6
        line(d, [(x, gy), (x + w, gy)], fill=(170, 196, 214), width=1)
    for shape in LAND:
        pts = [project(lon, lat, b) for lon, lat in shape]
        poly(d, pts, fill=(226, 216, 178), outline=(150, 138, 104))
    spots = {}
    for s in BIG + MED:
        if s["lon"] is not None:
            spots[s["n"]] = (s["lon"], s["lat"])
    for (n, place, lon, lat, head, cred) in TEXTS:
        spots.setdefault(n, (lon, lat))
    for n, (lon, lat) in sorted(spots.items()):
        cx, cy = project(lon, lat, b)
        pin(d, cx, cy, n, r=9 if n <= 15 else 8)
    txt(d, (x + 8, y + 6), "WHERE IT HAPPENED — pin numbers match the stories",
        F(SANS_BOLD, 11), fill=(40, 60, 84), anchor="la")
    txt(d, (x + w - 8, y + h - 18), "Mercury (11) is off the map — it is in orbit",
        F(SANS, 10), fill=(40, 60, 84), anchor="ra")


# ---------------------------------------------------------------- assembly

CRED_COL = {2: (30, 120, 60), 1: (190, 130, 20), 0: (170, 60, 50)}


def cred_chip(d, cx, cy, cred, r=5.5):
    """Credibility mark drawn as a circle (the font has no ●/◐/○ glyphs):
    filled = 3+ outlets, half = single source, ring = still developing."""
    col = CRED_COL[cred]
    if cred == 2:
        ellipse(d, [cx - r, cy - r, cx + r, cy + r], fill=col)
    elif cred == 1:
        ellipse(d, [cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
        d.pieslice(xy([cx - r, cy - r, cx + r, cy + r]), 90, 270, fill=col)
    else:
        ellipse(d, [cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    return 2 * r + 2


def big_panel(d, b, s):
    x, y, w, h = b
    rectwh(d, b, fill=PAPER2, outline=RULE, width=2)
    art_h = h * 0.44
    SCENES[s["scene"]](d, (x + 3, y + 3, w - 6, art_h))
    rect(d, [x + 3, y + 3 + art_h, x + w - 3, y + 6 + art_h], fill=RED)
    ty = y + art_h + 11
    txt(d, (x + 10, ty), f"{s['n']} · {s['place']}", F(SANS_BOLD, 11), fill=RED, anchor="la")
    cred_chip(d, x + w - 16, ty + 6, s["cred"])
    ty += 18
    head_lines = wrap(d, s["head"], F(SERIF_BLACK, 15.5), w - 20)
    for ln in head_lines[:3]:
        txt(d, (x + 10, ty), ln, F(SERIF_BLACK, 15.5), anchor="la")
        ty += 19
    # big number sits right of the body text
    txt(d, (x + w - 12, ty - 2), s["big"], F(SANS_BLACK, 27), fill=RED, anchor="ra")
    for i, ln in enumerate(wrap(d, s["bigcap"], F(SANS_BOLD, 8), 76)):
        txt(d, (x + w - 12, ty + 30 + i * 10), ln, F(SANS_BOLD, 8), fill=MUTE, anchor="ra")
    for ln in wrap(d, s["body"], F(SERIF, 10.5), w - 102)[:3]:
        txt(d, (x + 10, ty + 1), ln, F(SERIF, 10.5), fill=(52, 48, 42), anchor="la")
        ty += 13.5


def med_cell(d, b, s):
    x, y, w, h = b
    rectwh(d, b, fill=PAPER2, outline=(150, 142, 126), width=1)
    art_h = h * 0.56
    SCENES[s["scene"]](d, (x + 2, y + 2, w - 4, art_h))
    ty = y + art_h + 6
    txt(d, (x + 6, ty), f"{s['n']} · {s['place']}", F(SANS_BOLD, 8), fill=RED, anchor="la")
    cred_chip(d, x + w - 12, ty + 5, s["cred"], r=4.5)
    ty += 12
    for ln in wrap(d, s["head"], F(SERIF_BOLD, 10.5), w - 12)[:3]:
        txt(d, (x + 6, ty), ln, F(SERIF_BOLD, 10.5), anchor="la")
        ty += 12.5


def build():
    im, d = img_new()
    # faint paper grain (fixed seed -> deterministic)
    for i in range(2600):
        gx, gy = rng.uniform(0, 1024), rng.uniform(0, 1024)
        g = rng.randint(228, 244)
        rect(d, [gx, gy, gx + 1.6, gy + 1.6], fill=(g, g - 4, g - 18))

    # ---- masthead: the date is the headline
    txt(d, (512, 8), "THE WORLD IN ONE IMAGE · DAILY NEWS POSTER · EVERY PICTURE DRAWN BY THE PROGRAM",
        F(SANS_BOLD, 10.5), fill=MUTE, anchor="ma")
    txt(d, (512, 24), "TUESDAY 24 NOVEMBER 2026", F(SERIF_BLACK, 44), anchor="ma")
    line(d, [(14, 78), (1010, 78)], fill=INK, width=3)
    line(d, [(14, 82), (1010, 82)], fill=INK, width=1)
    txt(d, (14, 87), "44 STORIES · 6 CONTINENTS · 15 DRAWN SCENES · 43 MAP PINS",
        F(SANS_BOLD, 11), anchor="la")
    txt(d, (1010, 87), "SOURCES: REUTERS · AP · BBC · UN NEWS · NATIONAL WIRES",
        F(SANS_BOLD, 11), anchor="ra")
    lx = 322
    for cred, lab in [(2, "REPORTED BY 3+ OUTLETS"), (1, "SINGLE SOURCE"), (0, "STILL DEVELOPING")]:
        cred_chip(d, lx, 108, cred, r=5)
        txt(d, (lx + 10, 103), lab, F(SANS_BOLD, 10), fill=MUTE, anchor="la")
        lx += 10 + tw(d, lab, F(SANS_BOLD, 10)) + 26

    # ---- three big headlines
    bw = (1024 - 28 - 16) / 3
    for i, s in enumerate(BIG):
        big_panel(d, (14 + i * (bw + 8), 122, bw, 224), s)

    # ---- map band
    draw_map(d, (14, 354, 996, 170))

    # ---- by the numbers
    line(d, [(14, 532), (1010, 532)], fill=INK, width=2)
    txt(d, (14, 537), "THE DAY IN NUMBERS", F(SANS_BLACK, 12), fill=INK, anchor="la")
    nw = (1024 - 28) / 8
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 14 + i * nw
        txt(d, (cx + nw / 2, 556), num, F(SANS_BLACK, 19), fill=RED, anchor="ma")
        for j, ln in enumerate(wrap(d, cap, F(SANS, 8), nw - 10)[:2]):
            txt(d, (cx + nw / 2, 578 + j * 10), ln, F(SANS, 8), fill=MUTE, anchor="ma")
    line(d, [(14, 598), (1010, 598)], fill=INK, width=2)

    # ---- twelve medium illustrated stories: 6 x 2
    mw = (1024 - 28 - 5 * 6) / 6
    for i, s in enumerate(MED):
        r, c = divmod(i, 6)
        med_cell(d, (14 + c * (mw + 6), 606 + r * 107, mw, 102), s)

    # ---- one-line stories, three columns, one line each
    line(d, [(14, 824), (1010, 824)], fill=INK, width=2)
    txt(d, (14, 829), "AROUND THE WORLD IN ONE LINE EACH", F(SANS_BLACK, 12), anchor="la")
    cols = [TEXTS[0:10], TEXTS[10:20], TEXTS[20:29]]
    cw = (1024 - 28 - 2 * 14) / 3
    for ci, col in enumerate(cols):
        cx = 14 + ci * (cw + 14)
        if ci:
            line(d, [(cx - 7, 850), (cx - 7, 966)], fill=(180, 170, 152), width=1)
        ty = 850
        for (n, place, lon, lat, head, cred) in col:
            txt(d, (cx, ty), f"{n}", F(SANS_BLACK, 9.5), fill=RED, anchor="la")
            px = cx + 21
            txt(d, (px, ty + 0.5), place, F(SANS_BOLD, 8), fill=BLUE, anchor="la")
            hx = px + tw(d, place, F(SANS_BOLD, 8)) + 5
            txt(d, (hx, ty), head, F(SERIF, 9.5), anchor="la")
            cred_chip(d, hx + tw(d, head, F(SERIF, 9.5)) + 8, ty + 5, cred, r=4)
            ty += 12.5

    # ---- footer: the UTC reference line
    line(d, [(14, 974), (1010, 974)], fill=INK, width=2)
    txt(d, (14, 980), "24 NOV 2026, 00:00 UTC = 08:00 BEIJING · 05:30 DELHI · 03:00 RIYADH · "
                      "01:00 BERLIN · 00:00 LONDON · 19:00 NEW YORK (MON)",
        F(SANS_BOLD, 10), anchor="la")
    txt(d, (14, 996), "Drawn entirely in code from the day's wire reports. No photographs. "
                       "Pin and story numbers match across the page.",
        F(SERIF, 10), fill=MUTE, anchor="la")
    txt(d, (1010, 996), "44 STORIES · 1 IMAGE", F(SANS_BLACK, 11), fill=RED, anchor="ra")

    im = im.resize((1024, 1024), Image.LANCZOS)
    im.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
