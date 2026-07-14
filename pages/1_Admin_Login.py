import streamlit as st

st.set_page_config(page_title="Admin Login", layout="centered")

st.title("🔐 Admin Login")

# Default Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state["admin_logged_in"] = True
        st.success("Login Successful")
    else:
        st.error("Invalid Username or Password")