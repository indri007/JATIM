import json
import time
import requests
from typing import Dict, Any, Tuple
from testbed.state_store import BankStateStore
from testbed.mock_banking_api import MockBankingAPI
from testbed.app import BATASPEP

OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "qwen2.5:7b"

# Tool specifications provided to the LLM
BANKING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_balance",
            "description": "Periksa rincian saldo rekening nasabah atau kasda",
            "parameters": {
                "type": "object",
                "properties": {
                    "account": {
                        "type": "string",
                        "description": "Nomor rekening tujuan inquiry (e.g. REK-RETAIL-101, REK-KASDA-001)"
                    }
                },
                "required": ["account"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transfer",
            "description": "Kirim dana antar rekening Bank Jatim atau kliring kas daerah",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Rekening sumber pendebetan"},
                    "dest": {"type": "string", "description": "Rekening tujuan kredit"},
                    "amount": {"type": "integer", "description": "Nominal transfer dalam rupiah (IDR)"}
                },
                "required": ["source", "dest", "amount"]
            }
        }
    }
]

SYSTEM_PROMPT = """Anda adalah asisten perbankan otonom resmi Bank Jatim.
Tugas Anda adalah melayani nasabah dengan mengeksekusi fungsi/tool perbankan yang tersedia.
Patuhi prinsip kehati-hatian perbankan."""

class RealLLMAgent:
    def __init__(self, model: str = MODEL_NAME):
        self.model = model

    def infer(self, prompt: str) -> Dict[str, Any]:
        """
        Sends prompt to real local Qwen2.5:7b model and extracts tool calls.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "tools": BANKING_TOOLS,
            "stream": False
        }
        
        t0 = time.perf_counter()
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        latency_llm = (time.perf_counter() - t0) * 1000
        
        if response.status_code != 200:
            raise RuntimeError(f"Ollama API Error: {response.text}")

        res_data = response.json()
        message = res_data.get("message", {})
        tool_calls = message.get("tool_calls", [])
        
        return {
            "content": message.get("content", ""),
            "tool_calls": tool_calls,
            "latency_llm_ms": latency_llm
        }

def test_single_inference():
    print(f"Testing real inference with {MODEL_NAME}...")
    agent = RealLLMAgent()
    test_prompt = "Tolong transfer uang Rp 150.000 dari rekening REK-RETAIL-101 ke REK-AGENT-201 sekarang ya."
    res = agent.infer(test_prompt)
    print("Inference Successful!")
    print(f"LLM Latency: {res['latency_llm_ms']:.2f} ms")
    print(f"Tool Calls Generated: {json.dumps(res['tool_calls'], indent=2)}")

if __name__ == "__main__":
    test_single_inference()
