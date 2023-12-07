from opensimplex import OpenSimplex
from PIL import Image
import random

shape = (32, 32)
scale = 9.1

blue = (66, 110, 255)
green = (36, 135, 32)
mountains = (140, 140, 140)

image_filepath = "noise.png"

seed = random.randint(0,1000)  # You can change this seed to any integer value
random.seed(seed)
noise_generator = OpenSimplex(seed)

image = Image.new(mode="RGB", size=shape)

def set_color(x, y, image, value):
    if value < 70:
        image.putpixel((x, y), blue)
    elif value < 200:
        image.putpixel((x, y), green)
    elif value < 255:
        image.putpixel((x, y), mountains)

for x in range(shape[0]):
    for y in range(shape[1]):
        value = noise_generator.noise2d(x/scale, y/scale)

        # Contrast
        value *= 1.2

        # Clipping
        if value > 1:
            value = 1
        elif value < -1:
            value = -1

        value = int(((value + 1.0) * 0.5) * 255)
        set_color(x, y, image, value)

image.save(image_filepath)
