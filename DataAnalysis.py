import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer


def DataAnalysis(df):
    @st.cache_resource
    def get_pyg_renderer() -> StreamlitRenderer:
        return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")
    
    renderer = get_pyg_renderer()
    renderer.explorer()