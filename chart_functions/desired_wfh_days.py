# chart_functions/desired_wfh_days.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_chart(df):    
    # Create the enhanced histogram
    fig = px.histogram(
        df,
        x="wfh_days_postCOVID_ss",
        nbins=6,  # Set number of bins to match days of the week
        title="Distribution of Desired WFH Days (Post-COVID)",
        labels={
            "wfh_days_postCOVID_ss": "Desired WFH Days per Week",
            "count": "Number of Responses"
        },
        color_discrete_sequence=["#1f77b4"],  # Professional blue color
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
        bargap=0.1,  # Add space between bars
        showlegend=False,
        # Set specific width and height
        width=1000,
        height=600,
        # Add margins for better spacing
        margin=dict(l=50, r=50, t=80, b=50),
    )

    # Add grid lines only for y-axis
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
        dtick=1  # Show every day number
    )

    # Add mean line and annotation
    mean_value = df["wfh_days_postCOVID_ss"].mean()
    fig.add_vline(
        x=mean_value,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_value:.1f} days",
        annotation_position="top"
    )

    # Add insights below the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Display key statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Desired WFH Days", f"{mean_value:.1f}")
    with col2:
        st.metric("Most Common Choice", f"{df['wfh_days_postCOVID_ss'].mode().iloc[0]:.0f} days")
    with col3:
        st.metric("Total Responses", f"{len(df):,}")