'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk
from tkinter import font  as tkfont

from .start import Start_page
from .people import People_page
from .stations import Stations_page
from .generate import Gen_page
from .help_ import Help_page


# Gerenciador da aplicação
class Application(tk.Tk):

	def __init__(self, db, gen):
		tk.Tk.__init__(self)
		self.data = db
		self.gen = gen

		# Fontes padrão
		self.font_title = tkfont.Font(family='Arial', size=12, weight="bold")
		self.font_body = tkfont.Font(family='Arial', size=10)

		self.title("Escala Gen - Gerador de Escala PEB/PEQ")

		# Tamanho da tela
		wsize = 500
		hsize = 400
		self.minsize(wsize, hsize)
		# self.maxsize(wsize, hsize)

		# Corpo da aplicação
		container = tk.Frame(self)
		container.pack()

		# Gerenciador de janelas
		self.frames = {}
		for func in (	Start_page, 
						People_page, 
						Stations_page, 
						Gen_page, 
						Help_page):
			
			page_name = func.__name__
			frame = func(parent=container, ctrl=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("Start_page")

	# Mostra a janela selecionada
	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()
