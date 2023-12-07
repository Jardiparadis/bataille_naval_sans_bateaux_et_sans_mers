import pygame
from Utils import Utils

class SoldierStatsUI:


    def __init__(self, soldier, soldier_img, back_img, back_desactivated_img, hearth_btn, gun_btn, pos):

        self.soldier = soldier
        self.soldier_img = soldier_img
        self.back_img = back_img
        self.back_desactivated_img = back_desactivated_img
        self.hearth_btn = hearth_btn
        self.gun_btn = gun_btn

        self.is_soldier_dead = False

        self.nb_life_text = Utils.getTextWithColor(str(1), 20, pygame.Color("white"))
        self.nb_gun_text = Utils.getTextWithColor(str(1), 20, pygame.Color("white"))
        self.pos_life_text = (pos[0] + 98, pos[1] + 7)
        self.pos_gun_text = (pos[0] + 206, pos[1] + 7)

        temp_soldier_rect = soldier_img.get_rect()
        self.soldier_rect = pygame.Rect(pos[0] + 6, pos[1] + 5, temp_soldier_rect.width, temp_soldier_rect.height)

        temp_back_rect = back_img.get_rect()
        self.back_rect = pygame.Rect(pos[0], pos[1], temp_back_rect.width, temp_back_rect.height)

        hearth_btn.fn_click = lambda: self.add_life()
        gun_btn.fn_click = lambda: self.add_gun()



    def display(self, screen):

        if self.is_soldier_dead:
            screen.blit(self.back_desactivated_img, self.back_rect)
        else:
            screen.blit(self.back_img, self.back_rect)

        screen.blit(self.soldier_img, self.soldier_rect)
        self.hearth_btn.display(screen)
        self.gun_btn.display(screen)

        screen.blit(self.nb_life_text, self.pos_life_text)
        screen.blit(self.nb_gun_text, self.pos_gun_text)

    def check_interaction(self):
        self.hearth_btn.check_interaction()
        self.gun_btn.check_interaction()

    def add_life(self):
        print("Add life")
        self.is_soldier_dead = True


    def add_gun(self):
        print("Add gun")