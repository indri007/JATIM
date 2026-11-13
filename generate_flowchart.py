#!/usr/bin/env python3
"""
Generate crisp, publication-grade flowchart diagram for BATAS Zero Trust Architecture & Forensic Pipeline.
"""
import os
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.style.use('default')
fig, ax = plt.subplots(figsize=(12, 14), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 140)
ax.axis('off')

def draw_box(x, y, w, h, text, title="", color="#2b5797", text_color="white", shape="round", fontsize=9, title_fontsize=10):
    boxstyle = "round,pad=0.5,rounding_size=0.8" if shape == "round" else "square,pad=0.5"
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=boxstyle, facecolor=color, edgecolor="#1a365d", linewidth=1.5, zorder=2)
    ax.add_patch(rect)
    if title:
        ax.text(x + w/2, y + h - 3, title, ha='center', va='top', fontsize=title_fontsize, fontweight='bold', color=text_color, zorder=3)
        ax.text(x + w/2, y + (h-4)/2, text, ha='center', va='center', fontsize=fontsize, color=text_color, wrap=True, zorder=3)
    else:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=text_color, wrap=True, zorder=3)

def draw_diamond(cx, cy, size, text, color="#d97706", text_color="white"):
    d = patches.Polygon([[cx, cy + size], [cx + size*1.5, cy], [cx, cy - size], [cx - size*1.5, cy]],
                        facecolor=color, edgecolor="#92400e", linewidth=1.5, zorder=2)
    ax.add_patch(d)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=text_color, zorder=3)

def draw_arrow(x1, y1, x2, y2, label="", color="#475569", lw=2, label_offset=(0, 2)):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=15), zorder=1)
    if label:
        mx, my = (x1 + x2)/2 + label_offset[0], (y1 + y2)/2 + label_offset[1]
        ax.text(mx, my, label, fontsize=8, fontweight='bold', color="#1e293b",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor="#cbd5e1", alpha=0.9), zorder=4)

# Top Title Header
ax.text(50, 136, "DIAGRAM ALIR OTORISASI ZERO TRUST & FORENSIK DIGITAL BATAS",
        ha='center', va='center', fontsize=12.5, fontweight='bold', color="#0f172a")
ax.text(50, 133, "Sistem Pengamanan Otoritas Agen AI & Penelusuran Transaksi Terintegrasi Bank Jatim",
        ha='center', va='center', fontsize=9.5, style='italic', color="#475569")

# Step 1: User / Agent Ingress
draw_box(20, 120, 60, 9, "Instruksi Transaksi Finansial dari Nasabah / LLM Agent\n(Teks Bebas, Percakapan Alami, atau API Ingress)",
         title="1. PERMINTAAN TRANSAKSI MASUK (INGRESS)", color="#1e293b", text_color="#f8fafc")

# Arrow 1 -> 2
draw_arrow(50, 120, 50, 111)

# Step 2: Task Token Generation & Scope Verification
draw_box(15, 99, 70, 12, "Ekstraksi Sesi Terotentikasi & Penerbitan Ephemeral Task Token\n• Token Scopes (read:balance, transfer:retail_p2p)\n• Parameter Payload (source_account, dest_account, amount)\n• Anti-Replay TTL (expires_at)",
         title="2. POLICY ENFORCEMENT POINT (BATAS PEP)", color="#2563eb", text_color="#ffffff")

# Arrow 2 -> 3
draw_arrow(50, 99, 50, 90)

# Step 3: Decision Diamond (Token Expiration & Scope Check)
draw_diamond(50, 82, 7.5, "Apakah Token\nValid & Scope\nSesuai?", color="#0284c7")

# Branch DENY (Left)
draw_arrow(38.5, 82, 16, 82, label="TIDAK (Scope / TTL Saldo Habis)")
draw_box(2, 74, 28, 16, "PENCEGAHAN PELANGGARAN\n• Status: DENY (Blokir Eksekusi)\n• Reason: 'Token Expired / Missing Scope'\n• Netralisasi Injeksi Otomatis",
         title="BLOKIR DETERMINISTIK", color="#dc2626", text_color="#ffffff")

# From Deny -> Forensic Log
draw_arrow(16, 74, 16, 44)

# Branch YES (Down to Rule 4 Kasda)
draw_arrow(50, 74.5, 50, 66, label="YA (Token Valid)")

# Step 4: Kas Daerah & High Value Decision Diamond
draw_diamond(50, 58, 8, "Apakah Rekening\nKAS DAERAH\natau Nominal\n> Rp10 Juta?", color="#d97706")

# Branch YES -> Step-Up HITL Dual Control (Right)
draw_arrow(62, 58, 84, 58, label="YA (Kasda / High Value)")
draw_box(70, 48, 28, 18, "PADK OJK 1/2026 MANDAT:\n• Rekening Kasda (REK-KASDA)\n• Dual-Control Approval\n• Verifikasi Maker-Checker\n• Step-Up Biometrik Pejabat",
         title="HUMAN-IN-THE-LOOP (HITL)", color="#ea580c", text_color="#ffffff")

# HITL Approved -> Core Banking
draw_arrow(84, 48, 84, 28)
draw_arrow(84, 28, 68, 28, label="Disetujui Manusia")

# Branch NO (Direct Retail Transfer <= 10M)
draw_arrow(50, 50, 50, 36, label="TIDAK (Retail Reguler <= 10M)")

# Step 5: Core Banking Execution
draw_box(32, 22, 36, 14, "EKSEKUSI BUKU BESAR (CORE BANKING)\n• Validasi Invarian Saldo (Balance Invariant)\n• Settlement BI-FAST / Kliring Real-Time\n• Pembaruan Mutasi Rekening Nasabah",
         title="3. CORE BANKING LEDGER", color="#16a34a", text_color="#ffffff")

# Step 6: Immutable Forensic Log Engine (Bottom)
draw_box(6, 4, 88, 14, "JEJAK AUDIT FORENSIK DIGITAL ANTI-TAMPER (POJK 11/POJK.03/2022 PASAL 24)\n• Logging Terpusat (Promtail -> Grafana Loki 3.2)\n• SHA-256 Hash Chaining & Cryptographic Non-Repudiation Timestamping\n• Pemetaan Status Kepatuhan Otomatis (PostgreSQL Compliance Table)",
         title="4. FORENSIC AUDIT TRAIL & WORM STORAGE", color="#0f172a", text_color="#38bdf8")

# Arrows to Logging
draw_arrow(50, 22, 50, 18)
draw_arrow(16, 44, 16, 18)

plt.tight_layout()
plt.savefig('fig_flowchart_batas_zero_trust.png', dpi=300)
plt.close()
print("Saved fig_flowchart_batas_zero_trust.png")
