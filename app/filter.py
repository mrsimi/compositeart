from PIL import Image, ImageFont, ImageDraw
import math
import numpy as np
from PIL import Image, ImageOps
import random
from io import BytesIO
import glob 

def getChar(inputInt, charArray, interval):
    return charArray[math.floor(inputInt*interval)]

def apply_filter(image, output_dir, filter_type, filter_file_path=''):
    print(f'image {image.filename} output_dir {output_dir} filter_type {filter_type}')
    if filter_type == 'ascii':
        return ascii_mosaic(image, output_dir)
    if filter_type == 'emoji':
        tile_path = glob.glob(f'{filter_file_path}/*.png')
        return image_mosaic(image, tile_path[:50], output_dir)


def ascii_mosaic(image, output_dir):
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
    
    output_path = f'{output_dir}/mosaic.png'
    outputImage.save(output_path)
    return output_path

def resize_image(img : Image, size : tuple) -> np.ndarray:
        resz_img = ImageOps.fit(img, size, Image.LANCZOS, centering=(0.5, 0.5))
        return np.array(resz_img)

def blend_image(region, tile, opacity_percent):
    alpha = opacity_percent/100 # 1.0 - (color_diff / 255.0)
    blended_region = (alpha * region + (1.0 - alpha) * tile).astype(np.uint8)
    return blended_region

def find_closest_images(given_image, image_list, k=3):
    mse_values = [np.mean((given_image - img) ** 2) for img in image_list]
    closest_indices = np.argsort(mse_values)[:k]
    closest_images = [image_list[idx] for idx in closest_indices]
    return random.choice(closest_images)

def image_mosaic(target_image_path, tile_images_path, output_dir, divisions=50, scale=2, opacity_percent=50):
    target_image = Image.open(target_image_path)
    target_image = target_image.convert("RGB")
    original_width, original_height = target_image.size
    print('target image size', target_image.size)
    print('image mode', target_image.mode)
    target_image_resized = resize_image(target_image, (original_width * scale, original_height * scale))
    target_image_array = np.array(target_image_resized)
    grid_size = (target_image_array.shape[0] // divisions, target_image_array.shape[1] // divisions)

    
    # Preprocess tile images
    tile_images = []
    for tile_path in tile_images_path:
        tile_image = Image.open(tile_path)
        tile_image = tile_image.convert("RGB")
        #print('resize before ', tile_image.size)
        tile_image_resized = resize_image(tile_image, (grid_size[1], grid_size[0]))
        #print('resize after ', tile_image_resized.shape)
        tile_images.append(np.array(tile_image_resized))
        tile_image.close()

    combined_image = np.zeros_like(target_image_array)

    for i in range(divisions):
        for j in range(divisions):
            x1, y1 = j * grid_size[1], i * grid_size[0]
            x2, y2 = (j + 1) * grid_size[1], (i + 1) * grid_size[0]

            grid_image = target_image_array[y1:y2, x1:x2, :]
            # print(f'grid image', grid_image.shape)
            # print(f'tile images', tile_images[0].shape)
            # print(f'grid_size ',grid_size)
            closest_image = find_closest_images(grid_image, tile_images)
            blended_image = blend_image(grid_image, closest_image,opacity_percent)
            combined_image[y1:y2, x1:x2, :] = blended_image

    img = Image.fromarray(combined_image)

    output_path = f'{output_dir}/mosaic.png'
    img.save(output_path)
    return output_path