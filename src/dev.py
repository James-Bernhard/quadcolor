"""
The dev module contains functions that were used to save the package default config.font_dict. It should not be
needed any further, unless that package default is to be changed.

To make the initial config.font_dict, a font_dict was created. This was followed by:

save_font_dict_metadata()
save_font_dict_images()

Then the files that were created were placed in the data directory.
"""
import json
from pathlib import Path

from . import config


def save_font_dict_metadata(filename: str = "default_font_metadata.json") -> None:
    """Save everything in config.font_dict except for the images (masks and quadrants) to a json file."""
    pre_font_dict = dict()
    for key in config.font_dict.keys():
        pre_font_dict[key] = dict(x_divide=config.font_dict[key].x_divide,
                                  y_divide=config.font_dict[key].y_divide,
                                  width=config.font_dict[key].width,
                                  top_coord=config.font_dict[key].top_coord,
                                  bottom_coord=config.font_dict[key].bottom_coord)
    with open(filename, "w") as file:
        json.dump(pre_font_dict, file)


def save_font_dict_images(mask_filename: str = "default_font_mask.jpg",
                          quadrants_filename: str = "default_font_quadrants.jpg",
                          output_directory=".") -> None:
    """Save the images (masks and quadrants) in config.font_dict."""
    output_directory = Path(output_directory)
    mask_file = Path(mask_filename)
    quadrants_file = Path(quadrants_filename)

    for key, value in config.font_dict.items():
        file = (output_directory /
                mask_file.stem.replace(mask_file.stem,
                                       mask_file.stem + "_" + str(ord(key)))).with_suffix(".jpg")
        value.mask.save(file)
        file = (output_directory /
                quadrants_file.stem.replace(quadrants_file.stem,
                                            quadrants_file.stem + "_" + str(ord(key)))).with_suffix(".jpg")
        value.quadrants.save(file)

