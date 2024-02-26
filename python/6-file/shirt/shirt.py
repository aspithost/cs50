from os import path
from PIL import Image, ImageOps
from sys import argv, exit


def main():
    input, output = check_command_line()
    shirt = get_shirt()
    cropped_image = crop_image(input, shirt.size)
    cropped_image.paste(shirt, (0,0), shirt)
    cropped_image.save(output)


def check_command_line():
    length = len(argv)
    if length < 3:
        exit("Too few command-line arguments")
    elif length > 3:
        exit("Too many command-line arguments")
    else:
        input_ext = get_ext(argv[1])
        output_ext = get_ext(argv[2])
        if input_ext != output_ext:
            exit("Input and output have different extensions")
        elif not output_ext.endswith("jpg") and not output_ext.endswith("jpeg") and not output_ext.endswith("png"):
            exit("Invalid output")
        else:
            return argv[1], argv[2]


def crop_image(input, size):
    try:
        with Image.open(input) as img:
            return ImageOps.fit(img, size)
    except FileNotFoundError:
        exit("Input does not exist")


def get_shirt():
    try:
        return Image.open("./shirt.png")
    except FileNotFoundError:
        exit("Input does not exist")


def get_ext(p):
    return path.splitext(p)[1].lower()


main()