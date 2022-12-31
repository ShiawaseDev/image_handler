import os


class ImageClazz(object):

    def __init__(self, image_path, width: int, height: int) -> None:
        self._image_path = image_path
        self._width = width
        self._height = height
        self._image_type = {
            (self._width / self._height < 1): 'mobile',
            (self._width / self._height >= 2.3): 'large_format',
            (1.5 <= self._width / self._height < 2.3): 'standard',
            (1 <= self._width / self._height < 1.5): 'square',
        }[True]
        self._image_size = os.path.getsize(self._image_path) // 1024

    def get_image_size(self):
        return str(self._image_size)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_image_type(self):
        return self._image_type

    def get_image_path(self):
        return self._image_path

    def update_image_size(self):
        if self._image_path:
            self._image_size = os.path.getsize(self._image_path) // 1024

    def update_image_type(self):
        self._image_type = {
            (self._width / self._height < 1): 'mobile',
            (self._width / self._height >= 2.3): 'large_format',
            (1.5 <= self._width / self._height < 2.3): 'standard',
            (1 <= self._width / self._height < 1.5): 'square',
        }[True]

    def update_resolution(self, width, height):
        self._height = height
        self._width = width

    def get_resolution(self):
        return self._width, self._height 

    def update_info(self, width: int, height: int):
        self.update_image_size()
        self.update_resolution(width=width, height=height)
        self.update_image_type()

