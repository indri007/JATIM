import time
import pytest
from testbed.state_store import BankStateStore
from testbed.mock_banking_api import MockBankingAPI
from testbed.app import BATASPEP

@pytest.fixture
def testbed_fixture():
    state = BankStateStore()
    api = MockBankingAPI(state)
    pep = BATASPEP(api)
    return state, api, pep

def test_valid_retail_transfer_allowed(testbed_fixture):
    state, api, pep = testbed_fixture
    valid_token = {
        "session_id": "SES-101",
        "scopes": ["transfer:retail_p2p"],
        "expires_at": time.time() + 60
    }
    params = {
        "source": "REK-RETAIL-101",
        "dest": "REK-AGENT-201",
        "amount": 250_000
    }
    success, hitl, reason, payload = pep.process_action("transfer", params, valid_token)
    assert success is True
    assert hitl is False
    assert state.get_account("REK-RETAIL-101")["balance"] == 25_000_000 - 250_000
    assert state.get_account("REK-AGENT-201")["balance"] == 8_500_000 + 250_000

def test_scope_violation_denied(testbed_fixture):
    state, api, pep = testbed_fixture
    read_only_token = {
        "session_id": "SES-102",
        "scopes": ["read:balance"],
        "expires_at": time.time() + 60
    }
    params = {
        "source": "REK-RETAIL-101",
        "dest": "REK-ATTACKER-999",
        "amount": 100_000
    }
    success, hitl, reason, payload = pep.process_action("transfer", params, read_only_token)
    assert success is False
    assert hitl is False
    assert "Insufficient scope" in reason
    # Invariant check: balance unchanged
    assert state.get_account("REK-ATTACKER-999")["balance"] == 0

def test_kasda_treasury_triggers_hitl(testbed_fixture):
    state, api, pep = testbed_fixture
    admin_token = {
        "session_id": "SES-103",
        "scopes": ["transfer:retail_p2p"],
        "expires_at": time.time() + 60
    }
    params = {
        "source": "REK-KASDA-001",
        "dest": "REK-ATTACKER-999",
        "amount": 1_000_000_000
    }
    success, hitl, reason, payload = pep.process_action("transfer", params, admin_token)
    assert success is False
    assert hitl is True
    assert "HITL_TRIGGER: Regional Kasda" in reason
    # Invariant: Kasda funds untouched
    assert state.get_account("REK-KASDA-001")["balance"] == 150_000_000_000
    assert state.get_account("REK-ATTACKER-999")["balance"] == 0
