# Product Requirements Document (PRD)
## Platform Analisis & Dashboard Keamanan AI Bank Jatim
**Aplikasi Live:** [https://bankjatim.streamlit.app/](https://bankjatim.streamlit.app/)  
**Repositori:** [https://github.com/indri007/JATIM](https://github.com/indri007/JATIM)  
**Versi Dokumen:** 1.0.0  
**Status:** Approved / Active Development  
**Penulis:** Indri Anjar Kartika Sari  

---

## 1. Executive Summary & Visi Produk

### 1.1 Visi Produk
Membangun platform analitik interaktif berbasis web yang menggabungkan dua kapabilitas strategis Bank Jatim (PT Bank Pembangunan Daerah Jawa Timur Tbk - IDX: BJTM):
1. **Analisis Kinerja Keuangan & Rasio Profitabilitas (2021–2025)**: Evaluasi empiris performa ROA (*Return on Assets*) dan ROE (*Return on Equity*) Bank Jatim dibandingkan perbankan nasional.
2. **Showcase Riset Keamanan AI (BATAS - *Bounded Agent Trust and Authority Scoping*)**: Demonstrasi interaktif arsitektur Zero Trust dan mitigasi *Prompt Injection* pada Agen AI perbankan daerah sesuai standar regulasi OJK (POJK No. 11/POJK.03/2022 & PADK OJK No. 1/2026).

### 1.2 Target Audiens
- **Manajemen & Analis Keuangan**: Pemangku kepentingan yang membutuhkan ringkasan visual performa profitabilitas BJTM.
- **Auditor & Regulator (OJK / BI)**: Pengawas kepatuhan tata kelola AI dan ketahanan siber perbankan.
- **Perekayasa AI & Praktisi Keamanan Siber**: Peneliti dan developer sistem AI perbankan yang menguji ketahanan model terhadap manipulasi prompt.

---

## 2. Struktur Arsitektur Fitur (Product Feature Breakdown)

### Modul A: Financial Analytics & Benchmark Engine
* **F-01: Ringkasan Metrik Utama (Executive KPI Cards)**
  * Menampilkan metrik snapshot tahun berjalan (ROA, ROE, Pertumbuhan YoY, Posisi Desil Industri).
* **F-02: Tren Historis Multi-Tahun (2021–2025)**
  * Visualisasi time-series interaktif (Plotly) untuk performa ROA dan ROE tahunan Bank Jatim.
* **F-03: Peer Benchmarking (Komparasi Perbankan Nasional)**
  * Filter komparasi dengan bank BPD lain dan bank umum nasional berdasarkan data `ROA_INDONESIA_2021-2025.xlsx` & `ROE_INDONESIA_2021-2025.xlsx`.
  * Distribusi persentil dan kuadran efisiensi operasional.

### Modul B: Showcase BATAS (Zero Trust AI Security Testbed)
* **F-04: Simulasi Mitigasi Prompt Injection (Live Sandbox)**
  * Playground interaktif untuk menguji prompt injeksi (bahasa formal birokrasi, slang, urgensi palsu) terhadap Policy Enforcement Point (PEP).
* **F-05: Monitor State Invariant & Policy Verification**
  * Visualisasi verifikasi kebijakan OPA (*Open Policy Agent*) secara *real-time* (penolakan transfer ilegal rekening kasda, pembatasan limit retail, autentikasi ganda).
* **F-06: Matriks Evaluasi & Metrik Keamanan**
  * Visualisasi hasil eksperimen riset: *Attack Success Rate* (ASR), p50/p95 latency, dan *False Rejection Rate*.

### Modul C: Document & Compliance Center
* **F-07: Verifikasi Integritas Sumber Data (Data Transparency)**
  * Tabel audit digital yang memetakan file laporan tahunan (Annual Report) dan LFR (2020–2026) lengkap dengan *SHA-256 Checksum* terverifikasi.
* **F-08: Unduhan Laporan & Ekspor Data**
  * Fitur unduh dataset hasil filter (CSV/Excel) dan naskah riset akademis.

---

## 3. Struktur Navigasi & Wireframe Layout

Aplikasi dirancang dengan tata letak modern, bersih, dan responsif menggunakan Streamlit:

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏦 BANK JATIM FINANCIAL ANALYTICS & AI ZERO TRUST DASHBOARD           │
├─────────────────┬──────────────────────────────────────────────────────┤
│ 📂 NAVIGASI     │ 📊 AREA KONTEN UTAMA                                 │
│                 │                                                      │
│ 1. 📈 Ringkasan │ • KPI Snapshot (ROA, ROE, Peringkat Industri)        │
│    Eksekutif    │ • Grafik Tren Profitabilitas 2021-2025               │
│                 │ • Insight Otomatis Performa Bank Jatim               │
│ 2. 🔍 Analisis  ├──────────────────────────────────────────────────────┤
│    Komparasi    │ • Filter Bank Pembanding (Peer Group)                │
│                 │ • Grafik Scatter Distribusi ROA vs ROE               │
│ 3. 🛡️ Uji BATAS │ • Tabel Data Komparasi dengan fitur Search/Sort      │
│    Zero Trust   ├──────────────────────────────────────────────────────┤
│                 │ • Simulator Prompt Injection (Birokratis / Slang)    │
│ 4. 📑 Dokumen   │ • Hasil Evaluasi OPA Policy: ALLOW / DENY / HITL     │
│    & Kepatuhan  │ • Benchmark Metrik Latensi dan Keamanan              │
└─────────────────┴──────────────────────────────────────────────────────┘
```

---

## 4. Spesifikasi Teknis & Data Pipeline

| Komponen | Spesifikasi | Keterangan |
| :--- | :--- | :--- |
| **Frontend Framework** | Streamlit (Python) | Dioptimalkan untuk visualisasi data interaktif |
| **Data Engine** | Pandas + OpenPyXL | Memproses `ROA_INDONESIA_2021-2025.xlsx` & `ROE_INDONESIA_2021-2025.xlsx` |
| **Grafik & Visualisasi** | Plotly Express / Graph Objects | Grafik interaktif dengan tooltip, zoom, dan ekspor PNG |
| **Security Testbed** | Python / OPA Simulation | Implementasi lightweight PEP berbasis `BATAS/testbed/app.py` |
| **Hosting & CI/CD** | Streamlit Community Cloud | Tersambung langsung ke repo `indri007/JATIM` (Branch `main`) |
| **Domain** | `https://bankjatim.streamlit.app/` | Akses publik langsung tanpa login |

---

## 5. Kebutuhan Non-Fungsional (NFR)

1. **Performa & Responsivitas:**
   * Waktu *load* halaman awal < 2.5 detik menggunakan `@st.cache_data`.
   * Desain adaptif untuk layar desktop, tablet, dan smartphone.
2. **Keamanan & Tata Kelola:**
   * Bebas dari *hardcoded credentials*, API key rahasia, atau data pribadi nasabah (PII).
   * Hanya memproses data agregat publik perbankan (laporan keuangan publik OJK/BEI).
3. **Kepatuhan Regulasi:**
   * Selaras dengan panduan POJK No. 11/POJK.03/2022 tentang Penyelenggaraan Teknologi Informasi oleh Bank Umum.
   * Mengacu pada prinsip etika dan tata kelola *OJK Artificial Intelligence Governance Handbook*.

---

## 6. Rencana Implementasi & Roadmap

- **Fase 1 (MVP - Sedang Berjalan):**
  - [x] Struktur repositori dan verifikasi data Excel (ROA/ROE 2021–2025).
  - [x] Publikasi repositori dan integrasi landing page ke Streamlit Cloud.
  - [ ] Pembuatan berkas `streamlit_app.py` dan `requirements.txt`.
- **Fase 2 (Rilis Penuh):**
  - [ ] Implementasi interaktif visualisasi ROA & ROE Bank Jatim vs BPD lain.
  - [ ] Implementasi demo interaktif simulator BATAS Zero Trust.
- **Fase 3 (Enhancement):**
  - [ ] Integrasi automated benchmarking live test.
  - [ ] Fitur ekspor laporan riset otomatis dalam format PDF/Word.
