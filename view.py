from widgets import *
from util import  *
from files import *
from calculate import *

from PySide6.QtCore import QLocale, Slot, Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QPushButton, QLabel, \
	QRadioButton

class MainCalc(QDialog):

    def __init__(self, parent=None):
        super(MainCalc, self).__init__(parent) #Qt.WindowType.FramelessWindowHint FOR FRAMELESS WINDOWS
        self.POSITIVE_DOUBLE_VALIDATOR = QDoubleValidator(1, 1000000, 5)
        self.POSITIVE_DOUBLE_VALIDATOR.setLocale(QLocale.Language.English)
        self.layout_init()
        self.setWindowTitle("Bullington Calculator")
        self.line_dict = {}

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

        self.file_op = FileOperations(self.routes_list, self.line_dict, self.radio_controller) #will go out of scope and not work without "self"
        self.file_op.list_load()
        self.routes_list.currentItemChanged.connect(self.file_op.item_load)

        self.name_line = QLineEdit()
        self.name_line.setMaximumWidth(100)
        self.name_line.setPlaceholderText("Wprowadź nazwę")
        self.line_dict["save_name"] = self.name_line

        save_button = QPushButton()
        save_button.setMaximumWidth(50)
        save_button.setText("Zapisz")
        save_button.clicked.connect(self.file_op.list_save)
        save_button.setObjectName("save_button")

        remove_button = QPushButton()
        remove_button.setMaximumWidth(50)
        remove_button.setText("Usuń")
        remove_button.clicked.connect(self.file_op.list_remove)
        remove_button.setObjectName("remove_button")

        self.upload_button = DragDropBttn()
        self.upload_button.setText("Upuść CSV")
        self.upload_button.setObjectName("upload_button")
        self.upload_button.setAcceptDrops(True)
        #value = self.upload_button.clicked.connect(self.upload_button.drop_load)
        #print(value)

        list_buttons_layout.addWidget(save_button)
        list_buttons_layout.addWidget(remove_button)

        wrapper_layout.addWidget(self.routes_list)
        wrapper_layout.addWidget(self.name_line)
        wrapper_layout.addLayout(list_buttons_layout)
        wrapper_layout.addWidget(self.upload_button)

        return wrapper_layout

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
        self.betweeen.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.betweeen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.betweeen.setMaximumWidth(100)
        self.line_dict["between"] = self.betweeen

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
        self.tx_h_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["tx_h"] = self.tx_h_line

        self.rx_h_line = QLineEdit()
        self.rx_h_line.setMaximumWidth(100)
        self.rx_h_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rx_h_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["rx_h"] = self.rx_h_line

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
        self.d1_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["d1"] = self.d1_line

        d2_label = QLabel("d2")
        self.d2_line = QLineEdit()
        self.d2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d2_line.setMaximumWidth(100)
        self.d2_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["d2"] = self.d2_line

        d3_label = QLabel("d3")
        self.d3_line = QLineEdit()
        self.d3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d3_line.setMaximumWidth(100)
        self.d3_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["d3"] = self.d3_line

        d4_label = QLabel("d4")
        self.d4_line = QLineEdit()
        self.d4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d4_line.setMaximumWidth(100)
        self.d4_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["d4"] = self.d4_line

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
        self.h1_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["h1"] = self.h1_line

        h2_label = QLabel("h2")
        self.h2_line = QLineEdit()
        self.h2_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h2_line.setMaximumWidth(100)
        self.h2_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["h2"] = self.h2_line

        h3_label = QLabel("h3")
        self.h3_line = QLineEdit()
        self.h3_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h3_line.setMaximumWidth(100)
        self.h3_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["h3"] = self.h3_line

        h4_label = QLabel("h4")
        self.h4_line = QLineEdit()
        self.h4_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.h4_line.setMaximumWidth(100)
        self.h4_line.setValidator(self.POSITIVE_DOUBLE_VALIDATOR)
        self.line_dict["h4"] = self.h4_line

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

        radio_list = [self.freq_radio_1, self.freq_radio_2, self.freq_radio_3, self.freq_radio_4]
        self.radio_controller = RadioController(radio_list)

        self.freq_radio_1.toggled.connect(self.radio_controller.change_active_1)
        self.freq_radio_2.toggled.connect(self.radio_controller.change_active_2)
        self.freq_radio_3.toggled.connect(self.radio_controller.change_active_3)
        self.freq_radio_4.toggled.connect(self.radio_controller.change_active_4)

        radio_layout.addWidget(self.freq_radio_1)
        radio_layout.addSpacing(25)
        radio_layout.addWidget(self.freq_radio_2)
        radio_layout.addSpacing(25)
        radio_layout.addWidget(self.freq_radio_3)
        radio_layout.addSpacing(25)
        radio_layout.addWidget(self.freq_radio_4)

        label_layout.addWidget(freq_label)
        label_layout.addLayout(radio_layout)
        label_layout.addSpacing(15)

        return label_layout

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
        self.line_dict["wavelength"] = self.wavelength_line

        wavelength_box.addSpacing(115)
        wavelength_box.addWidget(wavelength_title)
        wavelength_box.addSpacing(160)
        wavelength_box.addWidget(self.wavelength_line)
        wavelength_box.addSpacing(85)

        stim_title = QLabel("Horyzont radiowy nadajnika [m/km]")
        self.stim_line = QLineEdit()
        self.stim_line.setReadOnly(True)
        self.stim_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_dict["stim"] = self.stim_line
        stim_box.addSpacing(50)
        stim_box.addWidget(stim_title)
        stim_box.addSpacing(118)
        stim_box.addWidget(self.stim_line)
        stim_box.addSpacing(85)

        srim_title = QLabel("Horyzont radiowy odbiornika [m/km]")
        self.srim_line = QLineEdit()
        self.srim_line.setReadOnly(True)
        self.srim_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_dict["srim"] = self.srim_line
        srim_box.addSpacing(50)
        srim_box.addWidget(srim_title)
        srim_box.addSpacing(113)
        srim_box.addWidget(self.srim_line)
        srim_box.addSpacing(85)

        str_title = QLabel("Linia bezpośredniej widoczności [m/km]")
        self.str_line = QLineEdit()
        self.str_line.setReadOnly(True)
        self.str_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_dict["los"] = self.str_line
        str_box.addSpacing(50)
        str_box.addWidget(str_title)
        str_box.addSpacing(99)
        str_box.addWidget(self.str_line)
        str_box.addSpacing(85)

        db_title = QLabel("Odległość punktu Bullingtona od Tx [km]")
        self.db_line = QLineEdit()
        self.db_line.setReadOnly(True)
        self.db_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_dict["bull_p"] = self.db_line
        db_box.addSpacing(50)
        db_box.addWidget(db_title)
        db_box.addSpacing(95)
        db_box.addWidget(self.db_line)
        db_box.addSpacing(85)

        vb_title = QLabel("Parametr v Fresnela-Kirchoffa")
        self.vb_line = QLineEdit()
        self.vb_line.setReadOnly(True)
        self.vb_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_dict["v_param"] = self.vb_line
        vb_box.addSpacing(80)
        vb_box.addWidget(vb_title)
        vb_box.addSpacing(127)
        vb_box.addWidget(self.vb_line)
        vb_box.addSpacing(85)

        luc_title = QLabel("Straty dyfrakcyjne wirtualnej przeszkody [dB]")
        self.luc_line = QLineEdit()
        self.luc_line.setReadOnly(True)
        self.luc_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_dict["edge_l"] = self.luc_line
        luc_box.addSpacing(50)
        luc_box.addWidget(luc_title)
        luc_box.addSpacing(78)
        luc_box.addWidget(self.luc_line)
        luc_box.addSpacing(85)

        loss_title = QLabel("Łączne straty dyfrakcyjne [dB]")
        self.loss_line = QLineEdit()
        self.loss_line.setReadOnly(True)
        self.loss_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_dict["total_l"] = self.loss_line
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


    def results_calculate(self):
        #if self.check_non_empty():
        '''if self.active_radio == 1:
            f = 174 * pow(10,6)
        elif self.active_radio == 2:
            f = 880 * pow(10,6)
        elif self.active_radio == 3:
            f = 2500 * pow(10,6)
        elif self.active_radio == 4:
            f = 3500 * pow(10,6)'''
        line_edit_ldr = DataLoader(self.line_dict, self.radio_controller) #py is pass by assignement - dicts and objects are mutable so will pass by reference
        data_prep = DataPreparator(self.line_dict, self.radio_controller)
        data = data_prep.prepare_float()
        calculation = Bullington(data)
        results = calculation.calculate_total_loss()
        line_edit_ldr.load_output_values(results)

