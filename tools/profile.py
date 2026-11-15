"""Generates the profile pictures in assets/light and assets/dark.

Style: a monochrome "technical document" with numbered sections, plus a
neofetch-like card on top. Animation is deliberately light: a blinking cursor,
a pulsing status dot and moving dashes on the system map.

    python tools/profile.py

Edit the CONTENT block and re-run; README.md references the files by name.
"""

import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CONTENT ---
HANDLE = "darhan@almaty"
INFO = [
    ("Name", "Darhan Semiatov"),
    ("Role", "Go backend · AI/LLM engineering"),
    ("Location", "Almaty, Kazakhstan"),
    ("Uni", "Narxoz University, 4th year"),
    ("Work", "Intern @ QazCode"),
    ("Main", "Go, PostgreSQL, Docker, Linux"),
    ("ML", "Python, PyTorch, ONNX, LLM APIs"),
    ("Shipped", "Tropa (live), IELTS scorer, F1 model"),
    ("Status", "open to Go / AI roles from 2027"),
]

# Alatau ridge over Almaty, in the spirit of a neofetch distro logo.
ART = [
    r"            /\               ",
    r"           /**\      /\      ",
    r"     /\   /    \    /**\     ",
    r"    /**\ /      \  /    \    ",
    r"   /    \   /\   \/      \   ",
    r"  /      \ /  \   \       \  ",
    r" /   /\   /    \   \   /\  \ ",
    r"/___/__\_/______\___\_/__\__\ ",
    r"  .  almaty  .  alatau  .  ",
]

WHOAMI = [
    "Go backend developer who also ships the ML/LLM parts.",
    "I build services that run in production: Postgres, Docker,",
    "CI, backups, Telegram integrations, streaming LLM APIs.",
    "4th-year student at Narxoz University, intern at QazCode.",
]

# System map: the centre node and what is around it (label, sublabel).
CORE = ("DARHAN.SYS", "go services + ml models")
NODES = [
    ("TROPA", "go · postgres · sse"),
    ("TELEGRAM", "bots · notifications"),
    ("ORACLE ARM VM", "docker · caddy · backups"),
    ("GITHUB ACTIONS", "ci · race tests"),
    ("LLM APIs", "claude · gemini · ollama"),
    ("IELTS SCORER", "deberta-v3 · onnx"),
    ("F1 MODEL", "xgboost · pandas"),
    ("HACKATHONS", "decentrathon 6.0"),
]

PROJECTS = [
    ("01", "TROPA", "live",
     ["Map of places around Almaty for going out with friends; real users.",
      "SSE chats, Telegram notifications, rate-limited auth, moderation."],
     "go · postgresql · pgx · docker · caddy"),
    ("02", "IELTS WRITING SCORER", "ml",
     ["Fine-tuned DeBERTa-v3 scores essays on 4 criteria; an ONNX service",
      "called from Go. The LLM only explains the scores, it never grades."],
     "python · pytorch · onnx runtime · go"),
    ("03", "F1 RACE WINNER PREDICTION", "ml",
     ["Historical Formula 1 data: preprocessing, XGBoost, a custom",
      "race-level winner accuracy, feature importance, learning curve."],
     "python · xgboost · pandas"),
    ("04", "DECENTRATHON 6.0", "hackathon",
     ["Team captain, ~1,500 participants. A support copilot for a mobile",
      "operator: ticket category and priority, grounded answers."],
     "python · llm · classification"),
]

STACK = [
    ("BACKEND", "Go · PostgreSQL · REST · SSE · pgx"),
    ("INFRA", "Docker · Linux · Caddy · GitHub Actions"),
    ("ML / AI", "Python · PyTorch · ONNX · LLM APIs"),
    ("ALSO", "Java · JavaScript · SQL"),
    ("PRACTICE", "layered design · tests on every layer · ADRs · CI"),
]

STATUS = "open to Go / AI roles from 2027"
# ----------------------------------------------------------------------------

W = 900
PAD = 44
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Consolas,Menlo,monospace"

THEMES = {
    "dark": {"bg": "#0d1117", "fg": "#e6edf3", "dim": "#8b949e", "faint": "#30363d",
             "panel": "#161b22", "accent": "#d4a94a"},
    "light": {"bg": "#ffffff", "fg": "#1f2328", "dim": "#59636e", "faint": "#d1d9e0",
              "panel": "#f6f8fa", "accent": "#9a6b12"},
}


def svg(h, t, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">'
            f'<style>text{{font-family:{MONO}}}{css}'
            '@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
            f'<rect width="{W}" height="{h}" fill="{t["bg"]}"/>{body}</svg>\n')


def txt(x, y, s, size, fill, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'xml:space="preserve" {extra}>{escape(s)}</text>')


def heading(t, num, title, path, y=46):
    return (txt(PAD, y, num, 40, t["faint"], 700)
            + txt(PAD + 64, y - 8, " ".join(title.upper()), 15, t["dim"], 700)
            + txt(W - PAD, y - 8, path, 13, t["dim"], 400, 'text-anchor="end"'))


def header(t):
    h = 372
    b = [f'<rect x="{PAD}" y="18" width="{W - 2 * PAD}" height="{h - 36}" rx="10" '
         f'fill="{t["panel"]}" stroke="{t["faint"]}"/>']
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        b.append(f'<circle cx="{PAD + 22 + i * 18}" cy="38" r="6" fill="{c}"/>')
    b.append(txt(W / 2, 43, f"{HANDLE}: ~", 13, t["dim"], 400, 'text-anchor="middle"'))
    b.append(txt(PAD + 22, 80, "$ neofetch", 15, t["accent"], 700))
    for i, line in enumerate(ART):
        b.append(txt(PAD + 22, 112 + i * 20, line, 15, t["accent"] if i < len(ART) - 1 else t["dim"]))
    x = PAD + 340
    b.append(txt(x, 112, HANDLE, 16, t["accent"], 700))
    b.append(txt(x, 130, "-" * len(HANDLE), 16, t["dim"]))
    for i, (k, v) in enumerate(INFO):
        y = 154 + i * 19
        b.append(txt(x, y, f"{k}:", 14, t["accent"], 700))
        b.append(txt(x + 92, y, v, 14, t["fg"]))
    sy = 154 + len(INFO) * 19 - 2
    for i, c in enumerate(["#f85149", "#d4a94a", "#3fb950", "#58a6ff", "#bc8cff", "#39c5cf", t["fg"], t["dim"]]):
        b.append(f'<rect x="{x + i * 26}" y="{sy}" width="24" height="12" fill="{c}"/>')
    b.append(txt(PAD + 22, h - 36, "$", 15, t["accent"], 700))
    b.append(f'<rect class="cur" x="{PAD + 40}" y="{h - 49}" width="9" height="16" fill="{t["fg"]}"/>')
    css = ".cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    return svg(h, t, "".join(b), css)


def whoami(t):
    h = 100 + 26 * len(WHOAMI)
    b = [heading(t, "01", "whoami", "~/01-whoami")]
    for i, line in enumerate(WHOAMI):
        b.append(txt(PAD, 96 + i * 26, line, 16, t["fg"] if i == 0 else t["dim"]))
    return svg(h, t, "".join(b))


def system_map(t):
    h = 530
    cx, cy = W / 2, 306
    b = [heading(t, "02", "system map", "~/02-ecosystem"),
         txt(PAD, 96, "SYSTEM MAP — EVERYTHING FROM ONE PIPELINE", 13, t["fg"], 700, 'letter-spacing="2"'),
         txt(W - PAD, 96, "FIG. 01", 13, t["fg"], 700, 'text-anchor="end" letter-spacing="2"'),
         f'<rect x="{PAD}" y="106" width="{W - 2 * PAD}" height="1.5" fill="{t["dim"]}"/>']
    rx, ry = 296, 150
    boxes = []
    for i, (label, sub) in enumerate(NODES):
        a = -math.pi / 2 + i * 2 * math.pi / len(NODES)
        nx, ny = cx + rx * math.cos(a), cy + ry * math.sin(a)
        b.append(f'<line class="flow" x1="{cx:.0f}" y1="{cy:.0f}" x2="{nx:.0f}" y2="{ny:.0f}" '
                 f'stroke="{t["dim"]}" stroke-width="1.2" stroke-dasharray="3 7"/>')
        w = max(len(label), len(sub)) * 7.4 + 24
        boxes.append(f'<rect x="{nx - w / 2:.0f}" y="{ny - 21:.0f}" width="{w:.0f}" height="42" rx="4" '
                     f'fill="{t["bg"]}" stroke="{t["faint"]}"/>'
                     + txt(f"{nx:.0f}", f"{ny - 3:.0f}", label, 12, t["fg"], 700, 'text-anchor="middle"')
                     + txt(f"{nx:.0f}", f"{ny + 13:.0f}", sub, 10.5, t["dim"], 400, 'text-anchor="middle"'))
    b += boxes
    b.append(f'<rect x="{cx - 95}" y="{cy - 27}" width="190" height="54" rx="4" '
             f'fill="{t["panel"]}" stroke="{t["accent"]}"/>')
    b.append(txt(cx, cy - 4, CORE[0], 15, t["accent"], 700, 'text-anchor="middle"'))
    b.append(txt(cx, cy + 15, CORE[1], 11, t["dim"], 400, 'text-anchor="middle"'))
    b.append(f'<rect x="{PAD}" y="{h - 42}" width="{W - 2 * PAD}" height="1.5" fill="{t["dim"]}"/>')
    b.append(txt(W - PAD, h - 18, "DASHED LINES — DATA IN MOTION", 12, t["fg"], 700,
                 'text-anchor="end" letter-spacing="2"'))
    css = ".flow{animation:flow 1.6s linear infinite}@keyframes flow{to{stroke-dashoffset:-20}}"
    return svg(h, t, "".join(b), css)


def projects(t):
    row = 120
    h = 84 + row * len(PROJECTS)
    b = [heading(t, "03", "projects", "~/03-projects")]
    y = 74
    for num, name, tag, desc, stack in PROJECTS:
        b.append(f'<rect x="{PAD}" y="{y}" width="{W - 2 * PAD}" height="1" fill="{t["faint"]}"/>')
        b.append(txt(PAD, y + 30, num, 14, t["dim"], 700))
        b.append(txt(PAD + 40, y + 30, name, 16, t["fg"], 700, 'letter-spacing="1"'))
        tw = len(tag) * 8 + 18
        b.append(f'<rect x="{W - PAD - tw}" y="{y + 15}" width="{tw}" height="22" rx="3" '
                 f'fill="none" stroke="{t["accent"]}"/>')
        b.append(txt(W - PAD - tw / 2, y + 31, tag.upper(), 11, t["accent"], 700, 'text-anchor="middle"'))
        for i, line in enumerate(desc):
            b.append(txt(PAD + 40, y + 56 + i * 20, line, 13.5, t["dim"]))
        b.append(txt(PAD + 40, y + 100, "> " + stack, 12.5, t["accent"]))
        y += row
    return svg(h, t, "".join(b))


def stack(t):
    h = 84 + 34 * len(STACK)
    b = [heading(t, "04", "stack", "~/04-stack")]
    for i, (k, v) in enumerate(STACK):
        y = 98 + i * 34
        b.append(txt(PAD, y, k, 13, t["accent"], 700, 'letter-spacing="2"'))
        b.append(txt(PAD + 130, y, v, 15, t["fg"]))
        b.append(f'<rect x="{PAD}" y="{y + 12}" width="{W - 2 * PAD}" height="1" fill="{t["faint"]}"/>')
    return svg(h, t, "".join(b))


def footer(t):
    h = 74
    b = [f'<rect x="{PAD}" y="14" width="{W - 2 * PAD}" height="1.5" fill="{t["dim"]}"/>',
         f'<circle class="dot" cx="{PAD + 6}" cy="45" r="5" fill="#3fb950"/>',
         txt(PAD + 22, 50, "STATUS: " + STATUS.upper(), 13, t["fg"], 700, 'letter-spacing="1"'),
         txt(W - PAD, 50, "~/EOF", 13, t["dim"], 400, 'text-anchor="end"')]
    css = ".dot{animation:pulse 2s ease-in-out infinite}@keyframes pulse{50%{opacity:.35}}"
    return svg(h, t, "".join(b), css)


PARTS = {"header": header, "whoami": whoami, "system-map": system_map,
         "projects": projects, "stack": stack, "footer": footer}

if __name__ == "__main__":
    for theme, t in THEMES.items():
        out = ROOT / "assets" / theme
        out.mkdir(parents=True, exist_ok=True)
        for name, fn in PARTS.items():
            (out / f"{name}.svg").write_text(fn(t), encoding="utf-8", newline="\n")
    print("ok:", ", ".join(PARTS))
