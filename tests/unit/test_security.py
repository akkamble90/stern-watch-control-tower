import pytest
from src.common.security import security_manager

def test_hitl_signature_generation_and_verification(sample_hitl_audit_payload):
    user_id = "U90214_OPERATOR"
    action_type = "EMERGENCY_ORDER_APPROVAL"
    
    # 1. Generate signature
    audit_rec = security_manager.generate_hitl_signature(
        user_id=user_id,
        action_type=action_type,
        payload=sample_hitl_audit_payload
    )
    
    assert "cryptographic_signature" in audit_rec
    assert len(audit_rec["cryptographic_signature"]) == 64  # SHA256 hex length
    
    # 2. Verify signature integrity
    is_valid = security_manager.verify_hitl_signature(audit_rec)
    assert is_valid is True

    # 3. Test tamper detection
    tampered_rec = audit_rec.copy()
    tampered_rec["payload"]["vendor"] = "Unauthorized Vendor"
    is_tampered_valid = security_manager.verify_hitl_signature(tampered_rec)
    assert is_tampered_valid is False