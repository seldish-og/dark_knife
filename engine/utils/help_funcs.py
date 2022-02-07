import os

import pygame


class Helper:
    def create_picture(self, picture_group, picture_name):
        abs_path = os.path.abspath(__file__)
        final_path = fr'''{abs_path[:-20]}\resources\images\{picture_group}\{picture_name}.png'''
        picture = pygame.image.load(final_path)

        return picture
