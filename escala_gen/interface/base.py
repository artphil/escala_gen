'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk

class Base_page(tk.Frame):
	
	def __init__(self, parent, ctrl):
		tk.Frame.__init__(self, parent)
		self.ctrl = ctrl
		self.btn_size = 20

		# Navbar
		self.navbar = tk.Frame(self)
		self.navbar.pack(side=tk.TOP)

		# Campo dos botões
		button_start = tk.Button(self.navbar)
		button_start["padx"] = self.btn_size
		button_start['text'] = "Home"
		button_start['command'] = lambda: self.ctrl.show_frame("Start_page")
		button_start.pack(side=tk.LEFT)

		button_gen = tk.Button(self.navbar)
		button_gen["padx"] = self.btn_size
		button_gen['text'] = "Gerar escala"
		button_gen['command'] = lambda: self.ctrl.show_frame("Gen_page")
		button_gen.pack(side=tk.LEFT)

		button_people = tk.Button(self.navbar)
		button_people["padx"] = self.btn_size
		button_people['text'] = "Pessoas"
		button_people['command'] = lambda: self.ctrl.show_frame("People_page")
		button_people.pack(side=tk.LEFT)

		button_stations = tk.Button(self.navbar)
		button_stations["padx"] = self.btn_size
		button_stations['text'] = "Estações"
		button_stations['command'] = lambda: self.ctrl.show_frame("Stations_page")
		button_stations.pack(side=tk.LEFT)

		button_help = tk.Button(self.navbar)
		button_help["padx"] = self.btn_size
		button_help['text'] = "Créditos"
		button_help['command'] = lambda: self.ctrl.show_frame("Help_page")
		button_help.pack(side=tk.LEFT)
