from src.view.view import MainCalc
from os import path

from PySide6.QtWidgets import QApplication
# (TODO) WHEN AN ELEMENT HAS MORE THAN ONE BEHAVIOUR - CREATE A SEPERATE CLASS FOR IT FOR EXAMPLE RADIO BUTTONS WITH radio_checked, change_radio ETC...
# (TODO) HOVER PIAST URL HINT
# (TODO) TERRAIN PROFILE DISPLAY - GRAPH


if __name__ == '__main__':
    app = QApplication()
    calc = MainCalc()
    calc.show()

    with open(path.join('src','static','style.qss'), "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    app.exec()
