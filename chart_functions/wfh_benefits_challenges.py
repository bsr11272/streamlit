# chart_functions/wfh_benefits_challenges.py
import streamlit as st
import plotly.express as px
import pandas as pd

def show_chart(df):
    # Prepare the data
    df_benefits = df.melt(
        id_vars=["date_proper"], 
        value_vars=[
            "wfh_top3benefits_commute",
            "wfh_top3benefits_quiet", 
            "wfh_top3benefits_meetings",
            "lesseff_reasons_internet"
        ],
        var_name="Aspect",
        value_name="Count"
    )
    
    # Clean up aspect names for better readability
    aspect_names = {
        "wfh_top3benefits_commute": "No Commute",
        "wfh_top3benefits_quiet": "Quiet Environment",
        "wfh_top3benefits_meetings": "Better Meetings",
        "lesseff_reasons_internet": "Internet Issues"
    }
    df_benefits['Aspect'] = df_benefits['Aspect'].map(aspect_names)
    
    # Create enhanced bar chart
    fig = px.bar(
        df_benefits,
        x="date_proper",
        y="Count",
        color="Aspect",
        title="Evolution of WFH Benefits and Challenges Over Time",
        labels={
            "date_proper": "Date",
            "Count": "Number of Responses",
            "Aspect": "Benefits & Challenges"
        },
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Safe,  # Professional color palette
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
        legend_title="Benefits & Challenges",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        bargap=0.2,
        bargroupgap=0.1,
        width=1000,
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
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
    st.plotly_chart(fig, use_container_width=False)

    # Calculate and display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    latest_date = df_benefits['date_proper'].max()
    latest_data = df_benefits[df_benefits['date_proper'] == latest_date]
    
    metrics = {aspect: group['Count'].sum() 
              for aspect, group in latest_data.groupby('Aspect')}
    
    with col1:
        st.metric(
            "No Commute Impact", 
            f"{metrics['No Commute']:,.0f}",
            help="Number of respondents citing commute savings as a benefit"
        )
    with col2:
        st.metric(
            "Quiet Environment", 
            f"{metrics['Quiet Environment']:,.0f}",
            help="Number of respondents valuing quiet work environment"
        )
    with col3:
        st.metric(
            "Better Meetings", 
            f"{metrics['Better Meetings']:,.0f}",
            help="Number of respondents reporting improved meeting efficiency"
        )
    with col4:
        st.metric(
            "Internet Challenges", 
            f"{metrics['Internet Issues']:,.0f}",
            help="Number of respondents facing internet connectivity issues"
        )