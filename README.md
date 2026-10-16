# BATAS: Bounded Agent Trust and Authority Scoping
## Zero Trust Architecture for Agentic AI in an Indonesian Regional Development Bank (Bank Jatim Case)

**Author:** Indri Anjar Kartika Sari  
**Affiliations:** IDS Digital College / UPN "Veteran" Jawa Timur / Purwadhika JCAI  
**Repository:** [https://github.com/indri007/JATIM](https://github.com/indri007/JATIM)  

---

### Overview
This repository contains the official replication package, synthetic testbed, OPA authorization policies, evaluation datasets, and academic manuscripts for the research paper:
> **"Bounding Authority Rather Than Detecting Intent: A Zero Trust Architecture for Agentic AI in an Indonesian Regional Development Bank (The Bank Jatim Case)"**

### Key Components

1. **`BATAS/` — Core Research Artifact & Synthetic Testbed:**
   - `policies/authorization.rego`: Deterministic Open Policy Agent (OPA) policy rules enforcing least-agency boundaries and dual human control on public treasury (RKUD/SP2D).
   - `testbed/`: FastAPI mock core-banking API, BI-FAST transaction simulator, and state invariant store.
   - `dataset/`: 200 standardized evaluation cases (120 attack scenarios across Indonesian bureaucratic, urgency, and slang framings + 80 benign tasks).
   - `tests/`: Automated pytest suites validating invariant state conservation, token expiry, and prompt injection neutralization.
   - `benchmarks/`: Benchmark harness measuring Attack Success Rate (ASR), p50/p95 latency overhead, false rejection rates, and Wilson 95% confidence intervals.
   - `setup_batas.sh`: Automated turnkey shell script for setting up environments and executing benchmarks.

2. **`BATAS/BATAS_MANUSCRIPT.md` & `ORIGIN_Research_Report (11).md`:**
   - Full-length academic manuscript and ORIGIN verification report.

3. **`SUMBER.csv`:**
   - Verifiable SHA-256 checksums, official URLs, and file metadata for Bank Jatim (IDX: BJTM) Annual Reports (2020–2025) and Financial Reports (LFR 2023–2026).

---

### Quick Start: Running the Testbed

#### 1. Prerequisites
- macOS / Linux
- Python 3.11+
- Open Policy Agent (`opa`)

#### 2. Execute Policy Unit Tests
```bash
cd BATAS
opa test policies/ -v
```

#### 3. Run Benchmark Suite
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt # or pip install pytest scipy statsmodels requests
python -m pytest tests/ -v
python benchmarks/run_experiments.py
python benchmarks/analyze_results.py
```

---

### License & Compliance
This software testbed and dataset are provided for academic research and regulatory compliance evaluation under the MIT License. Mapped directly against PADK OJK No. 1/2026, POJK No. 11/POJK.03/2022, and the OJK AI Governance Handbook.
