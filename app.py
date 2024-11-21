# app.py
import streamlit as st
import zipfile
from io import BytesIO
import pandas as pd
from pathlib import Path
from chart_functions import (desired_wfh_days, 
                             employer_vs_employee_wfh, wfh_benefits_challenges, 
                             productivity_trends, industry_efficiency, 
                             regional_preferences, wfo_reactions, commute_satisfaction
                             )

# Set wide layout at the start
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    try:
        # Get the directory where app.py is located
        current_dir = Path(__file__).parent
        
        # Construct path to the zip file
        zip_path = current_dir / "data" / "WFHdata_October24_minimal.zip"
        
        st.write(f"Attempting to read from: {zip_path}")  # Debug info
        
        # Check if file exists
        if not zip_path.exists():
            st.error(f"Zip file not found at {zip_path}")
            return None

        # Read the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all files in zip for debugging
            st.write(f"Files in zip: {zip_ref.namelist()}")  # Debug info
            
            # Get the CSV filename (assuming it's the only or first CSV)
            csv_name = next(name for name in zip_ref.namelist() if name.endswith('.csv'))
            
            with zip_ref.open(csv_name) as csv_file:
                df = pd.read_csv(csv_file, low_memory=False)
                
                # Convert date string to datetime
                df["date_proper"] = pd.to_datetime(df["date"].str.replace("m", "-"), format="%Y-%m")
                return df

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

df = load_data()

# Get the chart parameter from URL
chart_type = st.query_params.get("chart", "home")

# Update chart selection
if chart_type == "employer_employee":
    employer_vs_employee_wfh.show_chart(df)
elif chart_type == "benefits_challenges":
    wfh_benefits_challenges.show_chart(df)
elif chart_type == "productivity":
    productivity_trends.show_chart(df)
elif chart_type == "industry":
    industry_efficiency.show_chart(df)
elif chart_type == "regional":
    regional_preferences.show_chart(df)
elif chart_type == "reactions":
    wfo_reactions.show_chart(df)
elif chart_type == "commute":
    commute_satisfaction.show_chart(df)
else:
    desired_wfh_days.show_chart(df)