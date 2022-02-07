from PyQt5.QtWidgets import QWidget
from utility import MetaObserver


class FinalMetaQWidget(type(QWidget), type(MetaObserver)):
    pass
