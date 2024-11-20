import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="WFH Productivity Graph",
    page_icon="📊",
    layout="wide"
)

# Hide deployment information
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        .viewerBadge_container__1QSob {display: none;}
        .viewerBadge_link__1QSob {display: none;}
        .viewerBadge_text__1QSob {display: none;}
    </style>
""", unsafe_allow_html=True)

# Create sample data
def generate_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
    np.random.seed(42)
    
    return pd.DataFrame({
        'Date': dates,
        'WFH_Productivity': 85 + np.random.normal(0, 2, len(dates)),
        'Office_Productivity': 82 + np.random.normal(0, 2, len(dates))
    })

# Load data
df = generate_sample_data()

# Add sidebar filters
st.sidebar.header("📊 Filters")

# Date range filter
start_date = st.sidebar.date_input(
    "Start Date",
    value=df['Date'].min()
)
end_date = st.sidebar.date_input(
    "End Date",
    value=df['Date'].max()
)

# Filter data based on date range
mask = (df['Date'] >= pd.Timestamp(start_date)) & (df['Date'] <= pd.Timestamp(end_date))
filtered_df = df.loc[mask]

# Create the plot
fig = go.Figure()

# Add WFH trace
fig.add_trace(go.Scatter(
    x=filtered_df['Date'],
    y=filtered_df['WFH_Productivity'],
    name='WFH',
    line=dict(color='#1f77b4', width=3),
    hovertemplate='<b>WFH Productivity</b>: %{y:.1f}%<br>' +
                  '<b>Date</b>: %{x|%B %Y}<extra></extra>'
))

# Add Office trace
fig.add_trace(go.Scatter(
    x=filtered_df['Date'],
    y=filtered_df['Office_Productivity'],
    name='Office',
    line=dict(color='#ff7f0e', width=3),
    hovertemplate='<b>Office Productivity</b>: %{y:.1f}%<br>' +
                  '<b>Date</b>: %{x|%B %Y}<extra></extra>'
))

# Update layout
fig.update_layout(
    title={
        'text': 'Productivity Comparison: WFH vs Office',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified',
    xaxis=dict(
        title='Date',
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        showline=True,
        linewidth=2,
        linecolor='#E5E5E5'
    ),
    yaxis=dict(
        title='Productivity (%)',
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        range=[75, 95],
        showline=True,
        linewidth=2,
        linecolor='#E5E5E5'
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.8)'
    ),
    margin=dict(l=60, r=30, t=80, b=60)
)

# Add buttons for time range selection
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.7,
            y=1.2,
            showactive=True,
            buttons=list([
                dict(
                    label="All Time",
                    method="relayout",
                    args=[{"xaxis.range": [df['Date'].min(), df['Date'].max()]}]
                ),
                dict(
                    label="Last 6 Months",
                    method="relayout",
                    args=[{"xaxis.range": [df['Date'].max() - pd.DateOffset(months=6), df['Date'].max()]}]
                ),
                dict(
                    label="Last 3 Months",
                    method="relayout",
                    args=[{"xaxis.range": [df['Date'].max() - pd.DateOffset(months=3), df['Date'].max()]}]
                )
            ]),
        )
    ]
)

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    avg_wfh = filtered_df['WFH_Productivity'].mean()
    st.metric(
        label="Average WFH Productivity",
        value=f"{avg_wfh:.1f}%",
        delta=f"{avg_wfh - filtered_df['Office_Productivity'].mean():.1f}%"
    )

with col2:
    max_wfh = filtered_df['WFH_Productivity'].max()
    st.metric(
        label="Peak WFH Productivity",
        value=f"{max_wfh:.1f}%"
    )

with col3:
    min_wfh = filtered_df['WFH_Productivity'].min()
    st.metric(
        label="Lowest WFH Productivity",
        value=f"{min_wfh:.1f}%"
    )

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Add download button for data
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="productivity_data.csv",
    mime="text/csv"
)