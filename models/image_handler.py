import os

from PIL import Image
from models.uploaded_image import ImageClazz

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
    try:
        resized_image.save(image.get_image_path(),
                           quality=quality,
                           optimize=True)
        image.update_image_size()
        while int(image.get_image_size()) > size_limit:
            quality -= 3
            resized_image.save(image.get_image_path(),
                               quality=quality,
                               optimize=True)
            image.update_image_size()

    except AttributeError:
        pass


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


# hub for classificated images
def resize_image(img: ImageClazz) -> Image:
    if img.get_image_type() in IMAGE_CLASSIFICATIONS:
        print(img.get_image_type())
        return globals()[IMAGE_CLASSIFICATIONS[img.get_image_type()]](img)

# example 5000x2000
def resize_large_format(img: ImageClazz) -> Image:
    with Image.open(img.get_image_path()) as image:
        image_width, image_height = img.get_width(), img.get_height()
        max_height = max([size for size in range(image_height,
                                                 image_height - 11, -1)
                          if size % RATIO_HEIGHT == 0])
        max_width = (RATIO_WIDTH * max_height) // RATIO_HEIGHT
        start_point_x = image_width // 2
        cropped = image.crop((start_point_x,
                              0,
                              start_point_x + max_width,
                              max_height
                              ))
        return cropped.resize(RESIZE_RESOLUTION)

# example 2000X5000
def resize_mobile(img: ImageClazz) -> Image:
    with Image.open(img.get_image_path()) as image:
        image_width, image_height = img.get_width(), img.get_height()
        max_width = max([size for size in range(image_width, image_width -
                                                20, -1)
                         if size % RATIO_WIDTH == 0])
        max_height_y = (RATIO_HEIGHT * max_width) / RATIO_WIDTH
        start_point_y = image_height // 10
        cropped = image.crop((0,
                              start_point_y * 4,
                              max_width,
                              start_point_y * 4 + max_height_y
                              ))
        return cropped.resize(RESIZE_RESOLUTION)

# example 1920x1080
def resize_standard(img: ImageClazz) -> Image:
    with Image.open(img.get_image_path()) as image:
        image_width, image_height = img.get_width(), img.get_height()
        max_width_x = max([size
                           for size in range(image_width,
                                             image_width - 20, -1)
                           if size % RATIO_WIDTH == 0])
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
        max_width_x = max([size
                           for size in range(image_width,
                                             image_width - 20, -1)
                           if size % RATIO_WIDTH == 0])
        max_height_y = (RATIO_HEIGHT * max_width_x) / RATIO_WIDTH
        start_point_y = image_height // 20
        cropped = image.crop((0,
                              start_point_y * 2,
                              max_width_x,
                              start_point_y * 2 + max_height_y))
        return cropped.resize(RESIZE_RESOLUTION)
