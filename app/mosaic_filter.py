from PIL import Image
import numpy as np
from PIL import Image, ImageOps
import random

def resize_image(img : Image, size : tuple) -> np.ndarray:
        resz_img = ImageOps.fit(img, size, Image.LANCZOS, centering=(0.5, 0.5))
        return np.array(resz_img)

def blend_image(region, tile, opacity_percent):
    alpha = opacity_percent/100 # 1.0 - (color_diff / 255.0)
    blended_region = (alpha * region + (1.0 - alpha) * tile).astype(np.uint8)
    return blended_region

def find_closest_images(given_image, image_list, k=3):
    image_array = np.stack(image_list)
    mse_values = np.mean((image_array - given_image) ** 2, axis=(1, 2, 3))
    closest_indices = np.argpartition(mse_values, k)[:k]
    closest_images = [image_list[idx] for idx in closest_indices]
    return random.choice(closest_images)

def remove_black_borders(image_array):
    mask = np.any(image_array != [0, 0, 0], axis=-1)
    coords = np.argwhere(mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    cropped_image_array = image_array[y0:y1, x0:x1]
    return cropped_image_array


def image_mosaic_v1(target_image_path, tile_images_path, output_dir, divisions=200, scale=1, opacity_percent=50):
    target_image = Image.open(target_image_path)
    target_image = target_image.convert("RGB")
    original_width, original_height = target_image.size
    print('target image size', target_image.size)
    print('image mode', target_image.mode)
    target_image_resized = resize_image(target_image, (original_width * scale, original_height * scale))
    target_image_array = np.array(target_image_resized)
    grid_size = (target_image_array.shape[0] // divisions, target_image_array.shape[1] // divisions)

    
    # Preprocess tile images
    tile_images = [np.array(resize_image(Image.open(tile_path).convert("RGB"), (grid_size[1], grid_size[0]))) for tile_path in tile_images_path]

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

    cropped_image = remove_black_borders(combined_image)
    img = Image.fromarray(cropped_image)

    output_path = f'{output_dir}/mosaic.png'
    img.save(output_path)
    return output_path