import matplotlib.pyplot as plt
from pathlib import Path


def display_images(images: list) -> None:
    """Use matplotlib to display a list of images."""
    for i, img in enumerate(images):
        plt.imshow(img)
        plt.show()


def save_images(images: list, output_file, single_file=True, dpi=300) -> None:
    """
    Save a list of images, according to the conventions of the image save method in the PIL package.

    The actual saving is done via the Pillow package, so whatever output formats that package can handle (as
    specified by the file extension) can be used here. If single_file is True and the output format can be
    used to save multiple images into a single file (as for pdf files, one image per page), then all images
    will be saved to a single file.
    :param images: List of Image.Images to be saved.
    :param output_file: Filename of the output file (will be appended with "-number" if multiple files are saved).
    :param single_file: Should all the images be saved to a single output file, if possible (as for a pdf)?
    :param dpi: Dots per inch in the output file.
    :return: None.
    """
    output_file = Path(output_file)
    if output_file.suffix:
        if len(images) == 1:
            images[0].save(output_file, dpi=(dpi, dpi))
        elif output_file.suffix == ".pdf" and single_file:
            images[0].save(output_file, save_all=True, append_images=images[1:], dpi=(dpi, dpi))
        else:
            for i, image in enumerate(images):
                stem = Path(str(output_file.with_suffix("")) + "-" + str(i + 1))
                image.save(stem.with_suffix(output_file.suffix), dpi=(dpi, dpi))
