from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.researcher import researcher_node
from src.agents.risk_analyst import risk_analyst_node
from src.agents.critic import critic_node

def route_critic(state: AgentState) -> str:
    if state["is_verified"] or state["revision_count"] >= 3:
        return "approved"
    return "revise"

def build_control_tower_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("risk_analyst", risk_analyst_node)
    workflow.add_node("critic", critic_node)

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "risk_analyst")
    workflow.add_edge("risk_analyst", "critic")

    workflow.add_conditional_edges(
        "critic",
        route_critic,
        {
            "approved": END,
            "revise": "risk_analyst"
        }
    )
    return workflow.compile()

agent_app = build_control_tower_agent()