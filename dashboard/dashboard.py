import streamlit as st
import pandas as pd
import os
from datetime import datetime

def load_threat_data():
    """Load and preprocess threat data"""
    csv_path = "logs/central_reports.csv"
    
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    
    try:
        # Read CSV without assuming headers
        df = pd.read_csv(csv_path, header=None)
        
        # Check if we have enough columns
        if len(df.columns) >= 5:
            # Assign proper column names based on your CSV structure
            df.columns = ['index', 'timestamp', 'source', 'threat_level', 'threat_type', 'indicators'][:len(df.columns)]
            
            # Convert timestamp
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df.sort_values('timestamp', ascending=False)
        else:
            st.error("CSV doesn't contain enough columns")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def main():
    st.title("Threat Intelligence Dashboard")
    
    threats = load_threat_data()
    
    if threats.empty:
        st.warning("No threat data available. Run the monitoring system first.")
        return
    
    # Show raw data for debugging
    with st.expander("View Raw Data"):
        st.write(threats)
    
    # Metrics
    st.subheader("Key Metrics")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Total Threats", len(threats))
    with cols[1]:
        st.metric("Critical Threats", len(threats[threats['threat_level'] == 'CRITICAL']))
    with cols[2]:
        st.metric("Last Alert", threats['timestamp'].max().strftime("%Y-%m-%d %H:%M"))
    
    # Visualizations
    st.subheader("Threat Breakdown")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("By Threat Level")
        st.bar_chart(threats['threat_level'].value_counts())
    
    with col2:
        st.write("By Source")
        st.bar_chart(threats['source'].value_counts())
    
    # Detailed View
    st.subheader("Recent Alerts")
    st.dataframe(
        threats[['timestamp', 'source', 'threat_level', 'threat_type', 'indicators']],
        column_config={
            "timestamp": "Time",
            "source": "Source",
            "threat_level": "Severity",
            "threat_type": "Type",
            "indicators": "Details"
        },
        hide_index=True,
        use_container_width=True
    )

if __name__ == "__main__":
    main()