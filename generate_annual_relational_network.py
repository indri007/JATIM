#!/usr/bin/env python3
"""
Visualisasi Grafik Hubungan Aktor, Isu, dan Media dari Tahun ke Tahun (2021-2026)
"""
import os
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axs = plt.subplots(2, 3, figsize=(18, 12), dpi=300)
axs = axs.flatten()

years_data = [
    {
        'year': 2021,
        'title': '2021: Mitigasi Krisis Pandemi & Risiko Awal',
        'theme_color': '#d9534f', # Merah
        'nodes': [
            ('Bank Jatim', 'Core', 1200),
            ('Pemprov Jatim', 'Gov', 600),
            ('Nasabah UMKM', 'User', 500),
            ('Kredit Macet (Kepanjen)', 'Risk', 550),
            ('Isu Kebocoran Data', 'Risk', 550),
            ('JatimTIMES & Bisnis', 'Media', 650)
        ],
        'edges': [
            ('Bank Jatim', 'Nasabah UMKM', 'Restrukturisasi Kredit'),
            ('Pemprov Jatim', 'Bank Jatim', 'Dorong Kredit Lunak'),
            ('Bank Jatim', 'Kredit Macet (Kepanjen)', 'Investigasi Rp179 M'),
            ('Bank Jatim', 'Isu Kebocoran Data', 'Klarifikasi Publik'),
            ('JatimTIMES & Bisnis', 'Bank Jatim', 'Liputan Aset Rp101 T')
        ],
        'summary': 'Fokus: Ketahanan likuiditas pandemi, mitigasi kredit bermasalah cabang Kepanjen, dan klarifikasi perlindungan data nasabah.'
    },
    {
        'year': 2022,
        'title': '2022: Akselerasi Pemulihan & Penghargaan Nasional',
        'theme_color': '#f0ad4e', # Oranye
        'nodes': [
            ('Bank Jatim', 'Core', 1300),
            ('Bank Indonesia (BI)', 'Reg', 650),
            ('BPJS Ketenagakerjaan', 'Gov', 550),
            ('Pemda Kab/Kota (Lamongan)', 'Gov', 500),
            ('JConnect Digital', 'Tech', 600),
            ('Bisnis.com & Kompas TV', 'Media', 700)
        ],
        'edges': [
            ('Bank Jatim', 'Bank Indonesia (BI)', 'Mitigasi Kenaikan Suku Bunga'),
            ('BPJS Ketenagakerjaan', 'Bank Jatim', 'Paritrana Award 2022'),
            ('Bank Jatim', 'Pemda Kab/Kota (Lamongan)', 'Digitalisasi BKPSDM'),
            ('Bank Jatim', 'JConnect Digital', 'Penyaluran KUR Peringkat I'),
            ('Bisnis.com & Kompas TV', 'Bank Jatim', 'Liputan Penghargaan')
        ],
        'summary': 'Fokus: Peringkat I Penyalur KUR, raih Paritrana Award, mitigasi kenaikan BI Rate, dan peluncuran awal ekosistem JConnect.'
    },
    {
        'year': 2023,
        'title': '2023: Inisiasi Ekspansi Antarpulau & Ekspor Daerah',
        'theme_color': '#0275d8', # Biru
        'nodes': [
            ('Bank Jatim', 'Core', 1400),
            ('Gubernur Khofifah', 'Gov', 750),
            ('LPEI (Eximbank)', 'Partner', 600),
            ('Investor & Analis Saham', 'Market', 650),
            ('Pasar Luar Jatim', 'Target', 600),
            ('Kompas TV & Katadata', 'Media', 700)
        ],
        'edges': [
            ('Gubernur Khofifah', 'Bank Jatim', 'Apresiasi Misi Dagang Ekspor'),
            ('Bank Jatim', 'LPEI (Eximbank)', 'Pembiayaan UKM Ekspor'),
            ('Bank Jatim', 'Pasar Luar Jatim', 'Eksplorasi Jaringan Luar Daerah'),
            ('Investor & Analis Saham', 'Bank Jatim', 'Riset Saham BJTM & Laba Rp1,09 T'),
            ('Kompas TV & Katadata', 'Bank Jatim', 'Publikasi Kinerja Positif')
        ],
        'summary': 'Fokus: Sinergi ekspor LPEI bersama Gubernur Khofifah, eksplorasi jaringan pasar luar Jatim, dan pembagian dividen Rp797 miliar.'
    },
    {
        'year': 2024,
        'title': '2024: Katalis Regulasi OJK & Aliansi Multi-BPD',
        'theme_color': '#5bc0de', # Biru Muda / Toska
        'nodes': [
            ('Bank Jatim', 'Core', 1500),
            ('OJK (Regulator)', 'Reg', 750),
            ('Bank Sultra & NTT', 'BPD', 700),
            ('Bank NTB Syariah', 'BPD', 650),
            ('RUPSLB Pemegang Saham', 'Market', 650),
            ('Bisnis.com & Detik', 'Media', 750)
        ],
        'edges': [
            ('OJK (Regulator)', 'Bank Sultra & NTT', 'Mandat Modal Inti Rp3 T'),
            ('RUPSLB Pemegang Saham', 'Bank Jatim', 'Restu Penyertaan Modal BPD'),
            ('Bank Jatim', 'Bank Sultra & NTT', 'Sinergitas Injeksi KUB'),
            ('Bank Jatim', 'Bank NTB Syariah', 'PKS Kolaborasi Syariah'),
            ('Bisnis.com & Detik', 'Bank Jatim', 'BPD Terbesar Pelopor KUB')
        ],
        'summary': 'Fokus: Respons POJK konsolidasi modal inti Rp3 triliun; RUPSLB restui penyertaan modal ke Bank Sultra, NTT, dan NTB Syariah.'
    },
    {
        'year': 2025,
        'title': '2025: Realisasi Injeksi Modal & Ketegasan Hukum',
        'theme_color': '#5cb85c', # Hijau
        'nodes': [
            ('Bank Jatim', 'Core', 1500),
            ('Bank Lampung (5.42%)', 'BPD', 750),
            ('Bank Banten (BEKS)', 'BPD', 700),
            ('Kejati DKI Jakarta', 'Law', 650),
            ('Kemenag Haji & Umroh', 'Gov', 600),
            ('BCA Sekuritas & IQPlus', 'Media', 750)
        ],
        'edges': [
            ('Bank Jatim', 'Bank Lampung (5.42%)', 'Injeksi Modal Rp100 Miliar'),
            ('Bank Jatim', 'Bank Banten (BEKS)', 'Efektif Berlaku KUB Des 2025'),
            ('Kejati DKI Jakarta', 'Bank Jatim', 'Penegakan Hukum Kredit Cab. Jkt'),
            ('Bank Jatim', 'Kemenag Haji & Umroh', 'MoU Keuangan Ibadah Haji'),
            ('BCA Sekuritas & IQPlus', 'Bank Jatim', 'Laba Rp1,54 T & Transparansi')
        ],
        'summary': 'Fokus: Akuisisi 5,42% saham Bank Lampung, implementasi resmi KUB Bank Banten, MoU Haji Kemenag, dan mitigasi tuntas kasus Jakarta.'
    },
    {
        'year': 2026,
        'title': '2026: Panen Konsolidasi & Visi BPD Terbesar',
        'theme_color': '#6f42c1', # Ungu
        'nodes': [
            ('Bank Jatim (Induk KUB)', 'Core', 1600),
            ('Aliansi 5 BPD Mitra', 'BPD', 800),
            ('Prof. Mohammad Nasih', 'Gov', 650),
            ('10 Pengembang KPR', 'User', 600),
            ('Laba Konsolidasi (+61%)', 'Outcome', 700),
            ('Bisnis.com & CNBC', 'Media', 750)
        ],
        'edges': [
            ('Bank Jatim (Induk KUB)', 'Aliansi 5 BPD Mitra', 'Integrasi Bisnis & Operasional'),
            ('Bank Jatim (Induk KUB)', '10 Pengembang KPR', 'Ekspansi Kredit Konsolidasi'),
            ('Prof. Mohammad Nasih', 'Bank Jatim (Induk KUB)', 'Penguatan Komite Audit & Risiko'),
            ('Bank Jatim (Induk KUB)', 'Laba Konsolidasi (+61%)', 'Dividen Rp850 Miliar Disetujui'),
            ('Bisnis.com & CNBC', 'Bank Jatim (Induk KUB)', 'Visi Jadi BPD Terbesar Nasional')
        ],
        'summary': 'Fokus: Laba konsolidasian meroket 61,89%, kredit tumbuh 41,68%, pembagian dividen Rp850 M, dan pemantapan posisi BPD nomor 1.'
    }
]

role_colors = {
    'Core': '#2b5797',     # Biru Tua
    'Gov': '#28a745',      # Hijau
    'Reg': '#fd7e14',      # Oranye
    'BPD': '#17a2b8',      # Cyan
    'Market': '#6610f2',   # Ungu
    'Risk': '#dc3545',     # Merah
    'Law': '#721c24',      # Coklat Marun
    'Tech': '#20c997',     # Toska
    'User': '#e83e8c',     # Pink
    'Partner': '#ffc107',  # Kuning Emas
    'Media': '#6c757d',    # Abu-abu
    'Outcome': '#d4ac0d',  # Emas
    'Target': '#1f77b4'
}

for idx, data in enumerate(years_data):
    ax = axs[idx]
    G = nx.Graph()
    for name, r, sz in data['nodes']:
        G.add_node(name, role=r, size=sz)
    for u, v, lbl in data['edges']:
        G.add_edge(u, v, label=lbl)
        
    pos = nx.spring_layout(G, seed=42, k=0.85)
    
    # Draw edges
    for u, v, d in G.edges(data=True):
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color='#aaaaaa', linewidth=1.5, linestyle='-', zorder=1)
        # Midpoint label
        mx, my = (pos[u][0] + pos[v][0])/2, (pos[u][1] + pos[v][1])/2
        ax.text(mx, my, d['label'], fontsize=6.2, ha='center', va='center', color='#333333',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff', edgecolor='#dddddd', alpha=0.9), zorder=2)
        
    # Draw nodes
    for n, d in G.nodes(data=True):
        col = role_colors.get(d['role'], '#333333')
        x, y = pos[n]
        ax.scatter(x, y, s=d['size'], color=col, edgecolor='white', linewidth=1.8, zorder=3)
        ax.text(x, y + (0.09 if d['size']<1000 else 0.12), n, fontsize=7.2, fontweight='bold', ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=col, alpha=0.85), zorder=4)
        
    ax.set_title(data['title'], fontsize=11, fontweight='bold', color=data['theme_color'], pad=10)
    
    # Bottom summary box
    ax.text(0.5, -0.08, data['summary'], transform=ax.transAxes, fontsize=7.5, ha='center', va='top', style='italic',
            bbox=dict(boxstyle='square,pad=0.4', facecolor='#fcfcfc', edgecolor='#e0e0e0', linewidth=1))
    
    ax.axis('off')
    # Border
    for spine in ax.spines.values():
        spine.set_color(data['theme_color'])
        spine.set_linewidth(2)

fig.suptitle("Evolusi Hubungan Antara Aktor, Isu Strategis & Ekosistem Media Bank Jatim (2021–2026)\n"
             "Transformasi Lintasan 6 Tahun: Dari Ketahanan Pandemi Menuju Kepemimpinan Konglomerasi BPD Terbesar",
             fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('fig6_annual_relational_evolution.png', dpi=300)
plt.close()
print("Saved fig6_annual_relational_evolution.png successfully!")
