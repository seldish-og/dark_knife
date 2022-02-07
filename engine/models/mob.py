import random

import pygame

MOB_WIDTH = 40
MOB_HEIGHT = 60
MOB_SCALE = (MOB_WIDTH, MOB_HEIGHT)
MOB_COLOR = pygame.Color("black")


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        random_mob_image = random.choice(images)
        self.image = pygame.transform.scale(random_mob_image, MOB_SCALE)

        self.rect = pygame.Rect(x, y, MOB_WIDTH, MOB_HEIGHT)
        self.rect.bottom = y

    def draw(self, screen):
        picture = pygame.transform.scale(
            self.image, MOB_SCALE)
        rect = picture.get_rect()
        rect = rect.move(MOB_SCALE)
        screen.blit(picture, self.rect)

    def update(self):
        pass
