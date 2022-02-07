import os
import re
import sys
from random import randrange

import pygame
from controllers import PlayerController, LevelController, KnifeController, MobsController, MenuController, \
    ResolutionController, ScoreController
from models import Platform, Player
from utils import Helper

BACKGROUND_COLOR = "#223759"


class Loop:

    def __init__(self) -> None:
        self.FREQUENCY = 75
        self.absolute_folder = re.sub(os.path.basename(
            __file__), "", os.path.abspath(__file__))

        self.helper = Helper()

        self.observers = []

        self.level_controller = LevelController(self)
        self.player_controller = PlayerController(self)
        self.knife_controller = KnifeController(self)
        self.mob_controller = MobsController(self)
        self.menu_controller = MenuController(self)
        self.resolution_controller = ResolutionController(self)
        self.score_controller = ScoreController(self)

        # ! обязательно должен быть первым, он должен подтягивать изменения первым, чтобы уже от него другие контроллеры все подтягивали
        self.add_observer(self)

        self.add_observer(self.player_controller)
        self.add_observer(self.knife_controller)
        self.add_observer(self.mob_controller)
        self.add_observer(self.menu_controller)
        self.add_observer(self.level_controller)

        # в нем вызывается метод notify_changes, который вызывает метод change у каждого объекта, которого мы хотим оповестить о загрузке нового уровня, для того чтобы он самостоятельно подтянул изменения
        self.level_controller.load_next_level()

        self.main()

    def add_observer(self, observer):
        self.observers.append(observer)

    def change(self, *args) -> None:

        # main_loop
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = pygame.display.Info(
        ).current_w, pygame.display.Info().current_h
        self.WINDOW_SCALE = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # level_controller
        self.cell_size = self.level_controller.cell_size
        self.platforms_coordinates = self.level_controller.platforms_coordinates
        self.spawn_coordinates: Platform = self.level_controller.spawn_coordinates
        self.set_level_number = self.level_controller.set_level_number

        self.LEVEL_WIDTH = self.level_controller.LEVEL_WIDTH
        self.LEVEL_HEIGHT = self.level_controller.LEVEL_HEIGHT

        # resolution_controller
        self.resolution_controller.change(self).apply_vertical_scale()

        # level_controller getting sprites
        self.level_controller.get_platforms_sprites()
        self.enemy_spawn_platforms = self.level_controller.enemy_spawn_platforms
        self.level_up_platforms = self.level_controller.level_up_platforms
        self.platforms = self.level_controller.platforms
        self.player_spawn_platforms: Platform = self.level_controller.player_spawn_platforms
        self.background = self.level_controller.background
        if not self.background:
            self.background = pygame.transform.scale(self.helper.create_picture(
                "background", "desert"), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        else:
            self.background = pygame.transform.scale(
                self.background, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # knifes_controller
        self.knifes = self.knife_controller.knifes

        # mobs_controller
        self.mobs = self.mob_controller.mobs

        # player_controller
        self.spawn_coordinate = self.player_spawn_platforms.sprites()[
            randrange(len(self.spawn_coordinates))]
        self.player: Player = self.player_controller.spawn_player(
            (self.spawn_coordinate.rect.left, self.spawn_coordinate.rect.top))
        self.player_controller.set_animation()

        # score controller
        self.get_spent_time = self.score_controller.get_spent_time
        self.clear_time = self.score_controller.clear
        self.update_time = self.score_controller.update_time

    def notify_changes(self) -> None:
        [observer.change(self) for observer in self.observers]

    def main(self) -> None:
        pygame.init()
        pygame.display.set_caption("Dark Knife")

        clock = pygame.time.Clock()

        while True:
            clock.tick(self.FREQUENCY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background, (0, 0))
            self.menu_controller.display(self.screen)
            self.knife_controller.display(self.screen)
            self.level_controller.display(self.screen)
            self.mob_controller.display(self.screen)
            self.player_controller.display(self.screen)
            self.score_controller.display(self.screen)

            pygame.display.update()


if __name__ == "__main__":
    run = Loop()

# Windows
# venv\Scripts\activate.bat
# python engine\test_loop.py

# Linux
# source venv/bin/activate
# python3 engine/test_loop.py
