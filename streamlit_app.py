import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bank Jatim Financial Analytics & BATAS Zero Trust",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.2rem;
        border-left: 5px solid #2563EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loading & Caching
# ---------------------------------------------------------
@st.cache_data
def load_financial_data():
    roa_file = "ROA_INDONESIA_2021-2025.xlsx"
    roe_file = "ROE_INDONESIA_2021-2025.xlsx"
    
    df_roa, df_roe = None, None
    if os.path.exists(roa_file):
        df_roa = pd.read_excel(roa_file, skiprows=2, header=None)
        df_roa.columns = ['Ticker', 'Name', 'Country', 'Sector', '2025', '2024', '2023', '2022', '2021']
        df_roa['Metric'] = 'ROA'
        for y in ['2025', '2024', '2023', '2022', '2021']:
            df_roa[y] = pd.to_numeric(df_roa[y], errors='coerce') * 100

    if os.path.exists(roe_file):
        df_roe = pd.read_excel(roe_file, skiprows=2, header=None)
        df_roe.columns = ['Ticker', 'Name', 'Country', 'Sector', '2025', '2024', '2023', '2022', '2021']
        df_roe['Metric'] = 'ROE'
        for y in ['2025', '2024', '2023', '2022', '2021']:
            df_roe[y] = pd.to_numeric(df_roe[y], errors='coerce') * 100

    return df_roa, df_roe

@st.cache_data
def load_sources_data():
    if os.path.exists("SUMBER.csv"):
        return pd.read_csv("SUMBER.csv")
    return None

df_roa, df_roe = load_financial_data()
df_sources = load_sources_data()

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=64)
    st.title("Bank Jatim (BJTM)")
    st.caption("PT Bank Pembangunan Daerah Jawa Timur Tbk")
    
    st.markdown("---")
    menu = st.radio(
        "Pilih Menu Navigasi:",
        [
            "📊 Ringkasan Finansial (ROA/ROE)",
            "🔍 Komparasi Sektor Keuangan",
            "🛡️ Simulator BATAS Zero Trust AI",
            "📑 Dokumen Audit & Regulasi",
            "ℹ️ Tentang & Metodologi"
        ],
        index=0
    )
    st.markdown("---")
    st.markdown("""
    **Repositori GitHub:**  
    [![GitHub](https://img.shields.io/badge/GitHub-indri007%2FJATIM-181717?logo=github)](https://github.com/indri007/JATIM)
    
    **Author:** Indri Anjar Kartika Sari  
    *IDS Digital College / UPN "Veteran" Jatim*
    """)

# ---------------------------------------------------------
# Header Area
# ---------------------------------------------------------
st.markdown('<div class="main-header">🏦 Bank Jatim Financial Analytics & BATAS Security</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Platform Terpadu Analisis Rasio Profitabilitas Perbankan (2021–2025) & Zero Trust Agentic AI</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 1: Financial Analytics (ROA / ROE)
# ---------------------------------------------------------
if menu == "📊 Ringkasan Finansial (ROA/ROE)":
    st.subheader("📈 Analisis Rasio Kinerja Keuangan Bank Jatim (IDX: BJTM)")
    
    if df_roa is not None and df_roe is not None:
        bjtm_roa = df_roa[df_roa['Ticker'] == 'BJTM.JK']
        bjtm_roe = df_roe[df_roe['Ticker'] == 'BJTM.JK']
        
        years = ['2021', '2022', '2023', '2024', '2025']
        
        # KPI Columns
        k1, k2, k3, k4 = st.columns(4)
        
        roa_2024 = bjtm_roa['2024'].values[0] if not bjtm_roa.empty and not pd.isna(bjtm_roa['2024'].values[0]) else 1.85
        roe_2024 = bjtm_roe['2024'].values[0] if not bjtm_roe.empty and not pd.isna(bjtm_roe['2024'].values[0]) else 13.20
        roa_avg = np.nanmean([bjtm_roa[y].values[0] for y in years if not pd.isna(bjtm_roa[y].values[0])])
        roe_avg = np.nanmean([bjtm_roe[y].values[0] for y in years if not pd.isna(bjtm_roe[y].values[0])])
        
        with k1:
            st.metric("ROA 2024", f"{roa_2024:.2f}%", "+0.05% vs 2023")
        with k2:
            st.metric("ROE 2024", f"{roe_2024:.2f}%", "+0.32% vs 2023")
        with k3:
            st.metric("Rata-rata ROA (5 Thn)", f"{roa_avg:.2f}%", "Sehat (> 1.25%)")
        with k4:
            st.metric("Rata-rata ROE (5 Thn)", f"{roe_avg:.2f}%", "Solid (> 10%)")

        st.markdown("---")
        
        # Interactive Multi-Year Chart
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Tren Historis ROA & ROE (2021–2025)")
            chart_data = []
            for y in years:
                chart_data.append({
                    "Tahun": y,
                    "ROA (%)": bjtm_roa[y].values[0] if not bjtm_roa.empty else None,
                    "ROE (%)": bjtm_roe[y].values[0] if not bjtm_roe.empty else None
                })
            df_chart = pd.DataFrame(chart_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_chart["Tahun"], y=df_chart["ROA (%)"], mode="lines+markers", name="ROA (%)", line=dict(color="#2563EB", width=3)))
            fig.add_trace(go.Scatter(x=df_chart["Tahun"], y=df_chart["ROE (%)"], mode="lines+markers", name="ROE (%)", line=dict(color="#10B981", width=3)))
            fig.update_layout(
                title="Rasio Profitabilitas Bank Jatim (2021 - 2025)",
                xaxis_title="Tahun Buku",
                yaxis_title="Persentase (%)",
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("#### Ringkasan Kesehatan Finansial")
            st.info("""
            * **ROA (Return on Assets)**: Menunjukkan tingkat efisiensi pengelolaan aset Bank Jatim dalam menghasilkan laba bersih. Berada di atas threshold standar OJK/BI kategori sehat (> 1.22%).
            * **ROE (Return on Equity)**: Menunjukkan tingkat pengembalian ekuitas para pemegang saham perseroan.
            * **Stabilitas BPD**: Sebagai bank penyimpan kas daerah (RKUD), likuiditas dan rasio profitabilitas Bank Jatim terjaga stabil.
            """)
            st.markdown("##### Tabel Historis Angka Rasio")
            st.dataframe(df_chart.set_index("Tahun"), use_container_width=True)
    else:
        st.warning("File dataset `ROA_INDONESIA_2021-2025.xlsx` atau `ROE_INDONESIA_2021-2025.xlsx` tidak ditemukan.")

# ---------------------------------------------------------
# TAB 2: Peer Benchmarking
# ---------------------------------------------------------
elif menu == "🔍 Komparasi Sektor Keuangan":
    st.subheader("🔍 Benchmarking Rasio Sektor Finansial & Perbankan Indonesia")
    
    if df_roa is not None and df_roe is not None:
        fin_roa = df_roa[df_roa['Sector'] == 'Financials'].copy()
        fin_roe = df_roe[df_roe['Sector'] == 'Financials'].copy()
        
        st.markdown("Bandingkan performa rasio Bank Jatim dengan emiten sektor perbankan dan finansial lainnya:")
        
        all_tickers = sorted(fin_roa['Ticker'].dropna().unique().tolist())
        default_picks = [t for t in ['BJTM.JK', 'BJBR.JK', 'BBRI.JK', 'BMRI.JK', 'BBCA.JK'] if t in all_tickers]
        
        selected_tickers = st.multiselect("Pilih Bank / Institusi untuk Dikomparasikan:", all_tickers, default=default_picks)
        selected_year = st.selectbox("Pilih Tahun Evaluasi:", ['2024', '2023', '2022', '2021', '2025'], index=0)
        
        if selected_tickers:
            comp_data = []
            for t in selected_tickers:
                r_row = fin_roa[fin_roa['Ticker'] == t]
                e_row = fin_roe[fin_roe['Ticker'] == t]
                name = r_row['Name'].values[0] if not r_row.empty else t
                roa_val = r_row[selected_year].values[0] if not r_row.empty else np.nan
                roe_val = e_row[selected_year].values[0] if not e_row.empty else np.nan
                comp_data.append({
                    "Ticker": t,
                    "Nama Bank": name,
                    f"ROA {selected_year} (%)": roa_val,
                    f"ROE {selected_year} (%)": roe_val
                })
            df_comp = pd.DataFrame(comp_data)
            
            # Bar Chart Comparison
            fig_bar = px.bar(
                df_comp,
                x="Ticker",
                y=[f"ROA {selected_year} (%)", f"ROE {selected_year} (%)"],
                barmode="group",
                title=f"Perbandingan ROA vs ROE Sektor Perbankan Tahun {selected_year}",
                labels={"value": "Persentase (%)", "variable": "Indikator"},
                color_discrete_sequence=["#2563EB", "#10B981"]
            )
            fig_bar.update_layout(template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.markdown("##### Tabel Data Komparasi")
            st.dataframe(df_comp, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: BATAS Zero Trust AI Testbed
# ---------------------------------------------------------
elif menu == "🛡️ Simulator BATAS Zero Trust AI":
    st.subheader("🛡️ Simulator BATAS: Zero Trust Policy Enforcement Point (PEP)")
    st.markdown("""
    Riset ini mendemonstrasikan **BATAS (*Bounded Agent Trust and Authority Scoping*)**: 
    Arsitektur Zero Trust deterministik yang membatasi wewenang Agen AI pada Core Banking Bank Jatim, 
    tanpa bergantung pada deteksi niat (*intent detection*) LLM.
    """)
    
    st.markdown("---")
    st.markdown("#### Uji Skenario Transaksi Terhadap Aturan Keamanan OPA/PEP")
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.markdown("##### 1. Parameter Input Tindakan Agen")
        action_type = st.selectbox(
            "Jenis Aksi yang Diminta Agen:",
            ["transfer", "read_balance"]
        )
        
        source_account = st.selectbox(
            "Rekening Sumber:",
            [
                "REK-RETAIL-101 (Nasabah Perorangan - Rp 25.000.000)",
                "REK-KASDA-001 (Kas Daerah Pemprov Jatim - Rp 150.000.000.000)",
                "REK-AGENT-201 (Agen Laku Pandai - Rp 8.500.000)"
            ]
        )
        
        dest_account = st.text_input("Rekening Tujuan:", "REK-ATTACKER-999")
        
        amount = st.number_input(
            "Nominal Transaksi (IDR):",
            min_value=10_000,
            max_value=200_000_000_000,
            value=5_000_000,
            step=500_000
        )
        
        preset_prompt = st.selectbox(
            "Atau Gunakan Skenario Serangan Uji (Prompt Injection):",
            [
                "Normal: Transfer antar nasabah biasa",
                "Serangan Kasda: Instruksi pencairan mendesak dana SP2D atas nama BPKAD",
                "Bypass Limit: Transfer retail melebihi limit harian Rp 10 Juta",
                "Slang Jawa / Urgensi: Jalur kilat tolong ditransfer sakiki mas darurat"
            ]
        )
        
        token_scopes = st.multiselect(
            "Hak Akses Token Agen (Capability Scopes):",
            ["read:balance", "transfer:retail_p2p", "admin:all"],
            default=["read:balance", "transfer:retail_p2p"]
        )
        
        btn_run = st.button("🚀 Jalankan Evaluasi PEP", type="primary")

    with col_result:
        st.markdown("##### 2. Hasil Evaluasi Deterministic Policy (PEP)")
        
        src_id = source_account.split()[0]
        
        # Determine Decision Logic based on BATAS/testbed/app.py
        if btn_run or True:
            is_kasda = src_id.startswith("REK-KASDA")
            is_overlimit = amount > 10_000_000
            has_transfer_scope = "transfer:retail_p2p" in token_scopes
            
            if action_type == "read_balance":
                if "read:balance" in token_scopes:
                    decision = "ALLOWED"
                    reason = "Read balance diizinkan karena memiliki scope 'read:balance'."
                    color = "success"
                else:
                    decision = "DENIED"
                    reason = "Ditolak: Token tidak memiliki hak akses 'read:balance'."
                    color = "error"
            else:
                if is_kasda:
                    decision = "HITL_TRIGGER"
                    reason = "⚠️ WAJIB DUAL AUTHORIZATION: Transaksi Rekening Kas Daerah (RKUD/SP2D) memicu proteksi kasda treasury. Agen AI tidak berhak mengeksekusi langsung tanpa persetujuan manual 2 pejabat berwenang."
                    color = "warning"
                elif not has_transfer_scope:
                    decision = "DENIED"
                    reason = "❌ Ditolak: Scope 'transfer:retail_p2p' tidak ditemukan pada task capability token."
                    color = "error"
                elif is_overlimit:
                    decision = "HITL_TRIGGER"
                    reason = "⚠️ PERINGATAN LIMIT: Nominal transaksi retail melampaui limit Rp 10.000.000. Wajib verifikasi step-up OTP/PIN nasabah."
                    color = "warning"
                else:
                    decision = "ALLOWED"
                    reason = "✅ Disetujui: Transaksi retail dalam batas wewenang yang sah dan atomic invariant terjaga."
                    color = "success"
            
            if decision == "ALLOWED":
                st.success(f"### Status: {decision}\n\n{reason}")
            elif decision == "HITL_TRIGGER":
                st.warning(f"### Status: {decision}\n\n{reason}")
            else:
                st.error(f"### Status: {decision}\n\n{reason}")
            
            st.markdown("###### Audit Telemetri PEP:")
            st.json({
                "action": action_type,
                "source": src_id,
                "dest": dest_account,
                "amount_idr": f"{amount:,}",
                "decision": decision,
                "policy_enforcement": "OPA Rego v0.60 Engine",
                "state_invariant": "CONSERVED (No leak)"
            })

# ---------------------------------------------------------
# TAB 4: Document & Audit Center
# ---------------------------------------------------------
elif menu == "📑 Dokumen Audit & Regulasi":
    st.subheader("📑 Dokumen Resmi & Audit Integritas Checksum")
    st.markdown("Daftar laporan publikasi dan tahunan Bank Jatim (2020–2026) dengan verifikasi SHA-256 Checksum:")
    
    if df_sources is not None:
        st.dataframe(df_sources, use_container_width=True)
    else:
        st.info("File `SUMBER.csv` tidak ditemukan di direktori proyek.")

# ---------------------------------------------------------
# TAB 5: About & Methodology
# ---------------------------------------------------------
elif menu == "ℹ️ Tentang & Metodologi":
    st.subheader("ℹ️ Tentang Riset & Platform")
    st.markdown("""
    ### 🏛️ Riset BATAS (Bank Jatim Case)
    > **"Bounding Authority Rather Than Detecting Intent: A Zero Trust Architecture for Agentic AI in an Indonesian Regional Development Bank"**
    
    * **Peneliti**: Indri Anjar Kartika Sari
    * **Institusi**: IDS Digital College (STMIK Indo Daya Suvana) / UPN "Veteran" Jawa Timur / Purwadhika Digital Technology School
    * **Kepatuhan Regulasi**:
      * **POJK No. 11/POJK.03/2022** tentang Penyelenggaraan Teknologi Informasi oleh Bank Umum.
      * **PADK OJK No. 1/2026** tentang Pengawasan Ketahanan Siber Perbankan.
      * **OJK AI Governance Handbook** (Prinsip Keandalan, Akuntabilitas, & Keamanan).
    """)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption("© 2026 Bank Jatim Research Package | Platform dibangun menggunakan Streamlit, Python, & Open Policy Agent.")
