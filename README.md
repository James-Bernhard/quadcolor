# `quadcolor` package for Python

This package is designed to produce text whose letters have
different-colored quadrants, as described
in the paper
[A Simple Method for Learning to Distinguish Mirror-Image Letters](https://edarxiv.org/m7a92/)
by James Bernhard. This type of text can be used to help people
learn to distinguish letters of the alphabet (usually lowercase
letters) from their mirror-image lookalikes.

Examples of text produced by this package can be found at
[letterreversals.org](https://letterreversals.org).

# The primary functions
The main functions for producing images with four color text are:

- `make_graphics`, which produces images whose sizes are
   determined by the sizes of the texts being set
- `make_flashcards`, which produces equal-sized images whose
   size is set by the user

Both functions take as their primary argument a list of strings
to be set. The function `make_graphics` produces a list of
images (one image per element of the input list), while
`make_flashcards` can be set to produce a list of images,
each having a specified number of rows (the `n_rows` argument)
and columns (the `n_columns` argument).

For example, `make_graphics(["this", "is a test"])` produces a list
consisting of the following two images:

![this](/readme_images/readme_images-this.jpg)

![is a test](/readme_images/readme_images-isatest.jpg)

The code documentation has more information about the optional
`margins` argument (which sets the left, top, right, and bottom
margins, in pixels) and `background` argument (which sets the RGB
background color).

`make_flashcards` works similarly but has additional arguments
to specify the size and grid layout of the images. To help
determine the size needed, the function `get_flashcard_size`
computes the minimum width and height needed for flashcards of
a given list of strings.

# Displaying and saving images
The lists of images that are generated by `make_graphics` and
`make_flashcards` can be displayed with the `display_images`
function, and can be saved with the `save_images` function.
The `save_images` function uses the
[image save](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save)
method in the Pillow package, so the file extensions and formats
that are supported are the same as those supported by the Pillow
package.

# Settings functions
Three functions to modify the package settings are provided:

- `set_font`, to use to font files other than the
  default Century Gothic,
- `set_colors`, to use colors other than the defaults, and
- `set_parameters`, for modifying other minor parameters.

See the code documentation for further information about these.
