import json
import pytest
from unittest.mock import MagicMock

def test_kafka_producer_serialization(sample_telemetry_payload):
    mock_producer = MagicMock()
    serialized_data = json.dumps(sample_telemetry_payload).encode("utf-8")
    
    mock_producer.send("raw_freight_telemetry", value=serialized_data)
    mock_producer.send.assert_called_once_with("raw_freight_telemetry", value=serialized_data)