"""
PMGSY Scheme Predictor - Main Application

A Streamlit application for predicting PMGSY (Pradhan Mantri Gram Sadak Yojana) 
scheme classification using IBM Cloud Machine Learning.

Usage:
    streamlit run app.py
"""

import streamlit as st

# Configure page - must be first Streamlit command
st.set_page_config(
    page_title="PMGSY Scheme Predictor",
    page_icon="🛣️",
    layout="wide"
)

# Import modules after page config
from src.config import config
from src.api import IBMCloudClient
from src.api.ibm_client import get_confidence_level
from src.data import DataLoader
from src.ui import (
    apply_styles,
    render_header,
    render_stats,
    render_input_form,
    render_result
)
from src.ui.components import render_model_metrics
from src.ui.charts import render_gauge_chart, render_probability_chart


def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'prediction_count' not in st.session_state:
        st.session_state.prediction_count = 0


def main():
    """Main application entry point."""
    
    # Initialize
    init_session_state()
    apply_styles()
    
    # Load data
    data_loader = DataLoader(config.DATA_PATH)
    stats = data_loader.get_statistics()
    states = data_loader.get_states()
    
    # Render UI components
    render_header()
    render_stats(stats, st.session_state.prediction_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_model_metrics()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input form
    form_data = render_input_form(states, data_loader.get_districts)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Predict button
    if st.button("🔮 Predict Scheme", width='stretch'):
        with st.spinner('Analyzing project data...'):
            
            # Create API client and make prediction
            client = IBMCloudClient()
            
            try:
                prediction, probabilities, max_confidence = client.predict_scheme(
                    state=form_data["state"],
                    district=form_data["district"],
                    road_sanctioned=form_data["road_sanctioned"],
                    length_sanctioned=form_data["length_sanctioned"],
                    bridges_sanctioned=form_data["bridges_sanctioned"],
                    cost_sanctioned=form_data["cost_sanctioned"],
                    road_completed=form_data["road_completed"],
                    length_completed=form_data["length_completed"],
                    bridges_completed=form_data["bridges_completed"],
                    expenditure=form_data["expenditure"],
                    road_balance=form_data["road_balance"],
                    length_balance=form_data["length_balance"],
                    bridges_balance=form_data["bridges_balance"]
                )
                
                # Increment prediction counter
                st.session_state.prediction_count += 1
                
                # Get confidence level styling
                conf_level, conf_class = get_confidence_level(max_confidence)
                
                # Render results
                st.markdown("<br>", unsafe_allow_html=True)
                render_result(prediction, max_confidence * 100, conf_class)
                render_gauge_chart(max_confidence * 100)
                render_probability_chart(probabilities, max_confidence)
                
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")
                st.info("Please check your IBM Cloud credentials and try again.")


if __name__ == "__main__":
    main()
