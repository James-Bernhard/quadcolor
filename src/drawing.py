from PIL import Image

from . import config


def get_bboxes(text_list: list) -> (list, list, list):
    """
    Get the width, top coordinate, and bottom coordinate of each entry in a list of str.

    The baseline of the text is taken to have a y coordinate of 0, and the top and bottom coordinates are
    computed relative to this. All dimensions are in pixels.
    :param text_list: A list of str, whose widths, top coordinates, and bottom coordinates are to be computed.
    :return: A tuple of three lists of ints: a width list, a top coordinates list, and a bottom coordinates list.
    """
    # font_dict = config.font_dict
    widths = [0 for _ in range(len(text_list))]
    tops = [0 for _ in range(len(text_list))]
    bottoms = [0 for _ in range(len(text_list))]

    for i, text in enumerate(text_list):
        for j in text:
            # needs error handling if j is not in font_dict
            if j in config.font_dict.keys():
                widths[i] += config.font_dict[j].width
                if j != " ":
                    tops[i] = min(tops[i], config.font_dict[j].top_coord)
                    bottoms[i] = max(bottoms[i], config.font_dict[j].bottom_coord)

    return widths, tops, bottoms


class OutOfFontError(Exception):
    """
    Error for handling when a character is not included in config.font_dict
    """
    pass


# draw a line of letters at a specified position on a given image
def draw_text(letters: str, image: Image.Image, pos=(0, 0),
              h_centered: bool = True, v_centered: bool = True,
              x_offset = 0, y_offset = 0) -> Image.Image:
    """
    Draw the specified letters string in colored letters.

    The letters will be drawn in the specified image at the specified (x, y) position, using the quadcolor font.
    The baseline of the letters will be at the specified y position. If h_centered is True, then the letters will be
    horizontally centered at the specified x position; otherwise, their leftmost extreme will be there. If
    v_centered is True, then the text will be shifted downward by half the x-height, if x is in the font_dict.

    In keeping with the PIL package, x coordinates increase from left to right, while y coordinates increase from
    top to bottom. The point (0, 0) is at the upper left corner of the image.

    :param letters: String of letters to be drawn.
    :param image: Image to draw the letters on.
    :param pos: (x, y) tuple of int giving the image coordinates of the position for the letters.
    :param h_centered: Should the text be centered horizontally at the specified position?
    :param v_centered: Should the text be shifted vertically by half the x-height?
    :param x_offset: Amount by which to shift the text of every flashcard horizontally (positive means to the right).
    :param y_offset: Amount by which to shift the text of every flashcard vertically (positive means downward).
    :return: The original image but with the colored letters drawn in it.
    """
    x_pos, y_pos = pos

    y_shift = 0
    if v_centered and "x" in config.font_dict.keys():
        # to vertically center, offset by half the x-height
        y_shift = config.font_dict["x"].quadrants.size[1] // 2

    width = 0

    for letter in letters:
        if letter in config.font_dict.keys():
            width += config.font_dict[letter].width
        else:
            raise OutOfFontError(letter + " is not in the current quadcolor font dictionary. "
                                 "Use set_font to specify a font and then set_parameters to "
                                 "specify which characters are in the quadcolor font dictionary.")

    current_x_pos = x_pos - (width // 2) if h_centered else int(x_pos)
    for letter in letters:
        if letter in config.font_dict.keys():
            image.paste(config.font_dict[letter].quadrants,
                        (current_x_pos + x_offset, y_pos + config.font_dict[letter].top_coord + y_shift + y_offset),
                        config.font_dict[letter].mask)
            current_x_pos += config.font_dict[letter].width
    return image


def compute_layout(images: list,
                   top_margin: int, left_margin: int, bottom_margin: int, right_margin: int,
                   n_rows: int = 0, n_columns: int = 0,
                   h_centered: bool = True) -> list:
    """
    Compute (image number, x, y) tuples of positions to place text at for a grid layout (for flashcards).

    All coordinates and dimensions are in pixels.
    :param images: A list of images (Image.Image objects) on which to make the grid layouts.
    :param top_margin: Top margin in each image, in pixels.
    :param left_margin: Left margin in each image, in pixels.
    :param bottom_margin: Bottom margin in each image, in pixels.
    :param right_margin: Right margin in each image, in pixels.
    :param n_rows: Number of rows per image.
    :param n_columns: Number of columns per image.
    :param h_centered: Should the text be horizontally centered at the computed positions?
    :return: List of (image number, x, y) tuples specifying image numbers and positions in a text layout.
    """
    n_pages = len(images)
    page_sizes = [image.size for image in images]

    if n_columns == 0:
        # rows specified but no columns, so do that many lines per page
        text_widths = [page_size[0] - left_margin - right_margin for page_size in page_sizes]
        x_offsets = [int(text_width / 2) for text_width in text_widths] if h_centered else [0 for _ in text_widths]
        line_heights = [(page_size[1] - top_margin - bottom_margin) / n_rows for page_size in page_sizes]
        y_offsets = [int(line_height / 2) for line_height in
                     line_heights]  # if v_centered else [0 for _ in line_heights]
        positions = [(k, left_margin + x_offsets[k], top_margin + int(i * line_heights[k] + y_offsets[k]))
                     for k in range(n_pages)
                     for i in range(n_rows)]
    else:
        # rows and columns both specified, so do a grid layout
        card_widths = [(page_size[0] - left_margin - right_margin) / n_columns for page_size in page_sizes]
        x_offsets = [int(card_width / 2) for card_width in card_widths] if h_centered else [0 for _ in card_widths]
        card_heights = [(page_size[1] - top_margin - bottom_margin) / n_rows for page_size in page_sizes]
        y_offsets = [int(card_height / 2) for card_height in card_heights]
        positions = [(k, left_margin + int(j * card_widths[k] + x_offsets[k]),
                      top_margin + int(i * card_heights[k] + y_offsets[k]))
                     for k in range(n_pages)
                     for i in range(n_rows)
                     for j in range(n_columns)]

    return positions

