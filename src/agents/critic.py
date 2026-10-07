from src.agents.state import AgentState

def critic_node(state: AgentState) -> dict:
    # Safe retrieval prevents KeyError
    report = state.get("analysis_report", "")
    revision_count = state.get("revision_count", 0) + 1

    # Check if report satisfies conditions
    is_verified = revision_count >= 2 or len(report) > 50

    feedback = "Verified and approved." if is_verified else "Requesting deeper lead-time analysis."

    return {
        "critic_feedback": feedback,
        "is_verified": is_verified,
        "revision_count": revision_count,
        "requires_hitl": not is_verified
    }