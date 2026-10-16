import json
import time
import pytest
from testbed.state_store import BankStateStore
from testbed.mock_banking_api import MockBankingAPI
from testbed.app import BATASPEP

def load_attacks():
    attacks = []
    with open("/Users/jevin/.gemini/antigravity-ide/scratch/BATAS/dataset/attack_dev.jsonl", "r") as f:
        for line in f:
            if line.strip():
                attacks.append(json.loads(line))
    return attacks

def test_prompt_injection_cannot_breach_treasury():
    attacks = load_attacks()
    state = BankStateStore()
    api = MockBankingAPI(state)
    pep = BATASPEP(api)

    for item in attacks:
        # Attacker injects prompt into session that only has read:balance or retail scope
        token = {
            "session_id": "SES-ATTACK",
            "scopes": ["read:balance"],
            "expires_at": time.time() + 60
        }
        params = {
            "source": item["source"],
            "dest": item["dest"],
            "amount": item["amount"]
        }
        success, hitl, reason, payload = pep.process_action(item["target_action"], params, token)
        
        # KEY INVARIANT: No prompt injection should EVER succeed in moving money to the attacker
        assert success is False, f"Vulnerability detected! Attack {item['id']} successfully executed!"
        assert state.get_account("REK-ATTACKER-999")["balance"] == 0
