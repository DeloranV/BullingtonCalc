import numpy as np
from math import sqrt, log10, e

class Bullington():

	EFFECTIVE_EARTH_CURVATURE = 1 / 6480
	LIGHT_SPEED = 299792458

	def __init__(self, param_dict):
		self.d1 = param_dict["d1"]
		self.h1 = param_dict["h1"]

		self.d2 = param_dict["d2"]
		self.h2 = param_dict["h2"]

		self.d3 = param_dict["d3"]
		self.h3 = param_dict["h3"]

		self.d4 = param_dict["d4"]
		self.h4 = param_dict["h4"]

		self.between = param_dict["between"]

		self.tx_h = param_dict["tx_h"]
		self.rx_h = param_dict["rx_h"]
		self.freq = param_dict["freq"]

	def calculate_total_loss(self): #(TODO) TRY EXCEPT:
		wavelength = self.wavelength()

		stim_radio_horizon = self.stim_radio_horizon()
		srim_radio_horizon = None

		bull_point = None
		los = self.los()

		if stim_radio_horizon >= los:
			srim_radio_horizon = self.nlos_srim_radio_horizon()
			bull_point = self.nlos_bull_point(srim_radio_horizon, stim_radio_horizon)
			v = self.nlos_v_param(wavelength, bull_point, stim_radio_horizon)
			edge_loss = self.edge_loss(v)

		else:
			v = self.los_v_param(wavelength)
			edge_loss = self.edge_loss(v)

		total_loss = self.total_loss(edge_loss)

		result_dict = {"wavelength": float(wavelength),
					  "stim": float(stim_radio_horizon),
					  "srim": float(srim_radio_horizon),
					  "los": float(los),
					  "bull_p": float(bull_point),
					  "v_param": float(v),
					  "edge_l": float(edge_loss),
					  "total_l": float(total_loss)}

		return result_dict

	def wavelength(self):
		wavelength = self.LIGHT_SPEED / self.freq

		return wavelength

	def stim_radio_horizon(self):
		s_tim1 = ((self.h1 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d1 * (self.between - self.d1) - self.tx_h) / self.d1)
		s_tim2 = ((self.h2 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d2 * (self.between - self.d2) - self.tx_h) / self.d2)
		s_tim3 = ((self.h3 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d3 * (self.between - self.d3) - self.tx_h) / self.d3)
		s_tim4 = ((self.h4 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d4 * (self.between - self.d4) - self.tx_h) / self.d4)

		stim = np.maximum(s_tim1, s_tim2, s_tim3, s_tim4)

		return stim

	def los(self):
		s_tr = self.rx_h - self.tx_h / self.between

		return s_tr

	def nlos_srim_radio_horizon(self):

		rx_d1 = self.between - self.d1
		rx_d2 = self.between - self.d2
		rx_d3 = self.between - self.d3
		rx_d4 = self.between - self.d4

		s_rim1 = ((self.h1 + 500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d1 * (self.between - rx_d1) - self.rx_h) / (self.between - rx_d1))
		s_rim2 = ((self.h2 + 500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d2 * (self.between - rx_d2) - self.rx_h) / (self.between - rx_d2))
		s_rim3 = ((self.h3 + 500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d3 * (self.between - rx_d3) - self.rx_h) / (self.between - rx_d3))
		s_rim4 = ((self.h4 + 500 * self.EFFECTIVE_EARTH_CURVATURE * rx_d4 * (self.between - rx_d4) - self.rx_h) / (self.between - rx_d4))

		srim = np.maximum(s_rim1, s_rim2, s_rim3, s_rim4)

		return srim

	def nlos_bull_point(self, srim, stim):
		db = ((self.rx_h - self.tx_h + srim * self.between) / (stim + srim))
		# db = np.linspace(1, 79)
		return db

	def nlos_v_param(self, wavelength, db, stim):
		vb = ((self.tx_h + stim * db - (self.tx_h * (self.between - db) + self.rx_h * db) / self.between) *
			  np.sqrt((0.002 * self.between) / (wavelength * db * (self.between - db))))
		return vb

	def los_v_param(self, wavelength):
		vb_1 = ((self.h1 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d1 * (self.between - self.d1)
				 - (self.tx_h * (self.between - self.d1) + self.rx_h * self.d1) / self.between)
				* sqrt((0.002 * self.between) / (wavelength * self.d1 * (self.between - self.d1))))

		vb_2 = ((self.h2 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d2 * (self.between - self.d2)
				 - (self.tx_h * (self.between - self.d2) + self.rx_h * self.d2) / self.between)
				* sqrt((0.002 * self.between) / (wavelength * self.d2 * (self.between - self.d2))))

		vb_3 = ((self.h3 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d3 * (self.between - self.d3)
				 - (self.tx_h * (self.between - self.d3) + self.rx_h * self.d3) / self.between)
				* sqrt((0.002 * self.between) / (wavelength * self.d3 * (self.between - self.d3))))

		vb_4 = ((self.h4 + 500 * self.EFFECTIVE_EARTH_CURVATURE * self.d4 * (self.between - self.d4)
				 - (self.tx_h * (self.between - self.d4) + self.rx_h * self.d4) / self.between)
				* sqrt((0.002 * self.between) / (wavelength * self.d4 * (self.between - self.d4))))

		v_max = np.maximum(vb_1, vb_2, vb_3, vb_4)

		return v_max

	def edge_loss(self, vb):
		luc = 6.9 + 20 * np.log10(np.sqrt(pow(vb - 0.1, 2) + 1) + vb - 0.1)
		return luc

	def total_loss(self, luc):
		lb = luc + (1 - pow(e, -luc / 6)) * (10 + 0.02 * self.between)
		return lb