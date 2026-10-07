from typing import TypedDict, Dict, Any, List, Optional

class AgentState(TypedDict):
    query: str
    research_data: Dict[str, Any]
    analysis_report: str
    critic_feedback: str
    revision_count: int
    is_verified: bool
    requires_hitl: bool