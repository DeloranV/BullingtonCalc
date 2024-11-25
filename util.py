class RadioController:
	def __init__(self, radio: list):
		self.radio_list = radio
		self.active_radio = None

	def radio_value(self):
		if self.active_radio == 1:
			return 174 * pow(10, 6)
		elif self.active_radio == 2:
			return 880 * pow(10, 6)
		elif self.active_radio == 3:
			return 2500 * pow(10, 6)
		else:
			return 3500 * pow(10, 6)

	def change_active_1(self):
		self.active_radio = 1

	def change_active_2(self):
		self.active_radio = 2

	def change_active_3(self):
		self.active_radio = 3

	def change_active_4(self):
		self.active_radio = 4

	def change_toggled_radio(self, radio) -> None:
		if radio == 1:
			self.radio_list[0].setChecked(True)

		if radio == 2:
			self.radio_list[1].setChecked(True)

		if radio == 3:
			self.radio_list[2].setChecked(True)

		if radio == 4:
			self.radio_list[3].setChecked(True)


class DragDropController:
	def __init__(self, drag_drop_bttn, line_edit_dict):
		self.drag_drop_bttn = drag_drop_bttn
		self.line_edit_dict = line_edit_dict

	def drop_load(self) -> None:
		loader = DataLoader(self.line_edit_dict)
		csv_file = []
		self.uploaded_distance = []
		if self.drag_drop_bttn.fileLoaded:
			self.dropped = self.drag_drop_bttn.csv_file.split("\n")

			for row in self.dropped:
				if "Index" not in row:
					csv_file.append(row.split(";"))

			for row in range(len(csv_file) - 1):
				self.uploaded_distance.append({})

				self.uploaded_distance[-1]["d"] = float(csv_file[row][3].replace(',', '.'))
				self.uploaded_distance[-1]["h"] = float(csv_file[row][4].replace(',', '.'))

		max_val = {"tx_h": self.uploaded_distance[0]["h"],
				   "rx_h": self.uploaded_distance[-1]["h"]}

		self.uploaded_distance.sort(reverse=True, key=self.sort_key)

		max_val["h1"] = self.uploaded_distance[0]["h"]
		max_val["d1"] = self.uploaded_distance[0]["d"]
		max_val["h2"] = self.uploaded_distance[1]["h"]
		max_val["d2"] = self.uploaded_distance[1]["d"]
		max_val["h3"] = self.uploaded_distance[2]["h"]
		max_val["d3"] = self.uploaded_distance[2]["d"]
		max_val["h4"] = self.uploaded_distance[3]["h"]
		max_val["d4"] = self.uploaded_distance[3]["d"]

				   #"between": "",


		loader.load_input_values(max_val)

		'''max_val = [0,0]
			for row in self.uploaded_distance:
				if row[1] > max_val[1]:
					max_val = row'''

	def sort_key(self, e) -> dict:  # for sorting list by second col
		return e["h"]


class DataPreparator:
	def __init__(self, line_edit_dict, radio_controller):
		self.line_edit_dict = line_edit_dict
		self.radio_controller = radio_controller

	def prepare_float(self) -> dict:
		freq = self.radio_controller.radio_value()
		ready_data = {"between": float(self.line_edit_dict["between"].text()),
					  "tx_h": float(self.line_edit_dict["tx_h"].text()),
					  "rx_h": float(self.line_edit_dict["rx_h"].text()),
					  "d1": float(self.line_edit_dict["d1"].text()),
					  "d2": float(self.line_edit_dict["d2"].text()),
					  "d3": float(self.line_edit_dict["d3"].text()),
					  "d4": float(self.line_edit_dict["d4"].text()),
					  "h1": float(self.line_edit_dict["h1"].text()),
					  "h2": float(self.line_edit_dict["h2"].text()),
					  "h3": float(self.line_edit_dict["h3"].text()),
					  "h4": float(self.line_edit_dict["h4"].text()),
					  "freq": float(freq)}

		return ready_data


class DataLoader:
	def __init__(self, line_edit_dict, radio_controller=None):
		self.line_edit_dict = line_edit_dict
		self.radio_controller = radio_controller

	def load_input_values(self, param_dict) -> None:
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

		if self.radio_controller is not None:
			self.radio_controller.change_toggled_radio(int(param_dict["active_radio"]))

	def load_output_values(self, param_dict) -> None:
		self.line_edit_dict["wavelength"].setText(str(param_dict["wavelength"]))
		self.line_edit_dict["stim"].setText(str(param_dict["stim"]))
		self.line_edit_dict["srim"].setText(str(param_dict["srim"]))
		self.line_edit_dict["los"].setText(str(param_dict["los"]))
		self.line_edit_dict["bull_p"].setText(str(param_dict["bull_p"]))
		self.line_edit_dict["v_param"].setText(str(param_dict["v_param"]))
		self.line_edit_dict["edge_l"].setText(str(param_dict["edge_l"]))
		self.line_edit_dict["total_l"].setText(str(param_dict["total_l"]))
