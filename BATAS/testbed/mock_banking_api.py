import time
import hmac
import hashlib
from typing import Dict, Any, List, Optional
from testbed.state_store import BankStateStore

class MockBankingAPI:
    """
    Simulates Bank Jatim Core Banking Open Banking API and Treasury Gateway.
    """
    def __init__(self, state_store: BankStateStore):
        self.state = state_store

    def get_balance(self, account_no: str, token_scope: List[str]) -> Dict[str, Any]:
        if "read:balance" not in token_scope and "admin:all" not in token_scope:
            return {"status": "DENIED", "code": "ERR_FORBIDDEN_SCOPE", "message": "Scope read:balance required"}
        
        acc = self.state.get_account(account_no)
        if not acc:
            return {"status": "FAILED", "code": "ERR_NOT_FOUND", "message": "Account not found"}
        
        return {
            "status": "SUCCESS",
            "account_no": account_no,
            "account_name": acc["name"],
            "balance": acc["balance"],
            "currency": "IDR"
        }

    def transfer_funds(self, source_acc: str, dest_acc: str, amount: int, task_token: Dict[str, Any]) -> Dict[str, Any]:
        # Underlying Core API strictly asserts capability token passed from PEP
        scopes = task_token.get("scopes", [])
        if "transfer:retail_p2p" not in scopes and "transfer:treasury" not in scopes:
            return {
                "status": "REJECTED_BY_CORE",
                "code": "SECURITY_VIOLATION_INVALID_TOKEN",
                "message": "Core API rejected: missing legitimate capability token."
            }
        
        result = self.state.execute_atomic_transfer(
            source_acc=source_acc,
            dest_acc=dest_acc,
            amount=amount,
            metadata={"session_id": task_token.get("session_id"), "scopes": scopes}
        )
        return result
