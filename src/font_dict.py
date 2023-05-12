from PIL import Image, ImageFont, ImageDraw
import re

from .coloredchar import ColoredChar
from . import config


def make_colored_char(char: chr, font: ImageFont.FreeTypeFont, ul_color=(255, 0, 0), ur_color=(0, 0, 255),
                      ll_color=(128, 0, 128), lr_color=(130, 130, 131), non_color=(0, 0, 0),
                      substitute_a: chr = "", to_color: str = "[a-z]") -> ColoredChar:
    """
    Make a ColoredChar object from the specified font.

    :param char: The character to be colored.
    :param font: The font from which the character is to be taken.
    :param ul_color: RGB color for the upper left quadrant of the character.
    :param ur_color: RGB color for the upper right quadrant of the character.
    :param ll_color: RGB color for the lower left quadrant of the character.
    :param lr_color: RGB color for the lower right quadrant of the character.
    :param non_color: RGB color for characters that at not to be colored.
    :param substitute_a: The character whose height is to be used to truncate a "d" to make it a rounded "a".
    :param to_color: A regular expression that determines which characters should be colored.
    :return: A ColoredChar object.
    """
    anchor = "ls"
    if char == "a" and substitute_a:
        truncate_top = True
        char = "d"
    else:
        truncate_top = False

    # remember that x increases from left to right, and y increases from top to bottom
    left, top, right, bottom = font.getbbox(char, anchor=anchor)

    # make sure every character has at least some height and some width
    if top == bottom:
        bottom += 1
    if left == right:
        right += 1
    bbox_shape = (right - left, bottom - top)

    # make a mask of the letter
    mask = Image.new("L", bbox_shape, 0)
    d = ImageDraw.Draw(mask)
    d.text((0, 0), char, fill=255, font=font, anchor="lt")

    # make the foreground image to be colored by quadrants (non_color by default)
    quadrants = Image.new("RGB", bbox_shape, non_color)

    if char.isupper():
        # distance from top to X-height is the coordinate of the bottom minus top
        x_height = font.getbbox("X", anchor="ls")[3] - font.getbbox("X", anchor="ls")[1]
    else:
        # distance from top to x-height is the coordinate of the bottom minus top
        x_height = font.getbbox("x", anchor="ls")[3] - font.getbbox("x", anchor="ls")[1]
    x_divide, y_divide = (left + right) // 2, -x_height // 2

    # if this matches the coloring condition, color the four quadrants
    if re.search(to_color, char):
        quadrants_draw = ImageDraw.Draw(quadrants)
        quadrants_draw.rectangle((0, 0, max(0, x_divide - left), max(0, y_divide - top)), fill=ul_color)
        quadrants_draw.rectangle((min(right - left, x_divide - left), 0, right - left, max(0, y_divide - top)),
                                 fill=ur_color)
        quadrants_draw.rectangle((0, min(bottom - top, y_divide - top), max(0, x_divide - left), bottom - top),
                                 fill=ll_color)
        quadrants_draw.rectangle((min(right - left, x_divide - left), min(bottom - top, y_divide - top),
                                  right - left, bottom - top), fill=lr_color)

        if truncate_top:
            midline = font.getbbox(substitute_a, anchor=anchor)[1]
            quadrants_draw.rectangle((0, 0, right - left, midline - top), fill="white")

    return ColoredChar(mask=mask, quadrants=quadrants, x_divide=x_divide, y_divide=y_divide,
                       width=right - left, top_coord=top, bottom_coord=bottom)


def make_font_dict() -> dict:
    """
    Make a dictionary of images of and information about the available colored letters.

    This dictionary is to be used as the quadcolor global variable config.font_dict. The keys are the characters
    that can be drawn (colored or uncolored), and the entries are ColoredChar objects.
    :return: A font dictionary, to be used as config.font_dict.
    """
    # clear the current global font dictionary
    config.font_dict = dict()

    # repopulate the global font dictionary
    for char in config.characters:
        config.font_dict[char] = make_colored_char(char=char, font=config.font,
                                                   ul_color=config.ul_color, ur_color=config.ur_color,
                                                   ll_color=config.ll_color, lr_color=config.lr_color,
                                                   non_color=config.non_color,
                                                   substitute_a=config.substitute_a,
                                                   to_color=config.to_color)
    return config.font_dict
