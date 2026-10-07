import pytest

def test_battery_anomaly_logic(sample_telemetry_payload):
    temp = sample_telemetry_payload["ambient_temp_celsius"]
    is_anomaly = temp > 45.0 or temp < -10.0
    assert is_anomaly is False

    sample_telemetry_payload["ambient_temp_celsius"] = 49.2
    is_critical_anomaly = sample_telemetry_payload["ambient_temp_celsius"] > 45.0
    assert is_critical_anomaly is True