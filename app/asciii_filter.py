from PIL import Image, ImageDraw
import numpy as np
from PIL import Image


def getChar(value, charArray, interval):
    return charArray[int(value * interval)]


def ascii_mosaicv4(image, output_dir):
    chars = ' .`-_\':,;^=+/"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q'
    charArray = list(chars)
    charLength = len(charArray)
    interval = charLength / 256

    scaleFactor = 0.09
    oneCharWidth = 10
    oneCharHeight = 18

    image.flush()
    im = Image.open(image.stream)
    width, height = im.size
    im = im.resize((int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))), Image.NEAREST)
    width, height = im.size

    pix = np.array(im)
    gray = np.dot(pix[..., :3], [0.2989, 0.5870, 0.1140]).astype(int)

    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
    d = ImageDraw.Draw(outputImage)

    chars_array = np.vectorize(lambda h: getChar(h, charArray, interval))(gray)

    # Prepare all text drawing commands
    text_commands = []
    for i in range(height):
        for j in range(width):
            char = chars_array[i, j]
            r, g, b = pix[i, j]
            position = (j * oneCharWidth, i * oneCharHeight)
            text_commands.append((position, char, (r, g, b)))

    # Execute drawing commands
    for position, char, color in text_commands:
        d.text(position, char, fill=color)

    output_path = f'{output_dir}/mosaic.png'
    outputImage.save(output_path)
    return output_path