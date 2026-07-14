import streamlit as st

st.set_page_config(
    page_title="Universal ID Studio - Admin",
    layout="wide"
)

st.title("🪪 Universal ID Studio")

menu = st.sidebar.selectbox(
    "Admin Menu",
    [
        "Dashboard",
        "Templates",
        "Template Designer",
        "Students",
        "Generated IDs",
        "Settings"
    ]
)

if menu == "Dashboard":
    st.header("Dashboard")

elif menu == "Templates":
    st.header("Upload Template")

elif menu == "Template Designer":
    st.header("Template Designer")

elif menu == "Students":
    st.header("Students")

elif menu == "Generated IDs":
    st.header("Generated IDs")

elif menu == "Settings":
    st.header("Settings")