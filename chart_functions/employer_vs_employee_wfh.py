# chart_functions/employer_vs_employee_wfh.py
import streamlit as st
import plotly.express as px
import pandas as pd

def show_chart(df):
    # Group and prepare the data
    df_grouped = df.groupby(
        ["wfh_days_postCOVID_ss", "wfh_days_postCOVID_boss_ss"]
    ).size().reset_index(name="counts")
    
    # Create enhanced bar chart
    fig = px.bar(
        df_grouped,
        x="wfh_days_postCOVID_ss",
        y="counts",
        color="wfh_days_postCOVID_boss_ss",
        barmode="group",
        title="Work From Home Days: Alignment Between Employers and Employees",
        labels={
            "wfh_days_postCOVID_ss": "Employee Desired WFH Days",
            "counts": "Number of Respondents",
            "wfh_days_postCOVID_boss_ss": "Employer Planned WFH Days"
        },
        color_discrete_sequence=px.colors.qualitative.Set3,  # Professional color palette
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
        legend_title="Employer Planned<br>WFH Days",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        bargap=0.2,
        bargroupgap=0.1,
        # Set specific width and height
        width=1000,
        height=600,
        # Add margins for better spacing
        margin=dict(l=50, r=50, t=80, b=50),
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
        tickmode='linear',
        tick0=0,
        dtick=1
    )

    # Calculate alignment metrics
    perfect_alignment = (df['wfh_days_postCOVID_ss'] == df['wfh_days_postCOVID_boss_ss']).mean() * 100
    avg_employee_desire = df['wfh_days_postCOVID_ss'].mean()
    avg_employer_plan = df['wfh_days_postCOVID_boss_ss'].mean()
    difference = avg_employee_desire - avg_employer_plan

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Perfect Alignment", 
            f"{perfect_alignment:.1f}%",
            help="Percentage where employer plans match employee preferences exactly"
        )
    with col2:
        st.metric(
            "Avg. Employee Desire", 
            f"{avg_employee_desire:.1f} days",
            f"{difference:+.1f} days vs employer",
            help="Average number of WFH days desired by employees"
        )
    with col3:
        st.metric(
            "Avg. Employer Plan", 
            f"{avg_employer_plan:.1f} days",
            help="Average number of WFH days planned by employers"
        )