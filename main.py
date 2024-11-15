from PySide6.QtGui import Qt, QDoubleValidator
from PySide6.QtCore import Slot, QLocale
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QRadioButton, QLineEdit, QVBoxLayout, QGridLayout, QHBoxLayout, QListWidget, QListWidgetItem
from math import sqrt, log10, e
#(TODO) WHEN AN ELEMENT HAS MORE THAN ONE BEHAVIOUR - CREATE A SEPERATE CLASS FOR IT FOR EXAMPLE RADIO BUTTONS WITH radio_checked, change_radio ETC...
#(TODO) HOVER PIAST URL HINT
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
        print(local_url)

        with open(local_url, 'r') as csv_file:
            self.csv_file = csv_file.read()

        self.fileLoaded = True

class IntLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def return_float(self):
        return float(self.text())

class MainCalc(QDialog):
    LIGHT_SPEED = 299792458
    EFFECTIVE_EARTH_CURVATURE = 1/6480

    def __init__(self, parent=None):
        super(MainCalc, self).__init__(parent) #Qt.WindowType.FramelessWindowHint FOR FRAMELESS WINDOWS
        self.uploaded_distance = []
        self.active_radio = None
        self.POSITIVE_DOUBLE_VALIDATOR = QDoubleValidator(1, 1000000, 5)
        self.POSITIVE_DOUBLE_VALIDATOR.setLocale(QLocale.Language.English)
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
        save_button.setObjectName("save_button")

        remove_button = QPushButton()
        remove_button.setMaximumWidth(50)
        remove_button.setText("Usuń")
        remove_button.clicked.connect(self.list_remove)
        remove_button.setObjectName("remove_button")

        self.upload_button = DragDropBttn()
        self.upload_button.setText("Upuść CSV")
        self.upload_button.setObjectName("upload_button")
        self.upload_button.setAcceptDrops(True)
        self.upload_button.clicked.connect(self.drop_load)

        list_buttons_layout.addWidget(save_button)
        list_buttons_layout.addWidget(remove_button)

        wrapper_layout.addWidget(self.routes_list)
        wrapper_layout.addWidget(self.name_line)
        wrapper_layout.addLayout(list_buttons_layout)
        wrapper_layout.addWidget(self.upload_button)

        return wrapper_layout

    def drop_load(self):
        csv_file = []
        if self.upload_button.fileLoaded:
            self.dropped = self.upload_button.csv_file.split("\n")

            for row in self.dropped:
                if "Index" not in row:
                    csv_file.append(row.split(";"))

            for row in range(len(csv_file)-1):
                self.uploaded_distance.append([])
                for column in 3,4:
                    self.uploaded_distance[-1].append(float(csv_file[row][column].replace(',', '.')))

            '''max_val = [0,0]
            for row in self.uploaded_distance:
                if row[1] > max_val[1]:
                    max_val = row'''


            self.uploaded_distance.sort(reverse=True, key=self.sort_key)

            print(self.uploaded_distance)

    def sort_key(self, e):  #for sorting list by second col
        return e[1]

    def list_load(self) -> None:
        self.saved_data = []

        with open("saved.bull", "r") as data_file:
            for line in data_file:
                if line[0] != "\n":
                    self.saved_data.append(line.split(";"))

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
        self.betweeen = IntLineEdit()
        self.betweeen.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.betweeen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.betweeen.setMaximumWidth(100)

        between_layout.addSpacing(-5)
        between_layout.addWidget(self.betweeen)

        tx_h_title = QLabel("Wysokość anteny nadawczej [m]")
        rx_h_title = QLabel("Wysokość anteny odbiorczej [m]")

        txrx_label_layout.addWidget(tx_h_title)
        txrx_label_layout.addSpacing(115)
        txrx_label_layout.addWidget(rx_h_title)

        self.tx_h_line = IntLineEdit()
        self.tx_h_line.setMaximumWidth(100)
        self.tx_h_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tx_h_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        self.rx_h_line = IntLineEdit()
        self.rx_h_line.setMaximumWidth(100)
        self.rx_h_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rx_h_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        txrx_height_layout.addWidget(self.tx_h_line)
        txrx_height_layout.addSpacing(180)
        txrx_height_layout.addWidget(self.rx_h_line)

        dist_title = QLabel("Odległość wzniesień od Tx [km]")
        dist_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #(TODO) convert this d and h stuff to lists
        d1_label = QLabel("d1")
        self.d1_line = IntLineEdit()
        self.d1_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d1_line.setMaximumWidth(100)
        self.d1_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        d2_label = QLabel("d2")
        self.d2_line = IntLineEdit()
        self.d2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d2_line.setMaximumWidth(100)
        self.d2_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        d3_label = QLabel("d3")
        self.d3_line = IntLineEdit()
        self.d3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d3_line.setMaximumWidth(100)
        self.d3_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        d4_label = QLabel("d4")
        self.d4_line = IntLineEdit()
        self.d4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d4_line.setMaximumWidth(100)
        self.d4_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

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
        self.h1_line = IntLineEdit()
        self.h1_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h1_line.setMaximumWidth(100)
        self.h1_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        h2_label = QLabel("h2")
        self.h2_line = IntLineEdit()
        self.h2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h2_line.setMaximumWidth(100)
        self.h2_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        h3_label = QLabel("h3")
        self.h3_line = IntLineEdit()
        self.h3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h3_line.setMaximumWidth(100)
        self.h3_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

        h4_label = QLabel("h4")
        self.h4_line = IntLineEdit()
        self.h4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h4_line.setMaximumWidth(100)
        self.h4_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)

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

        self.other_radio = QRadioButton(self)
        self.freq_other = IntLineEdit()
        self.freq_other.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.freq_other.setPlaceholderText("Inna")
        self.freq_other.setMaximumWidth(50)

        radio_layout.addSpacing(50)
        radio_layout.addWidget(self.freq_radio_1)
        radio_layout.addWidget(self.freq_radio_2)
        radio_layout.addWidget(self.freq_radio_3)
        radio_layout.addWidget(self.freq_radio_4)
        radio_layout.addWidget(self.other_radio)
        radio_layout.addWidget(self.freq_other)

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
        vb_box = QHBoxLayout()
        luc_box = QHBoxLayout()
        loss_box = QHBoxLayout()

        results_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        calc_button = QPushButton()
        calc_button.setText("Oblicz")
        calc_button.setObjectName("calc_button")
        calc_button.clicked.connect(self.results_calculate)

        button_box.addWidget(calc_button)

        results_title = QLabel("Wyniki")
        results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        wavelength_title = QLabel("Długość fali [m]")
        wavelength_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wavelength_line = QLineEdit()
        self.wavelength_line.setReadOnly(True)
        self.wavelength_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # wavelength_line.setMaximumWidth(100)

        wavelength_box.addSpacing(115)
        wavelength_box.addWidget(wavelength_title)
        wavelength_box.addSpacing(160)
        wavelength_box.addWidget(self.wavelength_line)
        wavelength_box.addSpacing(85)

        stim_title = QLabel("Horyzont radiowy nadajnika [m/km]")
        self.stim_line = QLineEdit()
        self.stim_line.setReadOnly(True)
        self.stim_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stim_box.addSpacing(50)
        stim_box.addWidget(stim_title)
        stim_box.addSpacing(118)
        stim_box.addWidget(self.stim_line)
        stim_box.addSpacing(85)

        srim_title = QLabel("Horyzont radiowy odbiornika [m/km]")
        self.srim_line = QLineEdit()
        self.srim_line.setReadOnly(True)
        self.srim_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        srim_box.addSpacing(50)
        srim_box.addWidget(srim_title)
        srim_box.addSpacing(113)
        srim_box.addWidget(self.srim_line)
        srim_box.addSpacing(85)

        str_title = QLabel("Linia bezpośredniej widoczności [m/km]")
        self.str_line = QLineEdit()
        self.str_line.setReadOnly(True)
        self.str_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        str_box.addSpacing(50)
        str_box.addWidget(str_title)
        str_box.addSpacing(99)
        str_box.addWidget(self.str_line)
        str_box.addSpacing(85)

        db_title = QLabel("Odległość punktu Bullingtona od Tx [km]")
        self.db_line = QLineEdit()
        self.db_line.setReadOnly(True)
        self.db_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        db_box.addSpacing(50)
        db_box.addWidget(db_title)
        db_box.addSpacing(95)
        db_box.addWidget(self.db_line)
        db_box.addSpacing(85)

        vb_title = QLabel("Parametr v Fresnela-Kirchoffa")
        self.vb_line = QLineEdit()
        self.vb_line.setReadOnly(True)
        self.vb_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vb_box.addSpacing(80)
        vb_box.addWidget(vb_title)
        vb_box.addSpacing(127)
        vb_box.addWidget(self.vb_line)
        vb_box.addSpacing(85)

        luc_title = QLabel("Straty dyfrakcyjne wirtualnej przeszkody [dB]")
        self.luc_line = QLineEdit()
        self.luc_line.setReadOnly(True)
        self.luc_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        luc_box.addSpacing(50)
        luc_box.addWidget(luc_title)
        luc_box.addSpacing(78)
        luc_box.addWidget(self.luc_line)
        luc_box.addSpacing(85)

        loss_title = QLabel("Łączne straty dyfrakcyjne [dB]")
        self.loss_line = QLineEdit()
        self.loss_line.setReadOnly(True)
        self.loss_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        results_layout.addLayout(vb_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(luc_box)
        results_layout.addSpacing(15)
        results_layout.addLayout(loss_box)
        results_layout.addSpacing(15)

        return results_layout

    def layout_init(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.right_side_layout = QVBoxLayout(self)


    #def check_non_empty(self):
       #if (self.betweeen.text() != "" and self.tx_h_line.text() != "" and self.rx_h_line.text() != ""
            #and self.d1_line.text() != "" and self.d2_line.text() != "" and self.d3_line.text() != ""
            #and self.d4_line.text() != "" and self.h1_line.text() != "" and self.h2_line.text() != ""
            #and self.h3_line.text() != "" and self.h4_line.text() != "" and self.active_radio != None):
            #return True    ALTERNATIVE TO TRY CATCH LOL

    def results_calculate(self):
        #if self.check_non_empty():
        if self.active_radio == 1:
            f = 174 * pow(10,6)
        elif self.active_radio == 2:
            f = 880 * pow(10,6)
        elif self.active_radio == 3:
            f = 2500 * pow(10,6)
        elif self.active_radio == 4:
            f = 3500 * pow(10,6)

        try:

            self.wavelength = self.LIGHT_SPEED/f
            self.wavelength_line.setText(str(round(self.wavelength, 3)))

            s_tim1 = ((self.h1_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * self.d1_line.return_float() * (self.betweeen.return_float() - self.d1_line.return_float()) - self.tx_h_line.return_float())
                      / self.d1_line.return_float())

            s_tim2 = ((self.h2_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * self.d2_line.return_float() * (
                               self.betweeen.return_float() - self.d2_line.return_float()) - self.tx_h_line.return_float())
                      / self.d2_line.return_float())

            s_tim3 = ((self.h3_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * self.d3_line.return_float() * (
                               self.betweeen.return_float() - self.d3_line.return_float()) - self.tx_h_line.return_float())
                      / self.d3_line.return_float())

            s_tim4 = ((self.h4_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * self.d4_line.return_float() * (
                               self.betweeen.return_float() - self.d4_line.return_float()) - self.tx_h_line.return_float())
                      / self.d4_line.return_float())

            self.stim = round(max(s_tim1,s_tim2,s_tim3,s_tim4),3)

            self.stim_line.setText(str(self.stim))

            s_tr = round((self.rx_h_line.return_float() - self.tx_h_line.return_float()) / self.betweeen.return_float(), 3)
            self.str_line.setText(str(s_tr))

            rx_d1 = self.betweeen.return_float() - self.d1_line.return_float()
            rx_d2 = self.betweeen.return_float() - self.d2_line.return_float()
            rx_d3 = self.betweeen.return_float() - self.d3_line.return_float()
            rx_d4 = self.betweeen.return_float() - self.d4_line.return_float()

            s_rim1 = ((self.h1_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d1 *
                       (self.betweeen.return_float() - rx_d1) - self.rx_h_line.return_float())
                      / (self.betweeen.return_float() - rx_d1))

            s_rim2 = ((self.h2_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d2 *
                       (self.betweeen.return_float() - rx_d2) - self.rx_h_line.return_float())
                      / (self.betweeen.return_float() - rx_d2))

            s_rim3 = ((self.h3_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d3 *
                       (self.betweeen.return_float() - rx_d3) - self.rx_h_line.return_float())
                      / (self.betweeen.return_float() - rx_d3))

            s_rim4 = ((self.h4_line.return_float() +
                       500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d4 *
                       (self.betweeen.return_float() - rx_d4) - self.rx_h_line.return_float())
                      / (self.betweeen.return_float() - rx_d4))

            self.srim = round(max(s_rim1, s_rim2, s_rim3, s_rim4), 3)

            self.srim_line.setText(str(self.srim))

            self.db = ((self.rx_h_line.return_float() - self.tx_h_line.return_float() + self.srim * self.betweeen.return_float())
                  / (self.stim+self.srim))

            self.db_line.setText(str(round(self.db,3)))

            self.vb = (self.tx_h_line.return_float() + self.stim * self.db -
                       (self.tx_h_line.return_float() * (self.betweeen.return_float() - self.db) + self.rx_h_line.return_float() * self.db)
                       / self.betweeen.return_float()) * sqrt((0.002 * self.betweeen.return_float()) / (self.wavelength * self.db * (self.betweeen.return_float() - self.db)))

            self.vb_line.setText(str(round(self.vb,3)))

            self.luc = 6.9 + 20*log10(sqrt(pow(self.vb-0.1,2)+1)+self.vb-0.1)

            self.luc_line.setText(str(round(self.luc,3)))

            self.lb = self.luc+(1-pow(e,-self.luc/6))*(10 + 0.02 * self.betweeen.return_float())

            self.loss_line.setText(str(round(self.lb, 3)))

        except UnboundLocalError:
            print("Zaznacz częstotliwość")

        except ValueError:
            print("Wypełnij wszystkie pola")

        except ZeroDivisionError:
            print("Błąd dzielenia przez zero - dobierz inne wartości")

if __name__ == '__main__':
    app = QApplication()
    calc = MainCalc()
    calc.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    app.exec()