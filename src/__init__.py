"""
The quadcolor package is used to draw and save images of four color letters.

The most important functions that it exports are:
    make_graphics: draw colored letters in images whose dimensions are determined by the size of the text.
    make_flashcards: draw colored letters in equal-sized images whose size is set by the user.
    get_flashcard_size: compute minimum width and height needed for flashcards for the given text.
    display_images: show generated images of colored letters on screen.
    save_images: save generated images of colored letters to one or more files.
    set_font: set the font used for the drawn letters.
    set_colors: set the colors used for the drawn letters.
    set_parameters: set other parameters used for drawing letters.

It also exports the load_font_dict function, which is used to load the default font dictionary when the
package loads. This function probably won't usually be needed by the user.
"""
from .config import load_font_dict
from .output import display_images, save_images
from .main import make_graphics, make_flashcards, get_flashcard_size
from .settings import set_font, set_colors, set_parameters

# use this if you'd like to remake the default font dictionary
# from . import dev

# load the default font_dict (colored Century Gothic lowercase)
load_font_dict()

