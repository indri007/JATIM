"""
Generator workbook Uji Pengalaman Pengguna Dashboard Bank Jatim.
Menghasilkan file: Uji_Pengalaman_Pengguna_BankJatim_FINAL.xlsx
Jalankan: pip install openpyxl && python buat_workbook_uji.py
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter

# ---------- Style helpers ----------
YELLOW = PatternFill("solid", fgColor="FFF2CC")
GRAY = PatternFill("solid", fgColor="E7E6E6")
HEADER = PatternFill("solid", fgColor="305496")
GREEN = PatternFill("solid", fgColor="C6EFCE")
RED = PatternFill("solid", fgColor="FFC7CE")
ORANGE = PatternFill("solid", fgColor="FFEB9C")
BOLD = Font(bold=True)
WHITE_BOLD = Font(bold=True, color="FFFFFF")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def style_range(ws, cell_range, fill=None, font=None, align=None, border=True):
    for row in ws[cell_range]:
        for c in row:
            if fill: c.fill = fill
            if font: c.font = font
            if align: c.alignment = align
            if border: c.border = BORDER


def header_row(ws, row, values, widths=None):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=i, value=v)
        c.fill = HEADER
        c.font = WHITE_BOLD
        c.alignment = CENTER
        c.border = BORDER
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w


wb = Workbook()

# =========================================================
# SHEET 1 — PETUNJUK
# =========================================================
ws = wb.active
ws.title = "Petunjuk"
ws["A1"] = "Lembar Uji Pengalaman Pengguna – Dashboard Bank Jatim (Auditor Forensik)"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:H1")

petunjuk = [
    ("", ""),
    ("Cara pakai:", ""),
    ("1. Sheet Tugas", "Isi hasil tiap skenario per responden (sel kuning). Satu baris = satu tugas oleh satu responden."),
    ("2. Sheet SUS", "Isi skor 1–5 (1 = sangat tidak setuju, 5 = sangat setuju) untuk 10 butir. Skor SUS dihitung otomatis."),
    ("3. Sheet Ringkasan", "Terisi otomatis dari Tugas dan SUS. Jangan diubah."),
    ("4. Sheet Sintesis", "Isi temuan kualitatif (sel kuning). Paragraf sintesis menyusun diri dari angka Ringkasan."),
    ("", ""),
    ("Legenda warna:", ""),
    ("Kuning", "Sel yang harus diisi manual dari sesi uji nyata."),
    ("Abu-abu", "Sel berisi rumus otomatis — jangan diubah."),
    ("", ""),
    ("Validasi input:", ""),
    ("Kolom 'Berhasil?'", "Dropdown Ya/Tidak."),
    ("Kolom 'Kesulitan'", "Angka 1–5."),
    ("Kolom 'Waktu'", "Angka desimal > 0."),
    ("Sheet SUS", "Angka 1–5."),
    ("", ""),
    ("Catatan penting:", ""),
    ("", "Workbook ini sengaja kosong. Data harus berasal dari sesi uji nyata Reza, Agus, dan Yudis."),
    ("", "Jangan menyalin data ilustrasi ke sheet Tugas/SUS."),
    ("", "Backup file sebelum mengisi data nyata."),
]
r = 3
for label, desc in petunjuk:
    ws.cell(row=r, column=1, value=label).font = BOLD
    ws.cell(row=r, column=2, value=desc).alignment = LEFT
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
    r += 1

ws.column_dimensions["A"].width = 22
ws.column_dimensions["B"].width = 90

# =========================================================
# SHEET 2 — TUGAS
# =========================================================
ws = wb.create_sheet("Tugas")
ws["A1"] = "Hasil Skenario Tugas per Responden"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:H1")
ws["A2"] = "Isi sel kuning dari sesi uji yang sebenarnya."
ws["A2"].font = Font(italic=True, color="808080")
ws.merge_cells("A2:H2")

headers = ["ID", "Skenario", "Responden", "Berhasil? (Ya/Tidak)",
           "Waktu (menit)", "Kesulitan (1–5)",
           "Kendala yang ditemui", "Catatan / kutipan"]
header_row(ws, 4, headers, widths=[6, 45, 12, 16, 12, 12, 30, 30])

skenario = {
    "T1": "Menelusuri transaksi mencurigakan berdasarkan nominal atau rekening",
    "T2": "Memfilter data berdasarkan periode waktu tertentu",
    "T3": "Melacak alur dana antar rekening",
    "T4": "Mengidentifikasi anomali atau pola tidak wajar pada dashboard",
    "T5": "Mengekspor temuan sebagai bukti atau laporan",
}
responden = ["Reza", "Agus", "Yudis"]

row = 5
for tid, desc in skenario.items():
    for resp in responden:
        ws.cell(row=row, column=1, value=tid).alignment = CENTER
        ws.cell(row=row, column=2, value=desc).alignment = LEFT
        ws.cell(row=row, column=3, value=resp).alignment = CENTER
        # kuning = input manual
        for col in [4, 5, 6, 7, 8]:
            c = ws.cell(row=row, column=col)
            c.fill = YELLOW
            c.border = BORDER
            c.alignment = CENTER if col in [4, 5, 6] else LEFT
        for col in [1, 2, 3]:
            ws.cell(row=row, column=col).border = BORDER
        row += 1

# Data validation
dv_ya = DataValidation(type="list", formula1='"Ya,Tidak"', allow_blank=True,
                       showErrorMessage=True, errorTitle="Input salah",
                       error="Pilih Ya atau Tidak")
ws.add_data_validation(dv_ya)
dv_ya.add("D5:D19")

dv_kesulitan = DataValidation(type="whole", operator="between", formula1="1",
                              formula2="5", allow_blank=True,
                              showErrorMessage=True, errorTitle="Input salah",
                              error="Kesulitan harus 1–5")
ws.add_data_validation(dv_kesulitan)
dv_kesulitan.add("F5:F19")

dv_waktu = DataValidation(type="decimal", operator="greaterThan", formula1="0",
                          allow_blank=True, showErrorMessage=True,
                          errorTitle="Input salah",
                          error="Waktu harus angka > 0")
ws.add_data_validation(dv_waktu)
dv_waktu.add("E5:E19")

# Conditional formatting: Ya hijau, Tidak merah
ws.conditional_formatting.add("D5:D19",
    CellIsRule(operator="equal", formula=['"Ya"'], fill=GREEN))
ws.conditional_formatting.add("D5:D19",
    CellIsRule(operator="equal", formula=['"Tidak"'], fill=RED))

# =========================================================
# SHEET 3 — SUS
# =========================================================
ws = wb.create_sheet("SUS")
ws["A1"] = "System Usability Scale (SUS)"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:I1")
ws["A2"] = "Skor 1–5 per butir. Kolom G–I = kontribusi otomatis (ganjil = skor−1, genap = 5−skor)."
ws["A2"].font = Font(italic=True, color="808080")
ws.merge_cells("A2:I2")

headers = ["No", "Pernyataan", "Reza", "Agus", "Yudis", "",
           "Kontribusi Reza", "Kontribusi Agus", "Kontribusi Yudis"]
header_row(ws, 4, headers, widths=[5, 60, 8, 8, 8, 2, 14, 14, 14])

pernyataan = [
    "Saya pikir saya akan sering menggunakan aplikasi ini.",
    "Saya merasa aplikasi ini terlalu rumit tanpa perlu.",
    "Saya merasa aplikasi ini mudah digunakan.",
    "Saya merasa membutuhkan bantuan orang teknis untuk dapat menggunakan aplikasi ini.",
    "Saya merasa fungsi-fungsi dalam aplikasi ini terintegrasi dengan baik.",
    "Saya merasa ada terlalu banyak inkonsistensi dalam aplikasi ini.",
    "Saya membayangkan kebanyakan orang akan cepat belajar menggunakan aplikasi ini.",
    "Saya merasa aplikasi ini sangat membingungkan.",
    "Saya merasa sangat percaya diri menggunakan aplikasi ini.",
    "Saya perlu belajar banyak hal sebelum dapat menggunakan aplikasi ini.",
]

for i, p in enumerate(pernyataan, start=1):
    r = 4 + i
    ws.cell(row=r, column=1, value=i).alignment = CENTER
    ws.cell(row=r, column=2, value=p).alignment = LEFT
    for col in [3, 4, 5]:
        c = ws.cell(row=r, column=col)
        c.fill = YELLOW
        c.alignment = CENTER
        c.border = BORDER
    # kolom F kosong (pemisah)
    for col in [7, 8, 9]:
        src = get_column_letter(col - 4)  # G->C, H->D, I->E
        ganjil = i % 2 == 1
        if ganjil:
            formula = f'=IF({src}{r}="","",{src}{r}-1)'
        else:
            formula = f'=IF({src}{r}="","",5-{src}{r})'
        c = ws.cell(row=r, column=col, value=formula)
        c.fill = GRAY
        c.alignment = CENTER
        c.border = BORDER
    for col in [1, 2]:
        ws.cell(row=r, column=col).border = BORDER

# Baris skor SUS (baris 15)
ws.cell(row=15, column=2, value="Skor SUS (0–100)").font = BOLD
ws.cell(row=15, column=2).alignment = LEFT
for col, letter in [(3, "C"), (4, "D"), (5, "E")]:
    c = ws.cell(row=15, column=col)
    c.value = f'=IF(COUNT({letter}5:{letter}14)=10,SUM({get_column_letter(col+4)}5:{get_column_letter(col+4)}14)*2.5,"")'
    c.fill = GRAY
    c.alignment = CENTER
    c.font = BOLD
    c.border = BORDER

# Baris kategori (16)
ws.cell(row=16, column=2, value="Kategori").font = BOLD
for col, letter in [(3, "C"), (4, "D"), (5, "E")]:
    c = ws.cell(row=16, column=col)
    c.value = (f'=IF({letter}15="","",'
               f'IF({letter}15>=85,"Sangat baik",'
               f'IF({letter}15>=68,"Baik (di atas rata-rata)",'
               f'IF({letter}15>=51,"Marjinal","Buruk"))))')
    c.fill = GRAY
    c.alignment = CENTER
    c.border = BORDER

# Rata-rata SUS (17)
ws.cell(row=17, column=2, value="Rata-rata SUS (semua responden)").font = BOLD
c = ws.cell(row=17, column=3, value='=IFERROR(AVERAGE(C15:E15),"")')
c.fill = GRAY
c.font = BOLD
c.alignment = CENTER
c.border = BORDER

# Catatan acuan (19)
ws.cell(row=19, column=2,
        value="Acuan kategori: ≥85 sangat baik; 68–84,9 baik; 51–67,9 marjinal; <51 buruk (ambang umum SUS).").font = Font(italic=True, color="808080")

# Data validation SUS 1-5
dv_sus = DataValidation(type="whole", operator="between", formula1="1",
                        formula2="5", allow_blank=True,
                        showErrorMessage=True, errorTitle="Input salah",
                        error="Skor SUS harus 1–5")
ws.add_data_validation(dv_sus)
dv_sus.add("C5:E14")

# Conditional formatting skor SUS
ws.conditional_formatting.add("C15:E15",
    CellIsRule(operator="lessThan", formula=["51"], fill=RED))
ws.conditional_formatting.add("C15:E15",
    CellIsRule(operator="between", formula=["51", "67.9"], fill=ORANGE))
ws.conditional_formatting.add("C15:E15",
    CellIsRule(operator="between", formula=["68", "84.9"], fill=GREEN))
ws.conditional_formatting.add("C15:E15",
    CellIsRule(operator="greaterThanOrEqual", formula=["85"],
               fill=PatternFill("solid", fgColor="00B050")))

# =========================================================
# SHEET 4 — RINGKASAN (otomatis)
# =========================================================
ws = wb.create_sheet("Ringkasan")
ws["A1"] = "Ringkasan Hasil (otomatis)"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:H1")

headers = ["Responden", "Tugas dinilai", "Tugas berhasil",
           "Tingkat keberhasilan", "Rata-rata waktu (menit)",
           "Rata-rata kesulitan (1–5)", "Skor SUS", "Kategori SUS"]
header_row(ws, 4, headers,
           widths=[14, 12, 12, 14, 14, 14, 10, 22])

responden_rows = [("Reza", 5, "C", 5), ("Agus", 6, "D", 6), ("Yudis", 7, "E", 7)]
for name, r, sus_col, _ in responden_rows:
    ws.cell(row=r, column=1, value=name).alignment = CENTER
    ws.cell(row=r, column=2, value=f'=COUNTIFS(Tugas!$C$5:$C$19,A{r},Tugas!$D$5:$D$19,"<>")')
    ws.cell(row=r, column=3, value=f'=COUNTIFS(Tugas!$C$5:$C$19,A{r},Tugas!$D$5:$D$19,"Ya")')
    ws.cell(row=r, column=4, value=f'=IF(B{r}=0,"",C{r}/B{r})')
    ws.cell(row=r, column=5, value=f'=IFERROR(AVERAGEIFS(Tugas!$E$5:$E$19,Tugas!$C$5:$C$19,A{r}),"")')
    ws.cell(row=r, column=6, value=f'=IFERROR(AVERAGEIFS(Tugas!$F$5:$F$19,Tugas!$C$5:$C$19,A{r}),"")')
    ws.cell(row=r, column=7, value=f'=SUS!{sus_col}15')
    ws.cell(row=r, column=8, value=f'=SUS!{sus_col}16')
    for col in range(1, 9):
        c = ws.cell(row=r, column=col)
        c.fill = GRAY
        c.border = BORDER
        c.alignment = CENTER if col != 8 else LEFT

# Keseluruhan (baris 8)
ws.cell(row=8, column=1, value="Keseluruhan").font = BOLD
ws.cell(row=8, column=2, value='=SUM(B5:B7)')
ws.cell(row=8, column=3, value='=SUM(C5:C7)')
ws.cell(row=8, column=4, value='=IF(B8=0,"",C8/B8)')
ws.cell(row=8, column=5, value='=IFERROR(AVERAGE(Tugas!$E$5:$E$19),"")')
ws.cell(row=8, column=6, value='=IFERROR(AVERAGE(Tugas!$F$5:$F$19),"")')
ws.cell(row=8, column=7, value='=SUS!C17')
ws.cell(row=8, column=8,
        value='=IF(G8="","",IF(G8>=85,"Sangat baik",IF(G8>=68,"Baik (di atas rata-rata)",IF(G8>=51,"Marjinal","Buruk"))))')
for col in range(1, 9):
    c = ws.cell(row=8, column=col)
    c.fill = GRAY
    c.font = BOLD
    c.border = BORDER
    c.alignment = CENTER if col != 8 else LEFT

# Per skenario (baris 12-16)
ws.cell(row=11, column=1, value="Rincian per Skenario").font = BOLD
headers2 = ["Skenario", "Dinilai", "Berhasil", "Tingkat keberhasilan",
            "Rata-rata waktu (menit)", "Rata-rata kesulitan (1–5)"]
header_row(ws, 11, headers2 + ["", ""], widths=[14, 12, 12, 14, 14, 14, 10, 22])

for i, (tid, _) in enumerate(skenario.items(), start=12):
    ws.cell(row=i, column=1, value=f"{tid}: {skenario[tid]}")
    ws.cell(row=i, column=1).alignment = LEFT
    ws.cell(row=i, column=2, value=f'=COUNTIFS(Tugas!$A$5:$A$19,"{tid}",Tugas!$D$5:$D$19,"<>")')
    ws.cell(row=i, column=3, value=f'=COUNTIFS(Tugas!$A$5:$A$19,"{tid}",Tugas!$D$5:$D$19,"Ya")')
    ws.cell(row=i, column=4, value=f'=IF(B{i}=0,"",C{i}/B{i})')
    ws.cell(row=i, column=5, value=f'=IFERROR(AVERAGEIFS(Tugas!$E$5:$E$19,Tugas!$A$5:$A$19,"{tid}"),"")')
    ws.cell(row=i, column=6, value=f'=IFERROR(AVERAGEIFS(Tugas!$F$5:$F$19,Tugas!$A$5:$A$19,"{tid}"),"")')
    for col in range(1, 7):
        c = ws.cell(row=i, column=col)
        c.fill = GRAY
        c.border = BORDER
        c.alignment = LEFT if col == 1 else CENTER

# =========================================================
# SHEET 5 — SINTESIS
# =========================================================
ws = wb.create_sheet("Sintesis")
ws["A1"] = "Sintesis Pengalaman Pengguna"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:B1")
ws["A2"] = "Isi sel kuning (kualitatif). Paragraf sintesis menyusun diri otomatis."
ws["A2"].font = Font(italic=True, color="808080")
ws.merge_cells("A2:B2")

labels = [
    (4, "Temuan positif yang konsisten"),
    (5, "Hambatan utama (muncul pada >1 responden)"),
    (6, "Saran perbaikan yang paling sering disebut"),
    (7, "Penilaian keseluruhan & prioritas perbaikan"),
]
for r, label in labels:
    ws.cell(row=r, column=1, value=label).font = BOLD
    ws.cell(row=r, column=1).alignment = LEFT
    ws.cell(row=r, column=1).border = BORDER
    c = ws.cell(row=r, column=2)
    c.fill = YELLOW
    c.border = BORDER
    c.alignment = LEFT
    ws.row_dimensions[r].height = 60

# Paragraf otomatis (B9)
ws.cell(row=9, column=1, value="Paragraf sintesis (otomatis)").font = BOLD
ws.cell(row=9, column=1).alignment = LEFT

formula_paragraf = (
    '="Tiga auditor forensik (Reza, Agus, dan Yudis) menguji dashboard Bank Jatim melalui "'
    '&IF(Ringkasan!B8="","[..]",TEXT(Ringkasan!B8,"0"))'
    '&" penilaian tugas. Skor SUS rata-rata sebesar "'
    '&IF(Ringkasan!G8="","[..]",TEXT(Ringkasan!G8,"0.0"))'
    '&" (kategori "&IF(Ringkasan!H8="","[..]",Ringkasan!H8)&"). "'
    '&"Tingkat keberhasilan tugas "'
    '&IF(Ringkasan!D8="","[..]",TEXT(Ringkasan!D8,"0%"))'
    '&", dengan waktu rata-rata "'
    '&IF(Ringkasan!E8="","[..]",TEXT(Ringkasan!E8,"0.0"))'
    '&" menit/tugas dan kesulitan rata-rata "'
    '&IF(Ringkasan!F8="","[..]",TEXT(Ringkasan!F8,"0.0"))'
    '&"/5. Temuan positif: "&IF(B4="","[..]",B4)'
    '&". Hambatan utama: "&IF(B5="","[..]",B5)'
    '&". Saran perbaikan: "&IF(B6="","[..]",B6)'
    '&". Penilaian keseluruhan: "&IF(B7="","[..]",B7)&"."'
)
c = ws.cell(row=9, column=2, value=formula_paragraf)
c.fill = GRAY
c.alignment = LEFT
c.border = BORDER
ws.row_dimensions[9].height = 120

ws.cell(row=11, column=1,
        value="Bagian bertanda [..] belum terisi. Hapus tanda tersebut hanya dengan mengisi data nyata.").font = Font(italic=True, color="C00000")

ws.column_dimensions["A"].width = 45
ws.column_dimensions["B"].width = 90

# ---------- Simpan ----------
out = "Uji_Pengalaman_Pengguna_BankJatim_FINAL.xlsx"
wb.save(out)
print(f"✅ Berhasil dibuat: {out}")
