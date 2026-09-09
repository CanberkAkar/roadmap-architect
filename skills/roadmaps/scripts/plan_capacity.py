#!/usr/bin/env python3
"""
plan_capacity.py — plan.json'dan kritik yol, paralellesebilirlik,
onerilen agent sayisi ve sprint dagilimini hesaplar.

Kullanim:
    python3 plan_capacity.py plan.json
    python3 plan_capacity.py plan.json --json > capacity.json
    python3 plan_capacity.py plan.json --estimate p80

Sema icin assets/plan.template.json dosyasina bakin.
Bagimlilik yok, sadece standart kutuphane.
"""

import argparse
import json
import math
import sys
from collections import defaultdict

AGENT_HARD_CAP = 8
DEFAULT_FOCUS = 0.65
DEFAULT_SPRINT_DAYS = 10
DEFAULT_REVIEWS_PER_DAY = 2.5


# --------------------------------------------------------------------------
# Yukleme ve dogrulama
# --------------------------------------------------------------------------

def load_plan(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def flatten_items(plan, estimate):
    """Fazlarin icindeki isleri tek bir sozluge indirger."""
    items = {}
    for phase in plan.get("phases", []):
        pid = phase.get("id") or phase.get("name")
        for raw in phase.get("items", []):
            iid = raw["id"]
            if iid in items:
                raise ValueError(f"Yinelenen is id'si: {iid}")
            items[iid] = {
                "id": iid,
                "name": raw.get("name", iid),
                "customer_name": raw.get("customer_name") or raw.get("name", iid),
                "phase": pid,
                "phase_name": phase.get("name", pid),
                "effort": resolve_effort(raw, estimate),
                "deps": list(raw.get("deps", [])),
                "risk": (raw.get("risk") or "low").lower(),
                "stream": raw.get("stream") or "default",
                "status": raw.get("status", "Planlandı"),
            }
    return items


def resolve_effort(raw, estimate):
    """effort tek sayi ya da {p50, p80} olabilir."""
    eff = raw.get("effort")
    if isinstance(eff, dict):
        if estimate == "p50":
            return float(eff.get("p50", eff.get("p80", 0)))
        if estimate == "p80":
            return float(eff.get("p80", eff.get("p50", 0)))
        p50 = float(eff.get("p50", 0))
        p80 = float(eff.get("p80", p50))
        return (p50 + p80) / 2.0
    return float(eff or 0)


def validate(items):
    """(problems, fatal) doner. fatal=True ise hesaplama yapilamaz."""
    problems, fatal = [], False
    for iid, it in items.items():
        for dep in it["deps"]:
            if dep not in items:
                problems.append(f"{iid} bilinmeyen bir işe bağımlı: {dep}")
                fatal = True
        if it["effort"] <= 0:
            problems.append(f"{iid} için effort tanımlı değil veya sıfır")
    cycle = find_cycle(items)
    if cycle:
        problems.append("Dependency döngüsü: " + " → ".join(cycle))
        fatal = True
    return problems, fatal


def find_cycle(items):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in items}
    stack = []

    def visit(node):
        color[node] = GRAY
        stack.append(node)
        for dep in items[node]["deps"]:
            if dep not in items:
                continue
            if color[dep] == GRAY:
                return stack[stack.index(dep):] + [dep]
            if color[dep] == WHITE:
                found = visit(dep)
                if found:
                    return found
        stack.pop()
        color[node] = BLACK
        return None

    for node in items:
        if color[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return None


# --------------------------------------------------------------------------
# Grafik metrikleri
# --------------------------------------------------------------------------

def longest_path(items):
    """Dugum agirlikli en uzun yol = kritik yol. (id_listesi, uzunluk) doner."""
    memo = {}

    def walk(node):
        if node in memo:
            return memo[node]
        best_len, best_path = 0.0, []
        for dep in items[node]["deps"]:
            if dep not in items:
                continue
            dlen, dpath = walk(dep)
            if dlen > best_len:
                best_len, best_path = dlen, dpath
        result = (best_len + items[node]["effort"], best_path + [node])
        memo[node] = result
        return result

    best = (0.0, [])
    for node in items:
        length, path = walk(node)
        if length > best[0]:
            best = (length, path)
    return best[1], best[0]


def dependent_counts(items):
    """Her isin dogrudan+dolayli olarak kac isin onunu actigi."""
    reverse = defaultdict(set)
    for iid, it in items.items():
        for dep in it["deps"]:
            if dep in items:
                reverse[dep].add(iid)

    memo = {}

    def downstream(node):
        if node in memo:
            return memo[node]
        memo[node] = set()  # dongu korumasi
        acc = set()
        for child in reverse[node]:
            acc.add(child)
            acc |= downstream(child)
        memo[node] = acc
        return acc

    return {iid: len(downstream(iid)) for iid in items}


# --------------------------------------------------------------------------
# Sprint dagilimi
# --------------------------------------------------------------------------

def pack_sprints(items, capacity, critical_set, sprint_days, max_sprints=60):
    """Acgozlu sprint yerlestirmesi.

    Iki kisit birlikte uygulanir:
      1. Kapasite  — sprintteki toplam effort, sprint kapasitesini asamaz
      2. Takvim    — sprint ICINDE bir bagimlilik zinciri sprint suresini asamaz

    Ikinci kisit sayesinde birbirine bagli isler ayni sprinte girebilir
    (gercekte oldugu gibi), bu da bos kapasiteyi ortadan kaldirir.
    """
    deps_count = dependent_counts(items)
    remaining = set(items)
    placed_sprint = {}
    finish_day = {}      # sprint icindeki bitis gunu
    sprints = []

    def duration(iid):
        # Sprintten uzun isler birden fazla kisiyle paylasilir varsayimi
        return min(items[iid]["effort"], sprint_days)

    while remaining and len(sprints) < max_sprints:
        idx = len(sprints) + 1
        bucket, used = [], 0.0
        progress = True

        while progress:
            progress = False
            ready = []
            for iid in remaining:
                if iid in bucket:
                    continue
                deps = [d for d in items[iid]["deps"] if d in items]
                if not all(d in placed_sprint for d in deps):
                    continue
                # sprint ICI bagimliliklarin bitisine gore en erken baslangic
                start = max(
                    [finish_day[d] for d in deps if placed_sprint[d] == idx] or [0.0]
                )
                if start + duration(iid) > sprint_days:
                    continue
                if used + items[iid]["effort"] > capacity and bucket:
                    continue
                ready.append((iid, start))

            if not ready:
                break

            ready.sort(key=lambda pair: (
                0 if items[pair[0]]["risk"] == "high"
                else 1 if items[pair[0]]["risk"] == "medium" else 2,
                -deps_count[pair[0]],
                0 if pair[0] in critical_set else 1,
                pair[1],
                items[pair[0]]["effort"],
            ))

            iid, start = ready[0]
            bucket.append(iid)
            used += items[iid]["effort"]
            placed_sprint[iid] = idx
            finish_day[iid] = start + duration(iid)
            remaining.discard(iid)
            progress = True

        if not bucket:
            break

        util = (used / capacity) if capacity else 0.0
        if util < 0.55 and remaining:
            note = ("dependency zinciri bağlıyor, kapasite değil — "
                    "boşta kalan kapasiteyi teknik borç/test altyapısına yönlendir "
                    "veya bir sonraki fazın işini böl")
        elif util > 0.95:
            note = "tampon yok — planlanmamış iş için %15-20 boşluk bırak"
        else:
            note = None

        sprints.append({
            "sprint": idx,
            "items": bucket,
            "planned_effort": round(used, 1),
            "capacity": round(capacity, 1),
            "utilization": round(util, 2),
            "streams": sorted({items[i]["stream"] for i in bucket}),
            "phases": sorted({items[i]["phase"] for i in bucket}),
            "note": note,
        })

    return sprints, sorted(remaining)


# --------------------------------------------------------------------------
# Agent onerisi
# --------------------------------------------------------------------------

def recommend_agents(parallelism, stream_count, review_capacity, cap=AGENT_HARD_CAP):
    candidates = {
        "işin yapısı (kritik yol)": max(1, math.ceil(parallelism)),
        "çakışmayan akış sayısı": max(1, stream_count),
        "inceleme kapasitesi": max(1, review_capacity),
        "sabit tavan": cap,
    }
    value = min(candidates.values())
    binding = [k for k, v in candidates.items() if v == value]
    return value, binding, candidates


def phase_breakdown(items, review_capacity):
    """Faz bazinda paralellik ve agent onerisi."""
    by_phase = defaultdict(list)
    for it in items.values():
        by_phase[it["phase"]].append(it)

    rows = []
    for pid, group in by_phase.items():
        sub = {i["id"]: i for i in group}
        # faz disi bagimliliklari kirp
        for i in sub.values():
            i = dict(i)
        trimmed = {
            k: {**v, "deps": [d for d in v["deps"] if d in sub]}
            for k, v in sub.items()
        }
        total = sum(i["effort"] for i in trimmed.values())
        _, crit = longest_path(trimmed)
        pi = (total / crit) if crit else 1.0
        streams = len({i["stream"] for i in trimmed.values()})
        agents, binding, _ = recommend_agents(pi, streams, review_capacity)
        rows.append({
            "phase": pid,
            "phase_name": group[0]["phase_name"],
            "effort": round(total, 1),
            "critical_path": round(crit, 1),
            "parallelism_index": round(pi, 2),
            "streams": streams,
            "recommended_agents": agents,
            "binding_constraint": binding[0],
        })
    rows.sort(key=lambda r: str(r["phase"]))
    return rows


# --------------------------------------------------------------------------
# Teslim guvenilirligi
# --------------------------------------------------------------------------

DEADLINE_STATUS_LABEL = {"rahat": "Rahat", "sikisik": "Sıkışık", "riskli": "Riskli"}


def deadline_confidence(plan, critical_path_days):
    """plan.json'daki 'deadline' alanindan teslim guvenilirligini hesaplar.

    plan.json'da deadline yoksa None doner — bu alan opsiyoneldir.
    """
    dl = plan.get("deadline")
    if not dl or dl.get("days_available") is None:
        return None

    available = float(dl["days_available"])
    buffer_days = available - critical_path_days
    buffer_pct = (buffer_days / available * 100) if available else 0.0

    if buffer_pct >= 20:
        status = "rahat"
    elif buffer_pct >= 0:
        status = "sikisik"
    else:
        status = "riskli"

    return {
        "days_available": available,
        "critical_path_days": round(critical_path_days, 1),
        "buffer_days": round(buffer_days, 1),
        "buffer_pct": round(buffer_pct, 1),
        "status": status,
        "driver": dl.get("driver"),
        "customer_text": dl.get("customer_text"),
    }


# --------------------------------------------------------------------------
# Isletme gideri
# --------------------------------------------------------------------------

def cost_summary(plan):
    """plan.json'daki 'cost_estimate' alanindan toplamlari hesaplar.

    plan.json'da cost_estimate yoksa None doner — bu alan opsiyoneldir.
    """
    ce = plan.get("cost_estimate")
    if not ce:
        return None

    one_time = ce.get("one_time", []) or []
    recurring = ce.get("recurring_monthly", []) or []
    one_time_total = sum(float(i.get("amount", 0) or 0) for i in one_time)
    monthly_total = sum(float(i.get("amount", 0) or 0) for i in recurring)

    return {
        "currency": ce.get("currency", ""),
        "one_time_items": one_time,
        "recurring_items": recurring,
        "one_time_total": round(one_time_total, 2),
        "monthly_total": round(monthly_total, 2),
        "annual_total": round(monthly_total * 12, 2),
        "notes": ce.get("notes"),
    }


# --------------------------------------------------------------------------
# Ana hesap
# --------------------------------------------------------------------------

def analyse(plan, estimate):
    items = flatten_items(plan, estimate)
    if not items:
        raise ValueError("plan.json içinde hiç iş bulunamadı")

    problems, fatal = validate(items)
    if fatal:
        return {"errors": problems}

    team = plan.get("team", {}) or {}
    people = float(team.get("people", team.get("devs", 1)) or 1)
    focus = float(team.get("focus_factor", DEFAULT_FOCUS))
    sprint_days = float(plan.get("sprint_length_days", DEFAULT_SPRINT_DAYS))
    reviewers = float(team.get("reviewers", 1) or 1)
    reviews_per_day = float(team.get("reviews_per_day", DEFAULT_REVIEWS_PER_DAY))

    total = sum(i["effort"] for i in items.values())
    crit_path, crit_len = longest_path(items)
    crit_set = set(crit_path)
    pi = (total / crit_len) if crit_len else 1.0
    streams = sorted({i["stream"] for i in items.values()})

    capacity = people * sprint_days * focus
    review_capacity = max(1, int(reviewers * reviews_per_day))

    for iid, it in items.items():
        if it["effort"] > sprint_days:
            problems.append(
                f"{iid} ({it['effort']:g} gün) tek sprintten büyük — bölünmeli, "
                f"yoksa sprint sonunda gösterilecek bir kanıt çıkmaz"
            )

    sprints, unplaced = pack_sprints(items, capacity, crit_set, sprint_days)
    min_by_capacity = math.ceil(total / capacity) if capacity else None
    min_by_critical = math.ceil(crit_len / sprint_days) if sprint_days else None

    agents, binding, candidates = recommend_agents(pi, len(streams), review_capacity)

    scale = ("S" if total < 20 else "M" if total < 80 else "L" if total <= 300 else "XL")

    deadline = deadline_confidence(plan, crit_len)
    if deadline and deadline["status"] == "riskli":
        problems.append(
            f"Kritik yol, deadline'ı {abs(deadline['buffer_days']):g} gün aşıyor "
            f"— kapsam, tarih veya kaynak değişmeli"
        )

    return {
        "project": plan.get("project", "(isimsiz)"),
        "goal": plan.get("goal"),
        "estimate_basis": estimate,
        "scale": scale,
        "totals": {
            "items": len(items),
            "total_effort": round(total, 1),
            "critical_path": round(crit_len, 1),
            "critical_path_items": crit_path,
            "parallelism_index": round(pi, 2),
            "streams": streams,
        },
        "capacity": {
            "people": people,
            "focus_factor": focus,
            "sprint_length_days": sprint_days,
            "sprint_capacity": round(capacity, 1),
            "min_sprints_by_capacity": min_by_capacity,
            "min_sprints_by_critical_path": min_by_critical,
            "min_sprints": max(min_by_capacity or 0, min_by_critical or 0),
            "planned_sprints": len(sprints),
        },
        "agents": {
            "recommended": agents,
            "binding_constraint": binding,
            "limits": candidates,
            "review_capacity": review_capacity,
        },
        "phases": phase_breakdown(items, review_capacity),
        "sprints": sprints,
        "unplaced_items": unplaced,
        "warnings": problems,
        "deadline": deadline,
        "cost": cost_summary(plan),
    }


# --------------------------------------------------------------------------
# Rapor
# --------------------------------------------------------------------------

def render(r, items_lookup):
    if "errors" in r:
        out = ["HATA — plan.json düzeltilmeli:"]
        out += [f"  - {p}" for p in r["errors"]]
        return "\n".join(out)

    t, c, a = r["totals"], r["capacity"], r["agents"]
    L = []
    L.append(f"# {r['project']} — kapasite analizi")
    if r.get("goal"):
        L.append(f"Hedef: {r['goal']}")
    L.append(f"Tahmin temeli: {r['estimate_basis']} · Ölçek: {r['scale']}")
    L.append("")

    L.append("## Büyüklükler")
    L.append(f"  Toplam effort           : {t['total_effort']} insan-günü ({t['items']} iş)")
    L.append(f"  Kritik yol              : {t['critical_path']} gün")
    L.append(f"  Paralelleşebilirlik (PI): {t['parallelism_index']}")
    L.append(f"  Akış (stream) sayısı    : {len(t['streams'])} → {', '.join(t['streams'])}")
    L.append("")
    L.append("  Kritik yol: " + " → ".join(t["critical_path_items"]))
    L.append("")

    L.append("## Süre")
    L.append(f"  Sprint kapasitesi       : {c['sprint_capacity']} insan-günü "
             f"({c['people']:g} kişi × {c['sprint_length_days']:g} gün × {c['focus_factor']} odak)")
    L.append(f"  Kapasiteye göre min.    : {c['min_sprints_by_capacity']} sprint")
    L.append(f"  Kritik yola göre min.   : {c['min_sprints_by_critical_path']} sprint")
    L.append(f"  Bağlayıcı minimum       : {c['min_sprints']} sprint")
    L.append(f"  Planlanan               : {c['planned_sprints']} sprint")
    if c["min_sprints_by_critical_path"] and c["min_sprints_by_capacity"]:
        if c["min_sprints_by_critical_path"] > c["min_sprints_by_capacity"]:
            L.append("  ! Kritik yol bağlıyor: kişi eklemek süreyi kısaltmaz. "
                     "Zinciri kısaltmak veya paralelleştirmek gerekir.")
        else:
            L.append("  ! Kapasite bağlıyor: kişi/agent eklemek süreyi kısaltabilir.")
    L.append("")

    if r.get("deadline"):
        d = r["deadline"]
        sign = "+" if d["buffer_days"] >= 0 else ""
        L.append("## Teslim güvenilirliği")
        L.append(f"  Kritik yol              : {d['critical_path_days']:g} gün")
        driver = f" ({d['driver']})" if d.get("driver") else ""
        L.append(f"  Elinizdeki süre         : {d['days_available']:g} gün{driver}")
        L.append(f"  Tampon                  : {sign}{d['buffer_days']:g} gün "
                 f"(%{d['buffer_pct']:g}) → {DEADLINE_STATUS_LABEL[d['status']]}")
        if d["status"] == "riskli":
            L.append("  ! Kritik yol deadline'ı aşıyor — kapsam, tarih veya kaynak değişmeli")
        L.append("")

    if r.get("cost"):
        c = r["cost"]
        cur = c["currency"]
        L.append("## İşletme gideri")
        if c["one_time_items"]:
            L.append(f"  Kurulum (tek seferlik)  : {c['one_time_total']:g} {cur}")
        L.append(f"  Aylık toplam            : {c['monthly_total']:g} {cur}")
        L.append(f"  Yıllık toplam           : {c['annual_total']:g} {cur}")
        for it in c["recurring_items"]:
            amt = float(it.get("amount", 0) or 0)
            L.append(f"    - {it.get('item', ''):<32s} {amt:>10g} {cur}/ay")
        L.append("")

    L.append("## Agent önerisi")
    L.append(f"  Önerilen eşzamanlı agent: {a['recommended']}")
    L.append(f"  Bağlayıcı sınır         : {', '.join(a['binding_constraint'])}")
    for k, v in a["limits"].items():
        mark = "<<" if v == a["recommended"] else "  "
        L.append(f"    {mark} {k:28s} {v}")
    L.append("")

    L.append("## Faz bazında")
    L.append(f"  {'Faz':<10}{'Effort':>8}{'Kritik':>8}{'PI':>7}{'Akış':>6}{'Agent':>7}  Sınırlayan")
    for p in r["phases"]:
        L.append(f"  {str(p['phase']):<10}{p['effort']:>8}{p['critical_path']:>8}"
                 f"{p['parallelism_index']:>7}{p['streams']:>6}{p['recommended_agents']:>7}"
                 f"  {p['binding_constraint']}")
    L.append("")

    L.append("## Sprint dağılımı")
    for s in r["sprints"]:
        L.append(f"  Sprint {s['sprint']} — {s['planned_effort']}/{s['capacity']} "
                 f"(%{int((s['utilization'] or 0) * 100)}) · akış: {', '.join(s['streams'])}")
        for iid in s["items"]:
            it = items_lookup[iid]
            flag = " [RİSK]" if it["risk"] == "high" else ""
            L.append(f"      {iid:<8} {it['name'][:46]:<46} {it['effort']:>5}g  "
                     f"{it['stream']}{flag}")
        if s.get("note"):
            L.append(f"      → {s['note']}")
    if r["unplaced_items"]:
        L.append("")
        L.append("  ! Yerleştirilemeyen işler (bağımlılık çözülemedi): "
                 + ", ".join(r["unplaced_items"]))
    if r["warnings"]:
        L.append("")
        L.append("## Uyarılar")
        L += [f"  - {w}" for w in r["warnings"]]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Roadmap kapasite ve agent hesaplayıcı")
    ap.add_argument("plan", help="plan.json yolu")
    ap.add_argument("--json", action="store_true", help="Ham JSON çıktısı ver")
    ap.add_argument("--estimate", choices=["p50", "p80", "mid"], default="mid",
                    help="Effort aralığının hangi ucu kullanılsın (varsayılan: mid)")
    args = ap.parse_args()

    try:
        plan = load_plan(args.plan)
        result = analyse(plan, args.estimate)
    except (OSError, ValueError, KeyError) as exc:
        print(f"HATA: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        lookup = flatten_items(plan, args.estimate) if "errors" not in result else {}
        print(render(result, lookup))
    return 2 if "errors" in result else 0


if __name__ == "__main__":
    sys.exit(main())
