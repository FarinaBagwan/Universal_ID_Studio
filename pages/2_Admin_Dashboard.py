import streamlit as st

st.set_page_config(page_title="Dashboard")

if "admin_logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

st.title("🎓 Admin Dashboard")

st.success("Welcome Admin")

st.write("This is your dashboard.")

st.write("Later we will add:")

st.write("✅ Upload Template")
st.write("✅ Template Designer")
st.write("✅ Student Records")
st.write("✅ Generated IDs")
st.write("✅ Settings")