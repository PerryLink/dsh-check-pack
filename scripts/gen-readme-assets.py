#!/usr/bin/env python3
"""README visuals for dsh-check-pack, derived from the shipped bundle pipeline.

Two figures, both read off `checkers.json`, `package.json`, `cordis.patch.yml`,
`build.mjs` and `verify.mjs` -- not from a generic checker template.

  hero 1440x576 (Pillow, zh/en x light/dark, four WebP files)
      Left column: kicker / wordmark / two value lines / one subtitle / one meta
      line / footer.  Right side: the bundle itself -- the one-line install
      command, three real members with their locked versions, a deck of offset
      sheets that collapses into the single bundle card (name, version, the
      three manifests each carrying 53), the empty-capability pills, the scope
      strip and the verify seal.

  flow 1100x660 (hand-written SVG, light/dark)
      Grammar: an HOURGLASS between two lanes.  Eight real members with their
      exact versions converge (build-time) into the bundle waist -- the three
      manifests plus the `node verify.mjs` gate with its pass and throw
      branches -- and fan back out (install-time) into the 53 insert rows of a
      Cordis profile.  A dashed return says the published snapshot does not
      drift in from upstream: rebuild and republish.  A footer keeps the eight
      scope domains.  Every number and name is read from `checkers.json` /
      `package.json`; nothing is invented.

All labels are measured before they are drawn; a label that would overflow
aborts the run instead of shipping clipped text.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow, Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
"""
from __future__ import annotations

import json
import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-check-pack"

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")
os.makedirs(OUT, exist_ok=True)

RADIUS = 20
SHADOW = 24

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", pill="#ece7f9", band="#f5f2fb",
        grid="#e7e4f0", mark="#b45309", mark_bg="#fdf3e9",
        ok="#15803d", ok_bg="#eaf6ee",
        shadow=(38, 30, 72), glow=34,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", pill="#242d42", band="#202839",
        grid="#262f42", mark="#d9a441", mark_bg="#2a2216",
        ok="#3fb950", ok_bg="#16281c",
        shadow=(0, 0, 0), glow=48,
    ),
}

# The eight scope domains: the suite's own coverage line (README "它是什么").
DOMAINS = {
    "zh": ["外贸", "报关", "招投标", "HSE", "医疗", "法律", "公文", "制造"],
    "en": ["trade", "customs", "bids", "HSE", "medical", "legal",
           "government", "manufacturing"],
}

# Members shown as samples. Every name/version pair is read from checkers.json.
HERO_MEMBERS = ["dsh-aqua-input-check", "dsh-hs-classify", "dsh-medrec-qc"]
FLOW_LEFT = [
    "dsh-aqua-input-check", "dsh-archive-check", "dsh-bid-ca-precheck",
    "dsh-customs-doc-check", "dsh-hazchem-check", "dsh-hs-classify",
    "dsh-medrec-qc", "dsh-soe-decision-check",
]
FLOW_ROWS = [
    "dsh-aqua-input-check", "dsh-archive-check", "dsh-bid-ca-precheck",
    "dsh-customs-doc-check", "dsh-hazchem-check", "dsh-hs-classify",
    "dsh-lc-doc-check", "dsh-medrec-qc", "dsh-tender-matrix",
]


def font(size: int, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], size)


def hx(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(top), hx(bottom)
    for y in range(h):
        t = 0.12 * (y / h) + 0.88 * (y / h) ** 1.3
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rgb = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=rgb + (int(alpha * (1 - i / 11)),))
    return Image.alpha_composite(img.convert("RGBA"),
                                 layer.filter(ImageFilter.GaussianBlur(26))
                                 ).convert("RGB")


def shadow_card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
                radius: int = RADIUS, shadow: int = SHADOW,
                fill: str | None = None, edge: str | None = None,
                width: int = 2) -> Image.Image:
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -2):
        sd.rounded_rectangle([x0 - i // 6, y0 + i // 2, x1 + i // 6, y1 + i],
                             radius=radius + i // 6,
                             fill=s["shadow"] + (int(10 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(11)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(edge or s["edge"]), width=width)
    return base.convert("RGB")


_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: int, kind: str) -> float:
    return _MEASURE.textlength(text, font=font(size, kind))


def require_w(text: str, size: int, kind: str, max_w: float, what: str) -> None:
    got = measure(text, size, kind)
    if got > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs "
                         f"{got:.1f}px > {max_w:.0f}px")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    size = start
    while size > minimum and measure(text, size, kind) > max_w:
        size -= 1
    if measure(text, size, kind) > max_w:
        raise SystemExit(f"FATAL: {text!r} cannot fit {max_w}px even at "
                         f"{minimum}px")
    return size


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    size = start
    while size > minimum and any(measure(l, size, kind) > max_w for l in lines):
        size -= 1
    return size


def pill(img: Image.Image, x: int, top: int, label: str, s: dict,
         size: int = 16, kind: str = "cjk", height: int | None = None,
         pad: int = 15, fg: str | None = None, bg: str | None = None,
         edge: str | None = None) -> tuple[Image.Image, int]:
    f = font(size, kind)
    h = height or int(size * 2.1)
    w = measure(label, size, kind) + pad * 2
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, top, x + w, top + h], radius=h / 2,
                        fill=hx(bg or s["pill"]),
                        outline=hx(edge) if edge else None,
                        width=2 if edge else 0)
    d.text((x + pad, top + h / 2 + 1), label, font=f,
           fill=hx(fg or s["accent"]), anchor="lm")
    return img, int(w)


# ---------------------------------------------------------------------------
# suite data: the manifests are the source of truth, so read them back and fail
# loudly if the picture would describe a suite that is not on disk
# ---------------------------------------------------------------------------
def load_suite() -> dict[str, str]:
    with open(os.path.join(ROOT, "checkers.json"), encoding="utf-8") as fh:
        rows = json.load(fh)
    with open(os.path.join(ROOT, "package.json"), encoding="utf-8") as fh:
        pkg = json.load(fh)
    if len(rows) != 53:
        raise SystemExit(f"FATAL: checkers.json has {len(rows)} rows, expected 53")
    deps = pkg.get("dependencies", {})
    if len(deps) != 53:
        raise SystemExit(f"FATAL: package.json has {len(deps)} deps, expected 53")
    versions: dict[str, str] = {}
    for row in rows:
        if deps.get(row["name"]) != row["version"]:
            raise SystemExit(f"FATAL: version mismatch for {row['name']}")
        versions[row["name"]] = row["version"]
    if pkg["dsh"].get("capabilities") != []:
        raise SystemExit("FATAL: dsh.capabilities is not empty")
    if pkg["dsh"]["bundle"]["patch"] != "./cordis.patch.yml":
        raise SystemExit("FATAL: bundle patch field changed")
    for name in HERO_MEMBERS + FLOW_LEFT + FLOW_ROWS:
        if name not in versions:
            raise SystemExit(f"FATAL: {name} is not in the suite")
    return versions


HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 套件入口",
        value=["一条命令装齐 53 个核查器", "一层 insert 写入 53 行配置"],
        sub="本包不含核查逻辑：锁版本、插行、过一致性校验。",
        meta="53 deps · 53 rows · 53 entries — suite OK",
        foot="Apache-2.0 · 零能力 · 无运行时代码 · 不碰业务文档",
        cmd="dsh plugin --profile <name> add dsh-check-pack",
        cmd_note="一条命令 · 53 个成员",
        more="+ 50",
        bundle_kicker="BUNDLE 层 · MANIFEST V1",
        units=["依赖", "行", "条目"],
        pills=["capabilities []", "零运行时代码", "只 insert"],
        scope="覆盖域",
        note="53 行 insert · 不覆写其他插件行",
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · suite entry",
        value=["53 checkers, one install", "one insert layer, 53 rows"],
        sub="No check logic: locked versions, 53 insert rows.",
        meta="53 deps · 53 rows · 53 entries — suite OK",
        foot="Apache-2.0 · zero capabilities · no runtime code",
        cmd="dsh plugin --profile <name> add dsh-check-pack",
        cmd_note="one command · 53 members",
        more="+ 50",
        bundle_kicker="BUNDLE LAYER · MANIFEST V1",
        units=["deps", "rows", "entries"],
        pills=["capabilities []", "no runtime code", "insert only"],
        scope="coverage",
        note="53 insert rows · no overwrite",
    ),
}


def hero(lang: str, skin: str, versions: dict[str, str]) -> None:
    s = SKIN[skin]
    h = HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1150, 90, 420, s["accent"], s["glow"])
    img = glow(img, 150, 560, 300, s["accent"], max(8, s["glow"] // 3))
    d = ImageDraw.Draw(img)
    m = 56
    col_w = 556

    # ---- left column --------------------------------------------------------
    img, _ = pill(img, m, 70, h["kicker"], s, size=16)
    d = ImageDraw.Draw(img)

    title_size = fit(NAME, "mono_bold", col_w, 58, 50)
    d.text((m - 1, 132), NAME, font=font(title_size, "mono_bold"),
           fill=hx(s["text"]))
    require_w(NAME, title_size, "mono_bold", col_w, "hero title")

    value_size = fit_lines(h["value"], "cjk_bold", col_w, 38, 31)
    for i, line in enumerate(h["value"]):
        d.text((m, 234 + i * 54), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]))
        require_w(line, value_size, "cjk_bold", col_w, "hero value line")

    sub_size = fit(h["sub"], "cjk", col_w, 22, 18)
    require_w(h["sub"], sub_size, "cjk", col_w, "hero subtitle")
    d.text((m, 352), h["sub"], font=font(sub_size, "cjk"), fill=hx(s["sub"]))

    require_w(h["meta"], 19, "cjk", col_w, "hero meta")
    d.text((m + 1, 406), h["meta"], font=font(19, "cjk"), fill=hx(s["faint"]))

    d.line([m + 1, 458, m + col_w - 4, 458], fill=hx(s["grid"]), width=2)
    require_w(h["foot"], 16, "cjk", col_w, "hero footer")
    d.text((m + 1, 476), h["foot"], font=font(16, "cjk"), fill=hx(s["faint"]))

    # ---- right: install command --------------------------------------------
    img, cmd_w = pill(img, 640, 70, h["cmd"], s, size=13.5, kind="mono",
                      height=34, pad=16, fg=s["text"], bg=s["card"],
                      edge=s["edge"])
    d = ImageDraw.Draw(img)
    require_w(h["cmd_note"], 12.5, "cjk", 1384 - (640 + cmd_w + 16),
              "hero command note")
    d.text((640 + cmd_w + 16, 92), h["cmd_note"], font=font(12.5, "cjk"),
           fill=hx(s["faint"]))

    # ---- right: three real members, then "+50" ------------------------------
    chip_w, chip_gap, chip_y, chip_h = 214, 10, 116, 38
    x = 640
    for name in HERO_MEMBERS:
        d.rounded_rectangle([x, chip_y, x + chip_w, chip_y + chip_h],
                            radius=12, fill=hx(s["card"]),
                            outline=hx(s["edge"]), width=2)
        require_w(name, 12.5, "mono", chip_w - 66, "hero member name")
        d.text((x + 12, chip_y + chip_h / 2 + 1), name, font=font(12.5, "mono"),
               fill=hx(s["text"]), anchor="lm")
        version = versions[name]
        d.text((x + chip_w - 12, chip_y + chip_h / 2 + 1), version,
               font=font(11, "mono"), fill=hx(s["faint"]), anchor="rm")
        x += chip_w + chip_gap
    d.rounded_rectangle([x, chip_y, 1384, chip_y + chip_h], radius=12,
                        fill=None, outline=hx(s["accent"]), width=2)
    d.text(((x + 1384) / 2, chip_y + chip_h / 2 + 1), h["more"],
           font=font(13, "mono_bold"), fill=hx(s["accent"]), anchor="mm")

    # ---- right: member deck collapsing into the bundle card ----------------
    front = (672, 236, 1232, 470)
    for i in range(4, 0, -1):
        box = (front[0] - 13 * i, front[1] - 14 * i,
               front[2] - 13 * i, front[3] - 14 * i)
        d.rounded_rectangle(box, radius=20, fill=hx(s["band"]),
                            outline=hx(s["edge"]), width=2)
        d.rounded_rectangle([box[0] + 14, box[1] + 18, box[0] + 18, box[3] - 18],
                            radius=2, fill=hx(s["pill"]))
    img = shadow_card(img, front, s, radius=20, shadow=26)
    d = ImageDraw.Draw(img)

    require_w(h["bundle_kicker"], 11, "cjk_bold", 480, "bundle kicker")
    d.text((692, 282), h["bundle_kicker"], font=font(11, "cjk_bold"),
           fill=hx(s["accent"]), anchor="ls")
    d.text((692, 336), NAME, font=font(34, "mono_bold"), fill=hx(s["text"]),
           anchor="ls")
    d.text((1200, 336), "0.2.0", font=font(14, "mono"), fill=hx(s["faint"]),
           anchor="rs")
    d.line([692, 352, 1200, 352], fill=hx(s["grid"]), width=2)

    manifests = ["package.json", "cordis.patch.yml", "checkers.json"]
    column_x = [692, 862, 1032]
    for cx, label, unit in zip(column_x, manifests, h["units"]):
        require_w(label, 13, "mono", 152, "manifest label")
        d.text((cx, 382), label, font=font(13, "mono_bold"), fill=hx(s["text"]),
               anchor="ls")
        d.text((cx, 416), "53", font=font(23, "mono_bold"), fill=hx(s["accent"]),
               anchor="ls")
        d.text((cx + measure("53", 23, "mono_bold") + 7, 414), unit,
               font=font(11.5, "cjk"), fill=hx(s["faint"]), anchor="ls")

    px = 692
    for i, label in enumerate(h["pills"]):
        w = measure(label, 12.5, "cjk") + 22
        if px + w > 1200:
            raise SystemExit(f"FATAL: hero pills overflow at {label!r}")
        d.rounded_rectangle([px, 436, px + w, 460], radius=12,
                            fill=hx(s["pill"]))
        d.text((px + 11, 449), label, font=font(12.5, "cjk"),
               fill=hx(s["accent"] if i == 0 else s["sub"]), anchor="lm")
        px += w + 10

    # ---- right: verify seal --------------------------------------------------
    cx, cy = 1300, 345
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=hx(s["card"]),
              outline=hx(s["grid"]), width=2)
    for a in range(0, 360, 12):
        if (a // 12) % 2:
            d.arc([cx - 60, cy - 60, cx + 60, cy + 60], a, a + 7,
                  fill=hx(s["ok"]), width=3)
    d.line([(cx - 17, cy - 10), (cx - 5, cy + 3), (cx + 19, cy - 25)],
           fill=hx(s["ok"]), width=5, joint="curve")
    d.text((cx, cy + 17), "suite OK", font=font(14, "cjk_bold"),
           fill=hx(s["ok"]), anchor="mm")
    d.text((cx, cy + 36), "53 / 53 / 53", font=font(11, "mono"),
           fill=hx(s["sub"]), anchor="mm")

    # ---- right: scope strip + closing note ----------------------------------
    d.text((640, 506), h["scope"], font=font(11, "cjk_bold"),
           fill=hx(s["accent"]))
    scope = " · ".join(DOMAINS[lang])
    require_w(scope, 12 if lang == "en" else 13, "cjk",
              1384 - 704, "hero scope")
    d.text((704, 506), scope, font=font(12 if lang == "en" else 13, "cjk"),
           fill=hx(s["sub"]))
    require_w(h["note"], 12.5, "cjk", 744, "hero note")
    d.text((640, 528), h["note"], font=font(12.5, "cjk"), fill=hx(s["faint"]))

    path = os.path.join(OUT, f"{NAME}-hero-{lang}-{skin}.webp")
    img.save(path, "WEBP", quality=90, method=6)
    print(f"wrote {os.path.relpath(path, ROOT)}  {W}x{H}")


# ---------------------------------------------------------------------------
# flow SVG (light + dark): hourglass between build-time and install-time
# ---------------------------------------------------------------------------
FONT_CSS_SANS = ("'Microsoft YaHei','Segoe UI','PingFang SC',"
                 "'Noto Sans CJK SC',sans-serif")
FONT_CSS_MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"


def flow_svg(skin: str, versions: dict[str, str]) -> str:
    s = SKIN[skin]
    W, H = 1100, 660
    total = len(versions)
    p: list[str] = []

    def add(line: str) -> None:
        p.append(line)

    def text(x: float, y: float, body: str, size: float, fill: str,
             kind: str = "sans", weight: str | None = None,
             anchor: str | None = None, ls: float | None = None) -> None:
        family = FONT_CSS_MONO if kind == "mono" else FONT_CSS_SANS
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'fill="{fill}"',
                 f'font-family="{family}"', f'font-size="{size:g}"']
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if anchor:
            attrs.append(f'text-anchor="{anchor}"')
        if ls:
            attrs.append(f'letter-spacing="{ls:g}"')
        add(f'<text {" ".join(attrs)}>{escape(body)}</text>')

    def rect(x0: float, y0: float, x1: float, y1: float, fill: str,
             rx: float = 12, stroke: str | None = None,
             width: float = 1.5, opacity: float | None = None,
             shadow: bool = False) -> None:
        attrs = [f'x="{x0:g}"', f'y="{y0:g}"', f'width="{x1 - x0:g}"',
                 f'height="{y1 - y0:g}"', f'rx="{rx:g}"', f'fill="{fill}"']
        if stroke:
            attrs.append(f'stroke="{stroke}" stroke-width="{width:g}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        add(f'<rect {" ".join(attrs)}/>')

    def line(x0: float, y0: float, x1: float, y1: float, color: str,
             width: float = 1, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x1="{x0:g}"', f'y1="{y0:g}"', f'x2="{x1:g}"',
                 f'y2="{y1:g}"', f'stroke="{color}"', f'stroke-width="{width:g}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        add(f'<line {" ".join(attrs)}/>')

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
    add('<title id="title">dsh-check-pack bundle lifecycle</title>')
    add('<desc id="desc">Eight sample members of the 53 checker suite, with '
        'their exact versions, converge at build time into the three manifests '
        'of one bundle: package.json dependencies, the cordis.patch.yml insert '
        'rows, and checkers.json. The node verify.mjs gate checks that all '
        'three carry the same 53 rows and that versions match; a mismatch '
        'throws. At install time the same bundle patch expands into 53 insert '
        'rows of a Cordis profile, with no tools, commands, services or routes '
        'registered. A dashed return shows the published snapshot does not '
        'drift in from upstream: rebuild and republish. The footer lists the '
        'eight scope domains.</desc>')
    add('<defs>')
    add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.2" y2="1">'
        f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
        f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    shadow_hex = "#2b2440" if skin == "light" else "#000000"
    add('<filter id="soft" x="-30%" y="-30%" width="160%" height="180%">'
        '<feDropShadow dx="0" dy="8" stdDeviation="10" '
        f'flood-color="{shadow_hex}" flood-opacity="0.13"/>'
        '</filter>')
    add(f'<pattern id="dots" width="24" height="24" '
        f'patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" r="1.2" '
        f'fill="{s["grid"]}"/></pattern>')
    add(f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{s["accent"]}"/></marker>')
    add('</defs>')
    add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    add(f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.55"/>')

    # ---- header -------------------------------------------------------------
    text(44, 58, NAME, 30, s["text"], "mono", "700")
    text(44, 88,
         "53 members → 3 manifests → 1 bundle → 53 Cordis rows; "
         "one gate keeps the counts equal.", 14.5, s["sub"])
    rect(812, 30, 1056, 58, s["pill"], rx=14)
    text(824, 48, "manifest v1 · capabilities []", 11.5, s["accent"], "mono")
    text(44, 116, "IN · 53 × package.json + cordis.patch.yml", 11, s["faint"],
         "mono")
    text(1056, 116, "OUT · 53 rows · 0 tools · 0 commands", 11, s["faint"],
         "mono", anchor="end")
    line(44, 128, 1056, 128, s["grid"], 1, opacity=0.75)

    # ---- zone labels --------------------------------------------------------
    text(44, 150, "UPSTREAM · 53 CHECKER REPOS", 11, s["faint"], "sans", "700",
         ls=1.2)
    text(356, 150, "BUILD · node build.mjs → 3 MANIFESTS", 11, s["faint"],
         "sans", "700", ls=1.2)
    text(772, 150, "INSTALL · PROFILE ROWS", 11, s["faint"], "sans", "700",
         ls=1.2)

    # ---- left: members with their exact versions ---------------------------
    text(44, 172, "own package.json + cordis.patch.yml", 11, s["faint"], "mono")
    chip_y, chip_h, step = 186, 30, 35
    centers = []
    for i, name in enumerate(FLOW_LEFT):
        y = chip_y + i * step
        rect(44, y, 300, y + chip_h, s["card"], rx=10, stroke=s["edge"])
        text(56, y + 20, name, 13, s["text"], "mono")
        text(288, y + 20, versions[name], 11.5, s["faint"], "mono",
             anchor="end")
        centers.append(y + chip_h / 2)
    gy = chip_y + len(FLOW_LEFT) * step
    add(f'<rect x="44" y="{gy:g}" width="256" height="{chip_h:g}" rx="10" '
        f'fill="none" stroke="{s["faint"]}" stroke-width="1.2" '
        f'stroke-dasharray="6 5"/>')
    text(56, gy + 20, f"+ {total - len(FLOW_LEFT)} more · checkers.json",
         11, s["faint"], "mono")

    # ---- waist: three manifests + verify gate ------------------------------
    rect(356, 162, 716, 528, s["card"], rx=20, stroke=s["edge"], shadow=True)
    text(376, 188, NAME, 15, s["text"], "mono", "700")
    text(696, 188, "0.2.0", 11, s["faint"], "mono", anchor="end")
    text(376, 207, "dsh.bundle.patch → ./cordis.patch.yml", 11, s["faint"],
         "mono")
    line(376, 216, 696, 216, s["grid"], 1)
    manifests = [
        ("package.json", "dependencies · exact versions"),
        ("cordis.patch.yml", "- insert · no overwrite"),
        ("checkers.json", "id · name · version"),
    ]
    for i, (label, desc) in enumerate(manifests):
        y = 224 + i * 64
        rect(372, y, 700, y + 58, s["band"], rx=12)
        text(386, y + 24, label, 13, s["text"], "mono", "700")
        text(386, y + 44, desc, 11, s["faint"], "mono")
        rect(656, y + 12, 692, y + 38, s["pill"], rx=13)
        text(674, y + 29, "53", 11.5, s["accent"], "mono", "700",
             anchor="middle")
    rect(372, 420, 700, 518, s["pill"], rx=14, stroke=s["accent"], width=1.5)
    text(392, 446, "node verify.mjs", 13, s["text"], "mono", "700")
    text(392, 466, "rows = deps = entries", 11, s["sub"], "mono")
    text(684, 446, "suite OK", 12.5, s["ok"], "sans", "700", anchor="end")
    text(684, 466, "53 / 53 / 53", 11, s["ok"], "mono", anchor="end")
    text(392, 492, "≠ 53 → throw", 11, s["mark"], "mono")
    text(684, 492, "ci.yml · Node 22", 11, s["faint"], "mono", anchor="end")

    # ---- right: profile rows ------------------------------------------------
    rect(772, 162, 1056, 528, s["card"], rx=20, stroke=s["edge"], shadow=True)
    text(792, 190, "Cordis profile", 13.5, s["text"], "sans", "700")
    rect(1000, 174, 1036, 198, s["pill"], rx=12)
    text(1018, 190, "53", 11.5, s["accent"], "mono", "700", anchor="middle")
    text(792, 208, "dsh.bundle.patch · 53 insert", 11, s["faint"], "mono")
    row_centers = []
    for i, name in enumerate(FLOW_ROWS):
        y = 218 + i * 30
        if i % 2 == 0:
            rect(784, y, 1044, y + 28, s["band"], rx=8)
        rect(784, y + 6, 788, y + 22, s["accent"], rx=2)
        text(794, y + 19, f"- id: {name}", 13, s["text"], "mono")
        text(1040, y + 19, "insert", 11, s["faint"], "mono", anchor="end")
        row_centers.append(y + 14)
    text(792, 508, f"+ {total - len(FLOW_ROWS)} more rows · all insert",
         11, s["faint"], "mono")

    # ---- convergence / divergence ------------------------------------------
    waist_y = 305
    for cy in centers:
        add(f'<path d="M300 {cy:g} C330 {cy:g} 336 {waist_y} 356 {waist_y}" '
            f'fill="none" stroke="{s["accent"]}" stroke-width="1.5" '
            f'opacity="0.42"/>')
    for cy in row_centers:
        add(f'<path d="M716 {waist_y} C740 {waist_y} 748 {cy:g} 772 {cy:g}" '
            f'fill="none" stroke="{s["accent"]}" stroke-width="1.5" '
            f'opacity="0.42"/>')
    for x in (356, 716):
        add(f'<circle cx="{x}" cy="{waist_y}" r="4" fill="{s["accent"]}" '
            f'stroke="{s["card"]}" stroke-width="2"/>')

    # ---- return loop: no automatic drift -----------------------------------
    add(f'<path d="M172 504 L172 574 L1040 574 L1040 542" fill="none" '
        f'stroke="{s["accent"]}" stroke-width="1.5" stroke-dasharray="7 6" '
        f'opacity="0.55" marker-end="url(#arr)"/>')
    add(f'<circle cx="172" cy="504" r="3" fill="{s["accent"]}"/>')
    text(560, 566,
         "nightly 18:00 UTC checks upstream; releases do not drift in — "
         "rebuild + republish", 11, s["sub"], "mono", anchor="middle")

    # ---- footer: scope ------------------------------------------------------
    line(44, 596, 1056, 596, s["grid"], 1, opacity=0.75)
    text(44, 620,
         "COVERAGE · trade · customs · bids · HSE · medical · legal · "
         "government · manufacturing", 11, s["faint"], "mono", ls=0.4)
    text(1056, 620, "Apache-2.0", 11, s["faint"], "mono", anchor="end")

    add('</svg>')
    return "\n".join(p) + "\n"


def main() -> None:
    versions = load_suite()
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin, versions)
    for skin in ("light", "dark"):
        path = os.path.join(OUT, f"{NAME}-flow-v5-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin, versions))
        print(f"wrote {os.path.relpath(path, ROOT)}  1100x660")


if __name__ == "__main__":
    main()
