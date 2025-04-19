import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
import datetime
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from sklearn.preprocessing import LabelEncoder
import base64
from ydata_profiling import ProfileReport
import tempfile
import numpy as np
from Stylish_plots import Scatter_3d_Plots,Line_3d_Plots,Surface_3d_Plots,Mesh_3d_Plots


def initial_state():
    if "df" not in st.session_state:
        st.session_state["df"] = None

    if "X_train" not in st.session_state:
        st.session_state["X_train"] = None

    if "X_test" not in st.session_state:
        st.session_state["X_test"] = None

    if "y_train" not in st.session_state:
        st.session_state["y_train"] = None

    if "y_test" not in st.session_state:
        st.session_state["y_test"] = None

    if "X_val" not in st.session_state:
        st.session_state["X_val"] = None

    if "y_val" not in st.session_state:
        st.session_state["y_val"] = None

    if "model" not in st.session_state:
        st.session_state["model"] = None

    if "trained_model" not in st.session_state:
        st.session_state["trained_model"] = False

    if "trained_model_bool" not in st.session_state:
        st.session_state["trained_model_bool"] = False

    if "problem_type" not in st.session_state:
        st.session_state["problem_type"] = None

    if "metrics_df" not in st.session_state:
        st.session_state["metrics_df"] = pd.DataFrame()

    if "is_train" not in st.session_state:
        st.session_state["is_train"] = False

    if "is_test" not in st.session_state:
        st.session_state["is_test"] = False

    if "is_val" not in st.session_state:
        st.session_state["is_val"] = False

    if "show_eval" not in st.session_state:
        st.session_state["show_eval"] = False

    if "all_the_process" not in st.session_state:
        st.session_state["all_the_process"] = """"""

    if "all_the_process_predictions" not in st.session_state:
        st.session_state["all_the_process_predictions"] = False

    if "y_pred_train" not in st.session_state:
        st.session_state["y_pred_train"] = None

    if "y_pred_test" not in st.session_state:
        st.session_state["y_pred_test"] = None

    if "y_pred_val" not in st.session_state:
        st.session_state["y_pred_val"] = None

    if "uploading_way" not in st.session_state:
        st.session_state["uploading_way"] = None

    if "lst_models" not in st.session_state:
        st.session_state["lst_models"] = []

    if "lst_models_predctions" not in st.session_state:
        st.session_state["lst_models_predctions"] = []

    if "models_with_eval" not in st.session_state:
        st.session_state["models_with_eval"] = dict()

    if "reset_1" not in st.session_state:
        st.session_state["reset_1"] = False

if not hasattr(np, "VisibleDeprecationWarning"):
    np.VisibleDeprecationWarning = DeprecationWarning


warnings.filterwarnings("ignore")






def area_chart(df, selected_column, col2):
    fig = px.area(
        df,
        x=col2,
        y=selected_column,
        title=f"{selected_column}",
        labels={col2: col2, selected_column: selected_column},
        template="plotly_white",
    )
    return fig


# Function to create a beautiful heatmap for the dashboard
# def create_heatmap(df):
#     df_encoded = df.copy()
#     label_encoder = LabelEncoder()

#     # Encode categorical features
#     for column in df_encoded.columns:
#         df_encoded[column] = label_encoder.fit_transform(df_encoded[column])

#     # Calculate the correlation matrix
#     corr_matrix = df_encoded.corr()

#     # Create an annotated heatmap
#     heatmap = ff.create_annotated_heatmap(
#         z=corr_matrix.values,
#         x=list(corr_matrix.columns),
#         y=list(corr_matrix.index),
#         annotation_text=corr_matrix.round(2).values,
#         colorscale="Rainbow",
#         showscale=True,
#         colorbar=dict(
#             title="Correlation",
#             thickness=20,
#             len=0.75,
#             tickmode="array",
#         ),
#     )

#         # Update layout for better UI/UX
#     heatmap.update_layout(
#         title=dict(
#             text="🔍 Feature Correlation Heatmap",
#             font=dict(size=20, color="#ffffff"),
#             x=0.5,
#             xanchor="center"
#         ),
#         xaxis=dict(
#             title=dict(
#                 text="🔻 Features",
#                 font=dict(size=14, color="#ffffff", family="Arial")
#             ),
#             tickangle=45,
#             tickfont=dict(size=12, color="#ffffff"),
#             showgrid=False,
#             zeroline=False
#         ),
#         yaxis=dict(
#             title=dict(
#                 text="🔺 Features",
#                 font=dict(size=14, color="#ffffff", family="Arial")
#             ),
#             tickfont=dict(size=12, color="#ffffff"),
#             showgrid=False,
#             zeroline=False
#         ),
#         template="plotly_dark",
#         height=650,
#         margin=dict(l=70, r=70, t=80, b=80),
#         paper_bgcolor="rgba(10,10,10,0.95)",
#         plot_bgcolor="rgba(20,20,20,0.9)",
#         coloraxis_colorbar=dict(
#             title=dict(text="Correlation", font=dict(color='white')),
#             tickfont=dict(color='white'),
#             thickness=15,
#             len=0.75,
#             outlinewidth=1,
#             outlinecolor="gray"
#         )
#     )

    # return heatmap


def create_heatmap(df: pd.DataFrame):
    """
    Display an annotated correlation heatmap whose colorscale
    can be chosen from presets or built dynamically via color pickers.
    """

    # 1) Let user pick a preset or custom
    presets = [
        "Rainbow", "Viridis", "Cividis", "Plasma", "Inferno",
        "Magma", "Turbo", "Jet", "Hot", "YlGnBu",
        "YlOrRd", "RdBu", "RdYlGn", "Spectral", "Picnic",
        "Portland", "Electric", "Earth", "Custom"
    ]
    choice = st.selectbox("🎨 Pick a colorscale", presets, index=0)

    if choice == "Custom":
        st.markdown("Define your own gradient:")
        low  = st.color_picker("⬛ Low color",  "#440154")
        mid  = st.color_picker("◼️ Mid color",  "#21908d")
        high = st.color_picker("⬜ High color", "#fde725")
        colorscale = [
            [0.0, low],
            [0.5, mid],
            [1.0, high]
        ]
    else:
        # plotly knows these names (lowercase)
        colorscale = choice.lower()

    # 2) Encode any categoricals so we can corr() everything
    df_encoded = df.copy()
    encoder = LabelEncoder()
    for col in df_encoded.columns:
        if df_encoded[col].dtype == "object":
            df_encoded[col] = encoder.fit_transform(df_encoded[col])

    corr = df_encoded.corr()

    # 3) Build the annotated heatmap
    heatmap = ff.create_annotated_heatmap(
        z=corr.values,
        x=list(corr.columns),
        y=list(corr.index),
        annotation_text=corr.round(2).values,
        colorscale=colorscale,
        showscale=True,
        colorbar=dict(
            title="Correlation",
            thickness=20,
            len=0.75,
            tickmode="array"
        )
    )

    # 4) Apply the refined layout
    heatmap.update_layout(
        
        xaxis=dict(
            title=dict(text="🔻 Features", font=dict(size=14, color="#ffffff")),
            tickangle=45,
            tickfont=dict(size=12, color="#ffffff"),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="🔺 Features", font=dict(size=14, color="#ffffff")),
            tickfont=dict(size=12, color="#ffffff"),
            showgrid=False,
            zeroline=False
        ),
        template="plotly_dark",
        height=650,
        margin=dict(l=70, r=70, t=80, b=80),
        paper_bgcolor="rgba(10,10,10,0.95)",
        plot_bgcolor="rgba(20,20,20,0.9)",
        coloraxis_colorbar=dict(
            title=dict(text="Correlation", font=dict(color='white')),
            tickfont=dict(color='white'),
            thickness=15,
            len=0.75,
            outlinewidth=1,
            outlinecolor="gray"
        )
    )
    
    st.plotly_chart(heatmap, use_container_width=True)


    
def create_boxplot(df, boxcolumns):
    fig = make_subplots(
        rows=len(boxcolumns),
        cols=1,
        subplot_titles=[f"Boxplot of {col}" for col in boxcolumns],
        vertical_spacing=0.1,
    )

    for i, boxcolumn in enumerate(boxcolumns):
        fig.add_trace(
            go.Box(
                x=df[boxcolumn],
                name=boxcolumn,
                boxpoints="outliers",
                marker=dict(color="#FF5733"),
            ),
            row=i + 1,
            col=1,
        )

    fig.update_layout(
        template="plotly_dark",
        hovermode="y",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
    )

    return fig


def create_scatter(df, xaxis, yaxis):
    fig = px.scatter(
        df,
        x=xaxis,
        y=yaxis,
        color=xaxis,
        color_continuous_scale="Viridis",
        title=f"{xaxis} by {yaxis}",
        labels={xaxis: xaxis, yaxis: yaxis},
        hover_data={xaxis: True, yaxis: True},
    )
    fig.update_layout(
        xaxis_title=xaxis,
        yaxis_title=yaxis,
        template="plotly_dark",
        hovermode="closest",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_histogram(df, column):
    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=f"Distribution of {column}",
        histnorm="density",
        opacity=0.7,
        color_discrete_sequence=["#60A5FA"],
        hover_data={column: True},
    )
    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Density",
        hovermode="x",
        bargap=0.05,
        height=400,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_pie_plot(df, column_to_plot):
    value_counts = df[column_to_plot].value_counts()
    fig = px.pie(
        values=value_counts.values,
        names=value_counts.index,
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(
        legend_title=column_to_plot,
        template="plotly_dark",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_bar_chart(df, xaxis, yaxis):
    fig = px.bar(
        df,
        x=xaxis,
        y=yaxis,
        color=xaxis,
        title=f"{xaxis} by {yaxis}",
        hover_data=[yaxis],
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_layout(
        xaxis_title=xaxis,
        yaxis_title=yaxis,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_treemap(df, path_columns, values_column):
    fig = px.treemap(
        df,
        path=path_columns,
        values=values_column,
        title=f"Treemap of {' > '.join(path_columns)} by {values_column}",
        color=values_column,
        color_continuous_scale="Viridis",
        hover_data=[values_column],
    )
    fig.update_layout(
        template="plotly_dark",
        margin=dict(t=50, l=25, r=25, b=25),
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_bubble_chart(df, x_col, y_col, size_col, color_col=None):
    if color_col is None:
        color_col = size_col

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        title=f"Bubble Chart of {x_col} vs {y_col} (Size: {size_col})",
        hover_name=df.index,
        size_max=50,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        template="plotly_dark",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_line_chart(df, x_col, y_col, group_col=None):
    if group_col:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=group_col,
            title=f"Trend of {y_col} Over {x_col} Grouped by {group_col}",
            markers=True,
        )
    else:
        fig = px.line(
            df, x=x_col, y=y_col, title=f"Trend of {y_col} Over {x_col}", markers=True
        )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        template="plotly_dark",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_sunburst(df, path_columns, values_column):
    fig = px.sunburst(
        df,
        path=path_columns,
        values=values_column,
        title=f"Sunburst of {' > '.join(path_columns)} by {values_column}",
        color=values_column,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        template="plotly_dark",
        margin=dict(t=50, l=25, r=25, b=25),
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def create_violin_plot(df, x_col, y_col):
    fig = px.violin(
        df,
        x=x_col,
        y=y_col,
        box=True,
        points="all",
        title=f"Distribution of {y_col} by {x_col}",
        color=x_col,
    )
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        template="plotly_dark",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def get_data_summary(df):
    numeric_df = df.select_dtypes(include=["number"])
    summary = pd.DataFrame(
        {
            "Mean": numeric_df.mean(),
            "Median": numeric_df.median(),
            "Std Dev": numeric_df.std(),
            "Min": numeric_df.min(),
            "Max": numeric_df.max(),
            "Missing": df.isnull().sum(),
        }
    )
    return summary


# Report Generation Functions
def generate_autoeda_report(df, filename="autoeda_report"):
    """Generate a report using pandas-profiling (ydata-profiling)"""
    # Create Profile Report
    profile = ProfileReport(
        df, title="Data Analysis Report", explorative=True, dark_mode=True
    )

    # Save report in various formats
    report_html = profile.to_html()

    # Return the HTML report and other formats
    return {"html": report_html, "title": "AutoEDA Data Analysis Report"}












def Get_Plot_Dashboard(df):
    numerical_cols = df.columns.to_list()
    hist_c = df.select_dtypes(include=["int", "float"]).columns.tolist()

    col3, col4, col5 = st.columns([2, 2, 2])

    # Scatter Plot Section
    with col3:
        st.markdown(
            "<div style='text-align: center; font-size: 18px; font-family: \"Times New Roman\";'>Scatter Plot</div>",
            unsafe_allow_html=True,
        )
        try:
            xaxis, yaxis = st.multiselect(
                "Select X and Y axes for Scatter Plot",
                numerical_cols,
                key="scatter_axes",
                default=numerical_cols[:2],
                label_visibility="collapsed",
            )

            fig = create_scatter(df, xaxis, yaxis)
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error creating scatter plot: {e}")

    # Bar Plot Section
    with col4:
        st.markdown(
            "<div style='text-align: center; font-size: 18px; font-family: \"Times New Roman\";'>Bar Plot</div>",
            unsafe_allow_html=True,
        )
        try:
            xaxis, yaxis = st.multiselect(
                "Select X and Y axes for Bar Plot",
                numerical_cols,
                key="bar_axes",
                default=numerical_cols[:2],
                label_visibility="collapsed",
            )

            fig = create_bar_chart(df, xaxis, yaxis)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error creating bar plot: {e}")

    # Histogram Section
    with col5:
        st.markdown(
            "<div style='text-align: center; font-size: 18px; font-family: \"Times New Roman\";'>Histogram</div>",
            unsafe_allow_html=True,
        )
        try:
            selected_column = st.selectbox(
                "Select a column for Histogram",
                hist_c,
                label_visibility="collapsed",
            )
            if selected_column:
                hist_fig = create_histogram(df, selected_column)
                st.plotly_chart(hist_fig)
            else:
                st.warning(
                    "Please select a numerical column to create a histogram."
                )
        except Exception as e:
            st.error(f"Error creating histogram: {e}")

    col6, col7 = st.columns([2, 4])

    # Pie Chart Section
    with col6:
        st.markdown(
            "<div style='text-align: center; font-size: 18px; font-family: \"Times New Roman\";'>Pie Chart</div>",
            unsafe_allow_html=True,
        )
        try:
            unique_value_counts = df.nunique()
            filtered_columns = unique_value_counts[
                unique_value_counts < 12
            ].index.tolist()

            column_to_plot = st.selectbox(
                "Select a column for Pie Chart",
                filtered_columns,
                label_visibility="collapsed",
            )

            if column_to_plot:
                pie_fig = create_pie_plot(df, column_to_plot)
                pie_fig.update_layout(height=500, width=500)
                st.plotly_chart(pie_fig)
            else:
                st.warning("Please select a categorical column to create a pie chart.")
        except Exception as e:
            st.error(f"Error creating pie chart: {e}")

    # Box Plot Section
    with col7:
        st.markdown(
            "<div style='text-align: center; font-size: 18px; font-family: \"Times New Roman\";'>Box Plot</div>",
            unsafe_allow_html=True,
        )
        try:
            boxcolumns = st.multiselect(
                "Select numerical columns for Box Plot",
                numerical_cols,
                label_visibility="collapsed",
            )

            if boxcolumns:
                fig = create_boxplot(df, boxcolumns)
                st.plotly_chart(fig)
            else:
                st.warning("Please select at least one numerical column to create box plots.")
        except Exception as e:
            st.error(f"Error creating box plot: {e}")

    # Area Chart Section
    # with col8:
    #     st.markdown(
    #         "<div style='text-align: center; font-size: 18px; font-family: \"Times New Roman\";'>Area Chart</div>",
    #         unsafe_allow_html=True,
    #     )
    #     try:
    #         col2, ara_col = st.multiselect(
    #             "Select a category and numerical value for Area Chart",
    #             numerical_cols,
    #             default=numerical_cols[:2],
    #             label_visibility="collapsed",
    #         )

    #         if col2 and ara_col:
    #             fig = area_chart(df, ara_col, col2)
    #             st.plotly_chart(fig)
    #         else:
    #             st.warning("Please select both a category and a numerical value to create an area chart.")
    #     except Exception as e:
    #         st.error(f"Error creating area chart: {e}")

    st.markdown(
        """
        <div style="
            text-align: center; 
            font-size: 26px; 
            font-family: Arial, sans-serif; 
            color: #ffffff; 
            margin-bottom: 20px;
        ">
            🔍 Correlation Heatmap
        </div>
        """,
        unsafe_allow_html=True,
    )
    colm, coln = st.columns([2, 2])
    with colm:
        Scatter_3d_Plots(df)
    with coln:
        Line_3d_Plots(df)
    
    create_heatmap(df)

    
