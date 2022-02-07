import pygame

KNIFE_WIDTH = 50
KNIFE_HEIGHT = 15
KNIFE_SCALE = (KNIFE_WIDTH, KNIFE_HEIGHT)
KNIFE_COLOR = pygame.Color("black")


class Knife(pygame.sprite.Sprite):
    def __init__(self, x, y, marker, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, KNIFE_SCALE)
        self.rect = pygame.Rect(x, y, KNIFE_WIDTH, KNIFE_HEIGHT)

        self.direction = pygame.math.Vector2(0, 0)
        self.marker = marker

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.marker == "left":
            self.direction.x = 8
            self.rect.x += self.direction.x
        if self.marker == "right":
            self.direction.x = -8
            self.rect.x += self.direction.x
