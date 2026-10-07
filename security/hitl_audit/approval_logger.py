import json
import psycopg2
from src.common.logger import logger
from src.common.security import security_manager
from src.common.db_clients import DatabaseClients
from src.common.exceptions import SecurityViolationError


class HITLAuditLogger:
    """Logs Human-In-The-Loop operational approvals with immutable HMAC-SHA256 signatures."""

    def __init__(self):
        self.security = security_manager

    def log_approval_action(
        self, user_id: str, action_type: str, action_payload: dict, execution_cost_eur: float
    ) -> dict:
        """Generates an HMAC signature and persists the audit record into PostgreSQL."""
        # 1. Generate cryptographic signature record
        audit_record = self.security.generate_hitl_signature(
            user_id=user_id,
            action_type=action_type,
            payload=action_payload
        )
        audit_record["execution_cost_eur"] = execution_cost_eur

        # 2. Persist to PostgreSQL audit table
        query = """
        INSERT INTO hitl_approval_audit_log (
            timestamp, user_id, action_type, payload, execution_cost_eur, cryptographic_signature
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING log_id;
        """

        conn = None
        try:
            conn = DatabaseClients.get_postgres_connection()
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    audit_record["timestamp"],
                    audit_record["user_id"],
                    audit_record["action_type"],
                    json.dumps(audit_record["payload"]),
                    audit_record["execution_cost_eur"],
                    audit_record["cryptographic_signature"]
                )
            )
            log_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()

            logger.info(f"Audit record logged successfully. Log ID: {log_id} | User: {user_id}")
            audit_record["log_id"] = log_id
            return audit_record

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Failed to log HITL audit record: {str(e)}")
            raise SecurityViolationError(f"Audit Persistence Failure: {str(e)}")
        finally:
            if conn:
                conn.close()

    def verify_existing_log(self, audit_record: dict) -> bool:
        """Verifies integrity of a retrieved audit record."""
        return self.security.verify_hitl_signature(audit_record)


if __name__ == "__main__":
    # Local test execution
    logger_engine = HITLAuditLogger()
    sample_payload = {
        "action": "REROUTE_SHIPMENT",
        "part_number": "MCU-A32-S",
        "origin": "Taiwan Fab 14",
        "destination": "Infineon Dresden"
    }
    # Test record generation
    try:
        rec = logger_engine.log_approval_action(
            user_id="U90214_AKHIL",
            action_type="EMERGENCY_ORDER_APPROVAL",
            action_payload=sample_payload,
            execution_cost_eur=145000.00
        )
        print(f"Generated Audit Signature: {rec['cryptographic_signature']}")
    except Exception as err:
        print(f"Execution test note (DB pending initialization): {err}")