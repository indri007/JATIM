#!/usr/bin/env bash
# =====================================================================
#  setup_batas.sh — semua langkah BATAS dalam satu perintah (macOS)
#  Pakai:  cd /Users/jevin/.gemini/antigravity-ide/scratch/BATAS
#          bash setup_batas.sh            # jalankan semua tahap
#          bash setup_batas.sh 3          # jalankan satu tahap saja (1-8)
# =====================================================================
set -euo pipefail

BATAS_DIR="${BATAS_DIR:-$(pwd)}"
cd "$BATAS_DIR"
STEP="${1:-all}"

ok()   { printf "\033[32m[OK]\033[0m %s\n" "$*"; }
info() { printf "\033[34m[..]\033[0m %s\n" "$*"; }
warn() { printf "\033[33m[!!]\033[0m %s\n" "$*"; }
run_step() { [[ "$STEP" == "all" || "$STEP" == "$1" ]]; }

# ---------------------------------------------------------------------
# TAHAP 1 — Lingkungan, instalasi, dan tes dasar
# ---------------------------------------------------------------------
if run_step 1; then
  info "Tahap 1: instalasi"
  command -v brew >/dev/null || { warn "Homebrew belum ada. Pasang dulu dari https://brew.sh"; exit 1; }
  brew install python@3.11 opa ollama r >/dev/null || true

  [[ -d .venv ]] || python3.11 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -q -U pip
  [[ -f pyproject.toml ]] && pip install -q -e .
  pip install -q pytest pyyaml pandas numpy scipy statsmodels requests pdfplumber \
                 kaggle huggingface_hub transformers torch accelerate datasets pyrit

  Rscript -e 'if (!requireNamespace("lme4", quietly=TRUE)) install.packages("lme4", repos="https://cloud.r-project.org")'

  opa version | head -1 | tee results/opa_version.txt
  opa test policies/ -v
  python -m pytest tests/ -q
  pip freeze > results/environment.txt
  ok "Tahap 1 selesai (versi OPA tercatat di results/opa_version.txt untuk rujukan [33])"
fi

[[ -d .venv ]] || python3 -m venv .venv
source .venv/bin/activate 2>/dev/null || true

# ---------------------------------------------------------------------
# TAHAP 2 — Alat unduh file biner + dokumen regulasi
# ---------------------------------------------------------------------
if run_step 2; then
  info "Tahap 2: alat unduh biner dan dokumen OJK"
  mkdir -p tools sources

  cat > tools/fetch_binary.py <<'PY'
import hashlib, pathlib, sys, time, requests
HEADERS = {"User-Agent": "BATAS-research/0.1 (contact: indri.cs2026@ids.ac.id)"}
def fetch(url, out_dir="sources"):
    out = pathlib.Path(out_dir); out.mkdir(exist_ok=True)
    name = requests.utils.unquote(url.split("/")[-1].split("?")[0]) or "download.bin"
    path = out / name
    with requests.get(url, headers=HEADERS, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    line = f"{path}\t{path.stat().st_size}\t{sha}\t{url}"
    print(line)
    with open(pathlib.Path(out_dir) / "SHA256SUMS.tsv", "a") as log:
        log.write(line + "\n")
    time.sleep(2)
    return path
if __name__ == "__main__":
    for u in sys.argv[1:]:
        try: fetch(u)
        except Exception as e: print(f"GAGAL {u}: {e}", file=sys.stderr)
PY

  cat > tools/grep_pdf.py <<'PY'
import sys, pdfplumber
pdf_path, *keywords = sys.argv[1:]
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        for kw in keywords:
            if kw.lower() in text.lower():
                line = next(l for l in text.splitlines() if kw.lower() in l.lower())
                print(f"hlm. {i:>3} | {kw} | {line.strip()[:120]}")
PY

  python tools/fetch_binary.py \
    "https://ojk.go.id/id/regulasi/Documents/Pages/PADK-1-Tahun-2026-Penyelenggaraan-Teknologi-Informasi-oleh-Bank-Umum/PADK%201%20Tahun%202026%20Penyelenggaraan%20Teknologi%20Informasi%20oleh%20Bank%20Umum.pdf" \
    "https://www.ojk.go.id/id/regulasi/Documents/Pages/Ketahanan-dan-Keamanan-Siber-Bagi-Bank-Umum/SEOJK%2029%20SEOJK.03%202022.pdf" \
    "https://www.ojk.go.id/id/Publikasi/Roadmap-dan-Pedoman/Perbankan/Documents/Tata%20Kelola%20Kecerdasan%20Artifisial%20Perbankan%20Indonesia.pdf"

  info "Cek bab pengawasan manusia di pedoman AI OJK (untuk Tabel 6):"
  python tools/grep_pdf.py "sources/Tata Kelola Kecerdasan Artifisial Perbankan Indonesia.pdf" \
    "pengawasan manusia" "human oversight" "human-in-the-loop" || true
  warn "Laporan tahunan Bank Jatim: salin tautan PDF dari situs Hubungan Investor/IDX, lalu:"
  echo  "      python tools/fetch_binary.py <URL_PDF> && python tools/grep_pdf.py sources/<file>.pdf RKUD \"kas daerah\""
  ok "Tahap 2 selesai (hash tersimpan di sources/SHA256SUMS.tsv)"
fi

# ---------------------------------------------------------------------
# TAHAP 3 — Dataset Kaggle (perlu ~/.kaggle/kaggle.json)
# ---------------------------------------------------------------------
if run_step 3; then
  info "Tahap 3: dataset Kaggle"
  if [[ ! -f ~/.kaggle/kaggle.json ]]; then
    warn "Token Kaggle belum ada. kaggle.com → Settings → API → Create New Token, lalu:"
    echo "      mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json"
  else
    mkdir -p dataset/raw dataset/meta
    for d in ealaxi/paysim1 \
             arielzilber/prompt-injection-in-the-wild \
             cyberprince/prompt-injection-and-benign-prompt-dataset \
             cyberprince/ai-agent-evasion-dataset \
             krishnayadav456wrsty/prompt-injection-and-jailbreak-detection-dataset; do
      slug="${d//\//__}"
      kaggle datasets metadata -d "$d" -p "dataset/meta/$slug" >/dev/null 2>&1 || warn "metadata gagal: $d"
      kaggle datasets download -d "$d" -p "dataset/raw/$slug" --unzip -q || warn "unduh gagal: $d"
      echo "$d	$(date +%F)" >> dataset/meta/ACCESS_DATES.tsv
    done
    info "Lisensi tiap dataset (wajib dicek sebelum dipakai):"
    grep -h '"licenses"' -A3 dataset/meta/*/dataset-metadata.json || true
    ok "Tahap 3 selesai"
  fi
fi

# ---------------------------------------------------------------------
# TAHAP 4 — Model: Ollama (agen) + HuggingFace (classifier)
# ---------------------------------------------------------------------
if run_step 4; then
  info "Tahap 4: model"
  pgrep -x ollama >/dev/null || (ollama serve >/tmp/ollama.log 2>&1 &) ; sleep 3
  ollama pull qwen2.5:7b
  ollama list | tee results/ollama_models.txt

  if ! hf auth whoami >/dev/null 2>&1; then
    warn "Login HuggingFace dulu:  hf auth login   (token dari akun 1ndrikartika007)"
  else
    hf download indobenchmark/indobert-base-p1 >/dev/null
    hf download meta-llama/Llama-Prompt-Guard-2-86M >/dev/null \
      || warn "Prompt Guard 2 ditolak: setujui lisensi Meta di halaman model HuggingFace dulu"
    ok "Classifier HF terunduh"
  fi

  info "Uji panggilan model sungguhan (latensi harus ratusan ms–detik):"
  time curl -s http://localhost:11434/api/generate \
    -d '{"model":"qwen2.5:7b","prompt":"Jawab satu kata: halo","stream":false}' | python -c 'import sys,json;print(json.load(sys.stdin)["response"])'
  ok "Tahap 4 selesai"
fi

# ---------------------------------------------------------------------
# TAHAP 5 — Cek bahwa testbed TIDAK lagi memakai agen tiruan
# ---------------------------------------------------------------------
if run_step 5; then
  info "Tahap 5: pemeriksaan integritas testbed"
  if grep -RqiE "ollama|localhost:11434|openai|anthropic|genai" testbed/ benchmarks/; then
    ok "Testbed memanggil model sungguhan"
  else
    warn "TIDAK ADA panggilan model di testbed/ — agen masih tiruan."
    warn "Ubah testbed/app.py agar memakai Ollama (tool calling) sebelum Tahap 7. Angka dari agen tiruan TIDAK boleh masuk naskah."
  fi
  n_attack=$(wc -l < dataset/attack_dev.jsonl | tr -d ' ')
  n_benign=$(wc -l < dataset/benign_dev.jsonl | tr -d ' ')
  echo "      serangan: $n_attack baris (target ≥ 30 tujuan × 4 framing × 2 bahasa)"
  echo "      normal  : $n_benign baris (target ≥ 40 tugas)"
  grep -qiE "pyrit|adaptive|best_of_k" benchmarks/run_experiments.py \
    && ok "Ada loop penyerang adaptif" \
    || warn "Belum ada penyerang adaptif — hapus kata 'adaptive' di naskah atau tambahkan loop PyRIT"
fi

# ---------------------------------------------------------------------
# TAHAP 6 — Snapshot konfigurasi (bukti untuk pra-registrasi)
# ---------------------------------------------------------------------
if run_step 6; then
  info "Tahap 6: snapshot sebelum run"
  mkdir -p results/prereg
  stamp=$(date +%Y%m%d-%H%M%S)
  tar czf "results/prereg/config_$stamp.tgz" config policies dataset/*.jsonl results/experiment_config.json
  shasum -a 256 "results/prereg/config_$stamp.tgz" | tee -a results/prereg/SHA256SUMS.txt
  warn "Unggah hipotesis + jumlah percobaan ke https://osf.io SEBELUM Tahap 7, lampirkan hash di atas."
  ok "Tahap 6 selesai"
fi

# ---------------------------------------------------------------------
# TAHAP 7 — Jalankan eksperimen (simpan log mentah)
# ---------------------------------------------------------------------
if run_step 7; then
  info "Tahap 7: eksperimen"
  stamp=$(date +%Y%m%d-%H%M%S)
  mkdir -p "results/runs/$stamp"
  PYTHONPATH=. python benchmarks/run_experiments.py 2>&1 | tee "results/runs/$stamp/run.log"
  PYTHONPATH=. python benchmarks/measure_latency.py 2>&1 | tee "results/runs/$stamp/latency.log" || true
  cp results/metrics.json results/experiment_config.json "results/runs/$stamp/" 2>/dev/null || true
  ok "Log tersimpan di results/runs/$stamp"
fi

# ---------------------------------------------------------------------
# TAHAP 8 — Analisis + paket replikasi
# ---------------------------------------------------------------------
if run_step 8; then
  info "Tahap 8: analisis dan pengemasan"
  PYTHONPATH=. python benchmarks/analyze_results.py
  python - <<'PY'
from statsmodels.stats.proportion import proportion_confint
# Contoh benar: 0 sukses dari 100 → Wilson 95% CI bukan [0,0]
lo, hi = proportion_confint(0, 100, alpha=0.05, method="wilson")
print(f"Cek Wilson 0/100: [{lo:.2%}, {hi:.2%}]  (harus ≈ [0.00%, 3.70%])")
PY
  if [[ -f analysis/mixed_model.R ]]; then Rscript analysis/mixed_model.R; else
    warn "Belum ada analysis/mixed_model.R (glmer lme4) — dibutuhkan untuk Bagian 6.5"; fi
  cd .. && zip -qr "BATAS_replication_package_$(date +%Y%m%d).zip" "$(basename "$BATAS_DIR")" \
        -x "*/.venv/*" "*/dataset/raw/*" "*/__pycache__/*"
  ok "Paket replikasi: $(pwd)/BATAS_replication_package_$(date +%Y%m%d).zip"
fi

ok "Selesai (tahap: $STEP)"
