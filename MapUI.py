import pygame
import os
from Button import Button
from InteractionState import InteractionState
from MapGenerator import *

class MapUI:


    def __init__(self):
        pygame.init()
        self.shape = (32,32)
        self.box_pixel_size = 29
        self.screen = pygame.display.set_mode((self.box_pixel_size * self.shape[0], self.box_pixel_size * self.shape[1]))
        pygame.display.set_caption('A L\'ATTAQUE')

        images = self.load_images()
        self.images = images
        self.boxes = []

        self.color_player = pygame.Color("#ffffff")
        self.player_side_rect_1 = pygame.Rect(0, self.box_pixel_size * 2 - 1, self.shape[0] * self.box_pixel_size, 2)
        self.player_side_rect_2 = pygame.Rect(0, (self.shape[1] - 2) * self.box_pixel_size - 1, self.shape[0] * self.box_pixel_size, 2)

        map_generator = MapGenerator(self.shape)

        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                boxType = map_generator.map[x][y]
                pos = (x * self.box_pixel_size, y * self.box_pixel_size)
                fn = lambda: self.click_box(x, y)

                if boxType == BoxType.Grass:
                    boxe = Button(images["Box_grass"], images["Box_grass_hovered"], images["Box_grass_clicking"], images["Box_grass_desactivated"], pos, lambda: self.click_box(x = x, y = y))
                elif boxType == BoxType.Water:
                    boxe = Button(images["Box_water"], images["Box_water_hovered"], images["Box_water_clicking"], images["Box_water"], pos, lambda: self.click_box(x = x, y = y))
                    boxe.is_activated = False
                elif boxType == BoxType.Mountain:
                    boxe = Button(images["Box_mountain"], images["Box_mountain_hovered"], images["Box_mountain_clicking"], images["Box_mountain_desactivated"], pos, lambda: self.click_box(x = x, y = y))

                self.boxes.append(boxe)

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

        pygame.draw.rect(self.screen, self.color_player, self.player_side_rect_1)
        pygame.draw.rect(self.screen, self.color_player, self.player_side_rect_2)

        pygame.display.flip()

    def check_interaction(self):
        for box in self.boxes:
            box.check_interaction()

    def click_box(self, x, y):
        # x = x_pos / self.box_pixel_size
        # y = y_pos / self.box_pixel_size
        print("Click box : x : ", x, ", y : " , y)