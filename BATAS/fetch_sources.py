import hashlib
import pathlib
import sys
import time
import requests

HEADERS = {"User-Agent": "BATAS-research/0.1 (contact: indri.cs2026@ids.ac.id)"}

def fetch(url: str, out_dir: str = "sources") -> pathlib.Path:
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    name = url.split("/")[-1].split("?")[0] or "download.bin"
    path = out / requests.utils.unquote(name)
    with requests.get(url, headers=HEADERS, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(path, "wb") as f:              # "wb" = tulis sebagai biner
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"{path}  {path.stat().st_size:,} bytes  sha256={sha[:16]}…  {r.headers.get('Content-Type')}")
    time.sleep(2)                                # jeda sopan antar-permintaan
    return path

if __name__ == "__main__":
    for u in sys.argv[1:]:
        fetch(u)
