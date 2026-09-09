#!/usr/bin/env python3
"""
render_visuals.py — plan.json'dan sunum gorsellerini SVG olarak uretir.

Uretilenler (docs/assets/ altina):
  journey.svg    Faz yolculugu — musteri ne zaman ne aliyor
  timeline.svg   Sprint zaman seridi, akislara gore renkli
  depgraph.svg   Bagimlilik haritasi, kritik yol vurgulu
  riskmatrix.svg Risk matrisi (etki x olasilik)
  capacity.svg   Faz bazinda paralellik ve onerilen agent sayisi
  deadline.svg   Teslim guvenilirligi (kritik yol vs deadline) — plan.json'da
                 "deadline" alani varsa uretilir, yoksa atlanir
  cost.svg       Isletme gideri dokumu, pasta (donut) grafik — plan.json'da
                 "cost_estimate" alani varsa uretilir, yoksa atlanir
  growth.svg     Hayata gectikten sonra 3/6/12 aylik birikmis musteri ve gelir,
                 sutun grafik — plan.json'da "growth_projection" alani varsa
                 uretilir, yoksa atlanir

Kullanim:
    python3 render_visuals.py plan.json --out docs/assets

Bagimlilik yok, sadece standart kutuphane. Ayni klasordeki
plan_capacity.py modulunu kullanir.
"""

import argparse
import html
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_capacity as pc  # noqa: E402

# --------------------------------------------------------------------------
# Palet — sunum temasiyla ayni
# --------------------------------------------------------------------------

INK = "#16233a"
MUTED = "#6b7280"
LINE = "#dfe3e8"
BG_SOFT = "#f5f7fa"
ACCENT = "#1f6feb"
CRIT = "#b3261e"
OK = "#2f7d55"
WARN = "#d98324"

STREAM_COLORS = [
    "#1f6feb", "#2f7d55", "#8b5cf6", "#d98324",
    "#0e7490", "#be185d", "#65a30d", "#6b7280",
]

RISK_FILL = {"high": "#b3261e", "medium": "#d98324", "low": "#8a9099"}
RISK_LABEL = {"high": "Yüksek", "medium": "Orta", "low": "Düşük"}

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', "
        "'Helvetica Neue', Arial, sans-serif")


# --------------------------------------------------------------------------
# Yardimcilar
# --------------------------------------------------------------------------

def esc(text):
    return html.escape(str(text), quote=True)


def wrap(text, max_chars, max_lines=3):
    """Kaba kelime sarmalama. SVG otomatik sarmaz."""
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        candidate = f"{cur} {w}".strip()
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = w
        if len(lines) == max_lines:
            break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and len(" ".join(lines)) < len(text) - 1:
        lines[-1] = lines[-1][:max_chars - 1].rstrip() + "…"
    return lines


AUDIENCE = "customer"


def label(it):
    """Musteri sunumunda musteri dilindeki ad, teknik sunumda asil ad."""
    if AUDIENCE == "customer":
        return it.get("customer_name") or it["name"]
    return it["name"]


def clip(text, n):
    text = str(text)
    return text if len(text) <= n else text[:n - 1].rstrip() + "…"


def text_el(x, y, content, size=13, weight="400", fill=INK,
            anchor="start", opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{op}>{esc(content)}</text>')


def svg_open(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="100%" role="img" aria-label="{esc(title)}">'
            f'<rect width="{w}" height="{h}" fill="none"/>')


def stream_color(streams, name):
    return STREAM_COLORS[streams.index(name) % len(STREAM_COLORS)]


def write(out_dir, name, body):
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body + "</svg>\n")
    return path


# --------------------------------------------------------------------------
# 1. Faz yolculugu — musteriye donuk ana gorsel
# --------------------------------------------------------------------------

def render_journey(plan, result, out_dir):
    """Faz kartlarini cizer. Kart yuksekligi, en uzun metne gore hesaplanir —
    sabit y-koordinatlari degisken sayida sarilmis satirla catisip metinleri
    ust uste bindirmesin diye (BU AŞAMA BİTİNCE / NASIL GÖRÜRÜZ)."""
    phases = plan.get("phases", [])
    n = max(1, len(phases))
    W = 1240
    pad, gap, arrow = 20, 18, 22
    bw = (W - 2 * pad - (n - 1) * (gap + arrow)) / n
    top = 28

    name_chars = max(8, int(bw / 9.6))
    body_chars = max(10, int(bw / 6.4))

    by_phase = {p["phase"]: p for p in result["phases"]}

    specs = []
    for ph in phases:
        name_lines = wrap(ph.get("name", ph.get("id", "")), name_chars, 2)
        outcome = ph.get("customer_outcome") or ph.get("purpose") or "—"
        outcome_lines = wrap(outcome, body_chars, 4)
        proof = ph.get("milestone")
        proof_lines = wrap(proof, body_chars, 2) if proof else []
        specs.append((name_lines, outcome_lines, proof_lines))

    def content_height(name_lines, outcome_lines, proof_lines):
        y = 32 + 23 + len(name_lines) * 18 + 12
        y += 18 + len(outcome_lines) * 16
        if proof_lines:
            y += 8 + 18 + len(proof_lines) * 15
        return y + 46  # alt cizgi + effort satiri icin sabit pay

    bh = max(max(content_height(*sp) for sp in specs), 200) + 14
    H = top + bh + 20

    s = [svg_open(W, H, "Faz yolculuğu")]

    for i, (ph, (name_lines, outcome_lines, proof_lines)) in enumerate(zip(phases, specs)):
        x = pad + i * (bw + gap + arrow)
        pid = ph.get("id") or ph.get("name")
        meta = by_phase.get(pid, {})
        accent = STREAM_COLORS[i % len(STREAM_COLORS)]

        s.append(f'<rect x="{x:.1f}" y="{top}" width="{bw:.1f}" height="{bh}" '
                 f'rx="12" fill="{BG_SOFT}" stroke="{LINE}"/>')
        s.append(f'<rect x="{x:.1f}" y="{top}" width="{bw:.1f}" height="5" '
                 f'rx="2.5" fill="{accent}"/>')

        cx = x + 18
        cy = top + 32
        s.append(text_el(cx, cy, f"AŞAMA {i + 1}", 11, "700", accent))
        cy += 23
        for ln in name_lines:
            s.append(text_el(cx, cy, ln, 14.5, "700"))
            cy += 18
        cy += 12

        s.append(text_el(cx, cy, "BU AŞAMA BİTİNCE", 9.5, "700", MUTED))
        cy += 18
        for ln in outcome_lines:
            s.append(text_el(cx, cy, ln, 12, "400", INK))
            cy += 16

        if proof_lines:
            cy += 8
            s.append(text_el(cx, cy, "NASIL GÖRÜRÜZ", 9.5, "700", MUTED))
            cy += 18
            for ln in proof_lines:
                s.append(text_el(cx, cy, ln, 11.5, "400", INK))
                cy += 15

        foot_y = top + bh - 22
        s.append(f'<line x1="{cx}" y1="{foot_y - 20}" x2="{x + bw - 18:.1f}" '
                 f'y2="{foot_y - 20}" stroke="{LINE}"/>')
        eff = meta.get("effort")
        s.append(text_el(cx, foot_y, f"{eff:g} iş günü" if eff else "—",
                         12, "700", MUTED))
        prio = ph.get("priority")
        if prio:
            s.append(text_el(x + bw - 18, foot_y, prio, 11, "700",
                             accent, anchor="end"))

        if i < n - 1:
            ax = x + bw + gap / 2
            ay = top + bh / 2
            s.append(f'<path d="M{ax:.1f} {ay - 7} l11 7 l-11 7 z" '
                     f'fill="{LINE}"/>')

    return write(out_dir, "journey.svg", "".join(s))


# --------------------------------------------------------------------------
# 2. Sprint zaman seridi
# --------------------------------------------------------------------------

def render_timeline(plan, result, items, out_dir):
    sprints = result["sprints"]
    if not sprints:
        return None
    streams = result["totals"]["streams"]
    crit = set(result["totals"]["critical_path_items"])

    order, phase_rows = [], {}
    for row in result["phases"]:
        pid = row["phase"]
        members = [i for s in sprints for i in s["items"]
                   if items[i]["phase"] == pid]
        if members:
            phase_rows[pid] = members
            order.append(pid)

    rows = sum(len(v) for v in phase_rows.values())
    left, pad, rh = 292, 20, 28
    W = 1240
    band = 26
    H = 92 + rows * rh + len(order) * band + 46
    cw = (W - left - pad - 12) / len(sprints)

    sprint_of = {i: s["sprint"] for s in sprints for i in s["items"]}

    s = [svg_open(W, H, "Sprint zaman şeridi")]
    s.append(text_el(pad, 26, "Zaman şeridi — hangi iş hangi sprintte", 17, "700"))
    s.append(text_el(pad, 46, "Kalın çerçeveli işler kritik yol üzerinde: "
                              "gecikirse tüm plan kayar", 11.5, "400", MUTED))

    ty = 74
    for k, sp in enumerate(sprints):
        x = left + k * cw
        s.append(f'<rect x="{x:.1f}" y="{ty - 18}" width="{cw - 4:.1f}" '
                 f'height="24" rx="5" fill="{BG_SOFT}"/>')
        s.append(text_el(x + cw / 2 - 2, ty - 1, f"Sprint {sp['sprint']}",
                         11.5, "700", INK, anchor="middle"))
        s.append(f'<line x1="{x:.1f}" y1="{ty + 10}" x2="{x:.1f}" '
                 f'y2="{H - 40}" stroke="{LINE}" stroke-dasharray="2 4"/>')

    y = ty + 24
    for pid in order:
        meta = next(r for r in result["phases"] if r["phase"] == pid)
        s.append(f'<rect x="{pad}" y="{y - 2}" width="{W - 2 * pad}" '
                 f'height="{band - 6}" rx="4" fill="{BG_SOFT}"/>')
        s.append(text_el(pad + 10, y + 13,
                         f"{pid} · {clip(meta['phase_name'], 46)}", 12, "700"))
        y += band

        for iid in phase_rows[pid]:
            it = items[iid]
            s.append(text_el(pad + 10, y + 16, clip(label(it), 37), 12))
            k = sprint_of[iid] - 1
            x = left + k * cw + 3
            bw = cw - 10
            col = stream_color(streams, it["stream"])
            is_crit = iid in crit
            s.append(f'<rect x="{x:.1f}" y="{y + 4}" width="{bw:.1f}" '
                     f'height="{rh - 9}" rx="5" fill="{col}" '
                     f'fill-opacity="{0.9 if is_crit else 0.6}" '
                     f'stroke="{CRIT if is_crit else "none"}" '
                     f'stroke-width="{2 if is_crit else 0}"/>')
            s.append(text_el(x + 9, y + 18, f"{iid} · {it['effort']:g}g",
                             10.5, "700", "#ffffff"))
            if it["risk"] == "high":
                s.append(f'<circle cx="{x + bw - 10:.1f}" cy="{y + 13.5}" r="4.5" '
                         f'fill="#ffffff"/>')
                s.append(f'<circle cx="{x + bw - 10:.1f}" cy="{y + 13.5}" r="2.5" '
                         f'fill="{CRIT}"/>')
            y += rh

    ly = H - 20
    s.append(text_el(pad, ly, "Ekipler:", 11, "700", MUTED))
    lx = pad + 58
    for st in streams:
        s.append(f'<rect x="{lx}" y="{ly - 9}" width="11" height="11" rx="3" '
                 f'fill="{stream_color(streams, st)}"/>')
        s.append(text_el(lx + 16, ly, st, 11, "400", MUTED))
        lx += 24 + len(st) * 6.6
    s.append(f'<circle cx="{lx + 6}" cy="{ly - 4}" r="4.5" fill="{CRIT}"/>')
    s.append(text_el(lx + 16, ly, "yüksek riskli", 11, "400", MUTED))

    return write(out_dir, "timeline.svg", "".join(s))


# --------------------------------------------------------------------------
# 3. Bagimlilik haritasi
# --------------------------------------------------------------------------

def render_depgraph(result, items, out_dir):
    crit = result["totals"]["critical_path_items"]
    crit_set = set(crit)
    crit_pairs = set(zip(crit, crit[1:]))
    streams = result["totals"]["streams"]

    depth, memo = {}, {}

    def d(node):
        if node in memo:
            return memo[node]
        memo[node] = 0
        deps = [x for x in items[node]["deps"] if x in items]
        memo[node] = 0 if not deps else 1 + max(d(x) for x in deps)
        return memo[node]

    for iid in items:
        depth[iid] = d(iid)

    layers = {}
    for iid, lv in sorted(depth.items(), key=lambda kv: (kv[1], kv[0])):
        layers.setdefault(lv, []).append(iid)

    nw, nh = 168, 46
    gapx, gapy = 66, 20
    pad = 20
    cols = len(layers)
    maxrow = max(len(v) for v in layers.values())
    W = pad * 2 + cols * nw + (cols - 1) * gapx
    W = max(W, 900)
    H = 96 + maxrow * (nh + gapy) + 22

    pos = {}
    for lv, group in layers.items():
        x = pad + lv * (nw + gapx)
        block = len(group) * (nh + gapy) - gapy
        y0 = 90 + (maxrow * (nh + gapy) - gapy - block) / 2
        for k, iid in enumerate(group):
            pos[iid] = (x, y0 + k * (nh + gapy))

    s = [svg_open(W, H, "Bağımlılık haritası")]
    s.append(text_el(pad, 26, "Neyin neyi beklediği", 17, "700"))
    s.append(text_el(pad, 47,
                     f"Kırmızı zincir kritik yol: {result['totals']['critical_path']:g} gün. "
                     f"Bu zincir kısalmadan proje daha hızlı bitmez.",
                     11.5, "400", MUTED))

    for iid, it in items.items():
        x2, y2 = pos[iid]
        for dep in it["deps"]:
            if dep not in pos:
                continue
            x1, y1 = pos[dep]
            sx, sy = x1 + nw, y1 + nh / 2
            ex, ey = x2, y2 + nh / 2
            mid = (sx + ex) / 2
            hot = (dep, iid) in crit_pairs
            s.append(f'<path d="M{sx:.1f} {sy:.1f} C{mid:.1f} {sy:.1f} '
                     f'{mid:.1f} {ey:.1f} {ex - 6:.1f} {ey:.1f}" fill="none" '
                     f'stroke="{CRIT if hot else LINE}" '
                     f'stroke-width="{2.2 if hot else 1.4}" '
                     f'opacity="{1 if hot else 0.9}"/>')
            s.append(f'<path d="M{ex - 6:.1f} {ey - 4:.1f} l6 4 l-6 4 z" '
                     f'fill="{CRIT if hot else LINE}"/>')

    for iid, it in items.items():
        x, y = pos[iid]
        hot = iid in crit_set
        col = stream_color(streams, it["stream"])
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{nw}" height="{nh}" '
                 f'rx="9" fill="#ffffff" stroke="{CRIT if hot else LINE}" '
                 f'stroke-width="{2 if hot else 1.2}"/>')
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="4" height="{nh}" '
                 f'rx="2" fill="{col}"/>')
        s.append(text_el(x + 13, y + 19, f"{iid} · {it['effort']:g}g", 10.5,
                         "700", MUTED))
        s.append(text_el(x + 13, y + 35, clip(label(it), 19), 12, "600"))
        if it["risk"] == "high":
            s.append(f'<circle cx="{x + nw - 12:.1f}" cy="{y + 14}" r="4.5" '
                     f'fill="{CRIT}"/>')

    return write(out_dir, "depgraph.svg", "".join(s))


# --------------------------------------------------------------------------
# 4. Risk matrisi
# --------------------------------------------------------------------------

LEVELS = ["Düşük", "Orta", "Yüksek"]
LEVEL_KEYS = {"düşük": 0, "dusuk": 0, "low": 0, "orta": 1, "medium": 1,
              "yüksek": 2, "yuksek": 2, "high": 2}


def _lvl(v):
    return LEVEL_KEYS.get(str(v).strip().lower(), 1)


def collect_risks(plan, items):
    risks = plan.get("risks")
    if risks:
        return [{
            "id": r.get("id", f"R{i + 1}"),
            "text": ((r.get("customer_text") or r.get("text"))
                     if AUDIENCE == "customer"
                     else (r.get("text") or r.get("customer_text"))) or "",
            "impact": _lvl(r.get("impact", "orta")),
            "prob": _lvl(r.get("probability", "orta")),
            "when": r.get("when", ""),
            "mitigation": r.get("mitigation", ""),
            "decision": r.get("decision", ""),
        } for i, r in enumerate(risks)]
    # plan.json'da risks yoksa is bazli risk seviyesinden turet
    out = []
    for i, (iid, it) in enumerate(
            sorted(items.items(), key=lambda kv: kv[0])):
        if it["risk"] == "low":
            continue
        lv = 2 if it["risk"] == "high" else 1
        out.append({"id": iid, "text": label(it), "impact": lv,
                    "prob": lv, "when": it["phase"], "mitigation": ""})
    return out[:9]


def render_riskmatrix(plan, items, out_dir):
    risks = collect_risks(plan, items)
    W, H = 1240, 460
    pad = 20
    cell = 116
    ox, oy = pad + 92, 58

    s = [svg_open(W, H, "Risk matrisi")]
    s.append(text_el(pad, 26, "Etki × olasılık — sağ üstteki riskler bilerek en "
                              "başa alındı, her birinin bir azaltma planı var",
                     12.5, "600", MUTED))

    tint = [["#f1f6f2", "#fbf6ec", "#fbeeec"],
            ["#fbf6ec", "#fbeeec", "#f7e0dd"],
            ["#fbeeec", "#f7e0dd", "#f2cfca"]]
    for r in range(3):
        for c in range(3):
            x = ox + c * cell
            y = oy + (2 - r) * cell
            s.append(f'<rect x="{x}" y="{y}" width="{cell - 4}" '
                     f'height="{cell - 4}" rx="8" fill="{tint[r][c]}" '
                     f'stroke="{LINE}"/>')

    for i, lab in enumerate(LEVELS):
        s.append(text_el(ox + i * cell + (cell - 4) / 2,
                         oy + 3 * cell + 18, lab, 11.5, "600", MUTED,
                         anchor="middle"))
        s.append(text_el(ox - 12, oy + (2 - i) * cell + (cell - 4) / 2 + 4,
                         lab, 11.5, "600", MUTED, anchor="end"))
    s.append(text_el(ox + 1.5 * cell, oy + 3 * cell + 40, "OLASILIK",
                     10.5, "700", MUTED, anchor="middle"))
    s.append(f'<text x="{pad + 14}" y="{oy + 1.5 * cell}" '
             f'font-family="{FONT}" font-size="10.5" font-weight="700" '
             f'fill="{MUTED}" text-anchor="middle" '
             f'transform="rotate(-90 {pad + 14} {oy + 1.5 * cell})">ETKİ</text>')

    buckets = {}
    for r in risks:
        buckets.setdefault((r["impact"], r["prob"]), []).append(r)
    for (imp, prob), group in buckets.items():
        bx = ox + prob * cell + (cell - 4) / 2
        by = oy + (2 - imp) * cell + (cell - 4) / 2
        per_row = 3
        rows_n = math.ceil(len(group) / per_row)
        r_dot = 15 if len(group) <= 3 else 12
        step = 32 if len(group) <= 3 else 27
        col = CRIT if imp == 2 else WARN if imp == 1 else OK
        for k, r in enumerate(group):
            row, col_i = divmod(k, per_row)
            in_row = min(per_row, len(group) - row * per_row)
            dx = (col_i - (in_row - 1) / 2) * step
            dy = (row - (rows_n - 1) / 2) * (step - 2)
            s.append(f'<circle cx="{bx + dx:.1f}" cy="{by + dy:.1f}" '
                     f'r="{r_dot}" fill="{col}"/>')
            s.append(text_el(bx + dx, by + dy + 4, r["id"],
                             10.5 if r_dot > 12 else 9, "700",
                             "#ffffff", anchor="middle"))

    lx = ox + 3 * cell + 34
    s.append(text_el(lx, oy + 4, "Nasıl yönetiyoruz", 11.5, "700", MUTED))
    ly = oy + 26
    for r in risks[:7]:
        col = CRIT if r["impact"] == 2 else WARN if r["impact"] == 1 else OK
        s.append(f'<circle cx="{lx + 9}" cy="{ly - 4}" r="9" fill="{col}"/>')
        s.append(text_el(lx + 9, ly - 0.5, r["id"], 9, "700", "#ffffff",
                         anchor="middle"))
        s.append(text_el(lx + 26, ly, clip(r["text"], 62), 12, "600"))
        if r.get("mitigation"):
            s.append(text_el(lx + 26, ly + 15,
                             clip("Azaltma: " + r["mitigation"], 74), 10.5,
                             "600", OK))
        elif r.get("when"):
            s.append(text_el(lx + 26, ly + 15, clip(r["when"], 76), 10.5,
                             "400", MUTED))
        if r.get("decision"):
            s.append(text_el(lx + 26, ly + 30, "→ " + clip(r["decision"], 72),
                             10.5, "600", WARN))
        ly += 52

    return write(out_dir, "riskmatrix.svg", "".join(s))


# --------------------------------------------------------------------------
# 5. Kapasite / paralellik
# --------------------------------------------------------------------------

def render_capacity(result, out_dir):
    rows = result["phases"]
    W = 1240
    pad = 20
    H = 120 + len(rows) * 62 + 40
    label_w = 210
    bar_x = pad + label_w
    bar_w = W - bar_x - 348

    peak = max([r["parallelism_index"] for r in rows] +
               [r["recommended_agents"] for r in rows] + [1])

    s = [svg_open(W, H, "Kapasite ve paralellik")]
    s.append(text_el(pad, 26, "Aynı anda kaç iş yürüyebilir", 17, "700"))
    s.append(text_el(pad, 47,
                     "Gri çubuk: işin izin verdiği paralellik. "
                     "Renkli çubuk: gerçekte önerilen eş zamanlı iş akışı. "
                     "Fark, darboğazın büyüklüğüdür.", 11.5, "400", MUTED))

    y = 88
    for r in rows:
        s.append(text_el(pad, y + 16, clip(f"{r['phase']} · {r['phase_name']}", 26),
                         12.5, "700"))
        s.append(text_el(pad, y + 34, f"{r['effort']:g} iş günü", 11, "400", MUTED))

        s.append(f'<rect x="{bar_x}" y="{y + 4}" width="{bar_w}" height="16" '
                 f'rx="8" fill="{BG_SOFT}"/>')
        pw = bar_w * r["parallelism_index"] / peak
        s.append(f'<rect x="{bar_x}" y="{y + 4}" width="{pw:.1f}" height="16" '
                 f'rx="8" fill="{LINE}"/>')
        s.append(text_el(bar_x + pw + 8, y + 17,
                         f"{r['parallelism_index']:g}", 11, "700", MUTED))

        aw = bar_w * r["recommended_agents"] / peak
        s.append(f'<rect x="{bar_x}" y="{y + 26}" width="{aw:.1f}" height="16" '
                 f'rx="8" fill="{ACCENT}"/>')
        s.append(text_el(bar_x + aw + 8, y + 39,
                         f"{r['recommended_agents']}", 11, "700", ACCENT))

        s.append(text_el(W - pad - 12, y + 17, "sınırlayan:", 10.5, "400",
                         MUTED, anchor="end"))
        s.append(text_el(W - pad - 12, y + 34, clip(r["binding_constraint"], 28),
                         11.5, "700", WARN, anchor="end"))
        y += 62

    cap = result["capacity"]
    note = (f"Ekip {cap['people']:g} kişi · sprint {cap['sprint_length_days']:g} gün · "
            f"odak {cap['focus_factor']} → sprint kapasitesi "
            f"{cap['sprint_capacity']:g} iş günü · en az {cap['min_sprints']} sprint")
    s.append(text_el(pad, H - 16, note, 11.5, "400", MUTED))

    return write(out_dir, "capacity.svg", "".join(s))


DEADLINE_STATUS_LABEL = {"rahat": "Rahat", "sikisik": "Sıkışık", "riskli": "Riskli"}
DEADLINE_STATUS_COLOR = {"rahat": OK, "sikisik": WARN, "riskli": CRIT}


def render_deadline(result, out_dir):
    """Kritik yol ile deadline'i karsilastiran tek cubuklu gauge.

    result['deadline'] yoksa (plan.json'da 'deadline' alani girilmemis) hicbir
    dosya yazmadan None doner — bu gorsel opsiyoneldir.
    """
    d = result.get("deadline")
    if not d:
        return None

    W, H = 1240, 170
    pad = 24
    bar_x, bar_y, bar_w, bar_h = pad, 68, W - pad * 2, 34

    s = [svg_open(W, H, "Teslim güvenilirliği")]
    s.append(text_el(pad, 28,
                     "Kritik yolun elinizdeki süreye sığıp sığmadığını gösterir — "
                     "tampon büyüdükçe gecikme riski düşer.", 12.5, "600", MUTED))

    color = DEADLINE_STATUS_COLOR[d["status"]]
    total = max(d["days_available"], d["critical_path_days"], 1)
    scale = bar_w / total

    s.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w:.1f}" height="{bar_h}" '
             f'rx="9" fill="{BG_SOFT}"/>')
    crit_w = min(d["critical_path_days"] * scale, bar_w)
    s.append(f'<rect x="{bar_x}" y="{bar_y}" width="{crit_w:.1f}" height="{bar_h}" '
             f'rx="9" fill="{color}"/>')

    dl_x = bar_x + min(d["days_available"] * scale, bar_w)
    s.append(f'<line x1="{dl_x:.1f}" y1="{bar_y - 10}" x2="{dl_x:.1f}" '
             f'y2="{bar_y + bar_h + 10}" stroke="{INK}" stroke-width="2" '
             f'stroke-dasharray="4 3"/>')
    s.append(text_el(dl_x, bar_y - 16, "elinizdeki süre", 10.5, "600", INK, anchor="end"))

    s.append(text_el(bar_x, bar_y + bar_h + 28,
                     f"Kritik yol: {d['critical_path_days']:g} gün", 12.5, "700", color))
    sign = "+" if d["buffer_days"] >= 0 else ""
    s.append(text_el(W - pad, bar_y + bar_h + 28,
                     f"Tampon: {sign}{d['buffer_days']:g} gün (%{d['buffer_pct']:g}) · "
                     f"{DEADLINE_STATUS_LABEL[d['status']]}", 12.5, "700", color, anchor="end"))

    if d.get("driver"):
        s.append(text_el(pad, H - 14, clip(f"Neden bu tarih: {d['driver']}", 110),
                         11, "400", MUTED))

    return write(out_dir, "deadline.svg", "".join(s))


PIE_COLORS = [ACCENT, OK, WARN, "#8b5cf6", "#0e7490", "#be185d", "#65a30d"]


def _polar(cx, cy, r, angle_deg):
    rad = math.radians(angle_deg - 90)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def _donut_slice(cx, cy, r_out, r_in, start, end):
    x1o, y1o = _polar(cx, cy, r_out, start)
    x2o, y2o = _polar(cx, cy, r_out, end)
    x1i, y1i = _polar(cx, cy, r_in, end)
    x2i, y2i = _polar(cx, cy, r_in, start)
    large = 1 if (end - start) > 180 else 0
    return (f'M {x1o:.2f} {y1o:.2f} '
            f'A {r_out:.2f} {r_out:.2f} 0 {large} 1 {x2o:.2f} {y2o:.2f} '
            f'L {x1i:.2f} {y1i:.2f} '
            f'A {r_in:.2f} {r_in:.2f} 0 {large} 0 {x2i:.2f} {y2i:.2f} Z')


def render_cost(result, out_dir):
    """Aylik isletme giderinin kalem dagilimini pasta (donut) grafik olarak cizer.

    result['cost'] yoksa (plan.json'da 'cost_estimate' alani girilmemis)
    hicbir dosya yazmadan None doner — bu gorsel opsiyoneldir.
    """
    c = result.get("cost")
    if not c:
        return None

    cur = c["currency"]
    items = [it for it in c["recurring_items"]
             if float(it.get("amount", 0) or 0) > 0]
    W, H = 1240, 420

    header = f"Aylık toplam: {c['monthly_total']:g} {cur}"
    if c["one_time_total"]:
        header += f" · Kurulum (tek seferlik): {c['one_time_total']:g} {cur}"

    s = [svg_open(W, H, "İşletme gideri")]
    s.append(text_el(24, 28, header, 13, "600", MUTED))

    if not items:
        s.append(text_el(W / 2, H / 2, "Aylık tekrarlayan gider yok",
                         16, "700", MUTED, anchor="middle"))
        return write(out_dir, "cost.svg", "".join(s))

    cx, cy, r_out, r_in = 230, 240, 148, 90
    total = sum(float(it.get("amount", 0) or 0) for it in items)

    angle = 0.0
    colors = []
    for i, it in enumerate(items):
        amt = float(it.get("amount", 0) or 0)
        sweep = (amt / total * 360) if total else 0
        color = PIE_COLORS[i % len(PIE_COLORS)]
        colors.append(color)
        if sweep >= 359.98:
            s.append(f'<circle cx="{cx}" cy="{cy}" r="{(r_out + r_in) / 2:.1f}" '
                     f'fill="none" stroke="{color}" stroke-width="{r_out - r_in}"/>')
        else:
            s.append(f'<path d="{_donut_slice(cx, cy, r_out, r_in, angle, angle + sweep)}" '
                     f'fill="{color}"/>')
        angle += sweep

    s.append(text_el(cx, cy - 4, f"{c['monthly_total']:g}", 32, "700", INK, anchor="middle"))
    s.append(text_el(cx, cy + 22, f"{cur}/ay", 13, "600", MUTED, anchor="middle"))

    lx, ly = 470, 84
    for i, it in enumerate(items):
        amt = float(it.get("amount", 0) or 0)
        pct = round(amt / total * 100) if total else 0
        color = colors[i]
        s.append(f'<rect x="{lx}" y="{ly - 15}" width="16" height="16" rx="4" fill="{color}"/>')
        s.append(text_el(lx + 26, ly - 2, clip(it.get("item", ""), 34), 14.5, "700"))
        if it.get("note"):
            s.append(text_el(lx + 26, ly + 16, clip(it["note"], 58), 10.5, "400", MUTED))
        s.append(text_el(W - 24, ly - 2, f"{amt:g} {cur}/ay · %{pct}",
                         13.5, "700", color, anchor="end"))
        ly += 60

    if c.get("notes"):
        s.append(text_el(24, H - 14, clip(c["notes"], 140), 11, "400", MUTED))

    return write(out_dir, "cost.svg", "".join(s))


def render_growth(result, out_dir):
    """Hayata gectikten sonra birikmis musteri ve gelir buyumesini iki panelde,
    sutun (dikey cubuk) grafik olarak cizer.

    result['growth'] yoksa (plan.json'da 'growth_projection' alani girilmemis)
    hicbir dosya yazmadan None doner — bu gorsel opsiyoneldir.
    """
    g = result.get("growth")
    if not g:
        return None

    ms = g["milestones"]
    cur = g["currency"]
    W, H = 1240, 430
    pad = 24
    panel_w = (W - pad * 3) / 2
    chart_h = 230
    base_y = 100 + chart_h

    s = [svg_open(W, H, "Büyüme projeksiyonu")]
    s.append(text_el(pad, 28,
                     "Hayata geçtikten sonra birikmiş müşteri sayısı ve gelir",
                     13, "600", MUTED))

    def panel(x0, title, values, suffix, color):
        peak = max(values + [1])
        bw = 76
        n = max(len(values), 1)
        slot = panel_w / n
        s.append(text_el(x0, 62, title, 15, "700"))
        s.append(f'<line x1="{x0}" y1="{base_y}" x2="{x0 + panel_w:.1f}" '
                 f'y2="{base_y}" stroke="{LINE}"/>')
        for i, (m, v) in enumerate(zip(ms, values)):
            bx = x0 + slot * i + (slot - bw) / 2
            bh = chart_h * (v / peak) if peak else 0
            by = base_y - bh
            s.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw}" height="{bh:.1f}" '
                     f'rx="8" fill="{color}"/>')
            s.append(text_el(bx + bw / 2, by - 12, f"{v:g}{suffix}", 13.5, "700",
                             color, anchor="middle"))
            s.append(text_el(bx + bw / 2, base_y + 24,
                             f"{m['months_after_launch']:g}. ay", 12, "600",
                             MUTED, anchor="middle"))

    panel(pad, "Müşteri sayısı (birikmiş)",
          [m["customers"] for m in ms], "", ACCENT)
    panel(pad * 2 + panel_w, f"Gelir (birikmiş, {cur})",
          [m["revenue"] for m in ms], "", OK)

    if g.get("notes"):
        s.append(text_el(pad, H - 14, clip(g["notes"], 140), 11, "400", MUTED))

    return write(out_dir, "growth.svg", "".join(s))


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Roadmap görsellerini üretir")
    ap.add_argument("plan")
    ap.add_argument("--out", default="docs/assets")
    ap.add_argument("--estimate", choices=["p50", "p80", "mid"], default="mid")
    ap.add_argument("--audience", choices=["customer", "delivery"],
                    default="customer",
                    help="customer: müşteri dilindeki adlar; delivery: teknik adlar")
    args = ap.parse_args()

    global AUDIENCE
    AUDIENCE = args.audience

    try:
        plan = pc.load_plan(args.plan)
        result = pc.analyse(plan, args.estimate)
    except (OSError, ValueError, KeyError) as exc:
        print(f"HATA: {exc}", file=sys.stderr)
        return 1
    if "errors" in result:
        print("HATA — plan.json düzeltilmeli:", file=sys.stderr)
        for p in result["errors"]:
            print(f"  - {p}", file=sys.stderr)
        return 2

    items = pc.flatten_items(plan, args.estimate)
    os.makedirs(args.out, exist_ok=True)

    made = [
        render_journey(plan, result, args.out),
        render_timeline(plan, result, items, args.out),
        render_depgraph(result, items, args.out),
        render_riskmatrix(plan, items, args.out),
        render_capacity(result, args.out),
        render_deadline(result, args.out),
        render_cost(result, args.out),
        render_growth(result, args.out),
    ]
    for p in made:
        if p:
            print(f"  yazıldı: {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
