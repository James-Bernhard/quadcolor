from PIL import ImageFont

from . import config
from .font_dict import make_font_dict


def set_font(filename: str, size: int) -> None:
    """
    Set config.font the the given font, specified by its filename and font size.

    Since this function uses ImageFont.truetype(), the fonts that can be used are dictated by that function.
    In particular, that function may search not only locally for the font file, but also in the system font
    directories.
    :param filename: Font filename.
    :param size: Font size in pixels.
    :return: None.
    """
    config.font = ImageFont.truetype(filename, size)
    make_font_dict()

class FontNotSetError(Exception):
    """
    Error for handling when config.font has not been set.
    """
    pass


def set_colors(ul=None, ur=None, ll=None, lr=None, non=None) -> None:
    """
    Set one or more of the colors to apply to letters. All colors are given as RGB triples of ints.

    Only the colors that are specified will be modified; all others will remain unchanged.
    :param ul: Color to apply to the upper left quadrant of letters.
    :param ur: Color to apply to the upper right quadrant of letters.
    :param ll: Color to apply to the lower left quadrant of letters.
    :param lr: Color to apply to the lower right quadrant of letters.
    :param non: Color of letters that are not to be colored.
    :return: None.
    """
    if config.font is None:
        raise FontNotSetError("The default font cannot be modified. To make changes, first set the font with set_font.")
    if ul is not None:
        config.ul_color = ul
    if ur is not None:
        config.ur_color = ur
    if ll is not None:
        config.ll_color = ll
    if lr is not None:
        config.lr_color = lr
    if non is not None:
        config.non_color = non
    make_font_dict()


def set_parameters(a_height: str = None, characters_to_color: str = None, font_characters: str = None) -> None:
    """
    Set parameters for how characters are to be colored, and which characters should be colored.

    The top coordinate of the character given in a_height will be used to truncate the top of a "d" as a substitute
    for the letter "a". This isn't perfect, but it can help when the font doesn't have a rounded "a". If no such
    substitution is desired (as when the font already has a rounded "a"), then a_height should be set to "",
    which is its initial value when the quadcolor package is loaded.

    The argument characters_to_color should be a regular expression whose match will determine that a letter
    should be colored. When the quadcolor package is loaded, this is set to "[a-z]", so only lowercase letters
    will be colored.

    The argument font_characters is a string containing all the characters that will be drawable (colored or
    uncolored) in the font. Since the font is turned into images in making the font dictionary and is then
    no longer used, this string is needed to specify all the characters to be drawn.

    :param a_height: The character whose height is to be used to truncate a "d" to make it a rounded "a".
    :param characters_to_color: A regular expression that determines which characters should be colored.
    :param font_characters: A string containing all the characters that are to be included in the font dictionary.

    :return: None
    """
    if config.font is None:
        raise FontNotSetError("The default font cannot be modified. To make changes, first set the font with set_font.")
    if a_height is not None:
        config.substitute_a = a_height
    if characters_to_color is not None:
        config.to_color = characters_to_color
    if font_characters is not None:
        config.characters = font_characters
    make_font_dict()
