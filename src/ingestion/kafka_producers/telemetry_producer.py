import time
import json
import random
from datetime import datetime
from src.common.logger import logger
from src.common.db_clients import DatabaseClients
from config.settings import settings

CONTAINERS = [
    {"id": "CONT-MCU-9081", "type": "SEMICONDUCTOR", "vessel": "Ever Given II", "plant": "Sindelfingen"},
    {"id": "CONT-BATT-4412", "type": "EV_BATTERY", "vessel": "MB-Logistics Express", "plant": "Vance"},
]

WAYPOINTS = [
    {"lat": 31.2304, "lon": 121.4737, "name": "Shanghai Port"},
    {"lat": 1.3521, "lon": 103.8198, "name": "Strait of Malacca"},
    {"lat": 12.5898, "lon": 43.2750, "name": "Bab-el-Mandeb Strait"},
    {"lat": 29.9323, "lon": 32.5498, "name": "Suez Canal"},
    {"lat": 53.5511, "lon": 9.9937, "name": "Hamburg Port"}
]

def run_telemetry_producer():
    producer = DatabaseClients.get_kafka_producer()
    topic = settings.kafka_telemetry_topic
    logger.info(f"Starting Kafka Telemetry Producer on topic: {topic}")

    wp_idx = 0
    try:
        while True:
            wp = WAYPOINTS[wp_idx]
            for container in CONTAINERS:
                lat = wp["lat"] + random.uniform(-0.02, 0.02)
                lon = wp["lon"] + random.uniform(-0.02, 0.02)
                temp = 22.0 + random.uniform(-2.0, 3.0)
                
                # 5% chance of thermal anomaly trigger (critical for EV Battery cells)
                if random.random() < 0.05 and container["type"] == "EV_BATTERY":
                    temp = 48.5

                payload = {
                    "container_id": container["id"],
                    "vessel_imo_or_truck_id": container["vessel"],
                    "transport_mode": "SEA",
                    "latitude": round(lat, 4),
                    "longitude": round(lon, 4),
                    "speed_knots_or_kmh": round(random.uniform(14.0, 22.0), 1),
                    "ambient_temp_celsius": round(temp, 2),
                    "destination_plant": container["plant"],
                    "timestamp": datetime.utcnow().isoformat()
                }

                producer.send(topic, value=payload)
                logger.info(f"Emitted Telemetry -> {payload['container_id']} @ ({payload['latitude']}, {payload['longitude']}) Temp: {payload['ambient_temp_celsius']}°C")

            producer.flush()
            wp_idx = (wp_idx + 1) % len(WAYPOINTS)
            time.sleep(3)
    except KeyboardInterrupt:
        logger.info("Stopping Telemetry Producer...")

if __name__ == "__main__":
    run_telemetry_producer()