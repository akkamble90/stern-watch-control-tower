import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Database Connection
DB_URL = "postgresql://postgres:password123@localhost:5432/control_tower_db"

def get_engine():
    return create_engine(DB_URL)

@st.fragment(run_every="3s")
def render_live_telemetry_stream():
    """Polled fragment for Kafka/PySpark PostgreSQL telemetry stream."""
    st.subheader(" Real-Time Vehicle & Asset Telemetry Stream")
    try:
        engine = get_engine()
        df_stream = pd.read_sql("SELECT * FROM telemetry_events ORDER BY timestamp DESC LIMIT 100", engine)
        
        if df_stream.empty:
            st.info("Waiting for incoming telemetry stream records from PySpark...")
            return

        stream_col1, stream_col2 = st.columns(2)
        
        with stream_col1:
            fig_speed = px.line(
                df_stream, 
                x="timestamp", 
                y="speed", 
                color="vehicle_id" if "vehicle_id" in df_stream.columns else None,
                title="Vehicle Speed Stream (km/h)"
            )
            st.plotly_chart(fig_speed, use_container_width=True)
            
        with stream_col2:
            fig_map = px.scatter_mapbox(
                df_stream, 
                lat="latitude", 
                lon="longitude", 
                hover_name="vehicle_id" if "vehicle_id" in df_stream.columns else None,
                zoom=4, 
                title="Live Asset Locations"
            )
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map, use_container_width=True)
            
    except Exception as e:
        st.warning("Waiting for live telemetry stream data...")

def render_powerbi_tab():
    st.header("📊 Executive Power BI Control Tower")
    st.caption("Live Power BI Dashboard — Updates published in Power BI sync here automatically.")

    # 🔗 PASTE THE LINK FROM YOUR SCREENSHOT HERE
    POWERBI_EMBED_URL = "https://app.powerbi.com/reportEmbed?reportId=87538da2-6beb-4568-8feb-e4878c01df79&autoAuth=true&ctid=b4c6b754-54e3-41e4-a8da-304355c62816"

    # Embed Power BI report iframe outside of st.fragment
    components.html(
        f"""
        <iframe 
            title="Supply Chain Control Tower Power BI" 
            width="100%" 
            height="750" 
            src="{POWERBI_EMBED_URL}" 
            frameborder="0" 
            allowFullScreen="true">
        </iframe>
        """,
        height=770
    )

    st.markdown("---")