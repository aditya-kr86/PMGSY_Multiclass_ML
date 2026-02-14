"""
CSS styles for the Streamlit application.
Clean, premium, minimal design.
"""

import streamlit as st


def apply_styles():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Base styling */
            .main {
                background-color: #fafbfc;
                font-family: 'Inter', sans-serif;
            }
            .stApp {
                background-color: #fafbfc;
            }
            
            /* Typography */
            h1, h2, h3 {
                color: #1a1a2e;
                font-weight: 600;
                letter-spacing: -0.02em;
            }
            
            /* Premium card */
            .premium-card {
                background: white;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                border: 1px solid #eef0f2;
                margin-bottom: 16px;
            }
            
            /* Stat cards */
            .stat-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.06);
                border: 1px solid #eef0f2;
            }
            .stat-value {
                font-size: 32px;
                font-weight: 700;
                color: #1a1a2e;
                margin: 8px 0;
            }
            .stat-label {
                font-size: 13px;
                color: #6b7280;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            /* Confidence badges */
            .confidence-badge {
                display: inline-block;
                padding: 6px 14px;
                border-radius: 100px;
                font-weight: 600;
                font-size: 13px;
            }
            .high-confidence {
                background-color: #ecfdf5;
                color: #059669;
            }
            .medium-confidence {
                background-color: #fffbeb;
                color: #d97706;
            }
            .low-confidence {
                background-color: #fef2f2;
                color: #dc2626;
            }
            
            /* Header */
            .header-section {
                padding: 40px 0 30px 0;
                border-bottom: 1px solid #eef0f2;
                margin-bottom: 32px;
            }
            .header-title {
                font-size: 28px;
                font-weight: 700;
                color: #1a1a2e;
                margin: 0 0 8px 0;
            }
            .header-subtitle {
                font-size: 15px;
                color: #6b7280;
                margin: 0;
            }
            
            /* Section titles */
            .section-title {
                font-size: 16px;
                font-weight: 600;
                color: #1a1a2e;
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            /* Input styling */
            .stSelectbox > div > div,
            .stNumberInput > div > div > input {
                border-radius: 10px !important;
                border: 1px solid #e5e7eb !important;
            }
            
            /* Input labels */
            .stSelectbox label,
            .stNumberInput label {
                font-weight: 500 !important;
                color: #374151 !important;
                font-size: 14px !important;
            }
            
            /* Button styling */
            .stButton > button {
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 32px;
                font-weight: 600;
                font-size: 15px;
                transition: all 0.2s ease;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
            }
            .stButton > button:hover {
                box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
                transform: translateY(-1px);
            }
            
            /* Test case buttons - smaller compact style with no hover effects */
            [data-testid="column"] [data-testid="stButton"] > button[kind="secondary"] {
                background: white;
                color: #374151;
                border: 1px solid #e5e7eb;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                transition: none;
            }
            [data-testid="column"] [data-testid="stButton"] > button[kind="secondary"]:hover {
                background: white;
                border-color: #e5e7eb;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                transform: none;
            }
            
            /* Metric override */
            [data-testid="stMetric"] {
                background: white;
                padding: 16px;
                border-radius: 12px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.06);
                border: 1px solid #eef0f2;
            }
            
            /* Form container */
            .form-section {
                background: white;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                border: 1px solid #eef0f2;
                margin: 16px 0;
            }
            
            .form-group-title {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 12px;
                padding-bottom: 8px;
                border-bottom: 1px solid #f3f4f6;
            }
            
            /* Hide default Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
