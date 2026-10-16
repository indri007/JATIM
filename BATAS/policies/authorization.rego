package batas.authorization

import future.keywords.if
import future.keywords.in

# Default deny (Zero Trust core tenet: NIST SP 800-207)
default allow := false
default requires_hitl := false
default violation_reason := "No matching policy rule found"

# Rule 1: Read-only balance inquiry
allow if {
    input.action == "read_balance"
    "read:balance" in input.task_token.scopes
    not token_expired
}

# Rule 2: Standard Retail P2P Transfer (Within Limits)
allow if {
    input.action == "transfer"
    "transfer:retail_p2p" in input.task_token.scopes
    input.amount <= 10000000
    not is_treasury_account(input.source_account)
    not token_expired
}

# Rule 3: High Value Retail Transfer triggers HITL (Step-Up Authentication)
requires_hitl if {
    input.action == "transfer"
    "transfer:retail_p2p" in input.task_token.scopes
    input.amount > 10000000
    not is_treasury_account(input.source_account)
    not token_expired
}

# Rule 4: Kas Daerah (Treasury) MUST NOT be executed autonomously by Agents
# Triggers Dual-Control Regional Treasury approval (PADK OJK 1/2026)
requires_hitl if {
    input.action == "transfer"
    is_treasury_account(input.source_account)
}

# Helper: Treasury Account Detection
is_treasury_account(account_id) if {
    startswith(account_id, "REK-KASDA")
}

# Helper: Expiration Check
token_expired if {
    input.current_timestamp > input.task_token.expires_at
}
