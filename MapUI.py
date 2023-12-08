import pygame
import os
from Button import Button
from InteractionState import InteractionState
from MapGenerator import *
from Utils import Utils
from SoldierStatsUI import SoldierStatsUI
from PIL import Image
import sys
from pygame import mixer
from Soldier import Soldier

class MapUI:


    def __init__(self):
        pygame.init()
        pygame.mixer.init()
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

        self.nb_turns = 1

        self.title_game = Utils.getTextWithColor("Frontline Conquest", 25, pygame.Color("white"))

        self.black_color = pygame.Color("#1C1C1C")
        self.color_player = pygame.Color("#ffffff")
        self.player_side_rect_1 = pygame.Rect(0, self.box_pixel_size * 2 - 1, self.shape[0] * self.box_pixel_size, 2)
        self.player_side_rect_2 = pygame.Rect(0, (self.shape[1] - 2) * self.box_pixel_size - 1, self.shape[0] * self.box_pixel_size, 2)


        self.loose_img = images["LooseSoldier"]
        self.win_img = images["WinSoldier"]
        self.back_end_img = images["Back_End_Dialog"]
        self.restart_btn = Button(self.images["RestartBtn"], self.images["RestartBtn_Hovered"], self.images["RestartBtn_Clicking"], self.images["RestartBtn"], (367,570), self.restart_click)
        self.restart_text = Utils.getTextWithColor("Restart", 25, pygame.Color("white"))

        self.quit_btn = Button(self.images["QuitBtn"], self.images["QuitBtn_Hovered"], self.images["QuitBtn_Clicking"], self.images["QuitBtn"], (628, 570), self.quit_click)
        self.quit_text = Utils.getTextWithColor("Quit", 25, pygame.Color("white"))

        self.next_turn_btn = Button(self.images["EndTurnBtn"], self.images["EndTurnBtn_Hovered"], self.images["EndTurnBtn_Clicking"], self.images["EndTurnBtn_Desactivated"], (995,871), self.end_turn_click)
        self.next_turn_text = Utils.getTextWithColor("End Turn", 20, pygame.Color("white"))

        self.turns_img = images["Turns"]
        self.turns_text = Utils.getTextWithColor("Turns", 20, pygame.Color("white"))
        self.turns_counter_text = Utils.getTextWithColor(str(self.nb_turns), 20, pygame.Color("white"))

        temp_end_soldier_rect = self.win_img.get_rect()
        self.end_soldier_rect = pygame.Rect(560, 385, temp_end_soldier_rect.width, temp_end_soldier_rect.height)

        self.end_game_text = Utils.getTextWithColor("You Won !", 32, pygame.Color("white"))

        self.back_img = images["back_end_game"]

        self.is_game_ended = False

        self.sounds = self.load_sounds()

        self.generate_map()

    def generate_map(self, seed=None):
        map_generator = MapGenerator(self.shape, seed)

        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                boxType = map_generator.map[x][y]
                pos = (x * self.box_pixel_size, y * self.box_pixel_size)

                fn = lambda x=x, y=y: self.click_box(x, y)

                if boxType == BoxType.Grass:
                    boxe = Button(self.images["Box_grass"], self.images["Box_grass_hovered"], self.images["Box_grass_clicking"], self.images["Box_grass_desactivated"], pos, fn)
                elif boxType == BoxType.Water:
                    boxe = Button(self.images["Box_water"], self.images["Box_water_hovered"], self.images["Box_water_clicking"], self.images["Box_water"], pos, fn)
                    boxe.is_activated = False
                elif boxType == BoxType.Mountain:
                    boxe = Button(self.images["Box_mountain"], self.images["Box_mountain_hovered"], self.images["Box_mountain_clicking"], self.images["Box_mountain_desactivated"], pos, fn)

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
    
    def load_sounds(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_path, "assets")
        sounds_path = os.path.join(asset_path, "sounds")

        sounds_to_load = [f for f in os.listdir(sounds_path) if os.path.isfile(os.path.join(sounds_path, f))]

        sounds = {}

        for sound_to_load in sounds_to_load:
            name, extension = os.path.splitext(sound_to_load)

            if not ".mp3" in extension and not ".wav" in extension:
                continue

            sound = pygame.mixer.Sound(os.path.join(sounds_path,sound_to_load))
            sounds[name] = sound


        sounds["back_sound"].play(-1)
        sounds["back_sound"].set_volume(.1)

        Button.click_sound = sounds["click"]

        return sounds
  

    def create_back_img(self, screen_size):
        base_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_path, "assets")
        images_path = os.path.join(asset_path, "images")


        image_temp = Image.new(mode="RGBA", size=screen_size)

        for x in range(screen_size[0]):
            for y in range(screen_size[1]):
                image_temp.putpixel((x, y), (0, 0, 0, 100))

        image_temp.save( os.path.join(images_path, "back_end_game.png"))



    def play_end_sound(self):

        self.sounds["back_sound"].set_volume(0.1)

        if InteractionState.has_won:
            self.sounds["success"].play()
        else:
            self.sounds["loose"].play()

    def display_map_page(self):

        if not self.is_game_ended and InteractionState.is_ended:
            self.is_game_ended = True
            self.play_end_sound()
            



        self.screen.fill(self.black_color)

        for box in self.boxes:
            box.display(self.screen)


        for soldier_stats_ui in self.soldier_stats_1:
            soldier_stats_ui.display(self.screen)

        for soldier_stats_ui in self.soldier_stats_2:
            soldier_stats_ui.display(self.screen)

        pygame.draw.rect(self.screen, self.color_player, self.player_side_rect_1)
        pygame.draw.rect(self.screen, self.color_player, self.player_side_rect_2)

        self.screen.blit(self.turns_img, (998,12))
        self.screen.blit(self.turns_text, (1040,18))
        self.screen.blit(self.turns_counter_text, (1144,18))

        self.next_turn_btn.display(self.screen)
        self.screen.blit(self.next_turn_text, (1023, 875))
        self.screen.blit(self.title_game, (967 , 451))


    def display_end_page(self):
        self.screen.blit(self.back_img, (0 , 0))

        self.screen.blit(self.back_end_img, (338, 296))

        self.screen.blit(self.win_img, self.end_soldier_rect)
        self.screen.blit(self.end_game_text, (560,331))

        self.restart_btn.display(self.screen)
        self.quit_btn.display(self.screen)

        self.screen.blit(self.restart_text, (443,583))
        self.screen.blit(self.quit_text, (720, 583))


    def display(self, soldiers):
        player_1_soldier_img = pygame.image.load("C:\\Users\\moisan_l\\Documents\\Python\\bataille_naval_sans_bateaux_et_sans_mers\\assets\\images\\Soldier1.png")
        player_2_soldier_img = pygame.image.load("C:\\Users\\moisan_l\\Documents\\Python\\bataille_naval_sans_bateaux_et_sans_mers\\assets\\images\\Soldier2.png")
        player_2_soldier_img = pygame.transform.rotate(player_2_soldier_img, 180)
        self.display_map_page()
        
        player_1_soldiers = soldiers[0]
        player_2_soldiers = soldiers[1]
        for soldier in player_1_soldiers:
            soldier_to_display = Soldier(player_1_soldier_img, x=soldier[0], y=soldier[1])
            soldier_to_display.display(self.screen)

        for soldier in player_2_soldiers:
            soldier_to_display = Soldier(player_2_soldier_img, x=soldier[0], y=soldier[1])
            soldier_to_display.display(self.screen)

        if self.is_game_ended:
            self.display_end_page()

        pygame.display.flip()

    
    def check_interaction_map_page(self):
        for box in self.boxes:
            box.check_interaction()

        for soldier_stats_ui in self.soldier_stats_1:
            soldier_stats_ui.check_interaction()

        for soldier_stats_ui in self.soldier_stats_2:
            soldier_stats_ui.check_interaction()

        self.next_turn_btn.check_interaction()


    def check_interaction_end_page(self):
        self.restart_btn.check_interaction()
        self.quit_btn.check_interaction()
    
    def check_interaction(self):

        if self.is_game_ended:
            self.check_interaction_end_page()
        else:
            self.check_interaction_map_page()


        

    def click_box(self, x, y):
        print("Click box : x : ", x, ", y : " , y)

    
    def add_soldier_stats(self, player_id, soldier):

        is_player_one = (player_id == 0)

        start_pos_soldier_stat = (956, 78) if is_player_one else (956, 528)

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

    def restart_click(self):
        InteractionState.want_restart = True

    def quit_click(self):
        sys.exit()

    def end_turn_click(self):
        self.nb_turns += 1
        self.turns_counter_text = Utils.getTextWithColor(str(self.nb_turns), 20, pygame.Color("white"))

        self.next_turn_btn.is_activated = False

