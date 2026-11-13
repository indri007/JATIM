# 🛡️ Panduan Observabilitas & Digital Forensik BATAS (Grafana Stack)
## Bank Jatim — Zero Trust Agentic AI Observability & Compliance Architecture

Dokumentasi resmi arsitektur observabilitas, pemantauan kepatuhan regulasi (**POJK No. 11/POJK.03/2022** & **PADK OJK No. 1/2026**), dan investigasi forensik digital untuk sistem perbankan terintegrasi BATAS.

---

### 1. Arsitektur Komponen Sistem

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       BATAS OBSERVABILITY ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────────────┘
  [ Agentic AI / LLM ]
           │
           ▼ (Intersepsi Kebijakan)
  [ OPA Policy Engine ] ──> /var/log/batas/*.log ──> [ Promtail ]
           │                                                │
           ▼ (Metrik Evaluasi)                              ▼ (Streaming Log)
  [ BATAS Exporter ]                                 [ Grafana Loki ]
       (Port 8000)                                     (Port 3100)
           │                                                │
           ▼ (Scraping Time-Series)                         │
    [ Prometheus ]                                          │
      (Port 9090)                                           │
           │                                                │
           └──────────────────┐   ┌─────────────────────────┘
                              ▼   ▼
                      [ Grafana UI (Port 3000) ]
                              ▲
                              │ (Status Regulasi OJK)
                      [ PostgreSQL (Port 5432) ]
```

---

### 2. Katalog Servis & Port Jaringan

| Layanan | Kontainer | Port Host | Fungsi Utama | Kredensial Default |
| :--- | :--- | :---: | :--- | :--- |
| **Grafana** | `batas-grafana` | **`3000`** | Visualisasi dashboard kepatuhan eksekutif & tim SOC forensik | `admin` / `batas2026` |
| **Prometheus** | `batas-prometheus` | **`9090`** | Time-series database pengumpul telemetri ASR & OPA decisions | *-* |
| **Loki** | `batas-loki` | **`3100`** | Penyimpanan log audit forensik anti-manipulasi (*immutable*) | *-* |
| **Promtail** | `batas-promtail` | *Internal* | Kolektor penarik berkas log dari host `/logs` ke Loki | *-* |
| **PostgreSQL** | `batas-postgres` | **`5432`** | Database relasional matriks kontrol kepatuhan POJK & PADK OJK | `batas_user` / `batas_password` (`batas_db`) |
| **BATAS Exporter** | `batas-exporter` | **`8000`** | Mesin kalkulasi metrik evaluasi benchmark & telemetry | *-* |
| **Streamlit** | `batas-streamlit` | **`8501`** | UI interaktif evaluasi benchmark & simulator Zero Trust | *-* |

---

### 3. Dua Dashboard Siap Pakai (*Auto-Provisioned*)

Kedua dashboard berikut otomatis terpasang tanpa perlu proses import manual:

#### A. Dashboard 1: Executive & Compliance — BATAS (Bank Jatim)
* **Target Pengguna**: Dewan Direksi, Komite Manajemen Risiko, dan Auditor OJK.
* **Panel Utama**:
  1. **Attack Success Rate (ASR)**: Target wajib `0.0%` (tervalidasi dengan *Wilson 95% Score Confidence Interval*).
  2. **Invariant Violations**: Pelanggaran integritas saldo dan rekening Kas Daerah (`REK-KASDA`) yang **wajib bernilai 0**.
  3. **Policy Deny Ratio (5m Rate)**: Rasio persentase aksi agen yang ditolak oleh gerbang OPA.
  4. **Compliance Controls Status Matrix**: Status kepatuhan kontrol `POJK-11-01` s/d `PADK-01-04` yang dibaca secara langsung (*live*) dari PostgreSQL.
  5. **Daily Incident Time Series Trend**: Grafik sebaran insiden serangan per hari.

#### B. Dashboard 2: SOC AI Agent — BATAS (Bank Jatim)
* **Target Pengguna**: Tim Keamanan Siber (*Blue Team*), SOC Analyst, dan Penyidik Forensik Digital.
* **Panel Utama**:
  1. **OPA Decision Rates**: Distribusi real-time keputusan `allow`, `deny`, dan `requires_hitl`.
  2. **Prompt Injection Ingress & Neutralization**: Membandingkan serangan injeksi yang masuk vs yang berhasil ditangkal deterministik.
  3. **Token Violations**: Pelanggaran token kedaluwarsa (*Anti-Replay*) dan ketidakcocokan scope (*Least Privilege*).
  4. **Top 5 Deny Reasons & Risky Actions**: Analisis akar penyebab penolakan paling sering terjadi.
  5. **Live Loki Security Logs**: Penampil log streaming interaktif untuk audit forensik mendalam.

---

### 4. Kueri LogQL untuk Investigasi Digital Forensik

Penyidik forensik dapat menggunakan kueri berikut di panel **Explore** Grafana (`http://localhost:3000/explore`):

```logql
# 1. Menelusuri seluruh penolakan transaksi oleh OPA
{job="batas-opa"} |= "DENY" | json

# 2. Investigasi percobaan akses ilegal ke rekening Kas Daerah (PADK OJK 1/2026)
{job="batas-opa"} |= "REK-KASDA" |= "DENY"

# 3. Investigasi upaya serangan Prompt Injection pada model LLM
{job="batas-agent"} |= "PROMPT_INJECTION_DETECTED" | json

# 4. Audit insiden pelanggaran masa berlaku token (Anti-Replay Rule)
{job="batas-opa"} |= "token_expired"
```

---

### 5. Panduan Operasional

#### A. Menyalakan Sistem
Pastikan aplikasi **Docker Desktop** telah dibuka dan berjalan di komputer Anda, lalu jalankan:
```bash
cd /Users/jevin/Downloads/jatim/dashboards
docker compose up -d
```

#### B. Memeriksa Status Kontainer
```bash
docker compose ps
```
Pastikan seluruh 7 kontainer berstatus `Up` / `running`.

#### C. Memantau Log Sistem
```bash
# Pantau log seluruh kontainer
docker compose logs -f

# Pantau log Grafana saja
docker compose logs -f grafana
```

#### D. Mematikan Sistem
```bash
# Hentikan tanpa menghapus data
docker compose stop

# Hentikan dan bersihkan kontainer (volume data tetap aman)
docker compose down
```

---

### 6. Pemecahan Masalah (*Troubleshooting*)

* **Masalah**: `Connection refused` pada port 3000.  
  * **Solusi**: Buka aplikasi Docker Desktop di Mac Anda terlebih dahulu (`open -a Docker`), tunggu indikator Docker menyala hijau, lalu ulangi `docker compose up -d`.
* **Masalah**: Dashboard Grafana kosong atau data tidak muncul.  
  * **Solusi**: Pastikan kontainer `batas-exporter` dan `batas-prometheus` aktif. Jalankan skenario uji di Streamlit (`http://localhost:8501`) untuk men-generate data telemetri baru ke berkas `/logs`.
