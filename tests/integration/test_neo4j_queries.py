import pytest
from src.agents.tools.neo4j_tools import query_part_dependencies

def test_query_part_dependencies(mock_neo4j_driver):
    res = query_part_dependencies("MCU-A32-S")
    assert "plant_name" in res
    assert "suppliers" in res
    assert len(res["suppliers"]) > 0