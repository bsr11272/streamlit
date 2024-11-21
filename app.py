# app.py
import streamlit as st
import zipfile
from io import BytesIO
import pandas as pd
from chart_functions import (desired_wfh_days, 
                             employer_vs_employee_wfh, wfh_benefits_challenges, 
                             productivity_trends, industry_efficiency, 
                             regional_preferences, wfo_reactions, commute_satisfaction
                             )

# Set wide layout at the start
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    # Read the zip file
    with zipfile.ZipFile('data/WFHdata_October24.zip', 'r') as zip_ref:
        # Assuming the CSV file name inside the zip is 'WFHdata_October24.csv'
        with zip_ref.open('WFHdata_October24.csv') as csv_file:
            # Read the CSV from the zip file
            df = pd.read_csv(csv_file, low_memory=False)
    
    # Convert date string to datetime
    df["date_proper"] = pd.to_datetime(df["date"].str.replace("m", "-"), format="%Y-%m")
    return df

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