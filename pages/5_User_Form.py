import streamlit as st
import os
from database import add_student
from id_generator import generate_id

st.set_page_config(
    page_title="Student Registration",
    layout="centered"
)

st.title("🎓 Student Registration")

st.write("Fill your details to generate your ID Card")

# -------------------------
# Student Details
# -------------------------

name = st.text_input("Full Name")

roll = st.text_input("Roll Number")

branch = st.text_input("Branch")

year = st.selectbox(
    "Year",
    [
        "First Year",
        "Second Year",
        "Third Year"
    ]
)

photo = st.file_uploader(
    "Upload Passport Size Photo",
    type=["jpg", "jpeg", "png"]
)

# -------------------------
# Submit Button
# -------------------------

if st.button("Submit"):

    # Validation

    if name.strip() == "":
        st.error("Please enter Name.")
        st.stop()

    if roll.strip() == "":
        st.error("Please enter Roll Number.")
        st.stop()

    if branch.strip() == "":
        st.error("Please enter Branch.")
        st.stop()

    if photo is None:
        st.error("Please upload Photo.")
        st.stop()

    # Create folders

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("generated_cards", exist_ok=True)

    # Save Photo

    photo_path = os.path.join(
        "uploads",
        photo.name
    )

    with open(photo_path, "wb") as f:
        f.write(photo.getbuffer())

    # Find Template

    templates = [
        file
        for file in os.listdir("templates")
        if file.lower().endswith(
            (
                ".png",
                ".jpg",
                ".jpeg"
            )
        )
    ]

    if len(templates) == 0:

        st.error("No Template Found.\nPlease upload template first.")

        st.stop()

    template_path = os.path.join(
        "templates",
        templates[0]
    )

    # Output File

    output_path = os.path.join(
        "generated_cards",
        roll + ".png"
    )

    # Generate ID

    generate_id(
        template_path,
        output_path,
        photo_path,
        name,
        roll,
        branch,
        year
    )

    # Save Record

    add_student(
        name,
        roll,
        branch,
        year,
        photo_path,
        output_path
    )

    # Success

    st.success("✅ ID Card Generated Successfully")

    st.image(
        output_path,
        caption="Generated ID Card",
        width=350
    )

    with open(output_path, "rb") as file:

        st.download_button(
            label="📥 Download ID Card",
            data=file,
            file_name=roll + ".png",
            mime="image/png"
        )