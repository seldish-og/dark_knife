import pygame
from listeners import CollisionListener
from models import Knife, Platform, Player
from utils import Helper


class KnifeController:

    def __init__(self, main_loop) -> None:
        self.knifes = pygame.sprite.Group()
        self.knife_collision_listener = CollisionListener()
        self.timer = 50
        self.helper = Helper()

    def change(self, main_loop) -> None:
        self._platforms: pygame.sprite.Group = main_loop.platforms
        self._player: Player = main_loop.player
        for sprite in self.knifes:
            sprite.kill()

    def _return_knife_to_normal_horizontal_position(self, *args) -> None:
        knife: Knife
        platform: Platform
        platform, knife = args[0], args[1]
        if knife.direction.x < 0:
            knife.rect.left = platform.rect.right
        elif knife.direction.x > 0:
            knife.rect.right = platform.rect.left

    def knife_horizontal_movement_collision(self) -> None:
        for knife in self.knifes:
            knife: Knife
            knife.rect.x += knife.direction.x
            self.knife_collision_listener.on_collide(knife, self._platforms,
                                                     self._return_knife_to_normal_horizontal_position)

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        self.timer -= 1

        if keys[pygame.K_e]:
            if self.timer <= 0:
                x, y = (self._player.rect.x, self._player.rect.y)
                image = self.helper.create_picture("knife", "knife_right")
                self.knife = Knife((x + 25), (y + 20), 'left', image)
                self.knifes.add(self.knife)
                self.timer = 50

        if keys[pygame.K_q]:
            if self.timer <= 0:
                x, y = (self._player.rect.x, self._player.rect.y)
                image = self.helper.create_picture("knife", "knife_left")
                self.knife = Knife((x - 25), (y + 20), 'right', image)
                self.knifes.add(self.knife)
                self.timer = 50

    def display(self, screen) -> None:
        self.update()
        self.knifes.update()
        self.knifes.draw(screen)
        self.knife_horizontal_movement_collision()
