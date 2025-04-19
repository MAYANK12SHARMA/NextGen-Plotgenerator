import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def Scatter_3d_Plots(data: pd.DataFrame):
    """
    A stylish Streamlit 3D scatter plot visualization with interactive column selection.
    """

    st.markdown("## ✨ 3D Scatter Plot Visualization")
    st.markdown("Customize the axes and color below:")

    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    all_cols = data.columns.tolist()

    # Layout: 3 columns for axis selections
    col1, col2, col3 = st.columns(3)
    with col1:
        x_col = st.selectbox("🟥 X Axis", numeric_cols, index=0)
    with col2:
        y_col = st.selectbox("🟩 Y Axis", numeric_cols, index=1)
    with col3:
        z_col = st.selectbox("🟦 Z Axis", numeric_cols, index=2)
    col4,col5 = st.columns(2)
    with col4:
        template = st.selectbox("Select Template", ["plotly_dark", "plotly_white", "ggplot2", "seaborn", "simple_white", "presentation", "xgridoff", "ygridoff", "gridon", "none"],key='scatter_template')
        
    with col5:
        color_col = st.selectbox("🎨 Color By (optional)", all_cols, index=len(all_cols)-1)

    fig = px.scatter_3d(
        data,
        x=x_col,
        y=y_col,
        z=z_col,
        color=color_col,
        opacity=0.8,
        size_max=8,
        height=500,
        template=template  # You can change to "plotly_white" if preferred
    )

    fig.update_traces(marker=dict(size=6, line=dict(width=0.5, color='DarkSlateGrey')))
    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=40),
        scene=dict(
            xaxis_title=f"<b>{x_col}</b>",
            yaxis_title=f"<b>{y_col}</b>",
            zaxis_title=f"<b>{z_col}</b>"
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# -------------------------------------- #
# 📈 2. 3D LINE PLOT FUNCTION            #
# -------------------------------------- #
def Line_3d_Plots(data: pd.DataFrame):
    """
    A stylish Streamlit 3D line plot visualization with interactive column selection.
    """

    st.markdown("## 📈 3D Line Plot Visualization")
    st.markdown("Select the columns to define the 3D line path:")

    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()

    col1, col2, col3 = st.columns(3)
    with col1:
        x_col = st.selectbox("🟥 X Axis", numeric_cols, index=0, key='line_x')
    with col2:
        y_col = st.selectbox("🟩 Y Axis", numeric_cols, index=1, key='line_y')
    with col3:
        z_col = st.selectbox("🟦 Z Axis", numeric_cols, index=2, key='line_z')

    col4,col5 = st.columns(2)
    with col5:
        line_color = st.color_picker("Line Color", "#00FF00")
    with col4:
        template = st.selectbox("Select Template", ["plotly_dark", "plotly_white", "ggplot2", "seaborn", "simple_white", "presentation", "xgridoff", "ygridoff", "gridon", "none"])
    fig = px.line_3d(
        data,
        x=x_col,
        y=y_col,
        z=z_col,
        template=template
    )

    fig.update_traces(line=dict(width=4, color=line_color))  # Added color=line_color
    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=40),
        scene=dict(
            xaxis_title=f"<b>{x_col}</b>",
            yaxis_title=f"<b>{y_col}</b>",
            zaxis_title=f"<b>{z_col}</b>"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------- #
# 🌄 3. 3D SURFACE PLOT FUNCTION         #
# -------------------------------------- #
def Mesh_3d_Plots(data: pd.DataFrame):
    """
    Interactive Streamlit 3D mesh plot where users pick X, Y, Z columns.
    """
    st.markdown("## 🧊 3D Mesh Plot")
    st.markdown("Select numeric columns to define your 3D mesh:")

    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 3:
        st.warning("You need at least 3 numeric columns to create a mesh.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        x_col = st.selectbox("🟥 X Axis", numeric_cols, index=0, key='mesh_x')
    with col2:
        y_col = st.selectbox("🟩 Y Axis", numeric_cols, index=1, key='mesh_y')
    with col3:
        z_col = st.selectbox("🟦 Z Axis", numeric_cols, index=2, key='mesh_z')

    try:
        fig = go.Figure(data=[go.Mesh3d(
            x=data[x_col],
            y=data[y_col],
            z=data[z_col],
            opacity=0.5,
            color='deepskyblue'
        )])

        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=10, r=10, b=10, t=40),
            scene=dict(
                xaxis_title=f"<b>{x_col}</b>",
                yaxis_title=f"<b>{y_col}</b>",
                zaxis_title=f"<b>{z_col}</b>"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Could not generate mesh plot: {e}")

# -------------------------------------- #
# 🧊 4. 3D MESH PLOT FUNCTION            #
# -------------------------------------- #
import plotly.graph_objects as go

def Surface_3d_Plots(data: pd.DataFrame):
    """
    Interactive Streamlit 3D surface plot where users pick X, Y, Z columns.
    Data must form a grid for the surface to display correctly.
    """
    st.markdown("## 🌄 3D Surface Plot")
    st.markdown("Select numeric columns to shape your 3D surface:")

    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 3:
        st.warning("You need at least 3 numeric columns to build a surface plot.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        x_col = st.selectbox("🟥 X Axis", numeric_cols, index=0, key='surf_x')
    with col2:
        y_col = st.selectbox("🟩 Y Axis", numeric_cols, index=1, key='surf_y')
    with col3:
        z_col = st.selectbox("🟦 Z Axis", numeric_cols, index=2, key='surf_z')

    # Create a pivot table to form grid
    try:
        grid_data = data[[x_col, y_col, z_col]]
        pivot = grid_data.pivot_table(index=y_col, columns=x_col, values=z_col)

        fig = px.surface(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            template="plotly_dark",
            height=700
        )

        fig.update_layout(
            margin=dict(l=10, r=10, b=10, t=40),
            scene=dict(
                xaxis_title=f"<b>{x_col}</b>",
                yaxis_title=f"<b>{y_col}</b>",
                zaxis_title=f"<b>{z_col}</b>"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Could not generate surface plot: {e}")


# -------------------------------------- #
# 🧠 RENDER BASED ON PLOT TYPE          #
# -------------------------------------- #

def Heatmap_2D_Plot(data: pd.DataFrame):
    """
    A stylish Streamlit 2D heatmap with dynamic column selection and pivoting.
    """
    st.markdown("## 🔥 2D Heatmap Visualization")
    st.markdown("Pick two axis dimensions and one value to visualize intensity:")

    numeric_cols = data.select_dtypes(include='number').columns.tolist()
    all_cols = data.columns.tolist()

    if len(numeric_cols) < 1 or len(all_cols) < 3:
        st.warning("Need at least 1 numeric and 2 other columns to create a heatmap.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        x_col = st.selectbox("🟥 X Axis", all_cols, index=0, key='heat_x')
    with col2:
        y_col = st.selectbox("🟩 Y Axis", all_cols, index=1, key='heat_y')
    with col3:
        z_col = st.selectbox("🟨 Value (Color Intensity)", numeric_cols, index=0, key='heat_z')

    try:
        pivot_df = data.pivot_table(index=y_col, columns=x_col, values=z_col, aggfunc='mean')

        fig = px.imshow(
            pivot_df,
            color_continuous_scale='Viridis',
            labels=dict(color=z_col),
            aspect='auto',
            height=700
        )

        fig.update_layout(
            template='plotly_dark',
            margin=dict(l=10, r=10, b=10, t=40),
            xaxis_title=f"<b>{x_col}</b>",
            yaxis_title=f"<b>{y_col}</b>",
            coloraxis_colorbar=dict(
                title=f"<b>{z_col}</b>",
                tickfont=dict(color='white'),
                titlefont=dict(color='white')
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Could not generate heatmap: {e}")


