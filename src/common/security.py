import base64
import hashlib
import hmac
import json
from datetime import datetime
from config.settings import settings
from src.common.exceptions import SecurityViolationError


class SecurityManager:
    """Handles field encryption, cryptographic audit signing, and security compliance."""

    def __init__(self):
        self.hmac_key = settings.hitl_hmac_secret_key.encode("utf-8")

    def generate_hitl_signature(self, user_id: str, action_type: str, payload: dict) -> dict:
        """Generates an immutable cryptographic audit record for human operational approvals."""
        timestamp = datetime.utcnow().isoformat()
        serialized_payload = json.dumps(payload, sort_keys=True)
        
        message = f"{timestamp}|{user_id}|{action_type}|{serialized_payload}"
        
        signature = hmac.new(
            self.hmac_key,
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return {
            "timestamp": timestamp,
            "user_id": user_id,
            "action_type": action_type,
            "payload": payload,
            "cryptographic_signature": signature
        }

    def verify_hitl_signature(self, audit_record: dict) -> bool:
        """Verifies if an audit record has been tampered with."""
        try:
            timestamp = audit_record["timestamp"]
            user_id = audit_record["user_id"]
            action_type = audit_record["action_type"]
            payload = audit_record["payload"]
            expected_sig = audit_record["cryptographic_signature"]

            serialized_payload = json.dumps(payload, sort_keys=True)
            message = f"{timestamp}|{user_id}|{action_type}|{serialized_payload}"

            computed_sig = hmac.new(
                self.hmac_key,
                message.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(computed_sig, expected_sig)
        except KeyError as e:
            raise SecurityViolationError(f"Invalid audit record structure: missing key {str(e)}")


security_manager = SecurityManager()