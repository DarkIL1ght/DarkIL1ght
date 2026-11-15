"""Generates assets/profile.svg: the whole profile as one animated picture.

Night steppe, falling snow over the full height, and the national ornament
as dividers. The ornament is taken from the flag of Kazakhstan (tools/kz-flag.svg, Wikimedia
Commons, public domain).

    python tools/profile.py

Edit the CONTENT block below and re-run; nothing else needs touching.
"""

import random
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CONTENT ---
NAME = "Darhan Semiatov"
ROLE = "Go backend · AI/LLM engineering"
PLACE = "Almaty, Kazakhstan"

ABOUT = (
    "I build Go services that run in production and the ML/LLM pieces around "
    "them: scoring models, LLM integrations, Telegram bots. 4th-year student "
    "at Narxoz University, intern at QazCode. Open to Go / AI roles from 2027."
)

PROJECTS = [
    ("Tropa", "live",
     "A map of places around Almaty for going out with friends, with real users. "
     "Go, PostgreSQL, SSE chats, Telegram notifications, rate-limited auth, "
     "admin moderation. Self-hosted: Docker and Caddy on an Oracle ARM VM, nightly backups."),
    ("IELTS writing scorer", "ML",
     "A fine-tuned DeBERTa-v3 regressor that scores essays on 4 criteria, "
     "exported to ONNX and served by a Python service that a Go app calls. "
     "The LLM only explains the scores. It does not grade."),
    ("F1 race winner prediction", "ML",
     "An ML study on historical Formula 1 data: preprocessing, XGBoost, a custom "
     "race-level winner accuracy metric, feature importance and a temporal learning curve."),
    ("Decentrathon 6.0", "hackathon",
     "Captained a team at a hackathon with about 1,500 participants. In 2 days "
     "we built a support copilot for a mobile operator: ticket category and "
     "priority classification, answers grounded in the knowledge base."),
]

STACK = [
    ("Main", ["Go", "PostgreSQL", "Docker", "Linux", "GitHub Actions", "Caddy"]),
    ("AI / ML", ["Python", "PyTorch", "ONNX Runtime", "LLM APIs"]),
    ("Also", ["Java", "JavaScript", "SQL"]),
]

HOW_I_WORK = (
    "Layered architecture (domain → application → adapters), tests on every "
    "layer, an architecture.md in every repo, and CI before merge."
)
# ----------------------------------------------------------------------------

W = 1000
PAD = 60
GOLD = "url(#gold)"
FONT = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"


def wrap(text, size, width):
    """Greedy word wrap by an average glyph width; good enough for Latin text."""
    limit = int(width / (size * 0.5))
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > limit:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def text(x, y, s, size, fill, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" {extra}>{escape(s)}</text>')


def flag_art():
    """The flag drawing without the sky-blue field and the sun, recoloured via currentColor."""
    s = (ROOT / "tools" / "kz-flag.svg").read_text(encoding="utf-8")
    inner = s[s.find(">") + 1:s.rfind("</svg>")]
    inner = inner.replace('<path fill="#00abc2" d="M0 0h1000v500H0z"/>', "")
    start = inner.find('<g transform="matrix(.5 0 0 .5 540.236 210)">')
    depth, i = 0, start
    while True:
        o, c = inner.find("<g", i), inner.find("</g>", i)
        if o != -1 and o < c:
            depth, i = depth + 1, o + 2
        else:
            depth, i = depth - 1, c + 4
            if depth == 0:
                break
    inner = inner[:start] + inner[i:]
    inner = inner.replace('fill="#ffec2d"', "").replace("#ffec2d", "currentColor")
    inner = inner.replace("xlink:href", "href")
    return re.sub(r"\s+", " ", inner)



def ornament_band(y, opacity=0.55):
    """The flag's vertical ornament (28..92 x 25..475) laid on its side and repeated."""
    seg_w, seg_h = 450 * 0.3, 64 * 0.3  # scaled band piece
    out = [f'<g opacity="{opacity}">']
    n = int((W - 2 * PAD + 4) // (seg_w + 4))
    x = (W - n * seg_w - (n - 1) * 4) / 2
    for _ in range(n):
        out.append(f'<svg x="{x:.1f}" y="{y}" width="{seg_w:.1f}" height="{seg_h:.1f}" viewBox="-475 28 450 64">'
                   f'<g transform="rotate(90)"><use href="#art"/></g></svg>')
        x += seg_w + 4
    out.append("</g>")
    return "".join(out)


def snow(height, count, rng):
    flakes = []
    for _ in range(count):
        x = rng.uniform(0, W)
        r = rng.choice([1.1, 1.5, 1.9, 2.3, 2.8])
        dur = rng.uniform(26, 48) * (3.2 / (r + 0.6))
        delay = -rng.uniform(0, dur)
        sway = rng.uniform(10, 30) * rng.choice([-1, 1])
        op = min(0.4 + 0.15 * r, 0.95)
        flakes.append(
            f'<g class="f" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">'
            f'<circle class="s" cx="{x:.0f}" cy="-8" r="{r}" fill="#fff" opacity="{op:.2f}" '
            f'style="--sx:{sway:.0f}px;animation-duration:{rng.uniform(3, 6):.1f}s"/></g>')
    return "".join(flakes)


def build():
    rng = random.Random(7)
    body = []
    y = 0

    # Header: sky, moon, mountains.
    ridge = [(0, 300), (70, 262), (120, 278), (190, 228), (245, 262), (300, 218), (360, 252),
             (420, 196), (470, 236), (540, 208), (600, 246), (660, 188), (720, 234), (790, 206),
             (850, 248), (910, 212), (980, 258), (1000, 250)]
    ridge_d = "M" + " L".join(f"{a},{b}" for a, b in ridge)
    body.append('<g class="moon"><circle cx="840" cy="80" r="24" fill="#f6e2a8" mask="url(#cres)"/></g>')
    body.append(f'<path d="{ridge_d} L1000,360 L0,360 Z" fill="#0a142b"/>')
    body.append(f'<path class="cap" d="{ridge_d}" fill="none" stroke="#e9f0ff" stroke-width="2" '
                'stroke-linejoin="round" opacity="0"/>')
    body.append('<path d="M0,330 C150,312 300,326 450,316 C600,306 750,330 1000,318 L1000,360 L0,360 Z" fill="#081022"/>')
    body.append('<rect y="318" width="1000" height="110" fill="url(#fade)"/>')
    body.append(text(PAD, 112, NAME, 52, GOLD, 700, 'letter-spacing="1"'))
    body.append(f'<rect x="{PAD + 2}" y="130" width="110" height="3" rx="1.5" fill="{GOLD}"/>')
    body.append(text(PAD, 170, ROLE, 24, "#d8e1f3"))
    body.append(text(PAD, 202, PLACE, 17, "#8d9ec2"))
    y = 360

    def section(title):
        nonlocal y
        y += 70
        body.append(ornament_band(y - 34, 0.45))
        y += 26
        body.append(text(PAD, y, title.upper(), 15, "#e2b75a", 700, 'letter-spacing="4"'))
        y += 18

    # About
    section("About")
    for line in wrap(ABOUT, 22, W - 2 * PAD):
        y += 32
        body.append(text(PAD, y, line, 22, "#d8e1f3"))

    # Projects
    section("Featured")
    for title, tag, desc in PROJECTS:
        lines = wrap(desc, 19, W - 2 * PAD - 48)
        h = 64 + 28 * len(lines)
        y += 16
        body.append(f'<rect x="{PAD}" y="{y}" width="{W - 2 * PAD}" height="{h}" rx="14" '
                    'fill="#0f1c3a" fill-opacity=".72" stroke="#e2b75a" stroke-opacity=".28"/>')
        body.append(text(PAD + 24, y + 40, title, 24, GOLD, 700))
        tw = len(title) * 24 * 0.5
        body.append(f'<rect x="{PAD + 24 + tw + 14:.0f}" y="{y + 21}" width="{len(tag) * 9 + 22}" height="24" rx="12" '
                    'fill="#e2b75a" fill-opacity=".14"/>')
        body.append(text(int(PAD + 24 + tw + 25), y + 38, tag, 14, "#e2b75a", 600))
        ly = y + 40
        for line in lines:
            ly += 28
            body.append(text(PAD + 24, ly, line, 19, "#c3cde4"))
        y += h

    # Stack
    section("Stack")
    for label, items in STACK:
        y += 22
        body.append(text(PAD, y + 22, label, 17, "#8d9ec2", 600))
        x = PAD + 110
        for item in items:
            cw = len(item) * 9.6 + 30
            if x + cw > W - PAD:
                x = PAD + 110
                y += 42
            body.append(f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="32" rx="16" '
                        'fill="#13244a" stroke="#e2b75a" stroke-opacity=".35"/>')
            body.append(text(int(x + 15), y + 22, item, 17, "#e6ecf8"))
            x += cw + 10
        y += 22

    # How I work
    section("How I work")
    for line in wrap(HOW_I_WORK, 21, W - 2 * PAD):
        y += 31
        body.append(text(PAD, y, line, 21, "#d8e1f3"))

    # Footer: snowy ground.
    y += 70
    body.append(ornament_band(y, 0.6))
    y += 40
    height = y + 70
    body.append(f'<path d="M0,{y + 30} C200,{y + 10} 380,{y + 34} 560,{y + 20} C740,{y + 6} 880,{y + 30} 1000,{y + 18} '
                f'L1000,{height} L0,{height} Z" fill="#dfe8f8" opacity=".9"/>')

    css = f"""
.f{{animation:fall linear infinite}}
.s{{animation:sway ease-in-out infinite alternate}}
@keyframes fall{{from{{transform:translateY(0)}}to{{transform:translateY({height + 20}px)}}}}
@keyframes sway{{from{{transform:translateX(0)}}to{{transform:translateX(var(--sx))}}}}
.moon{{animation:pulse 6s ease-in-out infinite alternate}}
@keyframes pulse{{from{{opacity:.8}}to{{opacity:1}}}}
.cap{{animation:cap 40s ease-out forwards}}
@keyframes cap{{to{{opacity:.45}}}}
@media (prefers-reduced-motion:reduce){{.f,.s,.moon{{animation:none}}.cap{{opacity:.45}}}}
text{{font-family:{FONT}}}
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" role="img" aria-label="{escape(NAME)}: {escape(ROLE)}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070d1f"/><stop offset="{360 / height:.3f}" stop-color="#132449"/><stop offset="1" stop-color="#0b1530"/></linearGradient>
<radialGradient id="glow" cx=".84" cy=".06" r=".35"><stop offset="0" stop-color="#f0cf7e" stop-opacity=".12"/><stop offset="1" stop-color="#f0cf7e" stop-opacity="0"/></radialGradient>
<linearGradient id="gold" x1="0" x2="1"><stop offset="0" stop-color="#f3d58a"/><stop offset=".5" stop-color="#d4a94a"/><stop offset="1" stop-color="#b8862b"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#081022"/><stop offset=".38" stop-color="#081022"/><stop offset="1" stop-color="#081022" stop-opacity="0"/></linearGradient>
<mask id="cres"><rect width="{W}" height="200" fill="#fff"/><circle cx="852" cy="72" r="22" fill="#000"/></mask>
<g id="art" fill="currentColor">{flag_art()}</g>
</defs>
<style>{css}</style>
<rect width="{W}" height="{height}" fill="url(#sky)"/>
<rect width="{W}" height="{height}" fill="url(#glow)"/>
<g style="color:#e2b75a">{"".join(body)}</g>
{snow(height, 240, rng)}
</svg>
"""


if __name__ == "__main__":
    out = ROOT / "assets" / "profile.svg"
    out.write_text(build(), encoding="utf-8", newline="\n")
    print(out, out.stat().st_size, "bytes")
