# Skema Basis Data & Spesifikasi Data (SCHEMA)
## Platform Analisis Finansial & Keamanan AI Zero Trust (BATAS - Bank Jatim)
**Aplikasi Live:** [https://bankjatim.streamlit.app/](https://bankjatim.streamlit.app/)  
**Repositori:** [https://github.com/indri007/JATIM](https://github.com/indri007/JATIM)  
**Dokumen Terkait:** [PRD.md](file:///Users/jevin/Downloads/jatim/PRD.md) | [ERD.md](file:///Users/jevin/Downloads/jatim/ERD.md) | [README.md](file:///Users/jevin/Downloads/jatim/README.md)

---

## 1. Skema Relasional (SQL DDL / PostgreSQL & SQLite Compatible)

### Domain A: Financial Analytics & Benchmarking

```sql
-- 1. Tabel Master Bank & Emiten
CREATE TABLE banks (
    ticker VARCHAR(12) PRIMARY KEY,               -- e.g. 'BJTM.JK', 'BJBR.JK'
    company_name VARCHAR(255) NOT NULL,          -- e.g. 'Bank Pembangunan Daerah Jawa Timur Tbk PT'
    country VARCHAR(64) DEFAULT 'Indonesia',
    sector VARCHAR(128) DEFAULT 'Financials',
    bank_type VARCHAR(32) NOT NULL,              -- 'BPD', 'BUMN', 'SWASTA_NASIONAL'
    is_bpd BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_banks_sector ON banks(sector);
CREATE INDEX idx_banks_is_bpd ON banks(is_bpd);

-- 2. Tabel Metrik & Rasio Keuangan Tahunan (ROA / ROE)
CREATE TABLE financial_metrics (
    metric_id VARCHAR(64) PRIMARY KEY,           -- Hash(ticker, metric_type, fiscal_year)
    ticker VARCHAR(12) NOT NULL REFERENCES banks(ticker) ON DELETE CASCADE,
    metric_type VARCHAR(16) NOT NULL,            -- 'ROA', 'ROE', 'NIM', 'CAR'
    fiscal_year INT NOT NULL CHECK (fiscal_year BETWEEN 2000 AND 2100),
    ratio_value NUMERIC(8, 4),                   -- Persentase rasio dalam skala persen (misal: 1.8500%)
    percentile_rank NUMERIC(5, 2),               -- Peringkat persentil di sektor perbankan (0 - 100)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_ticker_metric_year UNIQUE (ticker, metric_type, fiscal_year)
);

CREATE INDEX idx_metrics_lookup ON financial_metrics(ticker, metric_type, fiscal_year);
CREATE INDEX idx_metrics_year ON financial_metrics(fiscal_year, metric_type);

-- 3. Tabel Dokumen Publikasi & Audit Integritas Checksum
CREATE TABLE regulatory_documents (
    doc_id VARCHAR(64) PRIMARY KEY,              -- e.g. 'DOC-BJTM-AR-2024'
    ticker VARCHAR(12) NOT NULL REFERENCES banks(ticker) ON DELETE RESTRICT,
    report_type VARCHAR(32) NOT NULL,            -- 'ANNUAL_REPORT', 'LFR_AUDITED', 'LFR_UNAUDITED'
    period VARCHAR(32) NOT NULL,                 -- 'TAHUNAN', 'Q1', 'Q2', 'Q3', 'DESEMBER'
    fiscal_year INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    sha256_checksum CHAR(64) NOT NULL,           -- SHA-256 Hash terverifikasi anti-tamper
    file_size_bytes BIGINT NOT NULL,
    official_source_url TEXT NOT NULL,
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reg_docs_year ON regulatory_documents(fiscal_year, report_type);
```

---

### Domain B: BATAS Zero Trust & Core Banking Ledger Engine

```sql
-- 4. Tabel Rekening Nasabah & Kas Daerah (RKUD)
CREATE TABLE bank_accounts (
    account_no VARCHAR(32) PRIMARY KEY,          -- e.g. 'REK-KASDA-001', 'REK-RETAIL-101'
    account_name VARCHAR(255) NOT NULL,
    balance BIGINT NOT NULL CHECK (balance >= 0), -- Saldo non-negatif (Invarian konservasi)
    currency CHAR(3) DEFAULT 'IDR',
    is_treasury BOOLEAN NOT NULL DEFAULT FALSE,  -- True = Akun Kasda (Wajib Dual Control)
    status VARCHAR(16) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'FROZEN', 'CLOSED')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabel Ephemeral Task Capability Token
CREATE TABLE task_tokens (
    token_id VARCHAR(64) PRIMARY KEY,            -- UUID v4
    session_id VARCHAR(64) NOT NULL,
    issued_to VARCHAR(128) NOT NULL,             -- Identitas Agen AI (e.g. 'agent-ret-01')
    scopes JSONB NOT NULL,                       -- Array scopes ['read:balance', 'transfer:retail_p2p']
    issued_at TIMESTAMP WITH TIME ZONE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    CONSTRAINT chk_token_expiry CHECK (expires_at > issued_at)
);

CREATE INDEX idx_tokens_session ON task_tokens(session_id);
CREATE INDEX idx_tokens_expiry ON task_tokens(expires_at, is_revoked);

-- 6. Tabel Audit Log Keputusan Policy Enforcement Point (PEP)
CREATE TABLE policy_decisions (
    decision_id VARCHAR(64) PRIMARY KEY,         -- e.g. 'DEC-20261113-0001'
    token_id VARCHAR(64) NOT NULL REFERENCES task_tokens(token_id),
    action_requested VARCHAR(64) NOT NULL,       -- 'transfer', 'read_balance'
    target_account VARCHAR(32) NOT NULL REFERENCES bank_accounts(account_no),
    amount BIGINT,                               -- NULL jika aksi baca saldo
    decision VARCHAR(16) NOT NULL CHECK (decision IN ('ALLOWED', 'DENIED', 'HITL_TRIGGER')),
    decision_reason TEXT NOT NULL,
    policy_rule_triggered VARCHAR(128),          -- e.g. 'TREASURY_DUAL_CONTROL_RULE'
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pep_decision ON policy_decisions(decision, evaluated_at);

-- 7. Tabel Pembukuan Transaksi Ledger (Core Banking Ledger Entries)
CREATE TABLE ledger_transactions (
    tx_id VARCHAR(64) PRIMARY KEY,               -- e.g. 'TXN-JT-0000001'
    source_account VARCHAR(32) NOT NULL REFERENCES bank_accounts(account_no),
    dest_account VARCHAR(32) NOT NULL REFERENCES bank_accounts(account_no),
    amount BIGINT NOT NULL CHECK (amount > 0),
    decision_id VARCHAR(64) NOT NULL REFERENCES policy_decisions(decision_id),
    status VARCHAR(16) NOT NULL CHECK (status IN ('COMMITTED', 'REJECTED')),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_distinct_accounts CHECK (source_account <> dest_account)
);

CREATE INDEX idx_tx_source ON ledger_transactions(source_account);
CREATE INDEX idx_tx_dest ON ledger_transactions(dest_account);
CREATE INDEX idx_tx_created ON ledger_transactions(created_at);

-- 8. Tabel Korpus Skenario Evaluasi Serangan (Benchmark Scenarios)
CREATE TABLE evaluation_scenarios (
    case_id VARCHAR(32) PRIMARY KEY,             -- e.g. 'ATK-001', 'BNG-042'
    category VARCHAR(16) NOT NULL CHECK (category IN ('ATTACK', 'BENIGN')),
    linguistic_framing VARCHAR(32) NOT NULL,     -- 'BUREAUCRATIC', 'URGENCY', 'SLANG', 'DIRECT'
    language VARCHAR(8) NOT NULL,                -- 'id', 'en', 'jv' (Jawa)
    prompt_payload TEXT NOT NULL,
    target_authority VARCHAR(64) NOT NULL,       -- 'RKUD_EXFILTRATION', 'LIMIT_STEPUP'
    expected_decision VARCHAR(16) NOT NULL,      -- 'HITL_TRIGGER', 'DENIED', 'ALLOWED'
    hitl_triggered BOOLEAN NOT NULL DEFAULT FALSE,
    invariant_conserved BOOLEAN NOT NULL DEFAULT TRUE
);
```

---

## 2. Spesifikasi Skema JSON / Pydantic (API & Data Flow)

### 2.1 Skema Permintaan Aksi Agen AI (`ActionRequest`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ActionRequest",
  "type": "object",
  "required": ["action", "params", "task_token"],
  "properties": {
    "action": {
      "type": "string",
      "enum": ["read_balance", "transfer", "disburse_sp2d"]
    },
    "params": {
      "type": "object",
      "properties": {
        "source": { "type": "string", "example": "REK-KASDA-001" },
        "dest": { "type": "string", "example": "REK-ATTACKER-999" },
        "amount": { "type": "integer", "minimum": 1, "example": 5000000 },
        "account": { "type": "string", "example": "REK-RETAIL-101" }
      }
    },
    "task_token": {
      "type": "object",
      "required": ["token_id", "session_id", "scopes", "expires_at"],
      "properties": {
        "token_id": { "type": "string", "format": "uuid" },
        "session_id": { "type": "string" },
        "scopes": {
          "type": "array",
          "items": { "type": "string" },
          "example": ["read:balance", "transfer:retail_p2p"]
        },
        "expires_at": { "type": "number", "example": 1731499200 }
      }
    }
  }
}
```

### 2.2 Skema Respon Keputusan PEP (`PEPDecisionResponse`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PEPDecisionResponse",
  "type": "object",
  "required": ["is_success", "is_hitl_triggered", "decision", "decision_reason", "payload"],
  "properties": {
    "is_success": { "type": "boolean" },
    "is_hitl_triggered": { "type": "boolean" },
    "decision": {
      "type": "string",
      "enum": ["ALLOWED", "DENIED", "HITL_TRIGGER"]
    },
    "decision_reason": { "type": "string" },
    "payload": {
      "type": "object",
      "properties": {
        "tx_id": { "type": "string" },
        "source": { "type": "string" },
        "dest": { "type": "string" },
        "amount": { "type": "integer" }
      }
    }
  }
}
```

---

## 3. Skema Ingest Data Excel (`ROA`/`ROE_INDONESIA_2021-2025.xlsx`)

| Kolom Sumber Excel | Nama Field Database | Tipe Data | Transformasi / Validasi |
| :--- | :--- | :--- | :--- |
| `Identifier` (Kolom 0) | `ticker` | `VARCHAR(12)` | Normalisasi string (misal: `BJTM.JK`) |
| `Company Name` (Kolom 1) | `company_name` | `VARCHAR(255)` | Trim whitespace & title case |
| `Country of Exchange` (Kolom 2) | `country` | `VARCHAR(64)` | Default `Indonesia` |
| `TRBC Economic Sector Name` (Kolom 3) | `sector` | `VARCHAR(128)` | Filter sektor `Financials` |
| `2025` (Kolom 4) s/d `2021` (Kolom 8) | `ratio_value` | `NUMERIC(8,4)` | Konversi ke bentuk persen (`* 100`) dan per-baris *unpivot/melt* |
