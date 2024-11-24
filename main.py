from view import MainCalc

from PySide6.QtWidgets import QApplication
# (TODO) WHEN AN ELEMENT HAS MORE THAN ONE BEHAVIOUR - CREATE A SEPERATE CLASS FOR IT FOR EXAMPLE RADIO BUTTONS WITH radio_checked, change_radio ETC...
# (TODO) HOVER PIAST URL HINT
# (TODO) TERRAIN PROFILE DISPLAY - GRAPH


if __name__ == '__main__':
    app = QApplication()
    calc = MainCalc()
    calc.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    app.exec()
