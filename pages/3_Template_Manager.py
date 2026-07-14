import streamlit as st
import os

from database import (
    save_template,
    get_templates,
    delete_template
)

st.set_page_config(
    page_title="Template Manager",
    layout="wide"
)


TEMPLATE_FOLDER = "templates"
MAPPING_FOLDER = "config"

os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
os.makedirs(MAPPING_FOLDER, exist_ok=True)


st.title("🖼️ Template Manager")


st.subheader("Upload New Template")


template_name = st.text_input("Template Name")


uploaded_file = st.file_uploader(
    "Choose Template Image",
    type=["png", "jpg", "jpeg"]
)


if st.button("Save Template"):

    if uploaded_file is None:
        st.error("Please upload template.")

    elif template_name == "":
        st.error("Please enter template name.")

    else:

        filename = uploaded_file.name

        save_path = os.path.join(
            TEMPLATE_FOLDER,
            filename
        )


        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())


        mapping_file = os.path.join(
            MAPPING_FOLDER,
            filename.split(".")[0] + ".json"
        )


        save_template(
            template_name,
            save_path,
            mapping_file
        )


        st.success("Template Saved Successfully")

        st.rerun()



st.divider()


st.subheader("Available Templates")


templates = get_templates()


if len(templates) == 0:

    st.info("No Template Uploaded")


else:

    cols = st.columns(3)


    for index,temp in enumerate(templates):

        template_id = temp[0]
        name = temp[1]
        image = temp[2]


        with cols[index % 3]:

            if os.path.exists(image):

                st.image(
                    image,
                    use_column_width=True
                )


                st.write(
                    "Template:",
                    name
                )


            # Designer Button

            if st.button(
                "🎨 Designer",
                key=f"designer_{template_id}"
            ):

                st.session_state["selected_template"] = image
                st.session_state["selected_mapping"] = temp[3]

                st.switch_page(
                    "pages/4_Template_Designer.py"
                )



            # Delete Button

            if st.button(
                "🗑 Delete",
                key=f"delete_{template_id}"
            ):

                delete_template(template_id)

                if os.path.exists(image):
                    os.remove(image)

                st.rerun()

                delete_template(template_id)

                if os.path.exists(image):
                    os.remove(image)

                st.rerun()