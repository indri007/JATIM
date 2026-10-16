# BATAS: Bounded Agent Trust and Authority Scoping
> **Replication Package & Empirical Artifacts for Research Paper:**  
> *"Bounding Authority, Not Detecting Intent: A Zero Trust Architecture for Agentic AI in an Indonesian Regional Development Bank (the Bank Jatim Case)"*  
> Target: *Telematika: Jurnal Informatika dan Teknologi Informasi* (UPN "Veteran" Yogyakarta)

---

## 1. Directory Structure

```text
BATAS/
├── README.md                          <- Project overview, quickstart, and reproducibility instructions
├── pyproject.toml                     <- Python package metadata and dependencies
├── config/
│   └── policy.yaml                    <- Thresholds and regulatory mapping (POJK 11 / PADK OJK 1/2026)
├── policies/
│   ├── authorization.rego             <- OPA Zero Trust policy definitions (NIST SP 800-207)
│   └── authorization_test.rego        <- Unit tests for Rego authorization rules
├── testbed/
│   ├── app.py                         <- Policy Enforcement Point (PEP) controller
│   ├── mock_banking_api.py            <- Open Banking & Treasury API simulator
│   └── state_store.py                 <- Thread-safe Core Banking ledger store
├── dataset/
│   ├── attack_dev.jsonl               <- Prompt injection dataset (EN, ID, Suroboyoan slang, Invoices)
│   ├── benign_dev.jsonl               <- Legitimate banking operations (balance inquiry, P2P transfer)
│   └── dataset_card.md                <- Dataset provenance, schemas, and attack taxonomies
├── tests/
│   ├── test_authorization.py          <- Pytest tests for capability tokens & scope checks
│   ├── test_prompt_injection.py       <- Security test ensuring prompt injections fail state changes
│   └── test_state_invariants.py       <- Money conservation & ledger invariants
├── benchmarks/
│   ├── run_experiments.py             <- Full comparative benchmark runner (BATAS vs Baselines)
│   ├── measure_latency.py             <- Profiling script for SLA latency percentiles (p50, p95, p99)
│   └── analyze_results.py             <- Formatter for academic comparison tables
└── results/
    ├── metrics.json                   <- Empirical benchmark output data with 95% CIs
    ├── experiment_config.json         <- Metadata parameters of experimental run
    └── environment.txt                <- System architecture and library runtime versions
```

---

## 2. Quickstart & Verification

### Install Dependencies
```bash
pip install -e .
```

### Run Integrity & Invariant Tests
```bash
pytest tests/ -v
```

### Execute Comparative Experiment Suite
```bash
python benchmarks/run_experiments.py
python benchmarks/analyze_results.py
```
