from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QBoxLayout, QFrame, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget
from res import Ui_MainWindow as Template
from .painter import Painter
from utility import MetaObserver, FinalMeta

import base64
from time import sleep

class MainView(QMainWindow, MetaObserver, metaclass=FinalMeta):

	def __init__(self, controller, model):
		self._controller = controller
		super(MainView, self).__init__()
		self.template = Template()
		self.template.setupUi(self)
		self.showMaximized()

		self._model = model
		self._model.addObserver(self)

		self.createCanvas()

		self.template.header_add_button.setFocusPolicy(QtCore.Qt.NoFocus)

		self.template.header_add_button.clicked.connect(self._controller.addNewTexture)

	def keyPressEvent(self, event):
		if event.isAutoRepeat():
			return
		if event.key()==QtCore.Qt.Key_Space:
			self._chartilo.setIsSpacePressed(True)

	def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
		if event.isAutoRepeat():
			return
		if event.key()==QtCore.Qt.Key_Space:
			self._chartilo.setIsSpacePressed(False)

	def createCanvas(self):
		self._chartilo = Painter(self._model)
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self._chartilo)
		self.template.grid_frame.setLayout(layout)

	def setPainterBrash(self, obj, event):
		if isinstance(obj, QFrame) and event.type() == QtCore.QEvent.MouseButtonPress:
			Painter.textureBrash = obj.objectName()

	def eventFilter(self, obj, event):
		self.setPainterBrash(obj, event)
		return QWidget.eventFilter(self, obj, event)

	def change(self):
		_model = self._model.textures

		for i in reversed(range(self.template.textures_append_here.layout().count())): 
			self.template.textures_append_here.layout().itemAt(i).widget().setParent(None)

		for id in _model:

			frame = QFrame()
			frame.setObjectName(str(id))
			frame.installEventFilter(self)
			layout = QHBoxLayout()
			widget = QWidget()
			image = QLabel(widget)
			pixmap = QtGui.QPixmap()
			pixmap.loadFromData(base64.b64decode(_model[id].texture))
			image.setPixmap(pixmap.scaled(50, 50))
			layout.addWidget(image)
			label = QLabel(_model[id].name)
			label.setStyleSheet("color: #fff;")
			layout.addWidget(label)
			frame.setLayout(layout)

			self.template.textures_append_here.layout().addWidget(frame)

