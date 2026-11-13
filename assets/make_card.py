#!/usr/bin/env python3
"""Build the profile README's SVGs.

    python3 assets/make_card.py            hero, banners, pills, cards; stamps ?v= into README
    python3 assets/make_card.py upstream   merged-PR chart from live data (needs an authenticated gh)
"""
import hashlib
import re
import subprocess
import sys
import textwrap
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
USER = "VykosMolt"

BG, EDGE, DIM, MUTED, SOFT, FG = "#0d1117", "#30363d", "#484f58", "#8b949e", "#b1bac4", "#e6edf3"
HUE = dict(red="#ff7b72", orange="#f0883e", amber="#e3b341", green="#56d364",
           cyan="#39c5cf", blue="#58a6ff", purple="#bc8cff", pink="#f778ba")
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
W = 846     # README column on the profile page
PAIR = 412  # two of these and the space between them fit W

# ── content ────────────────────────────────────────────────────────────────
PANEL = [  # ("h", label, hue) | ("k", key, value) | ("c", value) | ("s",)
    ("h", "jan@github", "amber"),
    ("k", "Role", "ML Researcher / SWE"),
    ("k", "OS", "Arch Linux"),
    ("k", "DE", "KDE Plasma"),
    ("k", "Host", "Lenovo Legion Pro 5"),
    ("k", "Editor", "Neovim"),
    ("k", "Languages", "Python · C++"),
    ("k", "Research", "Looped / recurrent LMs"),
    ("c", "Interpretability"),
    ("c", "Agent learning"),
    ("s",),
    ("h", "Now", "green"),
    ("k", "OPI", "Proto-introspection in looped LMs"),
    ("k", "RPE", "Preference in loop states"),
    ("k", "Pluton", "French, A1 to C1, local-first"),
    ("s",),
    ("h", "Contact", "blue"),
    ("k", "Email", "vykos@tutamail.com"),
    ("k", "LinkedIn", "jan-kirin"),
    ("k", "Scholar", "JDFRr8sAAAAJ"),
    ("k", "arXiv", "Jan Kirin"),
]

BANNERS = {  # name: (hue, note)
    "research": ("cyan", "looped language models · reading vs. controlling"),
    "building": ("green", "outside research"),
    "upstream": ("blue", "patches sent where the code lives"),
    "stats": ("purple", "regenerated daily"),
    "archive": ("orange", "finished or parked"),
}

PILLS = {  # name: (label, hue)
    "email": ("Email", "amber"),
    "linkedin": ("LinkedIn", "blue"),
    "scholar": ("Google Scholar", "green"),
    "arxiv": ("arXiv", "red"),
}

PY, KT = ("Python", "#3572A5"), ("Kotlin", "#A97BFF")
CARDS = {  # name: (width, hue, kicker, right, title, text); right is a string or (language, colour)
    "opi": (PAIR, "amber", "PAPER", "arXiv:2607.18553",
            "Operational Proto-Introspection in Looped Language Models",
            "Can a looped model read the quality of its own computation, and can an "
            "intervention turn that readout into better outcomes? Process-quality taps, "
            "executable branching, the readout–control boundary."),
    "blt": (PAIR, "cyan", "CODE", PY,
            "Branching-Looped-Transformer",
            "Evaluator probes and branch-selection scaffolding for reading hidden-state signals "
            "in Ouro-RLTT loop states. Run records, sealed conversions and post-hoc checks "
            "behind the paper."),
    "rpe": (PAIR, "amber", "PAPER", "arXiv:2604.09870",
            "Reading Human Preference from Looped Transformer Internal States",
            "Lightweight evaluator heads on frozen Ouro-2.6B loop states. Version 3 replaces "
            "versions 1–2, Relational Preference Encoding, whose headline numbers were "
            "evaluation errors."),
    "hse": (PAIR, "cyan", "CODE", PY,
            "Hidden-State-Evaluator",
            "Pairwise evaluator over Ouro-2.6B-Thinking loop states. The original code kept as "
            "a snapshot, next to the version 3 analysis: scripts, per-pair outputs, fitted "
            "probe weights and the correction record."),
    "pluton": (2 * PAIR + 4, "green", "APP", KT,
               "Pluton",
               "Learn French for real, with Pluton the black cat. Ten stages from A1 to C1: "
               "ten-minute runs over 7,334 sentence-backed cards scheduled with FSRS, a "
               "20,000-word dictionary, verb tables and dictées. A local-first PWA; progress "
               "stays on your device."),
}


# ── primitives ─────────────────────────────────────────────────────────────
def T(x, y, s, fill, fs=13, bold=False, anchor=None):
    """Monospace text pinned to a 0.6em grid, whatever font the viewer has."""
    a = ' font-weight="600"' if bold else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{fs}"{a} '
            f'textLength="{len(s) * fs * 0.6:.1f}">{escape(s)}</text>')


def svg(w, h, body, label, glow=None, defs=""):
    """Dark rounded frame; `glow` washes a hue in from the left edge."""
    wash = ""
    if glow:
        defs += (f'<linearGradient id="w"><stop offset="0" stop-color="{glow}" stop-opacity=".16"/>'
                 f'<stop offset=".7" stop-color="{glow}" stop-opacity="0"/></linearGradient>')
        wash = f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="url(#w)"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h:.0f}" '
            f'viewBox="0 0 {w} {h:.0f}" role="img" aria-label="{escape(label)}" font-family="{FONT}">'
            f'<defs>{defs}</defs>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1:.0f}" rx="8" fill="{BG}" stroke="{EDGE}"/>'
            f'{wash}{"".join(body)}</svg>\n')


def banner(name, hue, note):
    c = HUE[hue]
    return svg(W, 46, [
        f'<rect x="16" y="13" width="4" height="20" rx="2" fill="{c}"/>',
        T(30, 29, f"~/{name}", c, 17, bold=True),
        T(W - 18, 28, note, MUTED, 12, anchor="end"),
    ], name, glow=c)


def pill(label, hue):
    c, w = HUE[hue], 46 + len(label) * 7.8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="30" viewBox="0 0 {w:.0f} 30" '
            f'role="img" aria-label="{escape(label)}" font-family="{FONT}">'
            f'<rect x=".5" y=".5" width="{w - 1:.0f}" height="29" rx="14.5" fill="{BG}" stroke="{c}" stroke-opacity=".6"/>'
            f'<circle cx="17" cy="15" r="4.5" fill="{c}"/>{T(30, 19.5, label, FG, 13, bold=True)}</svg>\n')


def card(width, hue, kicker, right, title, text, lines):
    """`lines` is the title+text line budget, shared by cards that sit side by side."""
    c = HUE[hue]
    title = textwrap.wrap(title, int((width - 40) / 8.4))
    text = textwrap.wrap(text, int((width - 40) / 7.2))
    assert len(title) + len(text) <= lines, f"{kicker} {title[0]}: {len(title) + len(text)} lines > {lines}"
    o = [f'<rect x="1" y="12" width="3" height="{40 + lines * 18}" rx="1.5" fill="{c}"/>',
         T(20, 27, kicker, c, 11, bold=True)]
    if isinstance(right, tuple):
        o += [T(width - 20, 27, right[0], MUTED, 11, anchor="end"),
              f'<circle cx="{width - 30 - len(right[0]) * 6.6:.1f}" cy="23" r="4" fill="{right[1]}"/>']
    else:
        o.append(T(width - 20, 27, right, MUTED, 11, anchor="end"))
    y = 52
    for s in title:
        o.append(T(20, y, s, FG, 14, bold=True))
        y += 19
    y += 3
    for s in text:
        o.append(T(20, y, s, SOFT, 12))
        y += 18
    return svg(width, 64 + lines * 18, o, " ".join(title), glow=c)


# ── hero: looped-transformer diagram + fetch panel ─────────────────────────
def diagram():
    """One shared block applied K times; a probe taps the state between passes."""
    cx, lx = 150, 306  # trunk, loop return
    line = lambda d, c=MUTED, extra="": (
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round"{extra}/>')
    tip = lambda x, y, d, c=MUTED: '<path d="M{},{}L{},{}L{},{}Z" fill="{}"/>'.format(*{
        "d": (x - 4.5, y - 7, x + 4.5, y - 7, x, y),
        "l": (x + 7, y - 4.5, x + 7, y + 4.5, x, y),
        "r": (x - 7, y - 4.5, x - 7, y + 4.5, x, y)}[d], c)

    def box(y, label, hue, cls="", x=cx - 78, w=156, h=34):
        c = HUE[hue]
        return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}" '
                f'fill-opacity=".1" stroke="{c}" stroke-width="1.5"/>'
                + T(x + w / 2, y + h / 2 + 4.5, label, c, 13, anchor="middle"))

    def add(y):  # residual add
        return (f'<circle cx="{cx}" cy="{y}" r="10" fill="{BG}" stroke="{SOFT}" stroke-width="1.5"/>'
                + line(f"M{cx - 5},{y}H{cx + 5}M{cx},{y - 5}V{y + 5}", SOFT))

    def skip(y0, y1):  # residual path around a sublayer
        return (line(f"M{cx},{y0}H74Q62,{y0} 62,{y0 + 12}V{y1 - 12}Q62,{y1} 74,{y1}H{cx - 12}", DIM)
                + tip(cx - 10, y1, "r", DIM))

    pink, loop = HUE["pink"], f"V396H{lx - 12}Q{lx},396 {lx},384V114Q{lx},102 {lx - 12},102"
    return "".join([
        f'<rect x="46" y="124" width="208" height="214" rx="10" fill="none" stroke="{DIM}" stroke-dasharray="3 5"/>',
        T(246, 142, "shared weights", MUTED, 10.5, anchor="end"),
        # trunk
        line(f"M{cx},22V46M{cx},80V152M{cx},186V198M{cx},218V242M{cx},276V288M{cx},308V428M{cx},462V486"),
        *(tip(cx, y, "d") for y in (46, 152, 242, 428, 486)),
        skip(138, 208), skip(228, 298),
        # recurrence
        line(f"M{cx},396{loop}H{cx + 8}", pink, ' class="flow" stroke-dasharray="6 6"'),
        tip(cx + 4, 102, "l", pink),
        T(lx + 12, 254, "× K", pink, 14, bold=True),
        f'<g class="dot"><circle r="9" fill="{pink}" fill-opacity=".3"/><circle r="4" fill="#fff"/>'
        f'<animateMotion dur="6s" repeatCount="indefinite" path="M{cx},102{loop}Z"/></g>',
        # probe tap
        line(f"M{cx - 5},362H99", HUE["amber"]), tip(92, 362, "l", HUE["amber"]),
        box(347, "probe", "amber", "g g3", x=20, w=72, h=30),
        # layers
        T(cx, 14, "tokens", HUE["green"], 13, anchor="middle"),
        box(46, "embed", "blue"),
        box(152, "norm → attn", "cyan", "g g1"), add(208),
        box(242, "norm → mlp", "green", "g g2"), add(298),
        f'<circle cx="{cx}" cy="102" r="3.5" fill="{pink}"/><circle cx="{cx}" cy="396" r="3.5" fill="{pink}"/>',
        f'<circle cx="{cx}" cy="362" r="4" fill="{FG}"/>', T(cx + 12, 366, "h", FG, 13), T(cx + 20.5, 370, "k", FG, 10),
        box(428, "unembed", "blue"),
        T(cx, 503, "logits", HUE["green"], 13, anchor="middle"),
    ])


DIAG_H = 508
# the dot's 6 s lap is 891 px; each box lights as it passes (attn 7.5%, mlp 17.6%, probe tap 29.2%)
GLOW = "".join(f"@keyframes g{i}{{0%,{p - 5}%,{p + 6}%,100%{{fill-opacity:.1}}{p}%{{fill-opacity:.55}}}}"
               for i, p in ((1, 7.5), (2, 17.6), (3, 29.2)))
STYLE = ("<style>@media (prefers-reduced-motion:no-preference){.flow{animation:flow .9s linear infinite}"
         ".g{animation:6s linear infinite}.g1{animation-name:g1}.g2{animation-name:g2}.g3{animation-name:g3}}"
         "@media (prefers-reduced-motion:reduce){.dot{display:none}}"
         "@keyframes flow{to{stroke-dashoffset:-12}}" + GLOW + "</style>")

FS, LH, COLS, PAD, BAR = 15, 23.25, 44, 24, 34
ADV = FS * 0.6


def hero():
    px, right = W - PAD - COLS * ADV, W - PAD
    o = [f'<circle cx="{20 + 18 * i}" cy="17" r="5.5" fill="{HUE[h]}"/>' for i, h in enumerate(("red", "amber", "green"))]
    o += [T(W / 2, 21, "jan@github: ~", MUTED, 12, anchor="middle"),
          f'<path d="M1,{BAR}H{W - 1}" stroke="{EDGE}"/>']
    y, hue = BAR + PAD + FS, None
    for kind, *row in PANEL:
        if kind == "s":
            y += LH * 0.5
            continue
        if kind == "h":
            hue = HUE[row[1]]
            assert len(row[0]) + 6 <= COLS, row
            y += LH * 0.4
            o.append(T(px, y, row[0], hue, FS, bold=True))
            o.append(f'<path d="M{px + (len(row[0]) + 2) * ADV:.1f},{y - FS * .34:.1f}H{right}" stroke="{EDGE}" stroke-width="1.5"/>')
        elif kind == "k":
            k, v = row
            dots = COLS - len(k) - len(v) - 2
            assert dots >= 2, f"row does not fit in {COLS} cols: {k}"
            o += [T(px, y, k, hue, FS), T(px + (len(k) + 1) * ADV, y, "." * dots, DIM, FS),
                  T(right, y, v, FG, FS, anchor="end")]
        else:
            o.append(T(right, y, row[0], FG, FS, anchor="end"))
        y += LH
    y += LH * 0.5 - FS
    o += [f'<rect x="{px + 36 * i:.1f}" y="{y:.1f}" width="30" height="14" rx="3" fill="{c}"/>'
          for i, c in enumerate(HUE.values())]
    inner = max(y + 14 - BAR - PAD, DIAG_H)
    ox, oy = (PAD + px - 30) / 2 - 182, BAR + PAD + (inner - DIAG_H) / 2
    o.append(f'<g transform="translate({ox:.1f},{oy:.1f})">{diagram()}</g>')
    return svg(W, BAR + PAD + inner + PAD, o, "Jan Kirin: looped transformer diagram and profile card", defs=STYLE)


# ── upstream: merged pull requests per project, from live data ─────────────
def upstream():
    q = ('query($endCursor:String){user(login:"%s"){pullRequests(first:100,after:$endCursor){'
         'nodes{state baseRepository{nameWithOwner}} pageInfo{hasNextPage endCursor}}}}' % USER)
    out = subprocess.run(
        ["gh", "api", "graphql", "--paginate", "-f", f"query={q}", "--jq",
         '.data.user.pullRequests.nodes[] | select(.baseRepository) | "\\(.state) \\(.baseRepository.nameWithOwner)"'],
        check=True, capture_output=True, text=True).stdout
    prs = [l.split() for l in out.splitlines()]
    prs = [(s, r) for s, r in prs if not r.startswith(USER + "/")]
    merged = Counter(r for s, r in prs if s == "MERGED")
    if not merged:
        raise SystemExit("no merged pull requests returned; keeping the old chart")
    n_open = sum(s == "OPEN" for s, _ in prs)
    total, top = sum(merged.values()), merged.most_common()
    x0, x1 = 240, W - 70
    o = [T(24, 42, str(total), HUE["blue"], 28, bold=True),
         T(36 + len(str(total)) * 16.8, 40, "pull requests merged upstream", FG, 14),
         T(W - 24, 40, f"{len(top)} projects · {n_open} more open", MUTED, 12, anchor="end")]
    for i, (repo, n) in enumerate(top):
        y, c = 78 + i * 27, list(HUE.values())[(5 + i) % 8]
        owner, name = repo.split("/")
        o += [T(24, y, owner + "/", MUTED, 13), T(24 + (len(owner) + 1) * 7.8, y, name, FG, 13),
              f'<rect x="{x0}" y="{y - 10}" width="{x1 - x0}" height="12" rx="6" fill="{EDGE}" fill-opacity=".5"/>',
              f'<rect x="{x0}" y="{y - 10}" width="{max(12, (x1 - x0) * n / top[0][1]):.1f}" height="12" rx="6" fill="{c}"/>',
              T(W - 24, y, str(n), FG, 13, bold=True, anchor="end")]
    return svg(W, 78 + len(top) * 27, o, f"{total} pull requests merged upstream", glow=HUE["blue"])


if __name__ == "__main__":
    if sys.argv[1:] == ["upstream"]:
        (HERE / "upstream.svg").write_text(upstream())
        sys.exit()
    files = {"hero.svg": hero()}
    files |= {f"h-{n}.svg": banner(n, *v) for n, v in BANNERS.items()}
    files |= {f"pill-{n}.svg": pill(*v) for n, v in PILLS.items()}
    files |= {f"c-{n}.svg": card(*v, lines=6 if v[0] == PAIR else 4) for n, v in CARDS.items()}
    # GitHub's image proxy caches by URL, so stamp each file's content hash into the README.
    readme = HERE.parent / "README.md"
    txt = readme.read_text()
    for name, s in files.items():
        (HERE / name).write_text(s)
        v = hashlib.sha256(s.encode()).hexdigest()[:8]
        txt = re.sub(rf"assets/{re.escape(name)}(\?v=[0-9a-f]+)?", f"assets/{name}?v={v}", txt)
    readme.write_text(txt)
    print(f"wrote {len(files)} svgs")
