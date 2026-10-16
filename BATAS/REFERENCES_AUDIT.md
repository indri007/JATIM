# Checklist Kebutuhan Rigor Ilmiah & Bibliografi BATAS (Scopus Target)

Dokumen ini melacak kesiapan lingkungan eksekusi eksperimen, status dependensi, serta kelengkapan sitasi IEEE untuk naskah:
**"Bounding Authority, Not Detecting Intent: A Zero Trust Architecture for Agentic AI in an Indonesian Regional Development Bank (the Bank Jatim Case)"**

---

## Bagian A: Status Lingkungan & Perkakas (macOS)

| Komponen | Kegunaan | Status di Sistem | Tindakan Berikutnya |
| :--- | :--- | :--- | :--- |
| **Python 3.11+** | Runtime utama testbed | ✅ Terpasang (`python3.13` & `python3.11`) | Siap digunakan di venv |
| **OPA (Open Policy Agent)** | Gateway PEP/PDP (C3) | ✅ Terpasang (`opa 1.21.2`) | Tes Rego lulus 3/3 |
| **Ollama** | Runtime model open-weight | ✅ Terpasang (`/opt/homebrew/bin/ollama`) | Perlu pull model: `ollama pull qwen2.5:7b` |
| **R Language** | Engine model efek campuran | ✅ Terpasang (`R version 4.5.2`) | Pasang paket: `install.packages("lme4")` |
| **Python Statistical Stack** | Wilson CI & Holm correction | ⚠️ Parsial (scipy/numpy terpasang) | Pasang: `pip install statsmodels pandas pyrit` |
| **Docker Desktop** | Kontainerisasi replikasi | ⏳ Opsional untuk rilis Zenodo | Menyiapkan `Dockerfile` & `docker-compose.yml` |

---

## Bagian B: Daftar Referensi Baru ([33] – [41]) Format IEEE

```text
[33] Qwen Team, "Qwen2.5 technical report," arXiv:2412.15115, 2024. [Online]. Available: https://arxiv.org/abs/2412.15115v1
[34] G. D. Lopez Munoz et al., "PyRIT: A framework for security risk identification and red teaming in generative AI systems," arXiv:2410.02828, 2024. [Online]. Available: https://arxiv.org/abs/2410.02828v1
[35] L. Derczynski et al., "garak: A framework for security probing large language models," arXiv:2406.11036, 2024. [Online]. Available: https://arxiv.org/abs/2406.11036v1
[36] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," J. Amer. Statist. Assoc., vol. 22, no. 158, pp. 209–212, 1927.
[37] S. Holm, "A simple sequentially rejective multiple test procedure," Scand. J. Statist., vol. 6, no. 2, pp. 65–70, 1979.
[38] D. Bates, M. Mächler, B. Bolker, and S. Walker, "Fitting linear mixed-effects models using lme4," J. Stat. Softw., vol. 67, no. 1, pp. 1–48, 2015.
[39] S. Seabold and J. Perktold, "Statsmodels: Econometric and statistical modeling with Python," in Proc. 9th Python in Science Conf., 2010.
[40] Open Policy Agent (OPA), version 1.21.2, Cloud Native Computing Foundation (CNCF), 2026. [Online]. Available: https://www.openpolicyagent.org/
[41] OpenAI / Anthropic / Google, API Documentation and Model Specifications (e.g., GPT-4o-mini / Claude 3.5 Sonnet / Gemini 1.5 Pro), Accessed: Oct. 2026.
```

---

## Bagian C: Audit & Verifikasi Referensi Lama

1. **[11] & [16] Beritajatim**:
   - Perlu dibuka tautan aslinya untuk menyalin judul artikel kata-demi-kata (verbatim) beserta tanggal publikasi.
2. **[8]–[19] Sumber Berita vs Sumber Primer**:
   - Sesuai rekomendasi, rujukan berita umum tentang Bank Jatim digantikan dengan **Laporan Tahunan Bank Jatim 2024/2025** dan keterbukaan informasi di **Bursa Efek Indonesia (IDX: BJTM)** agar lebih kredibel di mata reviewer Scopus.
3. **[30] Mahadevaswamy**:
   - Memverifikasi DOI `10.69554/MIWG3713` serta melengkapi nomor edisi (issue) dan halaman di situs jurnal Henry Stewart Publications (*Journal of AI, Robotics & Workplace Automation* / sejenis).
4. **Data RKUD Bank Jatim**:
   - Jumlah Rekening Kas Umum Daerah (RKUD) yang dikelola Bank Jatim disitasi langsung dari Bab Tata Kelola Keuangan Daerah di Laporan Tahunan 2025 resmi.
5. **Tabel 6 (Regulatory Compliance Mapping)**:
   - Pasal spesifik PADK OJK No. 1/PADK.03/2026 (terkait agen otonom & pengujian ketahanan siber).
   - SEOJK No. 29/SEOJK.03/2022 (Ketahanan Siber Bank Umum).
   - Bab panduan etika & tata kelola AI OJK (Prinsip Transparansi, Akuntabilitas, dan Keandalan).
