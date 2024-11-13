from PySide6.QtGui import Qt
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QRadioButton, QLineEdit, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QListWidgetItem
#(TODO) WHEN AN ELEMENT HAS MORE THAN ONE BEHAVIOUR - CREATE A SEPERATE CLASS FOR IT FOR EXAMPLE RADIO BUTTONS WITH radio_checked, change_radio ETC...
class MainCalc(QDialog):
    def __init__(self, parent=None):
        super(MainCalc, self).__init__(parent) #Qt.WindowType.FramelessWindowHint FOR FRAMELESS WINDOWS

        self.layout_init()

        self.setWindowTitle("Bullington Calculator")

        self.right_side_layout.addLayout(self.input_init())

        self.right_side_layout.addLayout(self.freq_init())

        self.right_side_layout.addLayout(self.results_init())

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

        self.name_line = QLineEdit()
        self.name_line.setMaximumWidth(100)
        self.name_line.setPlaceholderText("Wprowadź nazwę")

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
        wrapper_layout.addWidget(self.name_line)
        wrapper_layout.addLayout(list_buttons_layout)
        wrapper_layout.addWidget(upload_button)

        return wrapper_layout

    def list_load(self) -> None:
        self.saved_data = []

        with open("saved.bull", "r") as data_file:
            for line in data_file:
                self.saved_data.append(line.split(";"))
        print(self.routes_list.findItems("test3", Qt.MatchFlag.MatchExactly))
        for route in self.saved_data:
            self.routes_list.addItem(route[0])

    def item_load(self, item) -> None:
        for route in self.saved_data:
            if route[0] == item.text():
                self.betweeen.setText(route[1])

                self.tx_h_line.setText(route[2])
                self.rx_h_line.setText(route[3])

                self.d1_line.setText(route[4])
                self.d2_line.setText(route[5])
                self.d3_line.setText(route[6])
                self.d4_line.setText(route[7])

                self.h1_line.setText(route[8])
                self.h2_line.setText(route[9])
                self.h3_line.setText(route[10])
                self.h4_line.setText(route[11])

                self.change_active_radio(int(route[12]))

    @Slot()
    def list_remove(self) -> None:
        selected_item = self.routes_list.takeItem(self.routes_list.currentRow())
        saved_data = ""

        with open("saved.bull", 'r') as data_file:
            for line in data_file:
                if selected_item.text() not in line:
                    saved_data = saved_data + line

        with open("saved.bull", "w") as data_file:
            print(saved_data, file=data_file)

    @Slot()
    def list_save(self) -> None:
        name = self.name_line.text()
        self.routes_list.addItem(name)

        with open("saved.bull", 'a') as data_file:
            print(name,
                  self.betweeen.text(),
                  self.tx_h_line.text(),
                  self.rx_h_line.text(),
                  self.d1_line.text(),
                  self.d2_line.text(),
                  self.d3_line.text(),
                  self.d4_line.text(),
                  self.h1_line.text(),
                  self.h2_line.text(),
                  self.h3_line.text(),
                  self.h4_line.text(),
                  self.active_radio,
                  sep=";", file=data_file)

        self.saved_data.append([])
        self.saved_data[-1].append(name)
        self.saved_data[-1].append(self.betweeen.text())
        self.saved_data[-1].append(self.tx_h_line.text())
        self.saved_data[-1].append(self.rx_h_line.text())
        self.saved_data[-1].append(self.d1_line.text())
        self.saved_data[-1].append(self.d2_line.text())
        self.saved_data[-1].append(self.d3_line.text())
        self.saved_data[-1].append(self.d4_line.text())
        self.saved_data[-1].append(self.h1_line.text())
        self.saved_data[-1].append(self.h2_line.text())
        self.saved_data[-1].append(self.h3_line.text())
        self.saved_data[-1].append(self.h4_line.text())
        self.saved_data[-1].append(self.active_radio)


    def input_init(self) -> QHBoxLayout:
        title_layout = QVBoxLayout(self)
        between_layout = QHBoxLayout(self)
        txrx_label_layout = QHBoxLayout(self)
        txrx_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txrx_height_layout = QHBoxLayout(self)
        txrx_height_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dist_layout = QHBoxLayout(self)
        height_layout = QHBoxLayout(self)
        dist_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        between_title = QLabel("Dystans między antenami [km]")
        between_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.betweeen = QLineEdit()
        self.betweeen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.betweeen.setMaximumWidth(100)

        between_layout.addSpacing(-5)
        between_layout.addWidget(self.betweeen)

        tx_h_title = QLabel("Wysokość anteny nadawczej [m]")
        rx_h_title = QLabel("Wysokość anteny odbiorczej [m]")

        txrx_label_layout.addWidget(tx_h_title)
        txrx_label_layout.addSpacing(115)
        txrx_label_layout.addWidget(rx_h_title)

        self.tx_h_line = QLineEdit()
        self.tx_h_line.setMaximumWidth(100)
        self.tx_h_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rx_h_line = QLineEdit()
        self.rx_h_line.setMaximumWidth(100)
        self.rx_h_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        txrx_height_layout.addWidget(self.tx_h_line)
        txrx_height_layout.addSpacing(180)
        txrx_height_layout.addWidget(self.rx_h_line)

        dist_title = QLabel("Odległość wzniesień od Tx [km]")
        dist_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #(TODO) convert this d and h stuff to lists
        d1_label = QLabel("d1")
        self.d1_line = QLineEdit()
        self.d1_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d1_line.setMaximumWidth(100)

        d2_label = QLabel("d2")
        self.d2_line = QLineEdit()
        self.d2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d2_line.setMaximumWidth(100)

        d3_label = QLabel("d3")
        self.d3_line = QLineEdit()
        self.d3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d3_line.setMaximumWidth(100)

        d4_label = QLabel("d4")
        self.d4_line = QLineEdit()
        self.d4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        height_title = QLabel("Wysokość wzniesień [m]")
        height_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h1_label = QLabel("h1")
        self.h1_line = QLineEdit()
        self.h1_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h1_line.setMaximumWidth(100)

        h2_label = QLabel("h2")
        self.h2_line = QLineEdit()
        self.h2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h2_line.setMaximumWidth(100)

        h3_label = QLabel("h3")
        self.h3_line = QLineEdit()
        self.h3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h3_line.setMaximumWidth(100)

        h4_label = QLabel("h4")
        self.h4_line = QLineEdit()
        self.h4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        title_layout.addWidget(between_title)
        title_layout.addLayout(between_layout)
        title_layout.addSpacing(15)
        title_layout.addLayout(txrx_label_layout)
        title_layout.addLayout(txrx_height_layout)
        title_layout.addSpacing(15)
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

        self.freq_radio_1 = QRadioButton("174 MHz", self)
        self.freq_radio_2 = QRadioButton("880 MHz", self)
        self.freq_radio_3 = QRadioButton("2500 MHz", self)
        self.freq_radio_4 = QRadioButton("3.5 GHz", self)

        self.freq_radio_1.toggled.connect(self.radio_checked_1)
        self.freq_radio_2.toggled.connect(self.radio_checked_2)
        self.freq_radio_3.toggled.connect(self.radio_checked_3)
        self.freq_radio_4.toggled.connect(self.radio_checked_4)

        freq_other = QLineEdit()
        freq_other_label = QLabel("Inna")
        freq_other.setMaximumWidth(50)

        radio_layout.addSpacing(50)
        radio_layout.addWidget(self.freq_radio_1)
        radio_layout.addWidget(self.freq_radio_2)
        radio_layout.addWidget(self.freq_radio_3)
        radio_layout.addWidget(self.freq_radio_4)
        radio_layout.addWidget(freq_other)
        radio_layout.addWidget(freq_other_label)

        label_layout.addWidget(freq_label)
        label_layout.addLayout(radio_layout)
        label_layout.addSpacing(15)

        return label_layout

    def radio_checked_1(self, checked):
        if checked:
            self.active_radio = 1

    def radio_checked_2(self, checked):
        if checked:
            self.active_radio = 2

    def radio_checked_3(self, checked):
        if checked:
            self.active_radio = 3

    def radio_checked_4(self, checked):
        if checked:
            self.active_radio = 4

    def change_active_radio(self, radio):
        self.active_radio = radio
        if radio == 1:
            self.freq_radio_1.setChecked(True)

        if radio == 2:
            self.freq_radio_2.setChecked(True)

        if radio == 3:
            self.freq_radio_3.setChecked(True)

        if radio == 4:
            self.freq_radio_4.setChecked(True)

    def results_init(self) -> QVBoxLayout:
        results_layout = QVBoxLayout()
        button_box = QHBoxLayout()
        wavelength_box = QHBoxLayout()
        stim_box = QHBoxLayout()
        srim_box = QHBoxLayout()
        str_box = QHBoxLayout()
        db_box = QHBoxLayout()
        loss_box = QHBoxLayout()

        results_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        calc_button = QPushButton()
        calc_button.setText("Oblicz")
        calc_button.setObjectName("calc_button")

        button_box.addWidget(calc_button)

        results_title = QLabel("Wyniki")
        results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wavelength_title = QLabel("Długość fali [m]")
        wavelength_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wavelength_line = QLineEdit()
        # wavelength_line.setMaximumWidth(100)

        wavelength_box.addSpacing(115)
        wavelength_box.addWidget(wavelength_title)
        wavelength_box.addSpacing(160)
        wavelength_box.addWidget(self.wavelength_line)
        wavelength_box.addSpacing(85)

        stim_title = QLabel("Horyzont radiowy nadajnika [m/km]")
        self.stim_line = QLineEdit()
        stim_box.addSpacing(50)
        stim_box.addWidget(stim_title)
        stim_box.addSpacing(118)
        stim_box.addWidget(self.stim_line)
        stim_box.addSpacing(85)

        srim_title = QLabel("Horyzont radiowy odbiornika [m/km]")
        self.srim_line = QLineEdit()
        srim_box.addSpacing(50)
        srim_box.addWidget(srim_title)
        srim_box.addSpacing(113)
        srim_box.addWidget(self.srim_line)
        srim_box.addSpacing(85)

        str_title = QLabel("Linia bezpośredniej widoczności [m/km]")
        self.str_line = QLineEdit()
        str_box.addSpacing(50)
        str_box.addWidget(str_title)
        str_box.addSpacing(99)
        str_box.addWidget(self.str_line)
        str_box.addSpacing(85)

        db_title = QLabel("Odległość punktu Bullingtona od Tx [km]")
        self.db_line = QLineEdit()
        db_box.addSpacing(50)
        db_box.addWidget(db_title)
        db_box.addSpacing(95)
        db_box.addWidget(self.db_line)
        db_box.addSpacing(85)

        loss_title = QLabel("Łączne straty dyfrakcyjne [dB]")
        self.loss_line = QLineEdit()
        loss_box.addSpacing(85)
        loss_box.addWidget(loss_title)
        loss_box.addSpacing(120)
        loss_box.addWidget(self.loss_line)
        loss_box.addSpacing(85)

        results_layout.addLayout(button_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(wavelength_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(stim_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(srim_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(str_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(db_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(loss_box)
        results_layout.addSpacing(15)

        return results_layout

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