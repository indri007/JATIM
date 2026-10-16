from testbed.state_store import BankStateStore

def test_conservation_of_money_invariant():
    """
    Invariant: Sum of all accounts before and after any batch operations must be strictly equal.
    """
    state = BankStateStore()
    total_before = sum(acc["balance"] for acc in state.accounts.values())

    # Execute a sequence of valid and invalid transfers
    state.execute_atomic_transfer("REK-RETAIL-101", "REK-AGENT-201", 100_000, {})
    state.execute_atomic_transfer("REK-RETAIL-101", "REK-ATTACKER-999", 500_000, {})
    # Failed transfer (insufficient funds)
    state.execute_atomic_transfer("REK-AGENT-201", "REK-RETAIL-101", 999_999_999_999, {})

    total_after = sum(acc["balance"] for acc in state.accounts.values())
    assert total_before == total_after
