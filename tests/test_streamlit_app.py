"""
Unit test for Streamlit master dashboard compilation and syntax integrity.
"""
from pathlib import Path
import py_compile
import pytest

APP_PATH = Path(__file__).parent.parent / "streamlit_app.py"

def test_streamlit_app_exists():
    assert APP_PATH.exists(), f"App file {APP_PATH} does not exist"

def test_streamlit_app_syntax_compile():
    # py_compile compiles python file to bytecode, raising PyCompileError on syntax error
    compiled = py_compile.compile(str(APP_PATH), doraise=True)
    assert compiled is not None
