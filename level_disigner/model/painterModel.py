class PainterModel:
    def __init__(self, textures_map=[]) -> None:
        self.textures_map = textures_map
        self.background = None

        self.observers = []

    def setTexturesMap(self, map):
        self.textures_map = map
        self.notifyChanges()

    # textures
    def changeTexture(self, x, y, texture):
        self.textures_map[x][y] = texture
        self.notifyChanges()

    # observers
    def addObserver(self, observer) -> None:
        self.observers.append(observer)

    def removeObserver(self, observer) -> None:
        self.observers.remove(observer)

    def notifyChanges(self) -> None:
        for observer in self.observers:
            observer.change()
