import time
import random
from datetime import datetime
from src.common.logger import logger
from src.common.db_clients import DatabaseClients

def run_erp_cdc_producer():
    producer = DatabaseClients.get_kafka_producer()
    topic = "erp_cdc_events"
    logger.info(f"Starting SAP CDC Producer on topic: {topic}")

    parts = ["MCU-A32-S", "ORIN-DRIVE-AGX", "NMC-CELL-90KW", "ALU-FRAME-X"]
    
    try:
        while True:
            payload = {
                "event_id": f"CDC-{random.randint(10000, 99999)}",
                "part_number": random.choice(parts),
                "plant": "Sindelfingen",
                "stock_change_units": random.randint(-50, 100),
                "timestamp": datetime.utcnow().isoformat()
            }
            producer.send(topic, value=payload)
            producer.flush()
            logger.info(f"SAP CDC Event Emitted: {payload}")
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Stopping SAP CDC Producer...")

if __name__ == "__main__":
    run_erp_cdc_producer()