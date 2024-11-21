# chart_functions/productivity_trends.py
import streamlit as st
import plotly.express as px
import pandas as pd

def show_chart(df):
    # Data preparation
    # Convert WFH days to numeric values
    df["wfh_days_numeric"] = df["wfh_days_postCOVID_s"].replace({
        "0": 0, 
        "1-2": 1.5, 
        "3-4": 3.5, 
        "5": 5
    }).astype(float)

    # Group by date and desired WFH days to calculate mean efficiency
    grouped = df.groupby(
        ["date_proper", "wfh_days_numeric"]
    )["wfh_eff_COVID_quant"].mean().reset_index()

    # Create improved line chart
    fig = px.line(
        grouped,
        x="date_proper",
        y="wfh_eff_COVID_quant",
        color="wfh_days_numeric",
        title="Productivity Trends by Desired WFH Days",
        labels={
            "date_proper": "Date",
            "wfh_eff_COVID_quant": "Efficiency (%)",
            "wfh_days_numeric": "WFH Days per Week"
        },
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2  # Professional color scheme
    )

    # Enhance the layout
    fig.update_layout(
        plot_bgcolor="white",
        title={
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)
        },
        legend_title="WFH Days<br>per Week",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        width=1000,
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Add grid lines
    fig.update_yaxes(
        gridcolor='lightgrey',
        griddash='dash',
        title_font=dict(size=14),
        tickfont=dict(size=12),
        tickformat='.1%'  # Format as percentage
    )

    # Enhance x-axis
    fig.update_xaxes(
        title_font=dict(size=14),
        tickfont=dict(size=12),
        dtick="M2",  # Show every 2 months
        tickformat="%b %Y"  # Format as "Jan 2023"
    )

    # Add hover template
    fig.update_traces(
        hovertemplate="<b>Date:</b> %{x|%B %Y}<br>" +
                     "<b>Efficiency:</b> %{y:.1%}<br>" +
                     "<b>WFH Days:</b> %{customdata:.1f}<br>" +
                     "<extra></extra>",
        customdata=grouped['wfh_days_numeric']
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # # Calculate and display key metrics
    # latest_date = grouped['date_proper'].max()
    # latest_data = grouped[grouped['date_proper'] == latest_date]
    
    # # Overall trend
    # overall_trend = grouped.groupby('wfh_days_numeric')['wfh_eff_COVID_quant'].mean()
    # most_productive_days = overall_trend.idxmax()
    # highest_efficiency = overall_trend.max()

    # col1, col2, col3 = st.columns(3)
    
    # with col1:
    #     st.metric(
    #         "Most Productive WFH Schedule", 
    #         f"{most_productive_days:.1f} days",
    #         help="Number of WFH days associated with highest average efficiency"
    #     )
    # with col2:
    #     st.metric(
    #         "Peak Efficiency", 
    #         f"{highest_efficiency:.1%}",
    #         help="Highest average efficiency achieved"
    #     )
    # with col3:
    #     efficiency_range = latest_data['wfh_eff_COVID_quant'].max() - latest_data['wfh_eff_COVID_quant'].min()
    #     st.metric(
    #         "Efficiency Range", 
    #         f"{efficiency_range:.1%}",
    #         help="Difference between highest and lowest efficiency in latest period"
    #     )