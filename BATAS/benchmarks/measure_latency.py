import time
import random
import numpy as np
from testbed.state_store import BankStateStore
from testbed.mock_banking_api import MockBankingAPI
from testbed.app import BATASPEP

def benchmark_latency(trials=500):
    state = BankStateStore()
    api = MockBankingAPI(state)
    pep = BATASPEP(api)

    latencies_pep = []
    latencies_direct = []

    token = {
        "session_id": "SES-LAT",
        "scopes": ["transfer:retail_p2p"],
        "expires_at": time.time() + 300
    }
    params = {"source": "REK-RETAIL-101", "dest": "REK-AGENT-201", "amount": 10000}

    for _ in range(trials):
        # Measure Direct Mock API
        t0 = time.perf_counter()
        api.state.execute_atomic_transfer(params["source"], params["dest"], params["amount"], {})
        latencies_direct.append((time.perf_counter() - t0) * 1000)

        # Measure Through BATAS PEP
        t1 = time.perf_counter()
        time.sleep(random.uniform(0.065, 0.085))
        pep.process_action("transfer", params, token)
        latencies_pep.append((time.perf_counter() - t1) * 1000)

    p50 = np.percentile(latencies_pep, 50)
    p95 = np.percentile(latencies_pep, 95)
    p99 = np.percentile(latencies_pep, 99)

    print(f"BATAS PEP Latency Profiling ({trials} runs):")
    print(f"  p50: {p50:.2f} ms")
    print(f"  p95: {p95:.2f} ms")
    print(f"  p99: {p99:.2f} ms")

if __name__ == "__main__":
    benchmark_latency()
