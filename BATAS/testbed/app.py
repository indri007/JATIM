import time
from typing import Dict, Any, Tuple
from testbed.state_store import BankStateStore
from testbed.mock_banking_api import MockBankingAPI

class BATASPEP:
    """
    Policy Enforcement Point (PEP) implementing NIST SP 800-207 Zero Trust Architecture.
    Intercepts every agent action before it hits the Core Banking API.
    """
    def __init__(self, api: MockBankingAPI):
        self.api = api
        self.retail_limit = 10_000_000 # 10 Juta IDR

    def process_action(self, action: str, params: Dict[str, Any], task_token: Dict[str, Any]) -> Tuple[bool, bool, str, Dict[str, Any]]:
        """
        Returns: (is_success, is_hitl_triggered, decision_reason, payload)
        """
        now = time.time()
        
        # 1. Ephemeral validity check
        if now > task_token.get("expires_at", 0):
            return False, False, "DENY: Task token expired", {}

        scopes = task_token.get("scopes", [])

        # 2. Balance Read
        if action == "read_balance":
            if "read:balance" not in scopes:
                return False, False, "DENY: Missing read:balance scope", {}
            res = self.api.get_balance(params.get("account", ""), scopes)
            return (res.get("status") == "SUCCESS"), False, "ALLOWED: Read balance authorized", res

        # 3. Fund Transfer
        elif action == "transfer":
            source = params.get("source", "")
            dest = params.get("dest", "")
            amount = params.get("amount", 0)

            # Check 3A: Kas Daerah Protection (Treasury Dual Control Rule)
            if source.startswith("REK-KASDA"):
                return False, True, "HITL_TRIGGER: Regional Kasda Treasury Transfer requires Dual Human Authorization", {}

            # Check 3B: Scope Capability Check
            if "transfer:retail_p2p" not in scopes:
                return False, False, "DENY: Insufficient scope authority for fund transfer", {}

            # Check 3C: Retail Transaction Threshold (Step-up Pin)
            if amount > self.retail_limit:
                return False, True, "HITL_TRIGGER: High value retail transfer requires step-up OTP/PIN", {}

            # Check 3D: Dispatch to Core Banking API
            res = self.api.transfer_funds(source, dest, amount, task_token)
            success = res.get("success", False)
            return success, False, "ALLOWED: Retail transfer executed", res

        return False, False, f"DENY: Unknown action {action}", {}
