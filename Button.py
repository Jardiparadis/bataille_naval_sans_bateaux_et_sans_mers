import pygame
from InteractionState import InteractionState


class Button:


    def __init__(self, img, img_hovered, img_clicking, img_disabled, position, fn_click):

        self.img = img
        self.img_hovered = img_hovered
        self.img_clicking = img_clicking
        self.img_disabled = img_disabled

        self.fn_click = fn_click

        temp_img_rect = img.get_rect()
        self.img_rect = pygame.Rect(position[0],position[1], temp_img_rect.width, temp_img_rect.height)

        self.is_hovered = False
        self.is_clicking = False
        self.is_activated = True

    def display(self, screen):

        if not self.is_activated:
            screen.blit(self.img_disabled, self.img_rect)
        elif self.is_clicking:
            screen.blit(self.img_clicking, self.img_rect)
        elif self.is_hovered:
            screen.blit(self.img_hovered, self.img_rect)
        else:
            screen.blit(self.img, self.img_rect)


    def check_interaction(self):

        is_hovered = self.img_rect.collidepoint(InteractionState.mouse_pos)

        if self.is_hovered != is_hovered:
            self.is_hovered = is_hovered
            InteractionState.nb_hovered = (1 if is_hovered else -1)

            if not is_hovered:
                self.is_clicking = False

        if is_hovered and InteractionState.pressed_click:
            self.is_clicking = True

        if self.is_clicking and InteractionState.released_click:
            self.fn_click()
            self.is_clicking = False

        

