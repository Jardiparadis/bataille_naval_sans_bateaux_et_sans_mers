


import pygame
import os

class Utils:

    asset_path = None
    FONT_NAME = "Exo2-Regular.ttf"
 
    title_color = pygame.Color("#C9C9C9")

    @staticmethod
    def getFont(size):
        return pygame.font.Font(os.path.join(Utils.asset_path, "fonts", "Exo_2", "static", Utils.FONT_NAME), size)


    @staticmethod
    def getText(text, size):
        return Utils.getFont(size).render(text, True, Utils.title_color)

    @staticmethod
    def getTextWithColor(text, size, color):
        return Utils.getFont(size).render(text, True, color)