import streamlit as st
from database import create_database

create_database()

st.set_page_config(
    page_title="Universal ID Studio",
    page_icon="🪪",
    layout="wide"
)

st.title("🪪 Universal ID Studio")

st.success("Database Connected Successfully")