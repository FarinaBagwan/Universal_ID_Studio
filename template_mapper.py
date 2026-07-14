import streamlit as st
import json
import os
from PIL import Image


# ----------------------------
# Template Mapper
# ----------------------------


def template_mapper():


    st.title("🎨 ID Card Template Designer")


    if "selected_template" not in st.session_state:

        st.warning(
            "Please select template from Template Manager"
        )

        return



    template_path = st.session_state["selected_template"]

    mapping_file = st.session_state["selected_mapping"]



    # -------------------------
    # Load Template Image
    # -------------------------


    if not os.path.exists(template_path):

        st.error(
            "Template image not found"
        )

        return



    image = Image.open(
        template_path
    )


    width,height=image.size


    st.info(
        f"Template Size : {width} x {height}"
    )



    st.image(
        image,
        width=500
    )



    st.divider()



    # -------------------------
    # Add Fields
    # -------------------------


    st.subheader(
        "Add Field Mapping"
    )


    field_name=st.selectbox(

        "Select Field",

        [
            "name",
            "roll",
            "branch",
            "year",
            "photo",
            "qr_code",
            "signature"
        ]

    )



    field_type=st.selectbox(

        "Field Type",

        [
            "text",
            "image"
        ]

    )



    col1,col2=st.columns(2)


    with col1:

        x=st.number_input(
            "X Position",
            min_value=0,
            value=100
        )


        y=st.number_input(
            "Y Position",
            min_value=0,
            value=100
        )


    with col2:


        w=st.number_input(
            "Width",
            min_value=10,
            value=200
        )


        h=st.number_input(
            "Height",
            min_value=10,
            value=50
        )



    font_size=st.slider(

        "Font Size",

        10,
        100,
        30

    )



    # -------------------------
    # Save Mapping
    # -------------------------


    if st.button(
        "💾 Save Field"
    ):



        if os.path.exists(mapping_file):

            with open(mapping_file,"r") as f:

                data=json.load(f)

        else:

            data={

                "template":
                os.path.basename(template_path),

                "fields":{}

            }



        data["fields"][field_name]={

            "type":field_type,

            "x":x,

            "y":y,

            "width":w,

            "height":h,

            "font_size":font_size

        }



        with open(mapping_file,"w") as f:

            json.dump(
                data,
                f,
                indent=4
            )


        st.success(
            "Field saved successfully"
        )



    st.divider()



    # -------------------------
    # Preview Mapping
    # -------------------------


    st.subheader(
        "Current Mapping"
    )


    if os.path.exists(mapping_file):

        with open(mapping_file) as f:

            mapping=json.load(f)


        st.json(mapping)

    else:

        st.info(
            "No mapping created"
        )