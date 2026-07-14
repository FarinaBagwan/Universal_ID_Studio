# template_engine.py

from PIL import Image, ImageDraw, ImageFont
import json
import os
from datetime import datetime


class TemplateEngine:


    def __init__(self):

        self.template_folder = "templates"
        self.config_folder = "config"
        self.output_folder = "generated_cards"
        self.font_folder = "fonts"



    # -----------------------------
    # Load Template Configuration
    # -----------------------------

    def load_config(self, config_file):

        with open(config_file,"r") as file:
            return json.load(file)



    # -----------------------------
    # Load Font
    # -----------------------------

    def get_font(self,size,font_name="arial.ttf"):


        font_path = os.path.join(
            self.font_folder,
            font_name
        )


        if os.path.exists(font_path):

            return ImageFont.truetype(
                font_path,
                size
            )


        return ImageFont.load_default()



    # -----------------------------
    # Draw Text
    # -----------------------------

    def draw_text(
            self,
            image,
            field,
            value
        ):


        draw = ImageDraw.Draw(image)


        font = self.get_font(
            field.get(
                "font_size",
                30
            ),
            field.get(
                "font",
                "arial.ttf"
            )
        )


        draw.text(

            (
                field["x"],
                field["y"]
            ),

            str(value),

            fill=field.get(
                "color",
                "black"
            ),

            font=font

        )



    # -----------------------------
    # Add Image
    # -----------------------------

    def draw_image(
            self,
            image,
            field,
            image_path
        ):


        if not os.path.exists(image_path):
            return


        img = Image.open(
            image_path
        )


        img = img.resize(

            (
                field["width"],
                field["height"]
            )

        )


        image.paste(

            img,

            (
                field["x"],
                field["y"]
            )

        )



    # -----------------------------
    # Generate ID Card
    # -----------------------------


    def generate(
            self,
            student_data,
            config_file
        ):


        config = self.load_config(
            config_file
        )



        # Load Background Template

        template_path = os.path.join(

            self.template_folder,

            config["template"]

        )


        card = Image.open(
            template_path
        )



        # Process fields


        for field_name,field in config["fields"].items():



            if field_name not in student_data:
                continue



            value = student_data[field_name]



            if field["type"]=="text":


                self.draw_text(

                    card,

                    field,

                    value

                )



            elif field["type"]=="image":


                self.draw_image(

                    card,

                    field,

                    value

                )



        # Save Output


        if not os.path.exists(
            self.output_folder
        ):

            os.makedirs(
                self.output_folder
            )


        filename = (

            student_data["roll"]
            +
            "_ID_CARD.png"

        )


        output=os.path.join(

            self.output_folder,

            filename

        )


        card.save(

            output,

            dpi=(300,300)

        )


        return output