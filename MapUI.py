import pygame
import os
from Button import Button
from InteractionState import InteractionState
from MapGenerator import *
from Utils import Utils
from SoldierStatsUI import SoldierStatsUI
from PIL import Image

class MapUI:


    def __init__(self):
        pygame.init()
        self.shape = (32,32)
        self.box_pixel_size = 29

        screen_size = (self.box_pixel_size * self.shape[0] + 300, self.box_pixel_size * self.shape[1])
        self.screen = pygame.display.set_mode(screen_size)

        
        pygame.display.set_caption('Frontline Conquest')

        base_path = os.path.dirname(os.path.abspath(__file__))
        Utils.asset_path = os.path.join(base_path, "assets")

        self.create_back_img(screen_size)

        images = self.load_images()
        self.images = images
        self.boxes = []
        self.soldier_stats_1 = []
        self.soldier_stats_2 = []

        self.title_game = Utils.getTextWithColor("Frontline Conquest", 25, pygame.Color("white"))

        self.black_color = pygame.Color("#1C1C1C")
        self.color_player = pygame.Color("#ffffff")
        self.player_side_rect_1 = pygame.Rect(0, self.box_pixel_size * 2 - 1, self.shape[0] * self.box_pixel_size, 2)
        self.player_side_rect_2 = pygame.Rect(0, (self.shape[1] - 2) * self.box_pixel_size - 1, self.shape[0] * self.box_pixel_size, 2)

        self.back_img = images["back_end_game"]

        map_generator = MapGenerator(self.shape)

        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                boxType = map_generator.map[x][y]
                pos = (x * self.box_pixel_size, y * self.box_pixel_size)

                fn = lambda x=x, y=y: self.click_box(x, y)

                if boxType == BoxType.Grass:
                    boxe = Button(images["Box_grass"], images["Box_grass_hovered"], images["Box_grass_clicking"], images["Box_grass_desactivated"], pos, fn)
                elif boxType == BoxType.Water:
                    boxe = Button(images["Box_water"], images["Box_water_hovered"], images["Box_water_clicking"], images["Box_water"], pos, fn)
                    boxe.is_activated = False
                elif boxType == BoxType.Mountain:
                    boxe = Button(images["Box_mountain"], images["Box_mountain_hovered"], images["Box_mountain_clicking"], images["Box_mountain_desactivated"], pos, fn)

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
    
    def create_back_img(self, screen_size):
        base_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_path, "assets")
        images_path = os.path.join(asset_path, "images")


        image_temp = Image.new(mode="RGBA", size=screen_size)

        for x in range(screen_size[0]):
            for y in range(screen_size[1]):
                image_temp.putpixel((x, y), (0, 0, 0, 100))

        image_temp.save( os.path.join(images_path, "back_end_game.png"))

    def display(self):

        self.screen.fill(self.black_color)

        for box in self.boxes:
            box.display(self.screen)


        for soldier_stats_ui in self.soldier_stats_1:
            soldier_stats_ui.display(self.screen)

        for soldier_stats_ui in self.soldier_stats_2:
            soldier_stats_ui.display(self.screen)

        pygame.draw.rect(self.screen, self.color_player, self.player_side_rect_1)
        pygame.draw.rect(self.screen, self.color_player, self.player_side_rect_2)

        self.screen.blit(self.title_game, (967 , 451))
        self.screen.blit(self.back_img, (0 , 0))

        pygame.display.flip()

    def check_interaction(self):
        for box in self.boxes:
            box.check_interaction()

        for soldier_stats_ui in self.soldier_stats_1:
            soldier_stats_ui.check_interaction()

        for soldier_stats_ui in self.soldier_stats_2:
            soldier_stats_ui.check_interaction()

    def click_box(self, x, y):
        print("Click box : x : ", x, ", y : " , y)

    
    def add_soldier_stats(self, player_id, soldier):

        is_player_one = (player_id == 0)

        start_pos_soldier_stat = (956, 68) if is_player_one else (956, 538)

        nb_soldier_stat = len(self.soldier_stats_1) if is_player_one else len(self.soldier_stats_2)

        pos_soldier_stat = (start_pos_soldier_stat[0], start_pos_soldier_stat[1] + 56 * nb_soldier_stat)

        hearth_btn = Button(self.images["Life"], self.images["Life_Hovered"], self.images["Life"], self.images["Life_Hovered"], (pos_soldier_stat[0] + 61, pos_soldier_stat[1] + 8), 0)
        gun_btn = Button(self.images["Gun"], self.images["Gun_Hovered"], self.images["Gun"], self.images["Gun_Hovered"], (pos_soldier_stat[0] + 150, pos_soldier_stat[1] + 7), 0)


        soldier_img = self.images["Soldier1"] if is_player_one else self.images["Soldier2"]
        back_img = self.images["Back_Stat_Player_1"] if is_player_one else self.images["Back_Stat_Player_2"]


        soldier_stats_ui = SoldierStatsUI(soldier, soldier_img, back_img, self.images["Back_Stat_Player_Desactivated"], hearth_btn, gun_btn, pos_soldier_stat)

        if is_player_one:
            self.soldier_stats_1.append(soldier_stats_ui)
        else:
            self.soldier_stats_2.append(soldier_stats_ui)

