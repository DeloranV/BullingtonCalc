from PySide6.QtWidgets import QPushButton


class DragDropBttn(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fileLoaded = False

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        url = event.mimeData().urls()
        local_url = url[0].toLocalFile()

        with open(local_url, 'r') as csv_file:
            self.csv_file = csv_file.read()

        self.fileLoaded = True
