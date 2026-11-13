import hashlib
import pathlib
import sys
import time
import os
import requests

HEADERS = {"User-Agent": "BATAS-research/0.1 (contact: indri.cs2026@ids.ac.id)"}

def fetch(url: str, out_dir: str = "sources") -> pathlib.Path:
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    name = url.split("/")[-1].split("?")[0] or "download.bin"
    path = out / requests.utils.unquote(name)
    with requests.get(url, headers=HEADERS, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"{path}  {path.stat().st_size:,} bytes  sha256={sha[:16]}…  {r.headers.get('Content-Type')}")
    time.sleep(2)
    return path

# -----------------------------------------------------------------------------
# Streamlit Cloud Entrypoint Bridge
# Streamlit Cloud is configured to execute BATAS/fetch_sources.py
# When run under Streamlit, bridge directly into root streamlit_app.py
# -----------------------------------------------------------------------------
try:
    import streamlit as st
    is_streamlit = True
except ImportError:
    is_streamlit = False

if is_streamlit:
    root_dir = pathlib.Path(__file__).resolve().parent.parent
    os.chdir(root_dir)
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    
    app_file = root_dir / "streamlit_app.py"
    if app_file.exists():
        with open(app_file, "r", encoding="utf-8") as f:
            code = f.read()
        exec(compile(code, str(app_file), "exec"), globals())
    else:
        st.error(f"Berkas streamlit_app.py tidak ditemukan di {root_dir}")

if __name__ == "__main__":
    if not is_streamlit and len(sys.argv) > 1:
        for u in sys.argv[1:]:
            fetch(u)
