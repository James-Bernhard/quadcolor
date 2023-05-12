"""
The config module contains several global variables for the quadcolor package:

font_dict: a dictionary containing colored letters, set (behind the scenes) by calling font_dict.make_font_dict()
font: an ImageFont.FreeTypeFont that can be set by the user with settings.set_font()
ul_color, ur_color, ll_color, lr_color, non_color: RGB color triples set by the user with settings.set_colors()
substitute_a, to_color, characters: parameters for coloring letters set by the user with settings.set_parameters()

Also, the module contains the function load_font_dict(), which is used to load the default font dictionary into
font_dict when the package is loaded. This is necessary since there is no guarantee what fonts any particular
computer will have.
"""
import io
import json
from pathlib import Path
from PIL import Image, ImageFont
import pkgutil

from .coloredchar import ColoredChar

font_dict: dict = dict()
font: ImageFont.FreeTypeFont = None
ul_color: tuple = (255, 0, 0)
ur_color: tuple = (0, 0, 255)
ll_color: tuple = (128, 0, 128)
lr_color: tuple = (130, 130, 131)
non_color: tuple = (0, 0, 0)
substitute_a: chr = ""
to_color: chr = "[a-z]"

# usual printable ascii characters, plus left single quote, right single quote, left double quote, right double quote
characters: str = str([chr(i) for i in range(32, 127)]) + u"\u2018\u2019\u201C\u201D"


# loads the default font_dict into the global variable font_dict
def load_font_dict(metadata_filename: str = "default_font_metadata.json", mask_filename: str = "default_font_mask.jpg",
                   quadrants_filename="default_font_quadrants.jpg", input_directory="default_font") -> None:
    global font_dict
    font_dict = dict()
    input_directory = Path(input_directory)
    metadata_file = input_directory / Path(metadata_filename)
    mask_file = Path(mask_filename)
    quadrants_file = Path(quadrants_filename)

    raw_data = pkgutil.get_data(__package__, str(metadata_file))
    pre_font_dict = json.loads(raw_data)
    for key, value in pre_font_dict.items():
        file = str((input_directory /
                    mask_file.stem.replace(mask_file.stem,
                                           mask_file.stem + "_" + str(ord(key)))).with_suffix(".jpg"))
        raw_mask = pkgutil.get_data(__package__, file)
        mask = Image.open(io.BytesIO(raw_mask))
        file = str((input_directory /
                    quadrants_file.stem.replace(quadrants_file.stem,
                                                quadrants_file.stem + "_" + str(ord(key)))).with_suffix(".jpg"))
        raw_quadrants = pkgutil.get_data(__package__, file)
        quadrants = Image.open(io.BytesIO(raw_quadrants))

        font_dict[key] = ColoredChar(mask=mask, quadrants=quadrants,
                                     x_divide=value["x_divide"], y_divide=value["y_divide"],
                                     width=value["width"], top_coord=value["top_coord"],
                                     bottom_coord=value["bottom_coord"])

