import streamlit as st

def render_kpi_cards():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Global Network Health", value="94.2%", delta="-1.8%")
    with col2:
        st.metric(label="Critical Part At Risk", value="MCU-A32-S", delta="3.5 Days Stock")
    with col3:
        st.metric(label="Active Shipments Monitored", value="14,290", delta="+312 Today")
    with col4:
        st.metric(label="Mitigated Stoppage Costs (MTD)", value="€42.8M", delta="+€8.1M")