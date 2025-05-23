# Custom CSS for better UI with dark mode compatibility and laptop screen optimization
import streamlit as st


def set_custom_style():
    st.markdown(
        """
    <style>
    .main-header {
        color: #60A5FA;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 0.8rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid #374151;
        font-family: Times New Roman, serif; !important;
        
        # background: linear-gradient(to right, #3B82F6, #60A5FA);
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #60A5FA;
        margin-top: 0.8rem;
        margin-bottom: 0.4rem;
    }
    .card {
        background-color: #1F2937;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        color: #E5E7EB;
    }
    .card h2, .card h3 {
        color: #60A5FA;
        margin-bottom: 0.6rem;
    }
    .card p, .card li {
        color: #E5E7EB;
        margin-bottom: 0.4rem;
    }
    .welcome-card {
        background-color: #1F2937;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        color: #E5E7EB;
        text-align: center;
    }
    .welcome-card h2 {
        color: #60A5FA;
        margin-bottom: 1rem;
    }
    .welcome-card p {
        color: #E5E7EB;
        margin-bottom: 0.8rem;
    }
    .welcome-card ul {
        display: inline-block;
        text-align: left;
        color: #E5E7EB;
        padding-left: 1.5rem;
    }
    .welcome-card li {
        color: #E5E7EB;
        margin-bottom: 0.4rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #374151;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding: 8px 16px;
        color: #E5E7EB;
        margin-right: 2px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6;
        color: white;
    }
    /* Make content use full width */
    .block-container {
        max-width: 95% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    /* Adjust sidebar width */
    [data-testid="stSidebar"] {
        min-width: 250px !important;
        max-width: 300px !important;
    }
    /* Add spacing between elements */
    .stSelectbox, .stMultiSelect, .stSlider {
        margin-bottom: 1rem !important;
    }
    /* Improve spacing in dataframes */
    .dataframe {
        margin-bottom: 1rem !important;
    }
    /* Improve chart spacing */
    .js-plotly-plot {
        margin-bottom: 1rem !important;
    }
    /* Make sidebar scrollable if needed */
    section[data-testid="stSidebar"] {
        overflow-y: auto;
    }
    /* Style for report options */
    .report-option {
        background-color: #374151;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .report-option:hover {
        background-color: #4B5563;
    }
    .report-option h3 {
        color: #60A5FA;
        margin-bottom: 0.5rem;
    }
    .report-option p {
        color: #E5E7EB;
        font-size: 0.9rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
