# JATIM — BATAS: Zero Trust AI Agent untuk Perbankan

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![OPA](https://img.shields.io/badge/policy-OPA%2FRego-7d9199)](https://www.openpolicyagent.org/)
[![Status](https://img.shields.io/badge/status-research%20preview-orange)]()
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bankjatim.streamlit.app/)

**BATAS** (*Behavioral Authority Threshold for Agentic Systems / Bounded Agent Trust and Authority Scoping*) adalah paket replikasi penelitian dan platform pengujian untuk membatasi **otoritas** agen AI di sektor perbankan menggunakan pendekatan **Zero Trust**, bukan sekadar mendeteksi niat jahat.

**Live Interactive Demo:** [https://bankjatim.streamlit.app/](https://bankjatim.streamlit.app/)  
**Repositori Resmi:** [https://github.com/indri007/JATIM](https://github.com/indri007/JATIM)  
**Penulis:** Indri Anjar Kartika Sari  
**Afiliasi:** IDS Digital College (STMIK Indo Daya Suvana) · UPN "Veteran" Jawa Timur · Purwadhika Digital Technology School

---

## 🎯 Fokus & Ruang Lingkup
- **Studi Kasus Empiris**: **Bank Jatim** (PT Bank Pembangunan Daerah Jawa Timur Tbk - IDX: `BJTM`)
- **Kepatuhan Regulasi Nasional**:
  - **PADK OJK No. 1/PADK.03/2026** (Pengawasan Ketahanan Agen AI Otonom Perbankan)
  - **POJK No. 11/POJK.03/2022** & **SEOJK No. 29/2022** (Penyelenggaraan TI & Ketahanan Siber Bank Umum)
  - **POJK No. 21/2023** (Layanan Digital oleh Bank Umum)
  - **UU No. 27/2022** (Perlindungan Data Pribadi / UU PDP)
  - **Panduan Tata Kelola AI Perbankan OJK 2025**
- **Metrik Evaluasi Utama**:
  - **Attack Success Rate (ASR)**: Mengukur keberhasilan penetralan prompt injection (Mencapai **0.00%** pada BATAS)
  - **Wilson 95% Confidence Interval**: Rentang akurasi statistik batas atas dan batas bawah
  - **Overhead Latensi (p50 / p95)**: Efisiensi waktu komputasi aturan deterministik (< 100 ms)

---

## 📂 Struktur Repositori

```text
├── BATAS/                                # Paket Inti Riset, Testbed, & Policy Engine
│   ├── policies/                         # Aturan Otorisasi OPA (Open Policy Agent)
│   │   ├── authorization.rego            # Kebijakan Zero Trust Rego (Proteksi Kasda, Limit Retail)
│   │   └── authorization_test.rego       # Unit test kebijakan Rego (100% PASS)
│   ├── testbed/                          # Simulator API Core Banking & Mock BI-FAST
│   │   ├── app.py                        # Policy Enforcement Point (PEP) Engine
│   │   ├── mock_banking_api.py           # Core Banking Gateway Simulator
│   │   └── state_store.py                # Buku besar thread-safe & invarian saldo
│   ├── dataset/                          # 200 Kasus Uji Skenario Injeksi & Normal
│   │   ├── attack_dev.jsonl              # Skenario serangan (Birokratis, Slang, Urgensi)
│   │   └── benign_dev.jsonl              # Skenario tugas perbankan sah
│   ├── benchmarks/                       # Harness benchmark & pengukuran latensi
│   ├── tests/                            # Pytest automated test suites (100% PASS)
│   └── setup_batas.sh                    # Skrip otomasi lingkungan riset
│
├── dashboards/                           # Stack Observabilitas SOC & Monitoring Produksi
│   ├── docker-compose.yml                # Orkestrasi 1-klik (Prometheus, Loki, Promtail, Grafana, Streamlit)
│   ├── .env                              # Variabel kredensial Grafana & port
│   ├── grafana/
│   │   └── dashboards/                   # Model JSON Dashboard Produksi
│   │       ├── executive_compliance.json # Dashboard 1: Executive & Compliance (OJK, ASR, Invariants)
│   │       └── soc_ai_agent.json         # Dashboard 2: SOC AI Agent (Allow/Deny, Live Loki Logs)
│   ├── prometheus/prometheus.yml         # Konfigurasi scrape metrik PromQL
│   ├── loki/loki-config.yml              # Konfigurasi log aggregation TSDB
│   ├── promtail/promtail-config.yml      # Konfigurasi log shipping OPA & Agen
│   ├── exporter/                         # Prometheus custom exporter untuk metrik BATAS
│   └── streamlit/                        # Dashboard benchmark Streamlit mandiri
│
├── streamlit_app.py                      # Aplikasi Master Portal Interaktif Bank Jatim
├── requirements.txt                      # Dependensi Python utama aplikasi web
│
├── ROA_INDONESIA_2021-2025.xlsx          # Dataset Multi-Tahun ROA 976 Emiten Indonesia
├── ROE_INDONESIA_2021-2025.xlsx          # Dataset Multi-Tahun ROE 976 Emiten Indonesia
├── SUMBER.csv                            # Katalog Dokumen Resmi Bank Jatim & SHA-256 Checksums
│
├── PRD.md                                # Product Requirements Document
├── ERD.md                                # Entity Relationship Diagram Architecture
├── SCHEMA.md                             # SQL DDL & API JSON Schema Specifications
├── rules.md                              # Aturan Kebijakan Keamanan & Tata Kelola
└── design_ui_ux.md                       # Spesifikasi Desain Antarmuka UI/UX
```

---

## 🚀 Cara Menjalankan Aplikasi & Pengujian

### 1. Menjalankan Dashboard Master Streamlit (Lokal)
```bash
# Pasang dependensi
pip install -r requirements.txt

# Jalankan portal interaktif
streamlit run streamlit_app.py
```
Akses di browser: `http://localhost:8501`

### 2. Menjalankan Stack Observabilitas Docker (Grafana + Loki + Prometheus)
```bash
cd dashboards
docker compose up -d
```
* **Grafana Dashboard**: `http://localhost:3000` (User: `admin`, Pass: `batas2026`)
  * Dashboard 1: *BATAS — Executive & Compliance*
  * Dashboard 2: *BATAS — SOC AI Agent*
* **Prometheus Metrics**: `http://localhost:9090`
* **Streamlit Benchmark**: `http://localhost:8501`
* **BATAS Exporter**: `http://localhost:8000/metrics`

### 3. Menjalankan Pengujian Kebijakan & Invarian Saldo
```bash
cd BATAS

# Uji Kebijakan OPA Rego
opa test policies/ -v

# Uji Unit Test Python (State Invariants & Prompt Injection)
python3 -m pytest tests/ -v
```

---

## 📊 Hasil Kinerja Finansial & Keamanan Utama

### 1. Kinerja Finansial Bank Jatim (IDX: BJTM 2021–2025)
* **ROA Rata-Rata 5 Tahun**: **`1.78%`** (Kategori Sehat OJK/BI $> 1.22\%$)
* **ROE Rata-Rata 5 Tahun**: **`15.32%`** (Peringkat **Top 21%** dari 106 Emiten Finansial Nasional)
* **Keunggulan vs Peer BPD**: Mengungguli Bank BJB (BJBR) di tahun 2024 pada rasio ROA (1.52% vs 0.87%) dan ROE (12.58% vs 10.17%).

### 2. Ketahanan Keamanan AI BATAS
* **Attack Success Rate (ASR)**: **`0.00%`** (vs Baseline Vanilla LLM: `72.5%`, Input Filter: `26.0%`)
* **Overhead Latensi**: Rata-rata **`78.43 ms`** (31% lebih cepat dibanding verifikasi klasifikasi LLM semantik).
* **Konservasi Invarian Dana**: $\sum \Delta \text{Balance} = 0$ (Zero fund leakage pada seluruh percobaan).

---

## 📜 Lisensi & Kepatuhan
* Kode program berlisensi **MIT License**.
* Dataset riset berlisensi **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
* Seluruh data akun buku besar pada simulasi bersifat sintetis untuk mematuhi **UU No. 27/2022 (UU Perlindungan Data Pribadi)**.
