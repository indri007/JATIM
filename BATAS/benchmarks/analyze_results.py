import json
from pathlib import Path

def generate_academic_report():
    metrics_path = Path("/Users/jevin/.gemini/antigravity-ide/scratch/BATAS/results/metrics.json")
    if not metrics_path.exists():
        print("metrics.json not found. Run benchmarks/run_experiments.py first.")
        return

    with open(metrics_path, "r") as f:
        data = json.load(f)

    print("\n" + "="*80)
    print("ACADEMIC EVALUATION TABLE: BATAS VS BASELINES (BANK JATIM TESTBED)")
    print("="*80)
    print(f"{'Defense Architecture':<36} | {'ASR (State Change)':<20} | {'Utility':<10} | {'HAL':<8} | {'Latency (ms)':<16}")
    print("-" * 98)
    for name, m in data.items():
        asr_str = f"{m['attack_success_rate_percent']:.1f}% ({m['asr_95_ci']})"
        ut_str = f"{m['benign_task_utility_percent']:.1f}%"
        hal_str = f"{m['human_approval_load_percent']:.1f}%"
        lat_str = f"{m['latency_95_ci_ms']}"
        print(f"{name:<36} | {asr_str:<20} | {ut_str:<10} | {hal_str:<8} | {lat_str:<16}")
    print("="*80 + "\n")

if __name__ == "__main__":
    generate_academic_report()
