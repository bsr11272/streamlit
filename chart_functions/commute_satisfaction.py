# chart_functions/commute_satisfaction.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def show_chart(df):
    # Define commute time bins
    bins = [0, 30, 60, 120]  # Define ranges for small, medium, and large commute times
    labels = ["Small (0-30 min)", "Medium (31-60 min)", "Large (61+ min)"]
    
    # Create commute categories
    df["commute_time_category"] = pd.cut(
        df["commutetime_quant"], 
        bins=bins, 
        labels=labels, 
        right=False
    )
    
    # Create enhanced boxplot
    fig = px.box(
        df,
        x="commute_time_category",
        y="wfh_feel_quant",
        title="WFH Value by Commute Time: Pay Trade-off Analysis",
        labels={
            "commute_time_category": "Daily Commute Duration",
            "wfh_feel_quant": "Acceptable Pay Change for WFH (%)"
        },
        color="commute_time_category",
        color_discrete_sequence=px.colors.qualitative.Set2,
        notched=True  # Add notches for better statistical comparison
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
        showlegend=False,  # Hide legend as it's redundant with x-axis
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
        # tickformat='.0%',  # Format as percentage
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    )

    # Enhance x-axis
    fig.update_xaxes(
        title_font=dict(size=14),
        tickfont=dict(size=12)
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # # Calculate and display key metrics
    # col1, col2, col3 = st.columns(3)
    
    # # Calculate statistics for each category
    # stats = df.groupby('commute_time_category')['wfh_feel_quant'].agg([
    #     ('median', 'median'),
    #     ('mean', 'mean'),
    #     ('count', 'count')
    # ])

    # # Find category with highest willingness to take pay cut
    # highest_paycut = stats['mean'].idxmin()
    # highest_paycut_value = stats.loc[highest_paycut, 'mean']

    # # Calculate correlation
    # correlation = df['commutetime_quant'].corr(df['wfh_feel_quant'])
    
    # with col1:
    #     st.metric(
    #         "Highest Pay Trade-off Group", 
    #         highest_paycut,
    #         f"{highest_paycut_value:.1%} avg. adjustment",
    #         help="Commute group willing to accept largest pay adjustment for WFH"
    #     )
    # with col2:
    #     st.metric(
    #         "Correlation", 
    #         f"{correlation:.2f}",
    #         help="Correlation between commute time and pay trade-off preference (-1 to 1)"
    #     )
    # with col3:
    #     total_responses = stats['count'].sum()
    #     st.metric(
    #         "Total Responses", 
    #         f"{total_responses:,}",
    #         help="Number of employees who provided both commute time and pay preference"
    #     )
