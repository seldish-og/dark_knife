from json.tool import main
import pygame
from pygame.sprite import Sprite
from models import Mob
from utils import Helper
from listeners import CollisionListener


class MobsController:
    def __init__(self, main_loop) -> None:
        self.collide_listener = CollisionListener()
        self.mobs = pygame.sprite.Group()
        self.helper = Helper()

    def change(self, main_loop):
        self.enemy_spawn_platforms = main_loop.enemy_spawn_platforms
        self.knifes = main_loop.knifes
        self.update_time = main_loop.update_time
        for mob in self.mobs:
            mob.kill()
        self.add_mobs()

    def add_mobs(self):
        images = []
        for numb in range(3):
            mob_image = self.helper.create_picture("enemy", f'enemy_{numb}')
            images.append(mob_image)

        for i in self.enemy_spawn_platforms:
            self.mobs.add(Mob(i.rect.x, i.rect.y, images))

    def display(self, screen):
        self.mobs.draw(screen)
        for knife in self.knifes:
            self.collide_listener.on_collide(knife, self.mobs, self.kill_mob)

    def kill_mob(self, *args):
        enemy: Sprite
        knife: Sprite
        enemy, knife = args[0], args[1]
        enemy.kill()
        knife.kill()
        self.update_time()
