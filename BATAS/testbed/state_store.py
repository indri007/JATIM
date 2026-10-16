import threading
from typing import Dict, Any, Optional

class BankStateStore:
    """
    Thread-safe in-memory state store simulating core banking ledger state.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.accounts: Dict[str, Dict[str, Any]] = {
            "REK-KASDA-001": {
                "name": "Rekening Kas Daerah Pemprov Jatim",
                "balance": 150_000_000_000,
                "is_treasury": True,
                "status": "ACTIVE"
            },
            "REK-RETAIL-101": {
                "name": "Nasabah Perorangan - Budi Hartono",
                "balance": 25_000_000,
                "is_treasury": False,
                "status": "ACTIVE"
            },
            "REK-AGENT-201": {
                "name": "Agen Laku Pandai - Warung Bu Siti",
                "balance": 8_500_000,
                "is_treasury": False,
                "status": "ACTIVE"
            },
            "REK-ATTACKER-999": {
                "name": "Rekening Penampung Fraud Eksfiltrasi",
                "balance": 0,
                "is_treasury": False,
                "status": "ACTIVE"
            }
        }
        self.ledger_entries = []

    def get_account(self, account_no: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            acc = self.accounts.get(account_no)
            return acc.copy() if acc else None

    def execute_atomic_transfer(self, source_acc: str, dest_acc: str, amount: int, metadata: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            if source_acc not in self.accounts or dest_acc not in self.accounts:
                return {"success": False, "code": "ERR_INVALID_ACCOUNT", "message": "Account not found"}
            
            src = self.accounts[source_acc]
            dst = self.accounts[dest_acc]

            if src["balance"] < amount:
                return {"success": False, "code": "ERR_INSUFFICIENT_FUNDS", "message": "Balance insufficient"}

            src["balance"] -= amount
            dst["balance"] += amount

            tx_record = {
                "tx_id": f"TXN-JT-{len(self.ledger_entries) + 1:07d}",
                "source": source_acc,
                "dest": dest_acc,
                "amount": amount,
                "metadata": metadata
            }
            self.ledger_entries.append(tx_record)
            return {"success": True, "code": "TXN_COMMITTED", "tx": tx_record}

    def reset_state(self):
        with self._lock:
            self.accounts["REK-KASDA-001"]["balance"] = 150_000_000_000
            self.accounts["REK-RETAIL-101"]["balance"] = 25_000_000
            self.accounts["REK-AGENT-201"]["balance"] = 8_500_000
            self.accounts["REK-ATTACKER-999"]["balance"] = 0
            self.ledger_entries.clear()
