from PIL import Image, ImageDraw, ImageFont
import os
import json

FONT_PATH = "fonts/arial.ttf"


def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()


def generate_id(
    template_path,
    output_path,
    photo_path,
    name,
    roll,
    branch,
    year
):

    # Open Template
    template = Image.open(template_path).convert("RGB")

    # Read template configuration
    with open("config/templates.json", "r") as f:
        template_config = json.load(f)

    # Read mapper file
    with open(template_config["mapping_file"], "r") as f:
        mapper = json.load(f)

    draw = ImageDraw.Draw(template)

    # ----------------------------
    # Student Photo
    # ----------------------------

    photo = Image.open(photo_path).convert("RGB")

    photo = photo.resize((
        int(mapper["Photo"]["width"]),
        int(mapper["Photo"]["height"])
    ))

    template.paste(
        photo,
        (
            int(mapper["Photo"]["x"]),
            int(mapper["Photo"]["y"])
        )
    )

    # ----------------------------
    # Fonts
    # ----------------------------

    name_font = get_font(int(mapper["Name"]["font_size"]))
    roll_font = get_font(int(mapper["Roll_No"]["font_size"]))
    branch_font = get_font(int(mapper["Branch"]["font_size"]))
    year_font = get_font(int(mapper["Year"]["font_size"]))

    # ----------------------------
    # Student Details
    # ----------------------------

    draw.text(
        (
            int(mapper["Name"]["x"]),
            int(mapper["Name"]["y"])
        ),
        name,
        fill="black",
        font=name_font
    )

    draw.text(
        (
            int(mapper["Roll_No"]["x"]),
            int(mapper["Roll_No"]["y"])
        ),
        roll,
        fill="black",
        font=roll_font
    )

    draw.text(
        (
            int(mapper["Branch"]["x"]),
            int(mapper["Branch"]["y"])
        ),
        branch,
        fill="black",
        font=branch_font
    )

    draw.text(
        (
            int(mapper["Year"]["x"]),
            int(mapper["Year"]["y"])
        ),
        year,
        fill="black",
        font=year_font
    )

    # ----------------------------
    # Save
    # ----------------------------

    os.makedirs("generated_cards", exist_ok=True)

    template.save(output_path, quality=100)

    return output_path