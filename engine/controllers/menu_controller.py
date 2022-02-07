import pygame
import pygame_menu
from utils import History


class MenuController:
    def __init__(self, main_loop) -> None:
        # just a plug
        self._callable = self.show_main_menu
        self._reload_game = main_loop.notify_changes
        self._menu = None
        self.history = History()

        self._MENU_THEME = pygame_menu.themes.THEME_DARK

    def change(self, main_loop) -> None:
        self._screen = main_loop.screen
        self._MENU_WIDTH, self._MENU_HEIGHT = main_loop.WINDOW_WIDTH, main_loop.WINDOW_HEIGHT
        self._set_level_number = main_loop.set_level_number
        self.get_spent_time = main_loop.get_spent_time
        self.clear_time = main_loop.clear_time

    def show_history(self) -> None:
        if (self._menu):
            self._menu.disable()
        self._callable = self.show_history
        results = self.history.get_results()

        self._menu = pygame_menu.Menu("Dark Knife", self._MENU_WIDTH, self._MENU_HEIGHT, theme=self._MENU_THEME)

        self._menu.add.button("Main menu", self.show_main_menu)

        if (results):
            self._menu.add.label("Your record: " + self._find_best_record(results),
                                 align=pygame_menu.locals.ALIGN_CENTER)
            for result in results:
                if result:
                    self._menu.add.label(result[0], align=pygame_menu.locals.ALIGN_CENTER)

        self._menu.mainloop(self._screen)

    def _find_best_record(self, results) -> str:
        min = float('inf')
        best_result = ""
        for result in results:
            result = result[0]
            h, m, s, ms, = map(lambda x: int(x), result.split(":"))
            record_ms = (h * (60 * 60 * 1000) + m * (60 * 1000) + s * (1000) + ms)
            if record_ms < min:
                min = record_ms
                best_result = result
        return best_result

    def show_main_menu(self) -> None:
        if (self._menu):
            self._menu.disable()
        self._callable = self.show_main_menu

        self._menu = pygame_menu.Menu("Dark Knife", self._MENU_WIDTH, self._MENU_HEIGHT, theme=self._MENU_THEME)

        self._menu.add.button("Play", self.show_do_nothing)
        self._menu.add.button("History", self.show_history)
        self._menu.add.button("Quit", pygame_menu.events.EXIT)

        self._menu.mainloop(self._screen)

    def show_do_nothing(self) -> None:
        self._callable = lambda: True
        self._menu.disable()

    def show_death(self) -> None:
        if (self._menu):
            self._menu.disable()
        self._callable = self.show_death

        self._menu = pygame_menu.Menu("you are dead man", self._MENU_WIDTH, self._MENU_HEIGHT, theme=self._MENU_THEME)

        self._menu.add.label("Your score: " + self.get_spent_time(), align=pygame_menu.locals.ALIGN_CENTER)
        self._menu.add.button("Try again", self.show_do_nothing)
        self._menu.add.button("Main menu", self.show_main_menu)

        self._set_level_number(0)

        self._reload_game()
        self.clear_time()

        self._menu.mainloop(self._screen)

    def show_win(self) -> None:
        if (self._menu):
            self._menu.disable()
        self._callable = self.show_win

        self._menu = pygame_menu.Menu("you still alive congratulations!!!", self._MENU_WIDTH, self._MENU_HEIGHT,
                                      theme=self._MENU_THEME)

        self._menu.add.label("Your score: " + self.get_spent_time(), align=pygame_menu.locals.ALIGN_CENTER)
        self._menu.add.button("Play again", self.show_do_nothing)
        self._menu.add.button("Main menu", self.show_main_menu)

        self._set_level_number(0)

        self.history.append_result(self.get_spent_time())

        self.clear_time()

        self._reload_game()

        self._menu.mainloop(self._screen)

    def on_key_pressed(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.show_main_menu()

    def display(self, screen) -> None:
        self._callable()
        self.on_key_pressed()
