import os

from PIL import Image
from models.image_model import ImageClazz

RESIZE_RESOLUTION = 1920, 1080
RATIO_WIDTH, RATIO_HEIGHT = 16, 9  # Standard ratio for 1920x1080 - 16:9
IMAGE_CLASSIFICATIONS = {
    'large_format': 'resize_large_format',
    'mobile': 'resize_mobile',
    'standard': 'resize_standard',
    'square': 'resize_square',
}


def save_with_size_limit(resized_image: Image, image: ImageClazz, quality=100,
                         size_limit=350):
    resized_image.save(image.get_image_path(),
                        quality=quality,
                        optimize=True,
                        dpi=(300, 300))
    if image.get_resolution() == RESIZE_RESOLUTION:
        image.update_image_size()
    else:
        image.update_info(resized_image.size[0], resized_image.size[1])
    while int(image.get_image_size()) > size_limit:
        quality -= 2
        resized_image.save(image.get_image_path(),
                            quality=quality,
                            optimize=True,
                            dpi=(300, 300))
        image.update_image_size()



def start_conversion(images: list[ImageClazz]):
    for image in images:
        resized_image = resize_image(image)
        save_with_size_limit(resized_image, image)


def convert_image_to_jpg(image_path):
    extension = os.path.splitext(image_path, )[1]
    if extension in ('.png', '.webp', '.jpeg'):
        old_image_path = image_path
        with Image.open(image_path) as image:
            image_path = str(image_path).replace(extension, '.jpg')
            converted_image = image.convert('RGB')
            converted_image.save(image_path)
        remove_image(old_image_path)
    return image_path


# Remove old image after conversion from PNG, WEBP
def remove_image(image_path):
    os.remove(image_path)

# need changes or not True - yes, False - no
def validate_image(img: ImageClazz) -> bool:
    height = (RATIO_HEIGHT * img.get_width()) / RATIO_WIDTH
    width = (RATIO_WIDTH * img.get_height()) // RATIO_HEIGHT
    if img.get_height() == height and img.get_width() == width:
        return False
    else:
        return True

# hub for classificated images
def resize_image(img: ImageClazz) -> Image:
    if img.get_image_type() in IMAGE_CLASSIFICATIONS and validate_image(img=img):
        return globals()[IMAGE_CLASSIFICATIONS[img.get_image_type()]](img)
    else:
        try:
            with Image.open(img.get_image_path()) as image:
                return image.resize(RESIZE_RESOLUTION)
        except FileNotFoundError:
            print('Loaded file path not found, you are changed filename after load.')# Add logger
            

# example 5000x2000
def resize_large_format(img: ImageClazz) -> Image:
    with Image.open(img.get_image_path()) as image:
        image_width, image_height = img.get_width(), img.get_height()
        max_height = find_max_height(image_height=image_height)
        max_width = (RATIO_WIDTH * max_height) // RATIO_HEIGHT
        start_point = (image_width // 2) - (max_width // 2)
        end_point = (image_width // 2) + (max_width // 2)
        cropped = image.crop((start_point,
                              0,
                              end_point,
                              max_height
                              ))
        return cropped.resize(RESIZE_RESOLUTION)

# example 2000X5000
def resize_mobile(img: ImageClazz) -> Image:
    with Image.open(img.get_image_path()) as image:
        image_width, image_height = img.get_width(), img.get_height()
        max_width = find_max_width(image_width=image_width)
        max_height = (RATIO_HEIGHT * max_width) / RATIO_WIDTH
        start_point = (image_height // 2) - (max_height // 2)
        end_point = (image_height // 2) + (max_height // 2)
        cropped = image.crop((0,
                              start_point,
                              max_width,
                              end_point
                              ))
        return cropped.resize(RESIZE_RESOLUTION)

# example 1920x1080
def resize_standard(img: ImageClazz) -> Image:
    with Image.open(img.get_image_path()) as image:
        image_width, image_height = img.get_width(), img.get_height()
        max_width_x = find_max_width(image_width=image_width)
        max_height_y = (RATIO_HEIGHT * max_width_x) / RATIO_WIDTH
        if max_height_y > image_height:
            max_height_y = image_height
        cropped = image.crop((0,
                              0,
                              max_width_x,
                              max_height_y))
        return cropped.resize(RESIZE_RESOLUTION)

# example 1280x1280
def resize_square(img: ImageClazz) -> Image:
    with Image.open(img.get_image_path()) as image:
        image_width, image_height = img.get_width(), img.get_height()
        max_width = find_max_width(image_width=image_width)
        max_height = (RATIO_HEIGHT * max_width) / RATIO_WIDTH
        start_point = (image_height // 2) - (max_height // 2)
        end_point = (image_height // 2) + (max_height // 2)
        cropped = image.crop((0,
                              start_point,
                              max_width,
                              end_point))
        return cropped.resize(RESIZE_RESOLUTION)

def find_max_width(image_width: int) -> int:
    max_width_x = max([size
                           for size in range(image_width,
                                             image_width - 20, -1)
                           if size % RATIO_WIDTH == 0])
    return max_width_x

def find_max_height(image_height):
    max_height = max([size for size in range(image_height,
                                             image_height - 20, -1)
                          if size % RATIO_HEIGHT == 0])
        
    return max_height