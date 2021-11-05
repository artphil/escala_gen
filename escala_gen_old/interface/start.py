'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk

from .base import Base_page

# Pagina de início
class Start_page(Base_page):
	
	def __init__(self, parent, ctrl):
		super().__init__(parent, ctrl)

		# Campos da janela
		# Titulo
		self.c_title = tk.Frame(self)
		self.c_title["padx"] = 20
		self.c_title["pady"] = 40
		self.c_title.pack()


		# Campo do titulo
		label = tk.Label(self.c_title)
		label['text'] = "Escala Gen" 
		label['font'] = self.ctrl.font_title
		label['pady'] = 20
		label.pack(side=tk.TOP)

