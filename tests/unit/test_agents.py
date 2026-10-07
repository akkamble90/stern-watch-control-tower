import pytest
from src.agents.state import AgentState
from src.agents.researcher import researcher_node
from src.agents.risk_analyst import risk_analyst_node
from src.agents.critic import critic_node, route_critic

def test_researcher_node(mock_neo4j_driver):
    state: AgentState = {
        "query": "Assess exposure for MCU-A32-S",
        "research_data": {},
        "analysis_report": "",
        "critic_feedback": "",
        "revision_count": 0,
        "is_verified": False,
        "requires_hitl": False
    }
    updated_state = researcher_node(state)
    assert "part_number" in updated_state["research_data"]
    assert updated_state["research_data"]["part_number"] == "MCU-A32-S"

def test_risk_analyst_node():
    state: AgentState = {
        "query": "Assess exposure",
        "research_data": {
            "part_number": "MCU-A32-S",
            "graph_context": {"plant_name": "Sindelfingen"},
            "buffer_inventory_days": 3.5,
            "alternative_suppliers": ["Infineon Dresden"]
        },
        "analysis_report": "",
        "critic_feedback": "",
        "revision_count": 0,
        "is_verified": False,
        "requires_hitl": False
    }
    updated_state = risk_analyst_node(state)
    assert "EXPOSURE & RISK EVALUATION REPORT" in updated_state["analysis_report"]
    assert updated_state["requires_hitl"] is True

def test_critic_node_cyclical_routing():
    # Test unverified iteration (triggers revision loop)
    state_unverified: AgentState = {
        "query": "",
        "research_data": {},
        "analysis_report": "Stoppage Cost: €16.8M / day.",
        "critic_feedback": "",
        "revision_count": 0,
        "is_verified": False,
        "requires_hitl": True
    }
    next_node = route_critic(critic_node(state_unverified))
    assert next_node == "revise"

    # Test verified iteration (triggers approval termination)
    state_verified: AgentState = {
        "query": "",
        "research_data": {},
        "analysis_report": "Verified report",
        "critic_feedback": "",
        "revision_count": 2,
        "is_verified": True,
        "requires_hitl": True
    }
    next_node_verified = route_critic(state_verified)
    assert next_node_verified == "approved"