import math
from PIL import Image, ImageDraw
from . import drawing


def make_graphics(text_list: list, margins=(0, 0, 0, 0), bg_color=(255, 255, 255)) -> list:
    """
    Generate a list of colored text images, each having dimensions determined its text.

    :param text_list: List of strings to make colored text images of.
    :param margins: Tuple of four ints giving the left, top, right, bottom margins around text, in pixels.
    :param bg_color: Tuple of three ints giving the RGB background color (each int between 0 and 255).
    :return: List of Image.Image's, each one displaying an item from text_list in colored letters.
    """
    left_margin, top_margin, right_margin, bottom_margin = margins
    images: list = [None for _ in range(len(text_list))]
    widths, tops, bottoms = drawing.get_bboxes(text_list=text_list)
    for i in range(len(text_list)):
        images[i] = Image.new("RGB", (widths[i] + left_margin + right_margin,
                                      bottoms[i] - tops[i] + top_margin + bottom_margin), bg_color)
        images[i] = drawing.draw_text(letters=text_list[i], image=images[i],
                                      pos=(left_margin + (widths[i] // 2), top_margin - tops[i]),
                                      h_centered=True)
    return images


def get_flashcard_size(text_list: list) -> (int, int):
    """
    Compute the minimum width and height, in pixels, needed to display all the strings in the given list.

    This is useful when deciding how large to make flashcards. Each string in the given text list is to be
    set on a flashcard. This function outputs the minimum dimensions that such flashcards must have, if
    they are all to be the same size, using the current quadcolor font.
    :param text_list: List of strings, where each string is to occupy a single flashcard.
    :return: A tuple giving width and height, in pixels.
    """
    widths, tops, bottoms = drawing.get_bboxes(text_list)
    heights = [bottoms[i] - tops[i] for i, _ in enumerate(tops)]
    return max(widths), max(heights)


def make_flashcards(text_list: list,
                    n_rows: int = 0, n_columns: int = 0,
                    width: int = 2550, height: int = 3450,
                    margins=(0, 0, 0, 0), bg_color=(255, 255, 255),
                    boundary_color=(180, 180, 180), x_offset=0, y_offset=0) -> list:
    """
    Generate a list of equal-sized four color text images with specified page dimensions and layout.

    If n_rows and n_columns are both nonzero, then the flashcards will be laid out in a grid, with the
    specified number of rows and columns per image (that is, per "page"). The grid locations will be
    evenly on the page, after removing the page margins. Each str in text_list will be placed at
    a grid location. If the centering doesn't look right, you can adjust the margins until it does.

    If n_rows is specified but n_columns remains at its default value of 0, then each entry of text_list
    will occupy a row of an image, with the specified number of rows per image.

    If n_rows and n_columns both remain at their default values of 0, then the same result is produced
    as if both were equal to 1. That is, each str in text_list will be placed on a single image.
    :param text_list: List of strings to make colored text images of.
    :param n_rows: Number of rows per page of flashcards.
    :param n_columns: Number of columns per page of flashcards.
    :param width: Page width in pixels.
    :param height: Page height in pixels.
    :param margins: Tuple of four ints giving the left, top, right, bottom margins around text, in pixels.
    :param bg_color: Tuple of three ints giving the RGB background color (each int between 0 and 255).
    :param boundary_color: Tuple of three ints giving the RGB color of the lines between flashcards.
    :param x_offset: Amount by which to shift the text of every flashcard horizontally (positive means to the right).
    :param y_offset: Amount by which to shift the text of every flashcard vertically (positive means downward).
    :return:
    """
    if type(n_rows) != int or type(n_columns) != int:
        raise ValueError("Number of rows and columns must be nonnegative integers.")
    if n_rows < 0 or n_columns < 0:
        raise ValueError("Number of rows and columns must be nonnegative integers.")
    if type(width) != int or type(height) != int:
        raise ValueError("Width and height must be positive integers.")
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")

    left_margin, top_margin, right_margin, bottom_margin = margins
    n_lines = len(text_list)

    images: list
    if n_rows == 0:
        # if no rows specified, use 1 row and 1 column
        n_rows = 1
        n_columns = 1

    if not n_columns:
        # only n_rows specified, so multiple lines per image layout
        n_pages = math.ceil(n_lines / n_rows)
        h_centered = False
        images = [Image.new("RGB", (width, height), bg_color) for _ in range(n_pages)]
    else:
        # n_rows and n_columns specified, so a grid layout on each image
        n_pages = math.ceil(n_lines / (n_rows * n_columns))
        h_centered = True
        images = [Image.new("RGB", (width, height), bg_color) for _ in range(n_pages)]

    positions = drawing.compute_layout(images=images,
                                       top_margin=top_margin, left_margin=left_margin,
                                       bottom_margin=bottom_margin, right_margin=right_margin,
                                       n_rows=n_rows, n_columns=n_columns,
                                       h_centered=h_centered)

    for i, position in enumerate(positions[:n_lines]):
        page, x, y = position
        images[page] = drawing.draw_text(letters=text_list[i], image=images[page],
                                         pos=(x, y), h_centered=h_centered,
                                         x_offset=x_offset, y_offset=y_offset)

    if n_rows > 1:
        for page, image in enumerate(images):
            page_width, page_height = image.size
            page_draw = ImageDraw.Draw(images[page])
            for i in range(1, n_rows):
                page_draw.line([(0, i*page_height//n_rows), (page_width, i*page_height//n_rows)],
                               fill=boundary_color)

    if n_columns > 1:
        for page, image in enumerate(images):
            page_width, page_height = image.size
            page_draw = ImageDraw.Draw(images[page])
            for j in range(1, n_columns):
                page_draw.line([(j*page_width//n_columns, 0), (j*page_width//n_columns, page_height)],
                               fill=boundary_color)

    return images
