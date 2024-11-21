# chart_functions/regional_preferences.py
import streamlit as st
import plotly.express as px
import pandas as pd

def show_chart(df):
    # Group by region to count preferences and calculate averages
    region_preferences = df.groupby("region").agg({
        "wfh_days_postCOVID_ss": ["count", "mean"],  # Count responses and average WFH days
        "wfh_eff_COVID_quant": "mean"  # Average efficiency
    }).reset_index()
    
    # Flatten column names
    region_preferences.columns = ["region", "counts", "avg_wfh_days", "avg_efficiency"]
    
    # Create enhanced choropleth
    fig = px.choropleth(
        region_preferences,
        locations="region",
        locationmode="USA-states",
        color="counts",
        title="WFH Survey Responses by State",
        color_continuous_scale="Blues",
        labels={
            "counts": "Number of Respondents",
            "region": "State",
            "avg_wfh_days": "Avg WFH Days",
            "avg_efficiency": "Avg Efficiency"
        },
        scope="usa",
        hover_data={
            "counts": True,
            "avg_wfh_days": ":.1f",
            "avg_efficiency": ":.1%"
        }
    )

    # Enhance the layout
    fig.update_layout(
        title={
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)
        },
        width=1200,
        height=600,
        margin=dict(l=20, r=20, t=80, b=20),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
            showland=True,
            landcolor="rgb(242, 242, 242)",
            showframe=False,
        )
    )

    # Update color bar
    fig.update_coloraxes(
        colorbar_title_font=dict(size=14),
        colorbar_tickfont=dict(size=12),
        colorbar_title_text="Number of<br>Respondents"
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # Calculate and display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Sort states by different metrics
    most_responses = region_preferences.nlargest(1, 'counts')
    highest_wfh = region_preferences.nlargest(1, 'avg_wfh_days')
    highest_eff = region_preferences.nlargest(1, 'avg_efficiency')
    
    with col1:
        st.metric(
            "Most Surveyed State", 
            most_responses['region'].iloc[0],
            f"{most_responses['counts'].iloc[0]:,} responses",
            help="State with the highest number of survey respondents"
        )
    with col2:
        st.metric(
            "State Coverage", 
            f"{len(region_preferences)} states",
            help="Number of states with survey responses"
        )
    with col3:
        st.metric(
            "Highest WFH Preference", 
            highest_wfh['region'].iloc[0],
            f"{highest_wfh['avg_wfh_days'].iloc[0]:.1f} days",
            help="State with highest average desired WFH days"
        )
    with col4:
        st.metric(
            "Most Efficient State", 
            highest_eff['region'].iloc[0],
            f"{highest_eff['avg_efficiency'].iloc[0]:.1%}",
            help="State with highest reported WFH efficiency"
        )