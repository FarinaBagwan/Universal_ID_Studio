import streamlit as st
import os
import shutil

from database import (
    save_template,
    get_templates,
    delete_template
)

# -----------------------------
# Folder Settings
# -----------------------------

TEMPLATE_FOLDER = "templates"
MAPPING_FOLDER = "config"

os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
os.makedirs(MAPPING_FOLDER, exist_ok=True)


# -----------------------------
# Template Manager
# -----------------------------

def template_manager():

    st.title("🆔 Template Manager")

    st.write(
        "Upload an ID Card template that will be used to generate student ID cards."
    )

    st.divider()

    # -----------------------------
    # Upload Section
    # -----------------------------

    st.subheader("Upload New Template")

    template_name = st.text_input(
        "Template Name",
        placeholder="Example : Student ID Card"
    )

    uploaded_template = st.file_uploader(
        "Choose Template Image",
        type=["png", "jpg", "jpeg"]
    )

    if st.button("Save Template"):

        if template_name == "":
            st.error("Please enter Template Name.")
            return

        if uploaded_template is None:
            st.error("Please upload a template image.")
            return

        filename = uploaded_template.name

        save_path = os.path.join(
            TEMPLATE_FOLDER,
            filename
        )

        with open(save_path, "wb") as file:

            file.write(uploaded_template.getbuffer())

        mapping_file = os.path.join(
            MAPPING_FOLDER,
            filename.split(".")[0] + ".json"
        )

        save_template(
            template_name,
            save_path,
            mapping_file
        )

        st.success("Template Saved Successfully.")

        st.rerun()

    st.divider()

    st.subheader("Available Templates")
    # -----------------------------
# Show Saved Templates
# -----------------------------

    templates = get_templates()

    if len(templates) == 0:

        st.info("No templates uploaded yet.")

    else:

        for template in templates:

            template_id = template[0]
            template_name = template[1]
            template_image = template[2]
            mapping_file = template[3]

            st.container(border=True)

            col1, col2 = st.columns([1,2])

            with col1:

                if os.path.exists(template_image):

                    st.image(
                        template_image,
                        width=220
                    )

                else:

                    st.warning("Template image not found.")

            with col2:

                st.write("### " + template_name)

                st.write("Image Path")

                st.code(template_image)

                st.write("Mapping File")

                st.code(mapping_file)

                c1, c2, c3 = st.columns(3)

                with c1:

                    if st.button(
                        "🎨 Designer",
                        key="designer_"+str(template_id)
                    ):

                        st.session_state["selected_template"] = template_image
                        st.session_state["selected_mapping"] = mapping_file

                        st.switch_page(
                            "pages/4_Template_Designer.py"
                        )

                with c2:

                    if st.button(
                        "⭐ Set Active",
                        key="active_"+str(template_id)
                    ):

                        st.success(
                            "Template selected successfully."
                        )

                with c3:

                    if st.button(
                        "🗑 Delete",
                        key="delete_"+str(template_id)
                    ):

                        delete_template(template_id)

                        if os.path.exists(template_image):

                            os.remove(template_image)

                        st.success("Template deleted.")

                        st.rerun()

    # -----------------------------
    # Show Saved Templates
    # -----------------------------

    