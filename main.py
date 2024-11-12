from PySide6.QtGui import Qt
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QRadioButton, QLineEdit, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QListWidgetItem

class MainCalc(QDialog):
    def __init__(self, parent=None):
        super(MainCalc, self).__init__(parent) #Qt.WindowType.FramelessWindowHint FOR FRAMELESS WINDOWS

        self.result_init()
        self.layout_init()

        self.right_side_layout.addLayout(self.input_init())

        self.right_side_layout.addLayout(self.freq_init())

        self.right_side_layout.addLayout(self.wavelength_init())

        self.right_side_layout.addLayout(self.result_init())


        self.main_layout.addLayout(self.list_init())
        self.main_layout.addSpacing(25)
        self.main_layout.addLayout(self.right_side_layout)

        self.setLayout(self.main_layout)


    def list_init(self) -> QVBoxLayout:
        wrapper_layout = QVBoxLayout()
        list_buttons_layout = QHBoxLayout()

        self.routes_list = QListWidget(self)
        self.routes_list.setMaximumWidth(100)
        self.routes_list.currentItemChanged.connect(self.item_load)

        self.list_load()

        save_button = QPushButton()
        save_button.setMaximumWidth(50)
        save_button.setText("Zapisz")
        save_button.clicked.connect(self.list_save)

        remove_button = QPushButton()
        remove_button.setMaximumWidth(50)
        remove_button.setText("Usuń")
        remove_button.clicked.connect(self.list_remove)

        upload_button = QPushButton()
        upload_button.setText("Z pliku CSV")

        list_buttons_layout.addWidget(save_button)
        list_buttons_layout.addWidget(remove_button)

        wrapper_layout.addWidget(self.routes_list)
        wrapper_layout.addLayout(list_buttons_layout)
        wrapper_layout.addWidget(upload_button)

        return wrapper_layout

    def list_load(self) -> None:
        self.saved_data = []
        with open("saved.txt", "r") as data_file:
            for line in data_file:
                self.saved_data.append(line.split(";"))

        for route in self.saved_data:
            self.routes_list.addItem(route[0])

    def item_load(self, item) -> None:
        for route in self.saved_data:
            if route[0] == item.text():
                self.d1_line.setText(route[1])
                self.d2_line.setText(route[2])
                self.d3_line.setText(route[3])
                self.d4_line.setText(route[4])

                self.h1_line.setText(route[5])
                self.h2_line.setText(route[6])
                self.h3_line.setText(route[7])
                self.h4_line.setText(route[8])



    @Slot()
    def list_remove(self) -> None:
        selected_item = self.routes_list.takeItem(self.routes_list.currentRow())
        saved_data = ""

        with open("saved.txt", 'r') as data_file:
            for line in data_file:
                if selected_item.text() not in line:
                    saved_data = saved_data + line

        with open("saved.txt", "w") as data_file:
            print(saved_data, file=data_file)

    @Slot()
    def list_save(self) -> None:
        name = str(input("Podaj nazwę"))
        self.routes_list.addItem(name)

        with open("saved.txt", 'a') as data_file:
            print(name,
                  self.d1_line.text(),
                  self.d2_line.text(),
                  self.d3_line.text(),
                  self.d4_line.text(),
                  self.h1_line.text(),
                  self.h2_line.text(),
                  self.h3_line.text(),
                  self.h4_line.text(), sep=";", file=data_file)

    def input_init(self) -> QHBoxLayout:
        title_layout = QVBoxLayout(self)
        dist_layout = QHBoxLayout(self)
        height_layout = QHBoxLayout(self)
        dist_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dist_title = QLabel()
        dist_title.setText("Odległość wzniesień")
        dist_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        d1_label = QLabel()
        d1_label.setText("d1")
        self.d1_line = QLineEdit()
        self.d1_line.setMaximumWidth(100)

        d2_label = QLabel()
        d2_label.setText("d2")
        self.d2_line = QLineEdit()
        self.d2_line.setMaximumWidth(100)

        d3_label = QLabel()
        d3_label.setText("d3")
        self.d3_line = QLineEdit()
        self.d3_line.setMaximumWidth(100)

        d4_label = QLabel()
        d4_label.setText("d4")
        self.d4_line = QLineEdit()
        self.d4_line.setMaximumWidth(100)

        dist_layout.addWidget(d1_label)
        dist_layout.addWidget(self.d1_line)
        dist_layout.addSpacing(15)

        dist_layout.addWidget(d2_label)
        dist_layout.addWidget(self.d2_line)
        dist_layout.addSpacing(15)

        dist_layout.addWidget(d3_label)
        dist_layout.addWidget(self.d3_line)
        dist_layout.addSpacing(15)

        dist_layout.addWidget(d4_label)
        dist_layout.addWidget(self.d4_line)
        dist_layout.addSpacing(15)

        height_title = QLabel()
        height_title.setText("Wysokość wzniesień")
        height_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h1_label = QLabel()
        h1_label.setText("h1")
        self.h1_line = QLineEdit()
        self.h1_line.setMaximumWidth(100)

        h2_label = QLabel()
        h2_label.setText("h2")
        self.h2_line = QLineEdit()
        self.h2_line.setMaximumWidth(100)

        h3_label = QLabel()
        h3_label.setText("h3")
        self.h3_line = QLineEdit()
        self.h3_line.setMaximumWidth(100)

        h4_label = QLabel()
        h4_label.setText("h4")
        self.h4_line = QLineEdit()
        self.h4_line.setMaximumWidth(100)

        height_layout.addWidget(h1_label)
        height_layout.addWidget(self.h1_line)
        height_layout.addSpacing(15)

        height_layout.addWidget(h2_label)
        height_layout.addWidget(self.h2_line)
        height_layout.addSpacing(15)

        height_layout.addWidget(h3_label)
        height_layout.addWidget(self.h3_line)
        height_layout.addSpacing(15)

        height_layout.addWidget(h4_label)
        height_layout.addWidget(self.h4_line)
        height_layout.addSpacing(15)

        title_layout.addWidget(dist_title)
        title_layout.addLayout(dist_layout)
        title_layout.addSpacing(15)
        title_layout.addWidget(height_title)
        title_layout.addLayout(height_layout)
        title_layout.addSpacing(15)

        return title_layout

    def freq_init(self) -> QVBoxLayout:
        label_layout = QVBoxLayout(self)
        radio_layout = QHBoxLayout(self)
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        freq_label = QLabel("Częstotliwość", self)
        freq_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        freq_radio_1 = QRadioButton("174 MHz", self)
        freq_radio_2 = QRadioButton("880 MHz", self)
        freq_radio_3 = QRadioButton("2500 MHz", self)
        freq_radio_4 = QRadioButton("3.5 GHz", self)

        freq_other = QLineEdit()
        freq_other_label = QLabel("Inna")
        freq_other.setMaximumWidth(50)

        radio_layout.addSpacing(50)
        radio_layout.addWidget(freq_radio_1)
        radio_layout.addWidget(freq_radio_2)
        radio_layout.addWidget(freq_radio_3)
        radio_layout.addWidget(freq_radio_4)
        radio_layout.addWidget(freq_other)
        radio_layout.addWidget(freq_other_label)

        label_layout.addWidget(freq_label)
        label_layout.addLayout(radio_layout)
        label_layout.addSpacing(15)

        return label_layout

    def wavelength_init(self) -> QHBoxLayout:
        wavelength_spacing_wrap = QVBoxLayout()
        wavelength_box = QHBoxLayout()

        wavelength_title = QLabel()
        wavelength_title.setText("Długość fali")
        wavelength_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wavelength_line = QLineEdit()
        self.wavelength_line.setObjectName("wavelength_line")
        #wavelength_line.setMaximumWidth(100)

        wavelength_box.addSpacing(125)
        wavelength_box.addWidget(wavelength_title)
        wavelength_box.addSpacing(100)
        wavelength_box.addWidget(self.wavelength_line)
        wavelength_box.addSpacing(85)

        wavelength_spacing_wrap.addLayout(wavelength_box)
        wavelength_spacing_wrap.addSpacing(15)

        return wavelength_spacing_wrap

    def result_init(self) -> QHBoxLayout:
        result_layout = QHBoxLayout()

        calc_button = QPushButton()
        calc_button.setMaximumWidth(100)
        calc_button.setText("Oblicz")

        result_line = QLineEdit()
        result_line.setMaximumWidth(100)

        result_layout.addWidget(calc_button)
        result_layout.addWidget(result_line)

        return result_layout

    def layout_init(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.right_side_layout = QVBoxLayout(self)



if __name__ == '__main__':
	app = QApplication()
	calc = MainCalc()
	calc.show()

	with open("style.qss", "r") as f:
		_style = f.read()
		app.setStyleSheet(_style)

	app.exec()