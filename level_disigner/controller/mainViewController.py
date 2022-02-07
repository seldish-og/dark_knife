import ast
import base64
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QFrame
from model import TextureModel, TexturesModel, PainterModel, LevelModel, Cell
from res import textures
from view import MainView, Painter


class MainViewController():
    background = None

    def __init__(self):
        self.texturesModel = TexturesModel()

        self.mView = MainView(self, self.texturesModel)

        start = TextureModel(textures.textures["start"], "start")
        finish = TextureModel(textures.textures["finish"], "finish")
        enemy = TextureModel(textures.textures["enemy"], "enemy")

        self.texturesModel.addTexture(start, "start")
        self.texturesModel.addTexture(finish, "finish")
        self.texturesModel.addTexture(enemy, "enemy")

        self._canvasSize = {"height": None, "width": None}
        self._createCanvas()

        self.mView.show()

    def set_background(self):
        fname = \
        QFileDialog.getOpenFileName(self.mView, 'Выбрать картинку ', '', "(*.jpg *.png *.jpeg, *.JPEG *.JPG, *.PNG)")[0]
        if not fname:
            return

        with open(fname, "rb") as image2string:
            converted_string = base64.b64encode(image2string.read())
            self.painterModel.background = converted_string

    def onWidthChanged(self, text: str):
        if text.isdigit() and int(text) >= 0:
            self._canvasSize["width"] = int(text)
            self._createCanvas()

    def onHeightChanged(self, text: str):
        if text.isdigit() and int(text) >= 0:
            self._canvasSize["height"] = int(text)
            self._createCanvas()

    def onCellChanged(self, text: str):
        if text.isdigit() and int(text) > 0:
            Cell.side = int(text)
            self._createCanvas()

    def _createCanvas(self, textures_map=None):
        if not textures_map:
            textures_map = []
        self.painterModel = PainterModel(textures_map)
        self._chartilo = Painter(self.texturesModel, self.painterModel, self._canvasSize)
        self.mView.pasteCanvas(self._chartilo)

    def saveFileAs(self):
        textures = {}
        for texture in self.texturesModel.__dict__["textures"]:
            textures[texture] = self.texturesModel.__dict__["textures"][texture].__dict__["texture"]

        print(self.painterModel.background)
        content = LevelModel(Cell.side, textures, self.painterModel.textures_map, self.painterModel.background)

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self.mView, "QFileDialog.getSaveFileName()", "txt",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            file = open(fileName, 'w')
            file.write(str(content.__dict__))
            file.close()

    def openFile(self):
        self.texturesModel.deleteTextures()
        fname = QFileDialog.getOpenFileName(self.mView, 'Выбрать картинку ', '', "(*.txt)")[0]
        if not fname:
            return
        head, tail = os.path.split(fname)
        with open(fname, "r") as file:
            file = ast.literal_eval(file.read())
            textures = file["textures"]
            for key in textures:
                self.texturesModel.addTexture(TextureModel(textures[key], key), key)
            self.onCellChanged(str(file["cell_size"]))
            self._canvasSize = {"height": len(file["textures_map"]), "width": len(file["textures_map"][0])}
            self._createCanvas(file["textures_map"])
            if "background" in file:
                self.painterModel.background = file["background"]

    def setPainterBrash(self, obj, event):
        if isinstance(obj, QFrame) and event.type() == QtCore.QEvent.MouseButtonPress:
            Painter.textureBrash = obj.objectName()

    def onSpacePressed(self, event):
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_Space:
            self._chartilo.setIsSpacePressed(True)

    def onSpaceReleased(self, event):
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_Space:
            self._chartilo.setIsSpacePressed(False)

    def addNewTexture(self, fname=None):
        if not fname:
            fname = QFileDialog.getOpenFileName(self.mView, 'Выбрать картинку ', '',
                                                "(*.jpg *.png *.jpeg, *.JPEG *.JPG, *.PNG)")[0]
        if not fname:
            return
        head, tail = os.path.split(fname)
        with open(fname, "rb") as image2string:
            converted_string = base64.b64encode(image2string.read())

            texture = TextureModel(converted_string, tail)

            self.texturesModel.addTexture(texture)
