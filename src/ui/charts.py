"""
Chart visualizations for the Streamlit application.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import List


def render_gauge_chart(confidence: float):
    """
    Render a confidence gauge chart.
    
    Args:
        confidence: Confidence percentage (0-100)
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        number={'suffix': '%', 'font': {'size': 36, 'color': '#1a1a2e'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "#e5e7eb",
                'tickfont': {'color': '#6b7280'}
            },
            'bar': {'color': "#3b82f6", 'thickness': 0.3},
            'bgcolor': "#f3f4f6",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 60], 'color': '#fef2f2'},
                {'range': [60, 80], 'color': '#fffbeb'},
                {'range': [80, 100], 'color': '#ecfdf5'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#1a1a2e", 'family': "Inter"},
        height=250,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, width='stretch')


def render_probability_chart(probabilities: List[float], max_confidence: float):
    """
    Render a bar chart showing probability distribution across classes.
    
    Args:
        probabilities: List of probability values for each class
        max_confidence: The highest confidence value (for highlighting)
    """
    with st.expander("View All Class Probabilities", expanded=False):
        fig = go.Figure(
            data=[
                go.Bar(
                    x=[f"Class {i}" for i in range(len(probabilities))],
                    y=[p * 100 for p in probabilities],
                    marker_color=[
                        '#3b82f6' if p == max_confidence else '#e5e7eb' 
                        for p in probabilities
                    ],
                    text=[f"{p*100:.1f}%" for p in probabilities],
                    textposition='outside',
                    textfont={'color': '#6b7280', 'size': 11}
                )
            ]
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Probability (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1a1a2e'),
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=20, b=40),
            yaxis=dict(gridcolor='#f3f4f6', zerolinecolor='#f3f4f6'),
            xaxis=dict(tickfont={'color': '#6b7280'})
        )

        st.plotly_chart(fig, width='stretch')
