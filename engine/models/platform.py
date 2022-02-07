import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, rect, image=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = image

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)
