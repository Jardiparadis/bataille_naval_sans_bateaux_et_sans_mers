from enum import Enum
from opensimplex import OpenSimplex
import random

class BoxType(Enum):
    Grass = 0,
    Water = 1,
    Mountain = 2


class MapGenerator:

    def __init__(self):

        shape = (32, 32)
        scale = 9.1

        seed = random.randint(0,1000)  # You can change this seed to any integer value
        random.seed(seed)
        noise_generator = OpenSimplex(seed)

        self.map = [[0 for x in range(shape[0])] for y in range(shape[1])] 

        def set_color(x, y, value):
            if value < 70: # Water
                self.map[x][y] = BoxType.Water
            elif value < 200: # Green
                self.map[x][y] = BoxType.Grass
            elif value < 255: # Mountain
                self.map[x][y] = BoxType.Mountain

        for x in range(shape[0]):
            for y in range(shape[1]):
                value = noise_generator.noise2(x/scale, y/scale)

                # Contrast
                value *= 1.2

                # Clipping
                if value > 1:
                    value = 1
                elif value < -1:
                    value = -1

                value = int(((value + 1.0) * 0.5) * 255)
                set_color(x, y, value)
