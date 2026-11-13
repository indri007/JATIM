-- DDL and Seed Data for Compliance Controls
CREATE TABLE IF NOT EXISTS compliance_controls (
    control_id VARCHAR(32) PRIMARY KEY,
    regulation VARCHAR(64) NOT NULL,
    control_name VARCHAR(255) NOT NULL,
    status VARCHAR(16) NOT NULL,
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed Regulatory Compliance Controls mapped to Bank Jatim & BATAS Zero Trust
INSERT INTO compliance_controls (control_id, regulation, control_name, status, last_verified_at) VALUES
('POJK-11-01', 'POJK 11/POJK.03/2022', 'Manajemen Risiko Penyediaan Teknologi Informasi & Ketahanan Siber', 'COMPLIANT', NOW()),
('POJK-11-02', 'POJK 11/POJK.03/2022', 'Prinsip Hak Akses Minimum (Least Privilege) pada Integrasi API Agen', 'COMPLIANT', NOW()),
('POJK-11-03', 'POJK 11/POJK.03/2022', 'Pencatatan Jejak Audit (Audit Trail) Anti-Manipulasi pada Transaksi Inti', 'COMPLIANT', NOW()),
('POJK-11-04', 'POJK 11/POJK.03/2022', 'Segregasi Tugas & Otorisasi Bertingkat Transaksi Finansial', 'COMPLIANT', NOW()),
('PADK-01-01', 'PADK OJK 1/2026', 'Pelarangan Eksekusi Otonom Penuh pada Akun Perbendaharaan Daerah (RKUD)', 'COMPLIANT', NOW()),
('PADK-01-02', 'PADK OJK 1/2026', 'Mekanisme Human-in-the-Loop (Dual-Control Approval) Transaksi Kasda', 'COMPLIANT', NOW()),
('PADK-01-03', 'PADK OJK 1/2026', 'Pertahanan Deterministik terhadap Rekayasa Manipulasi Prompt (Prompt Injection)', 'COMPLIANT', NOW()),
('PADK-01-04', 'PADK OJK 1/2026', 'Pembatasan Masa Berlaku Token Kapabilitas Transaksi (Ephemeral Token)', 'COMPLIANT', NOW()),
('OJK-AI-01', 'OJK AI Governance', 'Prinsip Akuntabilitas Algoritmik & Pemisahan Wewenang Agen AI', 'COMPLIANT', NOW()),
('OJK-AI-02', 'OJK AI Governance', 'Transparansi Keputusan Penolakan Transaksi (Audit Decision Reason)', 'COMPLIANT', NOW())
ON CONFLICT (control_id) DO UPDATE 
SET status = EXCLUDED.status, last_verified_at = EXCLUDED.last_verified_at;
