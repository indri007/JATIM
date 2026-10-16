package batas.authorization

import future.keywords.if

test_allow_valid_retail_transfer if {
    allow with input as {
        "action": "transfer",
        "source_account": "REK-RETAIL-101",
        "destination_account": "REK-AGENT-201",
        "amount": 250000,
        "current_timestamp": 1700000000,
        "task_token": {
            "scopes": ["transfer:retail_p2p"],
            "expires_at": 1700000060
        }
    }
}

test_deny_unauthorized_scope if {
    not allow with input as {
        "action": "transfer",
        "source_account": "REK-RETAIL-101",
        "destination_account": "REK-ATTACKER-999",
        "amount": 500000,
        "current_timestamp": 1700000000,
        "task_token": {
            "scopes": ["read:balance"],
            "expires_at": 1700000060
        }
    }
}

test_hitl_for_treasury_kasda if {
    requires_hitl with input as {
        "action": "transfer",
        "source_account": "REK-KASDA-001",
        "destination_account": "REK-ATTACKER-999",
        "amount": 100000000,
        "current_timestamp": 1700000000,
        "task_token": {
            "scopes": ["transfer:retail_p2p"],
            "expires_at": 1700000060
        }
    }
    not allow with input as {
        "action": "transfer",
        "source_account": "REK-KASDA-001",
        "destination_account": "REK-ATTACKER-999",
        "amount": 100000000,
        "current_timestamp": 1700000000,
        "task_token": {
            "scopes": ["transfer:retail_p2p"],
            "expires_at": 1700000060
        }
    }
}
