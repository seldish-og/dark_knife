import pygame
import time


class ScoreController:
    def __init__(self, main_loop) -> None:
        self.start_time = None
        self.current_time = None

    def start(self):
        self.start_time = time.time() * 1000

    def current(self):
        self.current_time = time.time() * 1000

    def get_spent_time(self) -> str:
        difference = self.current_time - self.start_time
        hours, minutes, seconds, milliseconds = map(lambda x: int(x),
                                                    [(difference // (60 * 60 * 1000)), (difference // (60 * 1000)),
                                                     (difference // 1000), (float(str(difference % 1000)[0:2]))])
        return f"{hours}:{minutes}:{seconds}:{milliseconds}"

    def update_time(self) -> None:
        self.start_time += 1000

    def clear(self):
        self.start_time = None
        self.current_time = None

    def display(self, screen):
        if not self.start_time:
            self.start()
        self.current()
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(self.get_spent_time(), False, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, 120, 40))
        screen.blit(textsurface, (12, 10))
