import streamlit as st
from database import get_students

st.set_page_config(page_title="Generate ID", layout="wide")

st.title("🪪 Generate ID Cards")

students = get_students()

if len(students) == 0:

    st.warning("No Student Records Found")

else:

    student_names = []

    for s in students:

        student_names.append(s[1])

    selected = st.selectbox(
        "Select Student",
        student_names
    )

    if st.button("Generate ID"):

        st.success("ID Generation Module")

        st.info(
            "Next we will connect the Template Designer and automatically create printable ID Cards."
        )