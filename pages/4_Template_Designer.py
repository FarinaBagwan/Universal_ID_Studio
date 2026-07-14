import streamlit as st

from components.template_designer import template_designer


st.set_page_config(
    page_title="Template Designer",
    layout="wide"
)


template_designer()