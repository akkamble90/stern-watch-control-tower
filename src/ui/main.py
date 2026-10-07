import sys
from pathlib import Path

# 1. MUST BE AT THE VERY TOP BEFORE ANY SRC IMPORTS
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# 2. Now import Streamlit and project components
import streamlit as st
from src.ui.components.header import render_header
from src.ui.components.kpi_cards import render_kpi_cards
from src.ui.components.powerbi_embed import render_powerbi_tab
from src.ui.components.agent_console import render_agent_tab
from src.ui.components.bom_table import render_bom_table

st.set_page_config(page_title="Mercedes-Benz Control Tower", page_icon="🚘", layout="wide")

render_header()
render_kpi_cards()

tab_pbi, tab_agents, tab_bom = st.tabs([
    "Executive Control Tower",
    "Cyclical Multi-Agent Command Center",
    "Strategic Stock & BOM Explosion"
])

with tab_pbi:
    render_powerbi_tab()

with tab_agents:
    render_agent_tab()

with tab_bom:
    render_bom_table()