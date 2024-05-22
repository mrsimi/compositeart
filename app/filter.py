from PIL import Image, ImageFont, ImageDraw
import math

def getChar(inputInt, charArray, interval):
    return charArray[math.floor(inputInt*interval)]

def apply_filter(image, output_dir, filter_type):
    print(f'image {image.filename} output_dir {output_dir} filter_type {filter_type}')
    if filter_type == 'ascii':
        return ascii(image, output_dir)

def ascii(image, output_dir):
    chars = ' .`-_\':,;^=+/"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q' #[::-1]
    #chars = "#Wo- "[::-1]
    charArray = list(chars)
    charLength = len(charArray)
    interval = charLength/256

    scaleFactor = 0.09
    oneCharWidth = 10
    oneCharHeight = 18

    im = Image.open(image)
    width, height = im.size
    im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
    width, height = im.size
    pix = im.load()
    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (0, 0, 0))
    d = ImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            r, g, b = pix[j, i]
            h = int(r/3 + g/3 + b/3)
            pix[j, i] = (h, h, h)
            #text_file.write(getChar(h))
            d.text((j*oneCharWidth, i*oneCharHeight), getChar(h, charArray,interval),fill = (r, g, b))
    
    output_path = f'{output_dir}/mosaic.jpg'
    outputImage.save(output_path)
    return output_path