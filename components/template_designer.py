import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import json
import os


LAYOUT_FILE = "config/mapper.json"


# -----------------------------
# Save Layout
# -----------------------------
def save_layout(data):
    os.makedirs("config", exist_ok=True)

    with open(LAYOUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Load Layout
# -----------------------------
def load_layout():

    if os.path.exists(LAYOUT_FILE):

        with open(LAYOUT_FILE, "r") as f:
            return json.load(f)

    return {}
    # -----------------------------
# Convert mapper.json to Canvas Objects
# -----------------------------
def mapper_to_objects(mapper):

    objects = []

    for key, value in mapper.items():

        if value["type"] == "text":

            objects.append({
                "type": "textbox",
                "text": key,
                "left": int(value["x"]),
                "top": int(value["y"]),
                "width": int(value["width"]),
                "height": int(value["height"]),
                "fontSize": int(value.get("font_size", 24)),
                "fill": "black"
            })

        elif value["type"] == "image":

            objects.append({
                "type": "rect",
                "left": int(value["x"]),
                "top": int(value["y"]),
                "width": int(value["width"]),
                "height": int(value["height"]),
                "fill": "rgba(255,255,255,0)",
                "stroke": "black",
                "strokeWidth": 2
            })

    return objects

    # -----------------------------
# Create Default Canvas Objects
# -----------------------------
def create_objects(fields):

    objects = []

    for field in fields:

        if field == "Photo":

            objects.append({
                "type": "rect",
                "left": 50,
                "top": 70,
                "width": 150,
                "height": 180,
                "fill": "rgba(255,255,255,0)",
                "stroke": "black",
                "strokeWidth": 2
            })

        else:

            objects.append({
                "type": "textbox",
                "text": field,
                "left": 250,
                "top": 100,
                "width": 250,
                "height": 40,
                "fontSize": 24,
                "fill": "black"
            })

    return objects

    # -----------------------------
# Template Designer
# -----------------------------
def template_designer():

    st.title("🎨 ID Card Template Designer")

    # Check whether a template is selected
    if "selected_template" not in st.session_state:

        st.error("No template selected.")
        st.info("Please open Template Manager and select a template.")
        return

    template_path = st.session_state["selected_template"]

    # Check template exists
    if not os.path.exists(template_path):

        st.error("Template image not found.")
        return

    # Open template image
    

    image = Image.open(template_path)

    MAX_WIDTH = 900

    if image.width > MAX_WIDTH:
        ratio = MAX_WIDTH / image.width
        new_height = int(image.height * ratio)
        image = image.resize((MAX_WIDTH, new_height), Image.LANCZOS)

    # -----------------------------
    # Sidebar
    # -----------------------------
    st.image(image, use_container_width=True)
    st.sidebar.header("Dynamic Fields")

    fields = [
        "Name",
        "Roll_No",
        "Branch",
        "Year",
        "Blood_Group",
        "Mobile",
        "Address",
        "Photo"
    ]

    selected = []

    for field in fields:

        if st.sidebar.checkbox(field):
            selected.append(field)

    # -----------------------------
    # Load Previous Design
    # -----------------------------
    if "canvas_objects" not in st.session_state:

        mapper = load_layout()

        if mapper:
            st.session_state.canvas_objects = mapper_to_objects(mapper)
        else:
            st.session_state.canvas_objects = []

            # -----------------------------
    # Add Selected Fields
    # -----------------------------
    if st.sidebar.button("➕ Add Selected Fields"):

        existing_fields = set()

        # Find existing fields
        for obj in st.session_state.canvas_objects:

            if obj["type"] == "textbox":
                existing_fields.add(obj["text"])

            elif obj["type"] == "rect":
                existing_fields.add("Photo")

        # Add only new fields
        for obj in create_objects(selected):

            if obj["type"] == "textbox":

                if obj["text"] not in existing_fields:
                    st.session_state.canvas_objects.append(obj)

            elif obj["type"] == "rect":

                if "Photo" not in existing_fields:
                    st.session_state.canvas_objects.append(obj)

        st.rerun()

    # -----------------------------
    # Clear Canvas
    # -----------------------------
    if st.sidebar.button("🗑 Clear Canvas"):

        st.session_state.canvas_objects = []

        save_layout({})

        st.rerun()

        # -----------------------------
    # Canvas
    # -----------------------------
    st.subheader("🪪 Design Your ID Card")

    canvas = st_canvas(
        fill_color="rgba(255,255,255,0)",
        stroke_width=2,
        background_image=image,
        initial_drawing={
            "objects": st.session_state.canvas_objects
        },
        drawing_mode="transform",
        update_streamlit=True,
        width=image.width,
        height=image.height,
        key="designer_canvas"
    )

        # -----------------------------
    # Save Design
    # -----------------------------
    if st.button("💾 Save Design"):

        if canvas.json_data is None:
            st.warning("Nothing to save.")
            return

        mapper = {}

        count = 1

        for obj in canvas.json_data["objects"]:

            scale_x = obj.get("scaleX", 1)
            scale_y = obj.get("scaleY", 1)

            width = int(round(obj["width"] * scale_x))
            height = int(round(obj["height"] * scale_y))

            x = int(round(obj["left"]))
            y = int(round(obj["top"]))

            if obj["type"] == "textbox":

                field_name = obj.get("text", f"text_{count}")

                mapper[field_name] = {
                    "type": "text",
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "font_size": int(obj.get("fontSize", 24))
                }

            elif obj["type"] == "rect":

                mapper["Photo"] = {
                    "type": "image",
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                }

            count += 1

        save_layout(mapper)

        # Keep the latest objects in the session
        st.session_state.canvas_objects = canvas.json_data["objects"]

        st.success("✅ Template saved successfully.")

        with st.expander("View mapper.json"):
            st.json(mapper)
        
        