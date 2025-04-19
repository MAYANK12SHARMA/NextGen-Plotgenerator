import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from assets.css import set_custom_style
from DataAnalysis import DataAnalysis
import tempfile
from sweet import generate_sweetviz_report
import base64
from Plots import initial_state, Get_Plot_Dashboard

initial_state()
# --- Page config and custom CSS ---
st.set_page_config(layout="wide", page_title="Data Analysis Dashboard")
set_custom_style()

# Header with logo
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=200)
with col2:
    st.markdown(
        '<h1 class="main-header" style="font-family: Algerian;font-weight:400;">Data Visualization Studio</h1>',
        unsafe_allow_html=True,
    )

# Additional CSS for cards & headings
st.markdown(
    """
    <style>
    .card {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .heading {
        font-size: 2rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Single horizontal nav menu ---
selected = option_menu(
    menu_title=None,
    options=["DashBoard", "Report Generate", "PlotWizard"],
    icons=["bar-chart", "file-text", "magic"],
    orientation="horizontal",
    default_index=1,  # Default to "Report Generate"
    styles={
        "container": {"padding": "0!important", "background-color": ""},
        "icon": {"color": "#bcc024", "font-size": "20px"},
        "nav-link": {
            "font-size": "18px",
            "font-weight": "600",
            "text-align": "center",
        },
        "nav-link-selected": {"background-color": "#2ecc71", "color": "white"},
    },
)

# If you need a second menu somewhere else, duplicate the above block and add:
#    key="unique_key_here"
# to its arguments to avoid duplicate IDs.

# --- Main content area ---
col2, col3 = st.columns([2, 2])
with col2:
    # Card container start
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a CSV file", type=["csv"], label_visibility="visible"
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

    # Card container end
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<h5></h5>", unsafe_allow_html=True)
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
    else:
        st.info("👈 Please upload a CSV file to see the preview.")


if selected == "PlotWizard" and uploaded_file:
    if uploaded_file:
        DataAnalysis(df)
    else:
        st.warning("Please upload a CSV file to perform data analysis.")

    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "DashBoard" and uploaded_file:   
    Get_Plot_Dashboard(df)
elif selected == "Report Generate" and uploaded_file:
    col1, col2 = st.columns([1, 1])
    with col1:
        report_type = st.selectbox(
            "Select Report Type",
            options=["SweetViz", "Detailed", "Custom"],
            index=0,
            label_visibility="collapsed",
        )
    st.markdown(
        """
        <style>
        /* restyle Streamlit buttons everywhere */
        .stButton > button {
            background-color: #2ecc71 !important;
            color: white !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 5px !important;
            cursor: pointer !important;
        }
        .stButton > button:hover {
            background-color: #27ae60 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Generate Sweetviz Report", key="sweetviz"):
        with st.spinner("Generating beautiful interactive report… This may take a minute."):
            try:
                # 2) Generate
                report_data = generate_sweetviz_report(df)

                # 3) Preview inside expander
                with st.expander("Report Preview (Click to expand)"):
                    st.components.v1.html(
                        report_data["html"],
                        height=1000,
                        scrolling=True,
                        width=1600,
                    )

                # 4) Save to temp file for full‑screen link
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
                    tmp.write(report_data["html"].encode("utf-8"))
                    tmp_path = tmp.name

                # 5) Two columns: Open vs. Download
                colx,col1, colm,col2,coly = st.columns([1, 2, 2,2, 1])

                with col1:
                    st.markdown(
                        f"""
                        <div style="text-align: center;x">
                            <a
                                href="file://{tmp_path}"
                                target="_blank"
                                style="
                                    display: inline-block;
                                    background-color: #2ecc71;
                                    color: white;
                                    padding: 10px 20px;
                                    text-decoration: none;
                                    border-radius: 5px;
                                    font-weight: bold;
                                    font-size: 16px;
                                "
                            >▶️ Open Report Full‑Screen</a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col2:
                    b64 = base64.b64encode(report_data["html"].encode()).decode()
                    ext = "html"
                    filename = "sweetviz_report"
                    st.markdown(
                        f"""
                        <div style="text-align: center;">
                            <a
                                href="data:file/{ext};base64,{b64}" download="{filename}.{ext}"
                                download="sweetviz_report.html"
                                style="
                                    display: inline-block;
                                    background-color: #2ecc71;
                                    color: white;
                                    padding: 10px 20px;
                                    text-decoration: none;
                                    border-radius: 5px;
                                    font-weight: bold;
                                    font-size: 16px;
                                "
                            >⬇️ Download Report</a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                st.error(f"Error generating report: {e}")


