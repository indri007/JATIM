"""
Unit tests for User Experience testing workbook (Uji_Pengalaman_Pengguna_BankJatim_FINAL.xlsx).
"""
from pathlib import Path
import openpyxl
import pytest

WORKBOOK_PATH = Path(__file__).parent.parent / "Uji_Pengalaman_Pengguna_BankJatim_FINAL.xlsx"

def test_workbook_file_exists():
    assert WORKBOOK_PATH.exists(), f"Workbook {WORKBOOK_PATH} does not exist"

def test_all_five_sheets_exist():
    wb = openpyxl.load_workbook(WORKBOOK_PATH)
    expected_sheets = ["Petunjuk", "Tugas", "SUS", "Ringkasan", "Sintesis"]
    for s in expected_sheets:
        assert s in wb.sheetnames, f"Sheet {s} not found in workbook"

def test_tugas_sheet_scenarios_and_respondents():
    wb = openpyxl.load_workbook(WORKBOOK_PATH)
    ws = wb["Tugas"]
    # 5 scenarios * 3 respondents = 15 task rows (rows 5 to 19)
    assert ws.max_row >= 19
    scenarios = set()
    respondents = set()
    for r in range(5, 20):
        tid = ws.cell(row=r, column=1).value
        resp = ws.cell(row=r, column=3).value
        if tid:
            scenarios.add(tid)
        if resp:
            respondents.add(resp)
    assert scenarios == {"T1", "T2", "T3", "T4", "T5"}
    assert respondents == {"Reza", "Agus", "Yudis"}

def test_sus_sheet_statements_count():
    wb = openpyxl.load_workbook(WORKBOOK_PATH)
    ws = wb["SUS"]
    statements = [ws.cell(row=r, column=2).value for r in range(5, 15)]
    assert len(statements) == 10
    # Check SUS row formula exists
    assert "SUM" in str(ws.cell(row=15, column=3).value)

