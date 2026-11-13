"""
Unit tests for NodeXL graph analysis and workbook data integrity.
"""
from pathlib import Path
import pandas as pd
import pytest

NODEXL_EXCEL = Path(__file__).parent.parent / "nodexl_bankjatim_network.xlsx"

def test_nodexl_file_exists():
    assert NODEXL_EXCEL.exists(), f"File {NODEXL_EXCEL} not found"

def test_nodexl_sheets_and_metrics():
    xl = pd.ExcelFile(NODEXL_EXCEL)
    assert "Edges" in xl.sheet_names
    assert "Vertices" in xl.sheet_names
    assert "Overall Metrics" in xl.sheet_names

    df_metrics = pd.read_excel(NODEXL_EXCEL, sheet_name="Overall Metrics")
    metrics_dict = dict(zip(df_metrics["Metric"], df_metrics["Value"]))

    assert metrics_dict.get("Total Vertices (Nodes)") == 27
    assert metrics_dict.get("Total Edges (Ties)") == 224
    assert metrics_dict.get("Total Total News Analyzed") == 174
    assert float(metrics_dict.get("Graph Density")) > 0.6

def test_vertices_degree_and_betweenness():
    df_vertices = pd.read_excel(NODEXL_EXCEL, sheet_name="Vertices")
    assert len(df_vertices) == 27
    # Bisnis.com should be top news volume
    top_v = df_vertices.sort_values(by="News Volume Count", ascending=False).iloc[0]
    assert top_v["Vertex"] == "Bisnis.com"
    assert top_v["News Volume Count"] == 38
