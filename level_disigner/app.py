import sys
from PyQt5.QtWidgets import QApplication
from controller import MainViewController


def main():
    app = QApplication(sys.argv)

    MainViewController()

    app.exec()


def start():
    if __name__ == '__main__':
        sys.exit(main())


start()
