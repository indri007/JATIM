#!/usr/bin/env python3
"""
Pengumpul berita & konten media sosial tentang Bank Jatim (5 tahun terakhir).

Sumber:
  1. Google News RSS  — media massa dalam negeri (hl=id) dan luar negeri (en-US, en-SG, en-GB, ms-MY, en-AU),
     dipecah per bulan agar tiap jendela waktu tidak terpotong batas 100 item.
  2. YouTube (yt-dlp)  — video berita/konten media sosial, dengan tanggal unggah & kanal.

Keluaran: berita_bankjatim.xlsx + berita_bankjatim.csv dengan kolom
  No | Tanggal Terbit | Judul | Media/Sumber | Domain | Asal Sumber (Dalam/Luar Negeri) |
  Jenis (Media Massa/Media Sosial) | Bahasa | Link | Link Google News | Kata Kunci

Pakai:
  pip install requests pandas openpyxl yt-dlp
  python kumpul_berita_bankjatim.py --target 1000
  python kumpul_berita_bankjatim.py --target 1000 --resolve     # ubah link Google News -> URL asli (lebih lama)
"""
from __future__ import annotations

import argparse
import base64
import csv
import email.utils
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from urllib.parse import quote_plus, urlparse

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

QUERIES_ID = ['"Bank Jatim"', '"BJTM" bank', '"Bank Pembangunan Daerah Jawa Timur"']
QUERIES_INTL = ['"Bank Jatim"', '"Bank Pembangunan Daerah Jawa Timur"', 'BJTM Indonesia bank']
EDITIONS_INTL = [("en-US", "US", "US:en"), ("en-SG", "SG", "SG:en"), ("en-GB", "GB", "GB:en"),
                 ("ms-MY", "MY", "MY:ms"), ("en-AU", "AU", "AU:en")]

# Domain luar negeri yang sering muncul di edisi ID (dan sebaliknya) — dipakai untuk klasifikasi asal
FOREIGN_HINT = ("reuters.com", "bloomberg.com", "theedgemalaysia.com", "straitstimes.com", "nikkei.com",
                "asia.nikkei.com", "ft.com", "wsj.com", "fitchratings.com", "moodys.com", "spglobal.com",
                "marketscreener.com", "businesstimes.com.sg", "scmp.com", "dealstreetasia.com", "theaseanpost.com",
                "globalbankingandfinance.com", "zawya.com", "investing.com", "yahoo.com", "msn.com",
                "thebanker.com", "euromoney.com", "asiamoney.com", "finews.asia", "bnm.gov.my", "bernama.com",
                "malaymail.com", "thestar.com.my", "nst.com.my", "abc.net.au", "bbc.com", "aljazeera.com",
                "voanews.com", "cnbc.com", "forbes.com", "fintechnews.sg", "techinasia.com", "theinvestor.vn")
SOCIAL_DOMAINS = ("youtube.com", "youtu.be", "tiktok.com", "instagram.com", "facebook.com", "x.com",
                  "twitter.com", "linkedin.com", "kompasiana.com", "medium.com", "threads.net")


def month_windows(years: int):
    end = date.today()
    start = date(end.year - years, end.month, 1)
    cur = start
    while cur <= end:
        nxt = date(cur.year + (cur.month // 12), cur.month % 12 + 1, 1)
        yield cur, min(nxt, end + timedelta(days=1))
        cur = nxt


def fetch_rss(q: str, after: date, before: date, hl: str, gl: str, ceid: str):
    query = f"{q} after:{after.isoformat()} before:{before.isoformat()}"
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl={hl}&gl={gl}&ceid={ceid}"
    for attempt in range(4):
        try:
            r = requests.get(url, headers=UA, timeout=30)
            if r.status_code == 429:
                time.sleep(20 * (attempt + 1))
                continue
            r.raise_for_status()
            root = ET.fromstring(r.content)
            out = []
            for it in root.iter("item"):
                src = it.find("source")
                title = (it.findtext("title") or "").strip()
                srcname = (src.text or "").strip() if src is not None else ""
                if srcname and title.endswith(" - " + srcname):
                    title = title[: -len(" - " + srcname)]
                pd = it.findtext("pubDate")
                dt = email.utils.parsedate_to_datetime(pd).astimezone(timezone(timedelta(hours=7))) if pd else None
                out.append({"judul": title, "media": srcname,
                            "domain": urlparse(src.get("url", "")).netloc.replace("www.", "") if src is not None else "",
                            "tanggal": dt.strftime("%Y-%m-%d %H:%M") if dt else "", "gn_link": it.findtext("link") or "",
                            "bahasa": hl, "query": q})
            return out
        except Exception as e:                               # jaringan/format
            if attempt == 3:
                print(f"  ! gagal {q} {after}: {e}", file=sys.stderr)
            time.sleep(5)
    return []


def decode_gn(link: str) -> str:
    """Ubah link news.google.com/rss/articles/... menjadi URL asli (best effort)."""
    try:
        m = re.search(r"/articles/([^?]+)", link)
        if not m:
            return ""
        token = m.group(1)
        # format lama: base64 berisi URL langsung
        raw = base64.urlsafe_b64decode(token + "=" * (-len(token) % 4))
        hit = re.search(rb"https?://[^\x00-\x20\"<>]+", raw)
        if hit and b"news.google" not in hit.group(0):
            return hit.group(0).decode("utf-8", "ignore").rstrip("\xd2\x01")
        # format baru: minta signature lalu batchexecute
        page = requests.get(f"https://news.google.com/articles/{token}", headers=UA, timeout=20).text
        sig = re.search(r'data-n-a-sg="([^"]+)"', page)
        ts = re.search(r'data-n-a-ts="([^"]+)"', page)
        if not (sig and ts):
            return ""
        payload = [[["Fbv4je", json.dumps(["garturlreq", [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1,
                                                          None, None, None, None, None, 0, 1], "X", "X", 1, [1, 1, 1],
                                                         1, 1, None, 0, 0, None, 0], token, int(ts.group(1)), sig.group(1)])]]]
        r = requests.post("https://news.google.com/_/DotsSplashUi/data/batchexecute",
                          data={"f.req": json.dumps(payload)}, headers={**UA, "Content-Type":
                          "application/x-www-form-urlencoded;charset=UTF-8"}, timeout=20)
        u = re.search(r'\[\\"garturlres\\",\\"(https?://[^\\"]+)', r.text)
        return u.group(1) if u else ""
    except Exception:
        return ""


def youtube(n: int):
    try:
        out = subprocess.run(["yt-dlp", f"ytsearchdate{n}:Bank Jatim", "--flat-playlist", "-J", "--no-warnings"],
                             capture_output=True, text=True, timeout=600)
        data = json.loads(out.stdout or "{}")
    except Exception as e:
        print(f"  ! yt-dlp tidak tersedia/gagal: {e}", file=sys.stderr)
        return []
    rows = []
    for e in data.get("entries", []):
        vid = e.get("id")
        rows.append({"judul": e.get("title", ""), "media": f"YouTube — {e.get('channel') or e.get('uploader') or ''}",
                     "domain": "youtube.com", "tanggal": "", "gn_link": "", "link": f"https://www.youtube.com/watch?v={vid}",
                     "bahasa": "", "query": "YouTube: Bank Jatim", "_vid": vid})
    # tanggal unggah butuh metadata per video
    for r in rows:
        try:
            meta = subprocess.run(["yt-dlp", "-j", "--skip-download", "--no-warnings", r["link"]],
                                  capture_output=True, text=True, timeout=60)
            m = json.loads(meta.stdout)
            d = m.get("upload_date")
            r["tanggal"] = f"{d[:4]}-{d[4:6]}-{d[6:]}" if d else ""
        except Exception:
            pass
    return rows


def classify(row, edition_foreign: bool):
    dom = row["domain"].lower()
    social = any(dom.endswith(s) for s in SOCIAL_DOMAINS)
    foreign = (edition_foreign and not dom.endswith(".id") and not dom.endswith(".co.id")) or any(
        dom.endswith(f) for f in FOREIGN_HINT)
    row["asal"] = "Luar Negeri" if foreign else "Dalam Negeri"
    row["jenis"] = "Media Sosial" if social else "Media Massa"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=1000)
    ap.add_argument("--years", type=int, default=5)
    ap.add_argument("--youtube", type=int, default=150, help="jumlah video YouTube terbaru (0 = lewati)")
    ap.add_argument("--resolve", action="store_true", help="ubah link Google News menjadi URL asli")
    ap.add_argument("--out", default="berita_bankjatim")
    a = ap.parse_args()

    seen, rows = set(), []

    def add(items, foreign):
        for r in items:
            key = (re.sub(r"\W+", " ", r["judul"].lower()).strip(), r["domain"])
            if not r["judul"] or key in seen:
                continue
            seen.add(key)
            rows.append(classify(r, foreign))

    wins = list(month_windows(a.years))
    print(f"[1/3] Google News edisi Indonesia: {len(wins)} bulan × {len(QUERIES_ID)} kata kunci")
    for i, (s, e) in enumerate(wins, 1):
        for q in QUERIES_ID:
            add(fetch_rss(q, s, e, "id", "ID", "ID:id"), False)
            time.sleep(1.2)
        print(f"  {s:%Y-%m}: total {len(rows)}")
    print("[2/3] Google News edisi luar negeri (per kuartal)")
    for s, e in [(wins[i][0], wins[min(i + 2, len(wins) - 1)][1]) for i in range(0, len(wins), 3)]:
        for hl, gl, ceid in EDITIONS_INTL:
            for q in QUERIES_INTL:
                add(fetch_rss(q, s, e, hl, gl, ceid), True)
                time.sleep(1.2)
        print(f"  {s:%Y-%m}: total {len(rows)}")
    if a.youtube:
        print("[3/3] YouTube")
        add(youtube(a.youtube), False)

    rows.sort(key=lambda r: r["tanggal"], reverse=True)
    if a.resolve:
        print(f"Resolusi URL asli untuk {len(rows)} item ...")
        for i, r in enumerate(rows, 1):
            if not r.get("link"):
                r["link"] = decode_gn(r["gn_link"]) or ""
                time.sleep(0.6)
            if i % 50 == 0:
                print(f"  {i}/{len(rows)}")
    for r in rows:
        r.setdefault("link", "")
        if not r["link"]:
            r["link"] = r["gn_link"]

    cols = [("tanggal", "Tanggal Terbit (WIB)"), ("judul", "Judul"), ("media", "Media/Sumber"), ("domain", "Domain"),
            ("asal", "Asal Sumber"), ("jenis", "Jenis"), ("bahasa", "Edisi/Bahasa"), ("link", "Link"),
            ("gn_link", "Link Google News"), ("query", "Kata Kunci")]
    with open(a.out + ".csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["No"] + [c[1] for c in cols])
        for i, r in enumerate(rows, 1):
            w.writerow([i] + [r.get(k, "") for k, _ in cols])
    try:
        import pandas as pd
        df = pd.read_csv(a.out + ".csv")
        with pd.ExcelWriter(a.out + ".xlsx", engine="openpyxl") as xw:
            df.to_excel(xw, index=False, sheet_name="Berita")
            pd.crosstab(df["Tanggal Terbit (WIB)"].str[:4], df["Asal Sumber"]).to_excel(xw, sheet_name="Rekap per Tahun")
            df["Media/Sumber"].value_counts().rename("Jumlah").to_frame().to_excel(xw, sheet_name="Rekap per Media")
    except ImportError:
        pass
    print(f"\nSELESAI: {len(rows)} item unik -> {a.out}.csv / .xlsx "
          f"(dalam negeri {sum(r['asal']=='Dalam Negeri' for r in rows)}, luar negeri {sum(r['asal']=='Luar Negeri' for r in rows)}, "
          f"media sosial {sum(r['jenis']=='Media Sosial' for r in rows)})")
    if len(rows) < a.target:
        print(f"Catatan: baru {len(rows)} < target {a.target}. Tambah --years atau kata kunci di QUERIES_ID.")


if __name__ == "__main__":
    main()
