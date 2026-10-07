import streamlit as st
import pandas as pd

def render_bom_table():
    st.header(" Critical Stock & Material Risk Matrix")
    st.caption("Real-time monitoring of raw material inventory, BOM availability, and component disruption risks.")

    # Comprehensive Automotive Parts & Categories
    bom_data = [
        # Engine and Powertrain Parts
        {"Category": "Engine & Powertrain", "Component Name": "Torque Converter Assembly", "Part Number": "TC-990-MB", "Stock Level (Units)": 420, "Reorder Threshold": 500, "Lead Time (Days)": 14, "Supplier": "ZF Friedrichshafen", "Risk Status": "CRITICAL"},
        {"Category": "Engine & Powertrain", "Component Name": "Drive Shaft / Propeller Shaft", "Part Number": "DS-441-EQ", "Stock Level (Units)": 650, "Reorder Threshold": 600, "Lead Time (Days)": 10, "Supplier": "GKN Automotive", "Risk Status": "HEALTHY"},
        {"Category": "Engine & Powertrain", "Component Name": "Axle Shaft (Front Left/Right)", "Part Number": "AX-102-MB", "Stock Level (Units)": 310, "Reorder Threshold": 450, "Lead Time (Days)": 18, "Supplier": "American Axle", "Risk Status": "HIGH RISK"},
        {"Category": "Engine & Powertrain", "Component Name": "Dual-Mass Flywheel", "Part Number": "FW-882-EX", "Stock Level (Units)": 890, "Reorder Threshold": 700, "Lead Time (Days)": 8, "Supplier": "LuK / Schaeffler", "Risk Status": "HEALTHY"},

        # Braking System Parts
        {"Category": "Braking System", "Component Name": "Ventilated Brake Discs (Front)", "Part Number": "BD-771-AMG", "Stock Level (Units)": 1200, "Reorder Threshold": 1000, "Lead Time (Days)": 6, "Supplier": "Brembo", "Risk Status": "HEALTHY"},
        {"Category": "Braking System", "Component Name": "Hydraulic Brake Caliper Module", "Part Number": "BC-204-MB", "Stock Level (Units)": 280, "Reorder Threshold": 400, "Lead Time (Days)": 12, "Supplier": "Continental Automotive", "Risk Status": "HIGH RISK"},
        {"Category": "Braking System", "Component Name": "ABS / ESP Control Unit", "Part Number": "ABS-909-CU", "Stock Level (Units)": 150, "Reorder Threshold": 350, "Lead Time (Days)": 21, "Supplier": "Bosch", "Risk Status": "CRITICAL"},

        # Suspension and Steering Parts
        {"Category": "Suspension & Steering", "Component Name": "Air Suspension Strut (AIRMATIC)", "Part Number": "AS-550-EQS", "Stock Level (Units)": 190, "Reorder Threshold": 300, "Lead Time (Days)": 15, "Supplier": "Bilstein", "Risk Status": "CRITICAL"},
        {"Category": "Suspension & Steering", "Component Name": "Electronic Power Steering Rack", "Part Number": "EPS-331-MB", "Stock Level (Units)": 520, "Reorder Threshold": 500, "Lead Time (Days)": 9, "Supplier": "Thyssenkrupp", "Risk Status": "HEALTHY"},
        {"Category": "Suspension & Steering", "Component Name": "Front Lower Control Arms", "Part Number": "CA-812-MB", "Stock Level (Units)": 740, "Reorder Threshold": 600, "Lead Time (Days)": 7, "Supplier": "Meyle", "Risk Status": "HEALTHY"},

        # Electrical Parts & Electronics
        {"Category": "Electrical Systems", "Component Name": "Microcontroller Unit (MCU-A32-S)", "Part Number": "MCU-A32-S", "Stock Level (Units)": 120, "Reorder Threshold": 500, "Lead Time (Days)": 45, "Supplier": "Infineon Technologies", "Risk Status": "CRITICAL"},
        {"Category": "Electrical Systems", "Component Name": "High-Voltage Wiring Harness", "Part Number": "WH-901-EV", "Stock Level (Units)": 340, "Reorder Threshold": 400, "Lead Time (Days)": 16, "Supplier": "Leoni AG", "Risk Status": "HIGH RISK"},
        {"Category": "Electrical Systems", "Component Name": "48V Mild-Hybrid Starter Generator", "Part Number": "SG-48V-MB", "Stock Level (Units)": 610, "Reorder Threshold": 500, "Lead Time (Days)": 11, "Supplier": "Valeo", "Risk Status": "HEALTHY"},

        # Cooling and Exhaust Parts
        {"Category": "Cooling & Exhaust", "Component Name": "Electric Water Pump (Battery Cooling)", "Part Number": "WP-112-EV", "Stock Level (Units)": 230, "Reorder Threshold": 350, "Lead Time (Days)": 14, "Supplier": "Pierburg", "Risk Status": "HIGH RISK"},
        {"Category": "Cooling & Exhaust", "Component Name": "Aluminum Radiator Core", "Part Number": "RAD-404-MB", "Stock Level (Units)": 910, "Reorder Threshold": 750, "Lead Time (Days)": 5, "Supplier": "Mahl", "Risk Status": "HEALTHY"},
        {"Category": "Cooling & Exhaust", "Component Name": "Selective Catalytic Reduction (SCR) Module", "Part Number": "SCR-880-DI", "Stock Level (Units)": 480, "Reorder Threshold": 400, "Lead Time (Days)": 10, "Supplier": "Eberspächer", "Risk Status": "HEALTHY"}
    ]

    df_bom = pd.DataFrame(bom_data)

    # Category Filter
    categories = ["All Categories"] + sorted(list(df_bom["Category"].unique()))
    selected_category = st.selectbox("🔍 Filter by Automotive System Category:", categories)

    if selected_category != "All Categories":
        filtered_df = df_bom[df_bom["Category"] == selected_category]
    else:
        filtered_df = df_bom

    # Quick Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Line Items", len(filtered_df))
    col2.metric("Critical Shortages", len(filtered_df[filtered_df["Risk Status"] == "CRITICAL"]))
    col3.metric("High Disruption Risk", len(filtered_df[filtered_df["Risk Status"] == "HIGH RISK"]))
    col4.metric("Healthy Stock Items", len(filtered_df[filtered_df["Risk Status"] == "HEALTHY"]))

    st.markdown("---")

    # Table Display Styling
    def highlight_risk(val):
        if val == "CRITICAL":
            return "background-color: #ff4b4b; color: white; font-weight: bold;"
        elif val == "HIGH RISK":
            return "background-color: #ffa500; color: black; font-weight: bold;"
        elif val == "HEALTHY":
            return "background-color: #28a745; color: white; font-weight: bold;"
        return ""

    styled_df = filtered_df.style.map(highlight_risk, subset=["Risk Status"])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)