from dataclasses import dataclass
from PIL import Image


@dataclass
class ColoredChar:
    """
    All information needed to render a (colored or uncolored) character.

    mask: an image that is white where the character appears and black elsewhere (with gray possible as well).
    quadrants: an image that is the same dimensions as the mask, but colored (or not, as desired) in quadrants.
    x_divide: x coordinate that separates the two left quadrants from the two right quadrants.
    y_divide: y coordinate that separates the two upper quadrants from the two lower quadrants.
    width: the width of the mask and quadrants.
    top_coord: the top coordinate of the mask and quadrants.
    bottom_coord: the bottom coordinate of the mask and quadrants.

    The baseline of the character in the mask has y coordinate 0. The top and bottom coordinates are relative to
    this (with Pillow's convention of increasing y coordinates as one goes downwards on screen).

    The main use for this class is as an entry in config.font_dict.
    """
    mask: Image.Image
    quadrants: Image.Image
    x_divide: int
    y_divide: int
    width: int
    top_coord: int
    bottom_coord: int
