from PySide6.QtCore import Slot
from util import DataLoader
class FileOperations():
	def __init__(self, routes_list, line_dict, radio_controller):
		self.routes_list = routes_list
		self.line_dict = line_dict
		self.radio_controller = radio_controller
		self.line_edit_loader = DataLoader(line_dict, radio_controller)
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
		name = self.line_dict["save_name"].text()
		self.routes_list.addItem(name)

		with open("saved.bull", 'a') as data_file:
			print(name,
				  self.line_dict["between"].text(),
				  self.line_dict["tx_h"].text(),
				  self.line_dict["rx_h"].text(),
				  self.line_dict["d1"].text(),
				  self.line_dict["d2"].text(),
				  self.line_dict["d3"].text(),
				  self.line_dict["d4"].text(),
				  self.line_dict["h1"].text(),
				  self.line_dict["h2"].text(),
				  self.line_dict["h3"].text(),
				  self.line_dict["h4"].text(),
				  self.radio_controller.active_radio,
				  sep=";", file=data_file)

			self.saved_data.append([])
			self.saved_data[-1].append(name)
			self.saved_data[-1].append(self.line_dict["between"].text())
			self.saved_data[-1].append(self.line_dict["tx_h"].text())
			self.saved_data[-1].append(self.line_dict["rx_h"].text())
			self.saved_data[-1].append(self.line_dict["d1"].text())
			self.saved_data[-1].append(self.line_dict["d2"].text())
			self.saved_data[-1].append(self.line_dict["d3"].text())
			self.saved_data[-1].append(self.line_dict["d4"].text())
			self.saved_data[-1].append(self.line_dict["h1"].text())
			self.saved_data[-1].append(self.line_dict["h2"].text())
			self.saved_data[-1].append(self.line_dict["h3"].text())
			self.saved_data[-1].append(self.line_dict["h4"].text())
			self.saved_data[-1].append(self.radio_controller.active_radio)

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
				self.line_edit_loader.load_input_values({"between": route[1],
														 "tx_h": route[2],
														 "rx_h": route[3],
														 "d1": route[4],
														 "d2": route[5],
														 "d3": route[6],
														 "d4": route[7],
														 "h1": route[8],
														 "h2": route[9],
														 "h3": route[10],
														 "h4": route[11],
														"active_radio": route[12]})