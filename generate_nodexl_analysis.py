#!/usr/bin/env python3
"""
Analisis NodeXL & Pembuatan 5 Gambar Grafik Jaringan Berita Bank Jatim (2021-2026)
"""
import os
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
import re
from collections import Counter, defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# 1. Load Data
df = pd.read_csv('Berita Bank Jatim 2021–2026 - Berita.csv')
print(f"Loaded {len(df)} news items.")

# Extract Year
def get_year(val):
    m = re.search(r'202[0-6]', str(val))
    return int(m.group(0)) if m else 2024

df['Tahun'] = df['Tanggal Terbit'].apply(get_year)

# Classify Topics
def assign_topic(title):
    t = title.lower()
    if any(k in t for k in ['kub', 'kelompok usaha bank', 'konsolidasi', 'induk kub', 'ntb syariah', 'bank lampung', 'sultra']):
        return 'Konsolidasi KUB & Sinergi BPD'
    elif any(k in t for k in ['dividen', 'saham', 'rupst', 'investor', 'direksi', 'komisaris', 'manajemen', 'buyback']):
        return 'Pasar Modal, Saham & Tata Kelola'
    elif any(k in t for k in ['digital', 'jconnect', 'qris', 'teknologi', 'layanan digital', 'it', 'keamanan']):
        return 'Transformasi Digital & Layanan'
    elif any(k in t for k in ['kredit', 'kpr', 'umkm', 'pembiayaan', 'penyaluran', 'fiktif', 'dugaan']):
        return 'Ekspansi Kredit & Manajemen Risiko'
    else:
        return 'Kinerja Finansial & Laba Bersih'

df['Topik'] = df['Judul'].apply(assign_topic)
print("\nDistribusi Topik:\n", df['Topik'].value_counts())

# Build Bipartite Network: Media <-> Topic
B = nx.Graph()
for idx, row in df.iterrows():
    media = row['Media/Sumber'].strip()
    topic = row['Topik']
    if not B.has_node(media):
        B.add_node(media, node_type='Media', count=0)
    if not B.has_node(topic):
        B.add_node(topic, node_type='Topik', count=0)
    B.nodes[media]['count'] += 1
    B.nodes[topic]['count'] += 1
    
    if B.has_edge(media, topic):
        B[media][topic]['weight'] += 1
    else:
        B.add_edge(media, topic, weight=1)

# Media projection network (Media connected if they report on same topics with shared intensity)
media_nodes = [n for n, d in B.nodes(data=True) if d['node_type'] == 'Media']
topic_nodes = [n for n, d in B.nodes(data=True) if d['node_type'] == 'Topik']

# Direct Co-occurrence between Media
G_media = nx.Graph()
for m in media_nodes:
    if B.nodes[m]['count'] >= 2: # filter active media
        G_media.add_node(m, count=B.nodes[m]['count'])

for i in range(len(media_nodes)):
    for j in range(i + 1, len(media_nodes)):
        m1, m2 = media_nodes[i], media_nodes[j]
        if m1 in G_media and m2 in G_media:
            # common topics weight
            shared_weight = sum(B[m1][t]['weight'] * B[m2][t]['weight'] for t in topic_nodes if B.has_edge(m1, t) and B.has_edge(m2, t))
            if shared_weight >= 3:
                G_media.add_edge(m1, m2, weight=shared_weight)

# Centrality Metrics
deg_cent = nx.degree_centrality(G_media)
bet_cent = nx.betweenness_centrality(G_media, weight='weight')
close_cent = nx.closeness_centrality(G_media)

# Community Detection
import networkx.algorithms.community as nx_comm
communities = list(nx_comm.greedy_modularity_communities(G_media))
community_map = {}
for comm_id, comm in enumerate(communities):
    for node in comm:
        community_map[node] = comm_id

print(f"Detected {len(communities)} media communities.")

# ==========================================
# GAMBAR 1: NodeXL Overall Discourse Network
# ==========================================
fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
pos = nx.spring_layout(G_media, k=0.45, seed=42, iterations=100)

palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
node_colors = [palette[community_map.get(n, 0) % len(palette)] for n in G_media.nodes()]
node_sizes = [max(180, B.nodes[n]['count'] * 75) for n in G_media.nodes()]

# Draw edges with varying transparency based on weight
weights = [G_media[u][v]['weight'] for u, v in G_media.edges()]
max_w = max(weights) if weights else 1
for (u, v, d) in G_media.edges(data=True):
    alpha = min(0.85, 0.15 + (d['weight'] / max_w) * 0.7)
    width = 0.8 + (d['weight'] / max_w) * 3.5
    ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color='#999999', alpha=alpha, linewidth=width)

nx.draw_networkx_nodes(G_media, pos, ax=ax, node_color=node_colors, node_size=node_sizes, alpha=0.92, edgecolors='white', linewidths=1.8)

# Labels with clean repulsion/fontsize
for node, (x, y) in pos.items():
    cnt = B.nodes[node]['count']
    font_size = 9.5 if cnt >= 8 else (8 if cnt >= 4 else 6.8)
    font_weight = 'bold' if cnt >= 8 else 'normal'
    ax.text(x, y + 0.035, f"{node} ({cnt})", fontsize=font_size, fontweight=font_weight,
            ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.75, edgecolor='none'), zorder=3)

# NodeXL Metrics Box Inset
metrics_text = (
    "NodeXL Graph Metrics Summary:\n"
    f"• Total Berita Dianalisis : {len(df)}\n"
    f"• Vertices (Media Node)   : {G_media.number_of_nodes()}\n"
    f"• Edges (Shared Ties)     : {G_media.number_of_edges()}\n"
    f"• Graph Density           : {nx.density(G_media):.3f}\n"
    f"• Modularity Index        : {nx_comm.modularity(G_media, communities):.3f}\n"
    f"• Avg Clustering Coeff    : {nx.average_clustering(G_media):.3f}\n"
    "• Layout Algorithm        : Fruchterman-Reingold Force-Directed"
)
ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes, fontsize=8.5, verticalalignment='top',
        fontfamily='monospace', bbox=dict(boxstyle='round,pad=0.6', facecolor='#f8f9fa', edgecolor='#2b5797', linewidth=1.5))

# Cluster Legend
legend_patches = [
    patches.Patch(color=palette[0], label='Klaster 1: Media Keuangan & Pasar Modal Nasional'),
    patches.Patch(color=palette[1], label='Klaster 2: Media Regional Jawa Timur & Pemerintah'),
    patches.Patch(color=palette[2], label='Klaster 3: Kantor Berita & Media Sindikasi Kilat'),
    patches.Patch(color=palette[3], label='Klaster 4: Portal Multinasional & Edisi Bahasa Inggris')
]
ax.legend(handles=legend_patches, loc='lower right', frameon=True, facecolor='white', edgecolor='#cccccc', fontsize=8.5, title='Komunitas Jaringan (NodeXL Louvain)', title_fontsize=9)

ax.set_title("Gambar 1: NodeXL Overall Media Discourse Network — Bank Jatim (2021–2026)\n"
             "Struktur Topologi Jaringan Media Berdasarkan Keterikatan Liputan Isu Strategis",
             fontsize=13, fontweight='bold', pad=15, color='#1a1a1a')
ax.axis('off')
plt.tight_layout()
plt.savefig('fig1_nodexl_overall_discourse.png', dpi=300)
plt.close()
print("Saved fig1_nodexl_overall_discourse.png")

# ==========================================
# GAMBAR 2: NodeXL Group-in-a-Box Clustered Network
# ==========================================
fig, axs = plt.subplots(2, 3, figsize=(15, 10), dpi=300)
axs = axs.flatten()
topics_order = [
    'Kinerja Finansial & Laba Bersih',
    'Konsolidasi KUB & Sinergi BPD',
    'Pasar Modal, Saham & Tata Kelola',
    'Transformasi Digital & Layanan',
    'Ekspansi Kredit & Manajemen Risiko'
]
box_colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#d62728']

for idx, (topic, b_col) in enumerate(zip(topics_order, box_colors)):
    ax = axs[idx]
    sub_df = df[df['Topik'] == topic]
    top_media = sub_df['Media/Sumber'].value_counts().head(7)
    
    # Subgraph star network: Topic in center, media around
    G_sub = nx.Graph()
    G_sub.add_node(topic, node_type='Center', count=len(sub_df))
    for m, c in top_media.items():
        G_sub.add_node(m, node_type='Media', count=c)
        G_sub.add_edge(topic, m, weight=c)
        
    pos_sub = nx.spring_layout(G_sub, seed=10, k=0.7)
    nx.draw_networkx_nodes(G_sub, pos_sub, ax=ax,
                           node_color=[b_col if d['node_type']=='Center' else '#ffffff' for _, d in G_sub.nodes(data=True)],
                           node_size=[1400 if d['node_type']=='Center' else max(300, d['count']*150) for _, d in G_sub.nodes(data=True)],
                           edgecolors=b_col, linewidths=2)
    nx.draw_networkx_edges(G_sub, pos_sub, ax=ax, edge_color=b_col, alpha=0.6, width=[d['weight']*1.2 for _, _, d in G_sub.edges(data=True)])
    
    for n, (x, y) in pos_sub.items():
        if n == topic:
            ax.text(x, y, f"{n}\n(N={len(sub_df)})", ha='center', va='center', fontsize=7.5, fontweight='bold', color='white', wrap=True)
        else:
            ax.text(x, y+0.08, f"{n}\n({G_sub.nodes[n]['count']}x)", ha='center', va='bottom', fontsize=7.5, color='#222222',
                    bbox=dict(boxstyle='square,pad=0.15', facecolor='#fbfbfb', edgecolor='#dddddd', alpha=0.9))
    
    ax.set_title(f"Grup {idx+1}: {topic}", fontsize=10.5, fontweight='bold', color=b_col, pad=8)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(b_col)
        spine.set_linewidth(1.8)

# 6th panel: Topic share summary bar chart
ax_last = axs[5]
topic_counts = df['Topik'].value_counts().loc[topics_order]
bars = ax_last.barh(range(len(topic_counts)), topic_counts.values, color=box_colors, alpha=0.85, edgecolor='black', linewidth=0.8)
ax_last.set_yticks(range(len(topic_counts)))
ax_last.set_yticklabels([t.split('&')[0].strip() for t in topics_order], fontsize=8.5)
ax_last.invert_yaxis()
ax_last.set_xlabel("Jumlah Publikasi Berita", fontsize=9)
ax_last.set_title("Proporsi Topik Narasi Bank Jatim", fontsize=10.5, fontweight='bold', pad=8)
for bar in bars:
    w = bar.get_width()
    pct = (w / len(df)) * 100
    ax_last.text(w + 1, bar.get_y() + bar.get_height()/2, f"{int(w)} ({pct:.1f}%)", va='center', fontsize=8.5, fontweight='bold')
ax_last.set_xlim(0, max(topic_counts.values) + 12)

fig.suptitle("Gambar 2: NodeXL Group-in-a-Box Clustered Network — 5 Pilar Narasi Utama Bank Jatim\n"
             "Pengelompokan Berita Berdasarkan Klaster Tematik & Media Dominan Tiap Pilar",
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('fig2_nodexl_group_in_a_box.png', dpi=300)
plt.close()
print("Saved fig2_nodexl_group_in_a_box.png")

# ==========================================
# GAMBAR 3: Semantic Co-occurrence Network
# ==========================================
key_terms = ['Laba', 'KUB', 'BPD', 'Dividen', 'Saham', 'Kredit', 'Digital', 'Syariah', 'Aset', 'RUPST',
             'Konsolidasi', 'KPR', 'UMKM', 'JConnect', 'Pendapatan', 'Komisaris', 'Mitigasi', 'Modal']
term_cooc = defaultdict(int)
term_freq = Counter()

for title in df['Judul']:
    t = title.lower()
    matched = []
    for term in key_terms:
        if term.lower() in t:
            matched.append(term)
            term_freq[term] += 1
    for i in range(len(matched)):
        for j in range(i + 1, len(matched)):
            term_cooc[(matched[i], matched[j])] += 1

G_sem = nx.Graph()
for term in key_terms:
    if term_freq[term] > 0:
        G_sem.add_node(term, freq=term_freq[term])

for (t1, t2), weight in term_cooc.items():
    if weight >= 1:
        G_sem.add_edge(t1, t2, weight=weight)

fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
pos_sem = nx.kamada_kawai_layout(G_sem)

node_sizes_sem = [max(350, term_freq[n] * 65) for n in G_sem.nodes()]
node_colors_sem = [term_freq[n] for n in G_sem.nodes()]

edges_sem = G_sem.edges(data=True)
max_sw = max([d['weight'] for _, _, d in edges_sem]) if edges_sem else 1
for u, v, d in edges_sem:
    w = d['weight']
    ax.plot([pos_sem[u][0], pos_sem[v][0]], [pos_sem[u][1], pos_sem[v][1]],
            color='#1f77b4', alpha=min(0.85, 0.2 + (w/max_sw)*0.7), linewidth=1 + (w/max_sw)*4)

sc = nx.draw_networkx_nodes(G_sem, pos_sem, ax=ax, node_color=node_colors_sem, cmap='YlOrRd',
                       node_size=node_sizes_sem, edgecolors='#444444', linewidths=1.5)
plt.colorbar(sc, ax=ax, label='Frekuensi Kemunculan Kata Kunci', shrink=0.7)

for n, (x, y) in pos_sem.items():
    ax.text(x, y, f"{n}\n({term_freq[n]})", ha='center', va='center', fontsize=8.5, fontweight='bold',
            color='#111111' if term_freq[n] < 20 else '#ffffff', zorder=3)

ax.set_title("Gambar 3: Semantic Co-occurrence Network — Hubungan Asosiasi Kata Kunci Berita Bank Jatim\n"
             "Keterkaitan Antar Isu Strategis (Laba, KUB, BPD, Dividen, dan Kredit Konsolidasi)",
             fontsize=12.5, fontweight='bold', pad=15)
ax.axis('off')
plt.tight_layout()
plt.savefig('fig3_nodexl_semantic_cooccurrence.png', dpi=300)
plt.close()
print("Saved fig3_nodexl_semantic_cooccurrence.png")

# ==========================================
# GAMBAR 4: Centrality Quadrant Matrix
# ==========================================
fig, ax = plt.subplots(figsize=(11, 8), dpi=300)

nodes_plot = list(G_media.nodes())
x_vals = [deg_cent[n] for n in nodes_plot]
y_vals = [bet_cent[n] for n in nodes_plot]
counts = [B.nodes[n]['count'] for n in nodes_plot]

med_x = np.median(x_vals)
med_y = np.median(y_vals)

ax.scatter(x_vals, y_vals, s=[max(120, c * 35) for c in counts],
           c=[palette[community_map.get(n, 0) % len(palette)] for n in nodes_plot],
           alpha=0.85, edgecolors='black', linewidth=1)

# Quadrant dividing lines
ax.axvline(med_x, color='#999999', linestyle='--', linewidth=1.2, alpha=0.7)
ax.axhline(med_y, color='#999999', linestyle='--', linewidth=1.2, alpha=0.7)

# Quadrant Labels
ax.text(max(x_vals)*0.95, max(y_vals)*0.95, "Kuadran I:\nCORE INFLUENCER / AGENDA SETTER\n(High Degree, High Betweenness)",
        ha='right', va='top', fontsize=8.5, fontweight='bold', color='#2b5797', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f0fe', edgecolor='#2b5797'))
ax.text(min(x_vals)*1.05, max(y_vals)*0.95, "Kuadran II:\nSTRATEGIC BRIDGES / BROKERS\n(Low Degree, High Betweenness)",
        ha='left', va='top', fontsize=8.5, fontweight='bold', color='#0f9d58', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e6f4ea', edgecolor='#0f9d58'))
ax.text(min(x_vals)*1.05, min(y_vals)+0.005, "Kuadran III:\nNICHE / REGIONAL SPECIALISTS\n(Low Degree, Low Betweenness)",
        ha='left', va='bottom', fontsize=8.5, fontweight='bold', color='#d93025', bbox=dict(boxstyle='round,pad=0.3', facecolor='#fce8e6', edgecolor='#d93025'))
ax.text(max(x_vals)*0.95, min(y_vals)+0.005, "Kuadran IV:\nHIGH-FREQUENCY BROADCASTERS\n(High Degree, Low Betweenness)",
        ha='right', va='bottom', fontsize=8.5, fontweight='bold', color='#f2994a', bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff0e6', edgecolor='#f2994a'))

# Label top points
for n, x, y, c in zip(nodes_plot, x_vals, y_vals, counts):
    if c >= 6 or y >= np.percentile(y_vals, 75):
        ax.annotate(f"{n}\n(N={c})", (x, y), xytext=(4, 5), textcoords='offset points',
                    fontsize=8, fontweight='bold' if c>=10 else 'normal',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='#cccccc'))

ax.set_xlabel("Degree Centrality (Konektivitas & Cakupan Liputan)", fontsize=10, fontweight='bold')
ax.set_ylabel("Betweenness Centrality (Peran Perantara / Bridging Role)", fontsize=10, fontweight='bold')
ax.set_title("Gambar 4: NodeXL Centrality Matrix — Pemetaan Pengaruh Media Pemberita Bank Jatim\n"
             "Analisis Kuadran Pengaruh Antara Volume Berita (Degree) dan Kekuatan Penghubung (Betweenness)",
             fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('fig4_nodexl_centrality_quadrant.png', dpi=300)
plt.close()
print("Saved fig4_nodexl_centrality_quadrant.png")

# ==========================================
# GAMBAR 5: Temporal Network Evolution
# ==========================================
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)

yearly_topic = pd.crosstab(df['Tahun'], df['Topik'])
years = yearly_topic.index.tolist()

bar_bottom = np.zeros(len(years))
for idx, (topic, col) in enumerate(zip(topics_order, box_colors)):
    if topic in yearly_topic.columns:
        vals = yearly_topic[topic].values
        ax.bar(years, vals, bottom=bar_bottom, label=topic, color=col, alpha=0.88, edgecolor='black', linewidth=0.7)
        for i, (yr, v) in enumerate(zip(years, vals)):
            if v >= 3:
                ax.text(yr, bar_bottom[i] + v/2, f"{v}", ha='center', va='center', fontsize=8, fontweight='bold', color='white')
        bar_bottom += vals

# Strategic Milestone Annotations
milestones = {
    2021: "Pemulihan Pandemi &\nRestrukturisasi Kredit",
    2022: "Akselerasi JConnect &\nPenguatan Modal",
    2023: "Inisiasi Skema KUB &\nRekor Dividen Rp797 M",
    2024: "MoU KUB BPD NTB Syariah\n& Bank Lampung",
    2025: "Integrasi KUB 5 BPD &\nKredit Tumbuh 41%",
    2026: "Laba Kuartal Melonjak 61% &\nVisi BPD Terbesar Nasional"
}
for yr, txt in milestones.items():
    tot = bar_bottom[years.index(yr)]
    ax.annotate(txt, xy=(yr, tot), xytext=(yr, tot + 4),
                ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1a1a1a',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#fffbe6', edgecolor='#d4b106', linewidth=1.2),
                arrowprops=dict(arrowstyle='->', color='#d4b106', lw=1.2))

ax.set_ylim(0, max(bar_bottom) + 12)
ax.set_xticks(years)
ax.set_xticklabels([f"Tahun {y}\n(Total: {int(bar_bottom[i])})" for i, y in enumerate(years)], fontsize=9, fontweight='bold')
ax.set_ylabel("Volume Publikasi Berita Terverifikasi", fontsize=10, fontweight='bold')
ax.set_title("Gambar 5: NodeXL Temporal Dynamics (2021–2026) — Evolusi Topik & Isu Strategis Bank Jatim\n"
             "Pergeseran Fokus Narasi dari Restrukturisasi Pasca-Pandemi ke Konsolidasi KUB dan Rekor Laba",
             fontsize=12, fontweight='bold', pad=15)
ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#cccccc', fontsize=8.5)
plt.tight_layout()
plt.savefig('fig5_nodexl_temporal_evolution.png', dpi=300)
plt.close()
print("Saved fig5_nodexl_temporal_evolution.png")

# ==========================================
# EXPORT NODEXL-READY WORKBOOK
# ==========================================
edges_data = []
for u, v, d in G_media.edges(data=True):
    edges_data.append({
        'Vertex 1': u,
        'Vertex 2': v,
        'Relationship': 'Shared Topics Coverage',
        'Relationship Date': '2021-2026',
        'Edge Weight': d['weight'],
        'Edge Width': min(5, 1 + d['weight'] * 0.3),
        'Edge Color': '#999999',
        'Edge Alpha': min(100, int(20 + d['weight'] * 10))
    })

vertices_data = []
for n in G_media.nodes():
    vertices_data.append({
        'Vertex': n,
        'Cluster / Group': f"Grup {community_map.get(n, 0) + 1}",
        'Degree': G_media.degree(n),
        'Degree Centrality': round(deg_cent[n], 4),
        'Betweenness Centrality': round(bet_cent[n], 4),
        'Closeness Centrality': round(close_cent[n], 4),
        'News Volume Count': B.nodes[n]['count'],
        'Vertex Shape': 'Disk',
        'Vertex Color': palette[community_map.get(n, 0) % len(palette)],
        'Vertex Radius': min(25, max(5, int(B.nodes[n]['count'] * 1.5)))
    })

overall_metrics = [
    {'Metric': 'Graph Type', 'Value': 'Undirected Weighted Media Network'},
    {'Metric': 'Total Vertices (Nodes)', 'Value': G_media.number_of_nodes()},
    {'Metric': 'Total Edges (Ties)', 'Value': G_media.number_of_edges()},
    {'Metric': 'Unique Edges', 'Value': G_media.number_of_edges()},
    {'Metric': 'Edges With Duplicates', 'Value': 0},
    {'Metric': 'Total Total News Analyzed', 'Value': len(df)},
    {'Metric': 'Graph Density', 'Value': round(nx.density(G_media), 4)},
    {'Metric': 'NodeXL Modularity Index', 'Value': round(nx_comm.modularity(G_media, communities), 4)},
    {'Metric': 'Average Geodesic Distance', 'Value': round(nx.average_shortest_path_length(G_media), 4) if nx.is_connected(G_media) else 'N/A (Multi-component)'},
    {'Metric': 'Average Clustering Coefficient', 'Value': round(nx.average_clustering(G_media), 4)}
]

with pd.ExcelWriter('nodexl_bankjatim_network.xlsx', engine='openpyxl') as xw:
    pd.DataFrame(edges_data).to_excel(xw, sheet_name='Edges', index=False)
    pd.DataFrame(vertices_data).to_excel(xw, sheet_name='Vertices', index=False)
    pd.DataFrame(overall_metrics).to_excel(xw, sheet_name='Overall Metrics', index=False)
    df.to_excel(xw, sheet_name='Raw News Data', index=False)

print("Exported nodexl_bankjatim_network.xlsx successfully!")
