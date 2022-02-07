class LevelModel:
    def __init__(self, cell_size, textures, texturesMap, background=None) -> None:
        self.cell_size = cell_size
        self.textures = textures
        self.textures_map = texturesMap
        self.background = background
