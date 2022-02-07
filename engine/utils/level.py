import base64
import io

import pygame


class Level:
    def __init__(self, level) -> None:
        self.level = level

        self.PLATFORM_WIDTH = 15
        self.PLATFORM_HEIGHT = 15
        self.PLATFORM_GEOMETRY = (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT)
        self.PLATFORM_COLOR = "#000000"

        self.textures_map = self.level["textures_map"]
        self.cell_size = self.level["cell_size"]

        self.used_textures = {}

    def get_background(self) -> str:
        if "background" in self.level and self.level["background"]:
            output = io.BytesIO(base64.b64decode(self.level["background"]))
            return pygame.image.load(output)

    def get_texture(self, id) -> pygame.image:
        try:
            output = io.BytesIO(base64.b64decode(self.level["textures"][id]))
            return pygame.image.load(output)

        except Exception as e:
            print(f"Textures with {id} not found because of {e}")

    def get_picture(self, texture_id):
        if texture_id not in self.used_textures:
            self.used_textures[texture_id] = self.get_texture(
                texture_id)

        return pygame.transform.scale(self.used_textures[texture_id], (self.cell_size, self.cell_size))

    def get_spawn_coordinates(self) -> list:
        spawn_platforms = []

        for y in range(len(self.textures_map)):
            for x in range(len(self.textures_map[y])):
                texture_id = self.textures_map[y][x]

                if (texture_id == ""):
                    continue

                if (texture_id == "start"):
                    spawn_platforms.append((x * self.cell_size, y * self.cell_size))

        return spawn_platforms

    def get_enemy_coordinates(self) -> list:
        enemy_platforms = []

        for y in range(len(self.textures_map)):
            for x in range(len(self.textures_map[y])):
                texture_id = self.textures_map[y][x]

                if (texture_id == ""):
                    continue

                if (texture_id == "enemy"):
                    enemy_platforms.append((x * self.cell_size, y * self.cell_size))

        return enemy_platforms

    def get_level_up_coordinates(self) -> list:
        level_up_coordinates = []
        for y in range(len(self.textures_map)):
            for x in range(len(self.textures_map[y])):
                texture_id = self.textures_map[y][x]

                if (texture_id == "finish"):
                    level_up_coordinates.append((x * self.cell_size, y * self.cell_size))
        return level_up_coordinates

    def get_platforms_coordinates(self) -> pygame.sprite.Group:
        self.platforms = []
        x = y = 0

        for y in range(len(self.textures_map)):
            for x in range(len(self.textures_map[y])):
                texture_id = self.textures_map[y][x]

                if (texture_id == ""):
                    continue

                self.platforms.append((x * self.cell_size, y * self.cell_size, texture_id))

        return self.platforms
