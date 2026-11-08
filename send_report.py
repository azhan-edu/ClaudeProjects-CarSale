#!/usr/bin/env python3
"""Send the CarSaleBot e-mail: latest-day table (green = new car, orange = price changed)
with cross-polo-2weeks.png attached. Usage: python send_report.py [--dry-run]
Needs SMTP_USER and SMTP_APP_PASSWORD (Google app password) in .env or the environment.
--dry-run writes out/preview.eml + out/preview.html and sends nothing."""
import os, re, sys, html, smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
D = Path(__file__).resolve().parent
TO, SUBJECT = "anatolii.zinhan.pl@gmail.com", "CarSaleBot"
GREEN, ORANGE = "#1e8e3e", "#e67e00"

def load_env():
    f = D/".env"
    if f.exists():
        for l in f.read_text().splitlines():
            if "=" in l and not l.lstrip().startswith("#"):
                k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"\''))

def cells(l): return [c.strip() for c in l.strip().strip("|").split("|")]
def rows(): return [cells(l) for l in (D/"cross-polo-summary.md").read_text(encoding="utf-8").splitlines()
                    if re.match(r"\|\s*\d{4}-\d\d-\d\d", l)]
ts = lambda r: datetime.strptime(r[0], "%Y-%m-%d %H:%M")
price = lambda r: int(re.sub(r"\D", "", r[8]))

def build():
    allr = rows(); day = max(r[0][:10] for r in allr)
    last = {}
    for r in sorted((r for r in allr if r[0][:10] == day), key=ts): last[r[4]] = r
    out = []
    for r in sorted(last.values(), key=lambda r: (ts(r), r[1] == "AUTO.RIA"), reverse=True):
        prev = [e for e in allr if e[4] == r[4] and e[0][:10] < day]
        if not prev: cls, was = "НОВОЕ", None
        else:
            p = max(prev, key=ts)
            cls, was = ("ЦЕНА", p[8]) if price(p) != price(r) else ("", None)
            if not cls: cls = "без изменений"
        out.append((r, cls, was))
    return day, out

def render(day, items):
    th = "".join(f"<th>{h}</th>" for h in ["Дата (UTC)","Источник","Модель","Год","Номер / ID","Л.с.","Объем","Пробег","Цена, $","Город","Ссылка"])
    body = ""
    for r, cls, was in items:
        col = GREEN if cls == "НОВОЕ" else ORANGE if cls == "ЦЕНА" else ""
        st = f' style="color:{col};font-weight:bold"' if col else ""
        c = [html.escape(x) for x in r]
        if was: c[8] = f"{c[8]} (было {html.escape(was)})"
        link = f'<a href="{html.escape(r[10])}"' + (f' style="color:{col}"' if col else "") + ">ссылка</a>"
        body += f"<tr{st}>" + "".join(f"<td>{x}</td>" for x in c[:10]) + f"<td>{link}</td></tr>"
    return (f'<div style="font-family:Arial,sans-serif;font-size:14px"><p><b>Последние объявления (за последний день), снимок {day}</b></p>'
            f'<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;font-size:13px"><tr style="background:#eee">{th}</tr>{body}</table>'
            f'<p style="font-size:12px;color:#555">Зелёный — новый автомобиль, оранжевый — изменилась цена. График цен за 2 недели — во вложении.</p></div>')

def main():
    load_env(); dry = "--dry-run" in sys.argv
    day, items = build(); page = render(day, items)
    msg = EmailMessage(); msg["Subject"] = SUBJECT; msg["To"] = TO
    msg["From"] = os.environ.get("SMTP_USER", "carsalebot@localhost")
    msg.set_content("Список объявлений и график — в HTML-версии письма. График во вложении.")
    msg.add_alternative(page, subtype="html")
    png = D/"cross-polo-2weeks.png"
    msg.add_attachment(png.read_bytes(), maintype="image", subtype="png", filename=png.name)
    if dry:
        (D/"out").mkdir(exist_ok=True)
        (D/"out"/"preview.eml").write_bytes(bytes(msg)); (D/"out"/"preview.html").write_text(page, encoding="utf-8")
        print("dry-run: out/preview.eml, out/preview.html;", len(items), "rows;", [c for _, c, _ in items]); return
    u, p = os.environ.get("SMTP_USER"), os.environ.get("SMTP_APP_PASSWORD")
    if not (u and p): sys.exit("Set SMTP_USER and SMTP_APP_PASSWORD in .env")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s: s.login(u, p); s.send_message(msg)
    print("sent to", TO, "with", png.name)
main()
