import pygame


class Player(pygame.sprite.Sprite):
    HERO_WIDTH = 30
    HERO_HEIGHT = 50
    MOVE_SPEED = 3
    HERO_COLOR = pygame.Color("red")
    JUMP_POWER = 1
    JUMP_HEIGHT = 10
    GRAVITY_FORCE = 0.5

    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.HERO_WIDTH, self.HERO_HEIGHT))
        self.image.fill(self.HERO_COLOR)

        self.rect = pygame.Rect(x, y, self.HERO_WIDTH, self.HERO_HEIGHT)
        self.direction = pygame.math.Vector2(0, 0)
        self.isJump = False

        self.walk_count = 0

        self.last_direction = "right"

        self.is_moves = True

    def animate(self):
        if self.direction.x < 0:
            self.image = self.animations["left"][self.walk_count //
                                                 2 % len(self.animations["left"])]
            self.walk_count += 1
            self.last_direction = "left"
        elif self.direction.x > 0:
            self.image = self.animations["right"][self.walk_count //
                                                  2 % len(self.animations["right"])]
            self.walk_count += 1
            self.last_direction = "right"
        else:
            self.image = self.animations[self.last_direction][0]

    def set_player_animations(self, animations):
        self.animations = animations
        self.animate()

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def gravity(self) -> None:
        self.direction.y += self.GRAVITY_FORCE
        self.rect.y += self.direction.y

    def jump(self) -> None:
        if self.direction.y == 0 and not self.isJump:
            self.direction.y -= self.JUMP_HEIGHT * self.JUMP_POWER
            self.isJump = True
