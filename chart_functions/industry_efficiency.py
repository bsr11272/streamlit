# chart_functions/industry_efficiency.py
import streamlit as st
import plotly.express as px
import pandas as pd

def show_chart(df):
    # Industry mapping
    industry_mapping = {
        1: "Agriculture",
        2: "Arts & Entertainment",
        3: "Finance & Insurance",
        4: "Construction",
        5: "Education",
        6: "Health Care & Social Assistance",
        7: "Hospitality & Food Services",
        8: "Information",
        9: "Manufacturing",
        10: "Mining",
        11: "Professional & Business Services",
        12: "Real Estate",
        13: "Retail Trade",
        14: "Transportation and Warehousing",
        15: "Utilities",
        16: "Wholesale Trade",
        17: "Government",
        18: "Other"
    }

    # Replace numeric industry codes with labels
    df["work_industry_label"] = df["work_industry"].map(industry_mapping)

    # Calculate median efficiency for sorting
    industry_medians = df.groupby('work_industry_label')['wfh_eff_COVID_quant'].median().sort_values(ascending=False)
    sorted_industries = industry_medians.index.tolist()

    # Create enhanced boxplot
    fig = px.box(
        df,
        x="work_industry_label",
        y="wfh_eff_COVID_quant",
        title="WFH Efficiency Across Industries",
        labels={
            "work_industry_label": "Industry",
            "wfh_eff_COVID_quant": "Efficiency (%)"
        },
        category_orders={"work_industry_label": sorted_industries},
        color="work_industry_label",
        color_discrete_sequence=px.colors.qualitative.Set3,
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
        showlegend=True,
        width=1000,
        height=800,
        margin=dict(l=50, r=50, t=80, b=120),  # Increased bottom margin for rotated labels
    )

    # Add grid lines and format y-axis
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
        tickfont=dict(size=12),
        tickangle=45,  # Rotate labels for better readability
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # # Calculate and display key metrics
    # col1, col2, col3 = st.columns(3)
    
    # # Find most and least efficient industries
    # industry_stats = df.groupby('work_industry_label')['wfh_eff_COVID_quant'].agg(['mean', 'std']).round(3)
    # most_efficient = industry_stats['mean'].idxmax()
    # least_efficient = industry_stats['mean'].idxmin()
    # overall_mean = df['wfh_eff_COVID_quant'].mean()
    
    # with col1:
    #     st.metric(
    #         "Most Efficient Industry", 
    #         most_efficient,
    #         f"{industry_stats.loc[most_efficient, 'mean']:.1%}",
    #         help="Industry with highest average WFH efficiency"
    #     )
    # with col2:
    #     st.metric(
    #         "Least Efficient Industry", 
    #         least_efficient,
    #         f"{industry_stats.loc[least_efficient, 'mean']:.1%}",
    #         help="Industry with lowest average WFH efficiency"
    #     )
    # with col3:
    #     st.metric(
    #         "Overall Average Efficiency", 
    #         f"{overall_mean:.1%}",
    #         help="Average efficiency across all industries"
    #     )
