import streamlit as st
from src.agents.graph_builder import agent_app

def render_agent_tab():
    st.header("Cyclical Multi-Agent Command Center")
    
    user_query = st.text_input(
        "Enter operational query:",
        placeholder="e.g., Evaluate supply chain risk for Torque Converters at Bremen Plant..."
    )
    
    if st.button("Run Multi-Agent Analysis", type="primary"):
        if not user_query.strip():
            st.warning("Please enter an operational query first.")
            return

        with st.spinner("Orchestrating LangGraph agents..."):
            # Initial state matches AgentState schema exactly
            initial_state = {
                "query": user_query,
                "research_data": {},
                "analysis_report": "",
                "critic_feedback": "",
                "revision_count": 0,
                "is_verified": False,
                "requires_hitl": False
            }
            
            final_state = agent_app.invoke(initial_state)
            
            st.success("Workflow Verified & Completed")
            st.markdown("### EXPOSURE & RISK EVALUATION REPORT")
            st.info(f"**Target Query Processed:** {user_query}")
            st.markdown(final_state.get("analysis_report", "No report generated."))