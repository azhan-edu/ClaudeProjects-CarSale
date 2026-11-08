#!/usr/bin/env python3
"""Cross Polo monitor: steps 1-5 (extract, merge into summary, classify, chart). Output: report.json"""
import re, json, glob, sys
from datetime import datetime, timedelta
from pathlib import Path
D = Path(__file__).resolve().parent
SUM = D/"cross-polo-summary.md"; PNG = D/"cross-polo-2weeks.png"
SRC = {"AUTO.RIA": "cross-polo_avto-riа-com.md", "OLX.ua": "cross-polo_olx-ua.md"}
used = {}
for s, n in SRC.items():
    if not (D/n).exists():
        c = sorted(glob.glob(str(D/"cross-polo_*.md")))
        c = [x for x in c if ("ria" in x.lower() or "ри" in x.lower()) == (s == "AUTO.RIA")]
        n = Path(c[0]).name
    used[s] = n
HDR = "| Дата и время (UTC) | Источник | Модель | Год | Госномер / ID | Л.с. | Объем двигателя | Пробег | Цена, $ | Город | Ссылка |"
def cells(l): return [c.strip() for c in l.strip().strip("|").split("|")]
def rows_of(path):
    out = []
    for l in path.read_text(encoding="utf-8").splitlines():
        if l.startswith("|") and re.match(r"\|\s*\d{4}-\d\d-\d\d", l): out.append(cells(l))
    return out
def price(r): return int(re.sub(r"\D", "", r[8]))
ts = lambda r: datetime.strptime(r[0], "%Y-%m-%d %H:%M")
# step 1
new = []
for s, n in used.items():
    rs = rows_of(D/n); rs = [[r[0], s]+r[1:] for r in rs]
    day = max(r[0][:10] for r in rs)
    latest = {}
    for r in sorted((r for r in rs if r[0][:10] == day), key=ts): latest[r[4]] = r  # last snapshot wins
    new += list(latest.values())
# step 3
head = SUM.read_text(encoding="utf-8").splitlines()
existing = rows_of(SUM)
have = {(r[4], r[0][:10]) for r in existing}
added = [r for r in new if (r[4], r[0][:10]) not in have]
# step 4
cls = []
for r in added:
    prev = [e for e in existing if e[4] == r[4] and ts(e) < ts(r)]
    if not prev: cls.append(("НОВОЕ", None))
    else:
        p = max(prev, key=ts)
        cls.append(("ЦЕНА", p[8]) if price(p) != price(r) else ("без изменений", None))
allrows = added + existing
allrows.sort(key=lambda r: (ts(r), r[1] == "AUTO.RIA"), reverse=True)
if added:
    title = next(l for l in head if l.startswith("# "))
    SUM.write_text(title+"\n\n"+HDR+"\n|---|---|---|---|---|---|---|---|---|---|---|\n"+"\n".join("| "+" | ".join(r)+" |" for r in allrows)+"\n", encoding="utf-8")
# step 5
chart = False
if added:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt, matplotlib.dates as md
    end = max(ts(r) for r in allrows); start = end - timedelta(days=14)
    cars = {}
    for r in allrows:
        if ts(r) >= start: cars.setdefault(r[4], []).append(r)
    fig, ax = plt.subplots(figsize=(14, 8), dpi=100, facecolor="white")
    cols = ["#2a78d6", "#eb6834", "#1baf7a", "#8e44ad"]; offs = [(0, 12), (0, -18), (0, 12), (0, -18)]
    for i, (k, rs) in enumerate(sorted(cars.items(), key=lambda kv: kv[0])):
        rs.sort(key=ts); x = [ts(r) for r in rs]; y = [price(r) for r in rs]; r0 = rs[-1]
        ax.plot(x, y, marker="o", ms=9, lw=2.2, color=cols[i % 4], label=f"{r0[9]}, {r0[3]}, {r0[1]}")
        for xi, yi in zip(x, y):
            ax.annotate(f"{yi:,}".replace(",", " "), (xi, yi), textcoords="offset points", xytext=offs[i % 4], ha="center", fontsize=11, color=cols[i % 4])
    ax.set_xlim(start, end + timedelta(days=0.7))
    ax.xaxis.set_major_locator(md.DayLocator(interval=1)); ax.xaxis.set_major_formatter(md.DateFormatter("%d.%m"))
    ax.set_xlabel("Дата", fontsize=13); ax.set_ylabel("Цена, $", fontsize=13)
    ax.set_title("Volkswagen Cross Polo — цены за 14 дней", fontsize=16)
    ax.tick_params(labelsize=11); ax.grid(alpha=.3); ax.legend(fontsize=12, loc="best")
    fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(PNG, facecolor="white"); chart = True
rep = {"sources": used, "added": [dict(row=r, cls=c[0], was=c[1]) for r, c in zip(added, cls)], "chart": chart}
(D/"report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(rep, ensure_ascii=False, indent=1))
