from PIL import Image

from models import image_handler
from models.uploaded_image import ImageClazz


def start_conversion(images: list[ImageClazz]):
    image_handler.start_conversion(images)


def create_image_entities(image_paths):
    images: list[ImageClazz] = []
    for image_path in image_paths:
        image_path = convert_image_to_jpg(image_path)
        with Image.open(image_path) as image:
            img = ImageClazz(image_path, image.size[0], image.size[1])
            images.append(img)
    return images


def convert_image_to_jpg(image_path):
    return image_handler.convert_image_to_jpg(image_path)
