from PIL import Image
import numpy as np

# need a string of chars to represent greyscale values from black > white
# credit to Paul Bourke (http://paulbourke.net/dataformats/asciiart/)
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
char_list = [char for char in chars]

chars_2 = " .:-=+*#%@"
char_list2 = [char for char in chars_2[::-1]]


def create_pil_image(filepath):
    """Creates a PIL image from a filepath.

    Args:
        filepath (str) : path to Image
    Returns:
        PIL.Image object
    """

    try:
        image = Image.open(filepath)
    except FileNotFoundError as e:
        print(e, f"{filepath} is not a valid path to an image")

    return image


def resize_image(image, new_width=250):
    """Helper function to resize image."""

    old_width, old_height = image.size

    aspect_ratio = old_height / old_width

    new_height = int(new_width / aspect_ratio)

    return image.resize((new_width, new_height))


def to_greyscale(image):
    """Helper function to convert image to greyscale."""

    return image.convert("L")


def pixel_to_ascii(image, char_list):
    """Function to convert a greyscale image to a string of ASCII characters based on intensity.

    Args:
        image (PIL.Image) : greyscale image to convert to ascii
        char_list (list) : ASCII characters ordered from greatest to least intensity

    The greater the value (ie how "white" it is) should dictate the intenstity of the ASCII character)
    Since our ASCII list is ordered from greatest to least intensity, we want the higher values to pull from
    the end of the list (ie 255 should pull from the last char in the list)
    """

    # lets use numpy to interpolate greyscale values to indexes in our list

    pixels = np.array(image.getdata())

    # interpolate values (0-255) to the length of char list, so the greater the value, the lower intensity ASCII char is selected
    pixels_interp = np.interp(pixels, [0, 255], [0, len(char_list) - 1])
    ascii_chars = "".join([char_list[int(pixel)] for pixel in pixels_interp])

    return ascii_chars


def ascii_chars_to_image(ascii_chars, width=250):
    """Function to take a string of ASCII chars, and append a new line character after X (width) of pixels.

    This essentially translates the ASCII string to an image.
    """

    # join a newline character after every X amount of pixels (ie if width is 100, adds a newline char every 100 chars)
    return "\n".join(
        ascii_chars[i : i + width] for i in range(0, len(ascii_chars), width)
    )


def main():

    desired_width = 400

    image = create_pil_image("nathan2.jpg")

    grey_image = to_greyscale(resize_image(image, desired_width))

    ascii_chars = pixel_to_ascii(grey_image, char_list2)

    ascii_image = ascii_chars_to_image(ascii_chars, desired_width)

    with open("test.txt", "w") as art:
        art.write(ascii_image)


if __name__ == "__main__":

    main()
