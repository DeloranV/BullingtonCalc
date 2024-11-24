from PySide6.QtCore import Slot
class RadioController:
	def __init__(self, radio: list):
		self.radio_list = radio
		self.active_radio = None

	def change_active_1(self):
		self.active_radio = 1

	def change_active_2(self):
		self.active_radio = 2

	def change_active_3(self):
		self.active_radio = 3

	def change_active_4(self):
		self.active_radio = 4

	def change_toggled_radio(self, radio):
		self.active_radio = radio
		if radio == 1:
			self.radio_list[0].setChecked(True)

		if radio == 2:
			self.radio_list[1].setChecked(True)

		if radio == 3:
			self.radio_list[2].setChecked(True)

		if radio == 4:
			self.radio_list[3].setChecked(True)

class DataPreparator():
	def __init__(self, widget_list):
		self.widget_list = widget_list

	def prepare_float(self):
		ready_data = {"between": float(self.widget_list[0].text()),
					  "tx_h": float(self.widget_list[1].text()),
					  "rx_h": float(self.widget_list[2].text()),
					  "h1": float(self.widget_list[3].text()),
					  "h2": float(self.widget_list[4].text()),
					  "h3": float(self.widget_list[5].text()),
					  "h4": float(self.widget_list[6].text()),
					  "d1": float(self.widget_list[7].text()),
					  "d2": float(self.widget_list[8].text()),
					  "d3": float(self.widget_list[9].text()),
					  "d4": float(self.widget_list[10].text()),}

		return ready_data

class DragDropController():
	def __init__(self, upload_button):
		self.upload_button = upload_button
		self.uploaded_distance = None
		self.dropped = None

	def drop_load(self):
		csv_file = []
		self.uploaded_distance = []
		if self.upload_button.fileLoaded:
			self.dropped = self.upload_button.csv_file.split("\n")

			for row in self.dropped:
				if "Index" not in row:
					csv_file.append(row.split(";"))

			for row in range(len(csv_file) - 1):
				self.uploaded_distance.append([])
				for column in 3, 4:
					self.uploaded_distance[-1].append(float(csv_file[row][column].replace(',', '.')))

		self.uploaded_distance.sort(reverse=True, key=self.sort_key)
		return self.uploaded_distance

			'''max_val = [0,0]
			for row in self.uploaded_distance:
				if row[1] > max_val[1]:
					max_val = row'''

	def sort_key(self, e):  # for sorting list by second col
		return e[1]

class LineEditLoader():
	def __init__(self, line_edit_dict):
		self.line_edit_dict = line_edit_dict

	def load_input_values(self, param_dict):
		self.line_edit_dict["between"].setText(str(param_dict["between"]))
		self.line_edit_dict["tx_h"].setText(str(param_dict["tx_h"]))
		self.line_edit_dict["rx_h"].setText(str(param_dict["rx_h"]))
		self.line_edit_dict["h1"].setText(str(param_dict["h1"]))
		self.line_edit_dict["h2"].setText(str(param_dict["h2"]))
		self.line_edit_dict["h3"].setText(str(param_dict["h3"]))
		self.line_edit_dict["h4"].setText(str(param_dict["h4"]))
		self.line_edit_dict["d1"].setText(str(param_dict["d1"]))
		self.line_edit_dict["d2"].setText(str(param_dict["d2"]))
		self.line_edit_dict["d3"].setText(str(param_dict["d3"]))
		self.line_edit_dict["d4"].setText(str(param_dict["d4"]))

		return self.line_edit_dict

	def load_output_values(self, param_dict):
		self.line_edit_dict["wavelength"].setText(str(param_dict["wavelength"]))
		self.line_edit_dict["stim"].setText(str(param_dict["stim"]))
		self.line_edit_dict["srim"].setText(str(param_dict["srim"]))
		self.line_edit_dict["los"].setText(str(param_dict["los"]))
		self.line_edit_dict["bull_p"].setText(str(param_dict["bull_p"]))
		self.line_edit_dict["v_param"].setText(str(param_dict["v_param"]))
		self.line_edit_dict["edge_l"].setText(str(param_dict["edge_l"]))
		self.line_edit_dict["total_l"].setText(str(param_dict["total_l"]))

		return self.line_edit_dict

class ItemListLoader():
	def __init__(self, list_widget):
		self.list_widget = list_widget

	def list_load(self) -> None:
		self.saved_data = []

		with open("saved.bull", "r") as data_file:
			for line in data_file:
				if line[0] != "\n":
					self.saved_data.append(line.split(";"))

		for route in self.saved_data:
			self.list_widget.addItem(route[0])

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


class FileOperations():
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