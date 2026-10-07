import pytest
from unittest.mock import MagicMock
from config.settings import settings

@pytest.fixture(scope="session")
def mock_settings():
    """Provides validated configuration overrides for unit tests."""
    return settings

@pytest.fixture
def mock_neo4j_driver(mocker):
    """Mocks the Neo4j Graph Database driver for offline testing."""
    mock_driver = MagicMock()
    mock_session = MagicMock()
    
    # Mock Neo4j record return
    mock_record = {
        "part_name": "ADAS Microcontroller Unit",
        "plant_name": "Sindelfingen Assembly Plant",
        "suppliers": ["TSMC", "NXP"]
    }
    mock_result = MagicMock()
    mock_result.single.return_value = mock_record
    mock_session.run.return_value = mock_result
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    mocker.patch("src.common.db_clients.DatabaseClients.get_neo4j_driver", return_value=mock_driver)
    return mock_driver

@pytest.fixture
def sample_telemetry_payload():
    """Provides a standardized sample freight telemetry dictionary."""
    return {
        "container_id": "CONT-MCU-9081",
        "vessel_imo_or_truck_id": "Ever Given II",
        "transport_mode": "SEA",
        "latitude": 31.2304,
        "longitude": 121.4737,
        "speed_knots_or_kmh": 18.5,
        "ambient_temp_celsius": 22.4,
        "destination_plant": "Sindelfingen",
        "timestamp": "2026-10-07T00:00:00Z"
    }

@pytest.fixture
def sample_hitl_audit_payload():
    """Provides a sample action payload for Human-In-The-Loop approval tests."""
    return {
        "action": "EMERGENCY_REROUTE_APPROVAL",
        "part_number": "MCU-A32-S",
        "vendor": "Infineon Dresden",
        "expedited_freight": True
    }