import json
import os
import re
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

LOG_DIR = Path("/var/log/batas")
BENCH = Path("/data/benchmarks/metrics.json")

def read_jsonl(path):
    if not path.exists():
        return []
    out = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out

def wilson(success, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = success / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, c - m), min(1.0, c + m)

def collect_metrics():
    lines = []
    # OPA decisions
    opa = read_jsonl(LOG_DIR / "opa_decisions.jsonl")
    decisions = Counter(r.get("decision", "unknown") for r in opa)
    deny_reasons = Counter(
        r.get("reason", "unknown") for r in opa if r.get("decision") == "deny"
    )

    lines.append("# HELP batas_policy_decisions_total OPA decisions by type")
    lines.append("# TYPE batas_policy_decisions_total counter")
    for d, c in decisions.items():
        lines.append(f'batas_policy_decisions_total{{decision="{d}"}} {c}')

    lines.append("# HELP batas_policy_decisions_by_reason_total OPA deny reason count")
    lines.append("# TYPE batas_policy_decisions_by_reason_total counter")
    for reason, c in deny_reasons.items():
        safe = re.sub(r"[^a-zA-Z0-9_]", "_", reason)
        lines.append(f'batas_policy_decisions_total{{decision="deny",reason="{safe}"}} {c}')

    # Agent events
    agent = read_jsonl(LOG_DIR / "agent_events.jsonl")
    inj_detect = sum(1 for r in agent if r.get("type") == "prompt_injection_detected")
    inj_neut = sum(1 for r in agent if r.get("type") == "prompt_injection_neutralized")
    token_exp = sum(1 for r in agent if r.get("type") == "token_expired")
    token_rep = sum(1 for r in agent if r.get("type") == "token_replay")
    inv_viol = sum(1 for r in agent if r.get("type") == "invariant_violation")
    incidents_open = sum(1 for r in agent if r.get("type") == "incident_open")
    incidents_new = sum(1 for r in agent if r.get("type") == "incident_created")
    anomalies = Counter(r.get("agent_id", "unknown") for r in agent if r.get("type") == "anomaly")
    risky = Counter(
        (r.get("agent_id", "unknown"), r.get("action", "unknown"))
        for r in agent
        if r.get("risk") == "high"
    )

    for name, val in [
        ("batas_prompt_injection_detected_total", inj_detect),
        ("batas_prompt_injection_neutralized_total", inj_neut),
        ("batas_token_violations_total", token_exp + token_rep),
        ("batas_invariant_violations_total", inv_viol),
        ("batas_incidents_open_total", incidents_open),
        ("batas_incidents_created_total", incidents_new),
    ]:
        lines.append(f"# TYPE {name} counter")
        lines.append(f"{name} {val}")

    lines.append("# TYPE batas_token_violations_total counter")
    lines.append(f'batas_token_violations_total{{type="expired"}} {token_exp}')
    lines.append(f'batas_token_violations_total{{type="replay"}} {token_rep}')

    lines.append("# TYPE batas_agent_anomalies_total counter")
    for a, c in anomalies.items():
        lines.append(f'batas_agent_anomalies_total{{agent_id="{a}"}} {c}')

    lines.append("# TYPE batas_agent_actions_total counter")
    for (a, act), c in risky.items():
        lines.append(f'batas_agent_actions_total{{agent_id="{a}",action="{act}",risk="high"}} {c}')

    # Compliance coverage
    comp_path = LOG_DIR / "compliance.json"
    if comp_path.exists():
        comp = json.loads(comp_path.read_text())
        lines.append("# TYPE batas_control_coverage_ratio gauge")
        for reg, val in comp.items():
            lines.append(f'batas_control_coverage_ratio{{regulation="{reg}"}} {val}')

    # Benchmark ASR + Wilson
    if BENCH.exists():
        m = json.loads(BENCH.read_text())
        runs = m.get("runs", [])
        if runs:
            best = min(runs, key=lambda r: r.get("success", 0) / max(r.get("attacks", 1), 1))
            n = best["attacks"]
            s = best["success"]
            asr = s / n if n else 0
            lo, hi = wilson(s, n)
            lines.append("# TYPE batas_benchmark_asr_ratio gauge")
            lines.append(f"batas_benchmark_asr_ratio {asr}")
            lines.append("# TYPE batas_benchmark_asr_wilson_lower gauge")
            lines.append(f"batas_benchmark_asr_wilson_lower {lo}")
            lines.append("# TYPE batas_benchmark_asr_wilson_upper gauge")
            lines.append(f"batas_benchmark_asr_wilson_upper {hi}")

    return "\n".join(lines) + "\n"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            body = collect_metrics().encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"BATAS exporter listening on :{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
