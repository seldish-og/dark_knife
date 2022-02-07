import base64

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QBrush, QPainter, QPen
from PyQt5.QtWidgets import QWidget
from model import Cell
from model import TextureModel, TexturesModel, PainterModel
from utility import MetaObserver, FinalMetaQWidget


class Painter(QWidget, MetaObserver, metaclass=FinalMetaQWidget):
    textureBrash: TextureModel = None

    XOffset = 0
    YOffset = 0
    isSpacePressed = False
    isLeftMouseButtonPressed = False
    isRightMouseButtonPressed = False

    decodedPictures = {}

    def __init__(self, texturesModel, mapModel, size) -> None:
        self._texturesModel: TexturesModel = texturesModel
        self._mapModel: PainterModel = mapModel
        self._mapModel.addObserver(self)
        self._size = size
        super(Painter, self).__init__()

    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)

        width = self.painter.device().width()
        height = self.painter.device().height()

        height_amount = height // Cell.side
        width_amount = width // Cell.side

        if not self._size["height"]:
            self._size["height"] = height_amount
        if not self._size["width"]:
            self._size["width"] = width_amount

        self.margin_horizontal = int(
            (width - (Cell.side * self._size["width"])) / 2)
        self.marging_vertical = int(
            (height - (Cell.side * self._size["height"])) / 2)

        self.draw_background()

        if (len(self._mapModel.textures_map) == 0):
            for y in range((self._size["height"])):
                self._mapModel.textures_map.append([])
                for x in range((self._size["width"])):
                    self._mapModel.textures_map[y].append("")

        self.drawGrid(self._mapModel.textures_map)

        self.painter.end()

    def draw_background(self):
        if self._mapModel.background:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(base64.b64decode(self._mapModel.background))
            self.painter.drawPixmap(self.rect(), pixmap)

    def set_background(self, image):
        self._mapModel.background = image

    def setIsSpacePressed(self, value):
        Painter.isSpacePressed = value

    def drawGrid(self, grid):

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if (grid[y][x] == ""):
                    self.painter.setPen(QPen())
                    self.painter.setBrush(QBrush())
                    self.painter.drawRect(x * Cell.side + self.margin_horizontal, y * Cell.side + self.marging_vertical,
                                          Cell.side, Cell.side)
                else:
                    if (grid[y][x] not in Painter.decodedPictures):
                        pixmap = QtGui.QPixmap()
                        pixmap.loadFromData(base64.b64decode(self._texturesModel.textures[grid[y][x]].texture))
                        Painter.decodedPictures[grid[y][x]] = pixmap
                    else:
                        pixmap = Painter.decodedPictures[grid[y][x]]
                    rect = QRect(x * Cell.side + self.margin_horizontal, y * Cell.side + self.marging_vertical,
                                 Cell.side, Cell.side)
                    self.painter.drawPixmap(rect, pixmap)

    def getCurrentPosition(self, event) -> dict:
        return {"x": event.x(), "y": event.y()}

    def mousePressEvent(self, event) -> None:
        self.mouseStartPosition = self.getCurrentPosition(event)
        self.previousMousePosition = self.mouseStartPosition

        if event.button() == QtCore.Qt.LeftButton:
            Painter.isLeftMouseButtonPressed = True

        if event.button() == QtCore.Qt.RightButton:
            Painter.isRightMouseButtonPressed = True

        self.drawTextures(event)
        self.deleteTextures(event)

    def movement(self, event):
        if (not Painter.isSpacePressed):
            return
        mouseCurrentPosition = self.getCurrentPosition(event)

        velocity = 1

        if abs(self.mouseStartPosition["x"] - mouseCurrentPosition["x"]) % Cell.side == 0:
            # mouse right drag
            if self.mouseStartPosition["x"] < mouseCurrentPosition["x"] and not Painter.XOffset <= 0:
                Painter.XOffset -= velocity

            # mouse left drag
            if self.mouseStartPosition["x"] > mouseCurrentPosition["x"]:
                Painter.XOffset += velocity

            self.mouseStartPosition["x"] = mouseCurrentPosition["x"]

        if abs(self.mouseStartPosition["y"] - mouseCurrentPosition["y"]) % Cell.side == 0:
            # mouse up drag
            if self.mouseStartPosition["y"] < mouseCurrentPosition["y"] and not Painter.YOffset <= 0:
                Painter.YOffset -= velocity

            # mouse down drag
            if self.mouseStartPosition["y"] > mouseCurrentPosition["y"]:
                Painter.YOffset += velocity

            self.mouseStartPosition["y"] = mouseCurrentPosition["y"]

        self.previousMousePosition = mouseCurrentPosition

    def deleteTextures(self, event):
        if (self.isSpacePressed or (not Painter.isRightMouseButtonPressed)) and Painter.textureBrash != None:
            return
        currentPosition = self.getCurrentPosition(event)
        for y in range(len(self._mapModel.textures_map)):
            for x in range(len(self._mapModel.textures_map[y])):
                cell_x = x * Cell.side + self.margin_horizontal
                cell_y = y * Cell.side + self.marging_vertical
                if cell_x <= currentPosition["x"] <= cell_x + Cell.side and cell_y <= currentPosition[
                    "y"] <= cell_y + Cell.side:
                    self._mapModel.textures_map[y][x] = ""
        self._mapModel.notifyChanges()

    def drawTextures(self, event):
        if (not Painter.textureBrash or self.isSpacePressed or (not Painter.isLeftMouseButtonPressed)):
            return
        currentPosition = self.getCurrentPosition(event)

        for y in range(len(self._mapModel.textures_map)):
            for x in range(len(self._mapModel.textures_map[y])):
                cell_x = x * Cell.side + self.margin_horizontal
                cell_y = y * Cell.side + self.marging_vertical
                if cell_x <= currentPosition["x"] <= cell_x + Cell.side and cell_y <= currentPosition[
                    "y"] <= cell_y + Cell.side:
                    self._mapModel.textures_map[y][x] = Painter.textureBrash

        self._mapModel.notifyChanges()

    def mouseMoveEvent(self, event) -> None:
        self.movement(event)
        self.drawTextures(event)
        self.deleteTextures(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            Painter.isLeftMouseButtonPressed = False
        if event.button() == QtCore.Qt.RightButton:
            Painter.isRightMouseButtonPressed = False

    def change(self):
        self.update()
