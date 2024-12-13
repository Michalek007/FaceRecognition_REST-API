import struct
import numpy as np
import torch
from PIL import Image


class RGB565:
    def __init__(self, image_width: int, image_height: int):
        self.image_width = image_width
        self.image_height = image_height

    @staticmethod
    def to_rgb888(rgb565):
        """
        Convert a single RGB565 value to an RGB888 tuple.

        :param rgb565: A 16-bit integer representing the RGB565 value.
        :return: A tuple of (R, G, B) values in RGB888 format.
        """
        r = (rgb565 >> 11) & 0x1F
        g = (rgb565 >> 5) & 0x3F
        b = rgb565 & 0x1F

        # Convert to 8-bit per channel
        r = (r << 3) | (r >> 2)
        g = (g << 2) | (g >> 4)
        b = (b << 3) | (b >> 2)

        return r, g, b

    def to_pil_image(self, rgb565_data: bytes):
        rgb888_data = bytearray()

        for i in range(0, len(rgb565_data), 2):
            if i + 1 < len(rgb565_data):
                # Unpack 2 bytes into a 16-bit integer
                rgb565 = struct.unpack('>H', rgb565_data[i:i + 2])[0]
                r, g, b = self.to_rgb888(rgb565)
                rgb888_data.extend([r, g, b])

        rgb888 = np.uint8(rgb888_data)
        rgb888.resize((self.image_height, self.image_width, 3))
        img = Image.fromarray(rgb888, mode="RGB")
        return img
