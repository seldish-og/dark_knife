import base64

from PyQt5 import QtCore, QtGui
from PyQt5 import sip
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget
from res import Ui_MainWindow as Template
from utility import MetaObserver, FinalMetaMainWindow


class MainView(QMainWindow, MetaObserver, metaclass=FinalMetaMainWindow):

    def __init__(self, controller, model):
        self._controller = controller
        super(MainView, self).__init__()
        self._template = Template()
        self._template.setupUi(self)
        self.showMaximized()

        self._model = model
        self._model.addObserver(self)

        self._template.header_add_button.setFocusPolicy(QtCore.Qt.NoFocus)

        self._template.actionsave_as.triggered.connect(self._controller.saveFileAs)
        self._template.actionopen.triggered.connect(self._controller.openFile)
        self._template.header_add_button.clicked.connect(self._controller.addNewTexture)
        self._template.set_background.clicked.connect(self._controller.set_background)
        self._template.line_edit__width.textChanged.connect(self._onWidthChanged)
        self._template.line_edit_height.textChanged.connect(self._onHeightChanged)
        self._template.line_edit_cell.textChanged.connect(self._onCellChanged)

    def _onWidthChanged(self, text: str):
        self._controller.onWidthChanged(text)

    def _onHeightChanged(self, text):
        self._controller.onHeightChanged(text)

    def _onCellChanged(self, text):
        self._controller.onCellChanged(text)

    def pasteCanvas(self, canvas):
        for child in self._template.grid_frame.children():
            sip.delete(child)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(canvas)
        self._template.grid_frame.setLayout(layout)

    def change(self):
        textures = self._model.textures

        for i in reversed(range(self._template.textures_append_here.layout().count())):
            self._template.textures_append_here.layout().itemAt(i).widget().setParent(None)

        for id in textures:
            frame = QFrame()
            frame.setObjectName(str(id))
            frame.installEventFilter(self)
            layout = QHBoxLayout()
            widget = QWidget()
            image = QLabel(widget)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(base64.b64decode(textures[id].texture))
            image.setPixmap(pixmap.scaled(50, 50))
            layout.addWidget(image)
            label = QLabel(textures[id].name)
            label.setStyleSheet("color: #fff;")
            layout.addWidget(label)
            frame.setLayout(layout)

            self._template.textures_append_here.layout().addWidget(frame)

    # ! global event listeners do not change
    def keyPressEvent(self, event):
        self._controller.onSpacePressed(event)
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        self._controller.onSpaceReleased(event)
        return super().keyReleaseEvent(event)

    def eventFilter(self, obj, event):
        self._controller.setPainterBrash(obj, event)
        return QWidget.eventFilter(self, obj, event)
