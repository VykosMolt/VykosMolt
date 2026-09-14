#!/usr/bin/env python3
"""Build the neofetch-style profile card SVGs.

Art comes from assets/art/<name>.txt (plain ASCII, one line per row). The
panel is laid out in character columns, so everything stays aligned whatever
the art is.

    python3 assets/make_card.py            # DEFAULT_ART
    python3 assets/make_card.py hilbert    # pick another
"""
import hashlib
import re
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent

# ── content ────────────────────────────────────────────────────────────────
# ("h", label)        section header, label followed by a rule to the margin
# ("k", key, value)   key with dot leaders, value right-aligned
# ("c", value)        continuation, aligns under the value above
# ("s",)              blank half-row
PANEL = [
    ("h", "jan@github"),
    ("k", "Role",      "ML Researcher / SWE"),
    ("k", "OS",        "Arch Linux"),
    ("k", "WM",        "Hyprland"),
    ("k", "Host",      "Lenovo Legion Pro 5"),
    ("k", "Editor",    "Neovim"),
    ("k", "Languages", "Python · C++"),
    ("k", "Research",  "Looped / recurrent LMs"),
    ("c", "Interpretability"),
    ("c", "Agent learning"),
    ("s",),
    ("h", "Selected"),
    ("k", "SemABI",  "Semantic interface induction"),
    ("k", "OPI",     "Proto-introspection in looped LMs"),
    ("k", "Curunír", "Evidence-grounded intelligence"),
    ("s",),
    ("h", "Contact"),
    ("k", "Email",    "vykos@tutamail.com"),
    ("k", "GitHub",   "@VykosMolt"),
    ("k", "LinkedIn", "jan-kirin"),
    ("k", "Scholar",  "JDFRr8sAAAAJ"),
    ("k", "arXiv",    "Jan Kirin"),
]

# ── geometry, in character columns ─────────────────────────────────────────
FS   = 17          # font size, px
ADV  = 0.600 * FS  # monospace advance width
LH   = 1.55 * FS   # line height
PAD  = 22          # outer padding, px
GAP  = 4           # columns between art and panel
COLS = 48          # panel width, in columns

THEMES = {
    "dark":  dict(art="#39c5cf", head="#39c5cf", key="#e3b341",
                  dot="#3d444d", val="#e6edf3", rule="#30363d"),
    "light": dict(art="#1b7c83", head="#1b7c83", key="#9a6700",
                  dot="#d1d9e0", val="#1f2328", rule="#d1d9e0"),
}


DEFAULT_ART = "block"

def load_art(name):
    p = HERE / "art" / f"{name}.txt"
    if not p.exists():
        raise SystemExit(f"no such art: {p}  (have: "
                         + ", ".join(sorted(q.stem for q in (HERE/'art').glob('*.txt'))) + ")")
    return p.read_text().rstrip("\n").split("\n")


def check(art, art_cols):
    """Fail loudly rather than emit a card with text running off the edge."""
    for row in PANEL:
        if row[0] == "k":
            need = len(row[1]) + len(row[2]) + 4   # key + 2 leaders + 2 spaces
            if need > COLS:
                raise SystemExit(f"row does not fit in {COLS} cols ({need}): {row[1]}")
        if row[0] == "h" and len(row[1]) + 6 > COLS:
            raise SystemExit(f"header does not fit: {row[1]}")
    for i, line in enumerate(art, 1):
        if len(line) > art_cols:
            raise SystemExit(f"art line {i} exceeds measured width")


def build(art, theme):
    c = THEMES[theme]
    art_w = max((len(l) for l in art), default=0)
    total = art_w + (GAP if art_w else 0) + COLS
    W = round(PAD * 2 + total * ADV)

    art_x   = PAD
    panel_x = PAD + (art_w + GAP if art_w else 0) * ADV
    right   = panel_x + COLS * ADV                      # right margin of panel

    rows = sum(1 for r in PANEL if r[0] != "s") + 0.5 * sum(1 for r in PANEL if r[0] == "s")
    rows += sum(1 for r in PANEL if r[0] == "h") * 0.4   # breathing room over headers
    H = round(PAD * 2 + max(len(art), rows) * LH)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="Jan Kirin — profile card" '
         f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
         f'font-size="{FS}" xml:space="preserve">']

    y = PAD + FS
    for line in art:
        if line.strip():
            o.append(f'<text x="{art_x}" y="{y:.1f}" fill="{c["art"]}">{escape(line)}</text>')
        y += LH

    y = PAD + FS
    for row in PANEL:
        kind = row[0]
        if kind == "s":
            y += LH * 0.5
        elif kind == "h":
            y += LH * 0.4
            o.append(f'<text x="{panel_x:.1f}" y="{y:.1f}" fill="{c["head"]}" '
                     f'font-weight="600">{escape(row[1])}</text>')
            rx = panel_x + (len(row[1]) + 2) * ADV
            o.append(f'<line x1="{rx:.1f}" y1="{y - FS * 0.34:.1f}" x2="{right:.1f}" '
                     f'y2="{y - FS * 0.34:.1f}" stroke="{c["rule"]}" stroke-width="1.5"/>')
            y += LH
        elif kind == "k":
            _, k, v = row
            o.append(f'<text x="{panel_x:.1f}" y="{y:.1f}" fill="{c["key"]}">{escape(k)}</text>')
            dots = COLS - len(k) - len(v) - 2
            o.append(f'<text x="{panel_x + (len(k) + 1) * ADV:.1f}" y="{y:.1f}" '
                     f'fill="{c["dot"]}">{"." * dots}</text>')
            o.append(f'<text x="{right:.1f}" y="{y:.1f}" fill="{c["val"]}" '
                     f'text-anchor="end">{escape(v)}</text>')
            y += LH
        elif kind == "c":
            o.append(f'<text x="{right:.1f}" y="{y:.1f}" fill="{c["val"]}" '
                     f'text-anchor="end">{escape(row[1])}</text>')
            y += LH

    o.append('</svg>')
    return "\n".join(o) + "\n", W, H, total


if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ART
    art = load_art(name)
    art_cols = max((len(l) for l in art), default=0)
    check(art, art_cols)
    digests = {}
    for theme in THEMES:
        svg, W, H, total = build(art, theme)
        (HERE / f"card-{theme}.svg").write_text(svg)
        digests[theme] = hashlib.sha256(svg.encode()).hexdigest()[:8]

    # GitHub's camo proxy caches by URL, so a changed SVG at an unchanged path
    # keeps serving the old bytes. Stamp the content hash into the query.
    readme = HERE.parent / "README.md"
    txt = readme.read_text()
    for theme, d in digests.items():
        txt = re.sub(rf"assets/card-{theme}\.svg(\?v=[0-9a-f]+)?",
                     f"assets/card-{theme}.svg?v={d}", txt)
    readme.write_text(txt)
    print("  cache-bust " + "  ".join(f"{t}=?v={d}" for t, d in digests.items()))
    px = 890 / total
    print(f"  art      {name}: {art_cols} cols x {len(art)} rows")
    print(f"  panel    {COLS} cols")
    print(f"  total    {total} cols  ->  {W}x{H}px")
    print(f"  renders  ~{px:.1f}px/char in GitHub's ~890px column "
          f"(font-size ~{px / 0.6:.1f}px)")
