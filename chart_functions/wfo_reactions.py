# chart_functions/wfo_reactions.py
import streamlit as st
import plotly.express as px
import pandas as pd

def show_chart(df):
    # Map numeric labels to descriptions
    response_mapping = {
        1: "Comply and return",
        2: "Return & start looking for a WFH job",
        3: "Quit, regardless of getting another job",
    }

    # Convert numeric labels to categorical descriptions
    df["wbp_react_qual_desc"] = df["wbp_react_qual"].map(response_mapping)

    # Count occurrences of each response category per month
    grouped = df.groupby(["date_proper", "wbp_react_qual_desc"]).size().reset_index(name="count")

    # Create enhanced stacked bar chart
    fig = px.bar(
        grouped,
        x="date_proper",
        y="count",
        color="wbp_react_qual_desc",
        title="Employee Reactions to Return-to-Office Mandate",
        labels={
            "date_proper": "Date",
            "count": "Number of Responses",
            "wbp_react_qual_desc": "Employee Response"
        },
        color_discrete_sequence=px.colors.qualitative.Set2,  # Professional color scheme
        barmode='relative'  # For better visualization of proportions
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
        legend_title="Employee Response",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        width=1000,
        height=600,
        margin=dict(l=50, r=150, t=80, b=50)  # Increased right margin for legend
    )

    # Add grid lines
    fig.update_yaxes(
        gridcolor='lightgrey',
        griddash='dash',
        title_font=dict(size=14),
        tickfont=dict(size=12)
    )

    # Enhance x-axis
    fig.update_xaxes(
        title_font=dict(size=14),
        tickfont=dict(size=12),
        dtick="M2",  # Show every 2 months
        tickformat="%b %Y"  # Format as "Jan 2023"
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # Calculate and display key metrics
    # Get latest month's data
    latest_date = grouped['date_proper'].max()
    latest_data = grouped[grouped['date_proper'] == latest_date]
    
    # Calculate total responses and percentages for the latest month
    total_latest = latest_data['count'].sum()
    response_percentages = latest_data.set_index('wbp_react_qual_desc')['count'] / total_latest * 100
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Would Comply", 
            f"{response_percentages.get('Comply and return', 0):.1f}%",
            help="Percentage of employees who would comply with return-to-office mandate"
        )
    with col2:
        st.metric(
            "Would Look for WFH Job", 
            f"{response_percentages.get('Return & start looking for a WFH job', 0):.1f}%",
            help="Percentage of employees who would look for a new WFH job"
        )
    with col3:
        st.metric(
            "Would Quit Immediately", 
            f"{response_percentages.get('Quit, regardless of getting another job', 0):.1f}%",
            help="Percentage of employees who would quit regardless of having another job"
        )

    # # Add trend analysis
    # st.markdown("### Trend Analysis")
    
    # # Calculate month-over-month change
    # previous_month = grouped[grouped['date_proper'] < latest_date]['date_proper'].max()
    # previous_data = grouped[grouped['date_proper'] == previous_month]
    
    # if not previous_data.empty:
    #     prev_total = previous_data['count'].sum()
    #     prev_percentages = previous_data.set_index('wbp_react_qual_desc')['count'] / prev_total * 100
        
    #     changes = {k: response_percentages.get(k, 0) - prev_percentages.get(k, 0) 
    #               for k in response_mapping.values()}
        
    #     trends = [f"- {'🔺' if changes[k] > 1 else '🔻' if changes[k] < -1 else '➖'} {k}: "
    #              f"{abs(changes[k]):.1f}% {'increase' if changes[k] > 0 else 'decrease' if changes[k] < 0 else 'no change'} "
    #              f"from previous month" for k in response_mapping.values()]
        
    #     st.markdown("\n".join(trends))