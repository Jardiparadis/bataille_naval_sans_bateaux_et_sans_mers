import pygame
import os
from Button import Button
from InteractionState import InteractionState
from MapGenerator import *

class MapUI:


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((928, 928))
        pygame.display.set_caption('A L\'ATTAQUE')

        images = self.load_images()
        self.images = images
        self.boxes = []

        map_generator = MapGenerator()

        for y in range(32):
            for x in range(32):
                boxType = map_generator.map[x][y]
                print("x : ", x , "y : ", y, boxType)
                if boxType == BoxType.Grass:
                    self.boxes.append(Button(images["Box_grass"], images["Box_grass_hovered"], images["Box_grass_clicking"], images["Box_grass_desactivated"], (x * 29, y * 29), self.click_box))
                elif boxType == BoxType.Water:
                    self.boxes.append(Button(images["Box_water"], images["Box_water_hovered"], images["Box_water_clicking"], images["Box_water_desactivated"], (x * 29, y * 29), self.click_box))
                elif boxType == BoxType.Mountain:
                    self.boxes.append(Button(images["Box_mountain"], images["Box_mountain_hovered"], images["Box_mountain_clicking"], images["Box_mountain_desactivated"], (x * 29, y * 29), self.click_box))


    def load_images(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_path, "assets")
        images_path = os.path.join(asset_path, "images")

        images_to_load = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))]

        images = {}

        for imageToLoadName in images_to_load:
            name, extension = os.path.splitext(imageToLoadName)

            if not ".png" in extension:
                continue

            img = pygame.image.load(os.path.join(images_path, imageToLoadName))
            pygame.Surface.convert_alpha(img)
            images[name] = img

        return images
    

    def display(self):
        for box in self.boxes:
            box.display(self.screen)

        pygame.display.flip()

    def check_interaction(self):
        for box in self.boxes:
            box.check_interaction()

    def click_box(idk):
        print("Click box")