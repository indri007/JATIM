"""
Unit tests for Bank Jatim 2021-2026 verified news dataset.
"""
from pathlib import Path
import pandas as pd
import re
import pytest

DATASET_FILE = Path(__file__).parent.parent / "Berita Bank Jatim 2021–2026 - Berita.csv"

def test_dataset_exists():
    assert DATASET_FILE.exists(), f"Dataset file not found at {DATASET_FILE}"

def test_dataset_structure_and_counts():
    df = pd.read_csv(DATASET_FILE)
    assert len(df) == 174, f"Expected 174 rows, got {len(df)}"
    expected_cols = ["No", "Tanggal Terbit", "Judul", "Media/Sumber", "Asal Sumber", "Jenis", "Link"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"

def test_no_missing_values():
    df = pd.read_csv(DATASET_FILE)
    null_counts = df.isnull().sum()
    assert null_counts.sum() == 0, f"Found null values in dataset: {null_counts}"

def test_valid_temporal_distribution():
    df = pd.read_csv(DATASET_FILE)
    years = df["Tanggal Terbit"].apply(lambda x: int(re.search(r"202[0-6]", str(x)).group(0)))
    counts = years.value_counts().to_dict()
    assert counts.get(2021) == 6
    assert counts.get(2022) == 22
    assert counts.get(2023) == 39
    assert counts.get(2024) == 35
    assert counts.get(2025) == 34
    assert counts.get(2026) == 38

def test_valid_urls():
    df = pd.read_csv(DATASET_FILE)
    for idx, url in enumerate(df["Link"]):
        assert str(url).startswith("http"), f"Invalid URL at row {idx}: {url}"
