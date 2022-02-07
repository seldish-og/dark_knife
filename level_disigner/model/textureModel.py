class TextureModel:
    def __init__(self, texture, name=None, description=None) -> None:
        self.texture = texture
        self.name = name
        self.description = description

    def setTexture(self, texture):
        self.texture = texture

    def getTexture(self):
        return self.texture
