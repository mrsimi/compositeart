import glob 
from asciii_filter import ascii_mosaicv4
from mosaic_filter import image_mosaic_v1


def apply_filter(image, output_dir, filter_type, opacity, divisions, filter_file_path=''):
    print(f'image {image.filename} output_dir {output_dir} filter_type {filter_type}')
    if filter_type == 'ascii':
        return ascii_mosaicv4(image, output_dir)
    if filter_type == 'emoji':
        tile_path = glob.glob(f'{filter_file_path}emoji/*.png')
        return image_mosaic_v1(image, tile_path[:50], output_dir, opacity_percent=opacity, divisions=divisions)
    if filter_type == 'shapes_dark':
        tile_path = glob.glob(f'{filter_file_path}shapes_dark/*.png')
        return image_mosaic_v1(image, tile_path, output_dir, opacity_percent=opacity, divisions=divisions)
    if filter_type == 'shapes_light':
        tile_path = glob.glob(f'{filter_file_path}shapes_light/*.png')
        return image_mosaic_v1(image, tile_path, output_dir, opacity_percent=opacity, divisions=divisions)



