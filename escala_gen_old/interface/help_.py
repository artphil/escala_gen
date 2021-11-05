'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk

from .base import Base_page

class Help_page(Base_page):
	
	def __init__(self, parent, ctrl):
		super().__init__(parent, ctrl)

		# Campos da janela
		## Titulo
		self.c_title = tk.Frame(self)
		self.c_title["padx"] = 20
		self.c_title.pack()

		## Dados
		self.c_data = tk.Frame(self)
		self.c_data["padx"] = 40
		self.c_data.pack()
		
		# Campo do titulo
		label = tk.Label(self.c_title)
		label['text'] = "Escala Gen" 
		label['font'] = self.ctrl.font_title
		label['pady'] = 10
		label.pack()

		# Campo dos dados
		self.l_desc = tk.Label(self.c_data)
		self.l_desc['text'] = "Gerador automático de escala PEB/PEQ" 
		self.l_desc['font'] = self.ctrl.font_body
		self.l_desc.pack()

		self.l_author = tk.Label(self.c_data)
		self.l_author['text'] = "Desenvolvedor: Arthur Phillip Silva" 
		self.l_author['font'] = self.ctrl.font_body
		self.l_author.pack()

		self.l_version = tk.Label(self.c_data)
		self.l_version['text'] = "Versão 2.0" 
		self.l_version['font'] = self.ctrl.font_body
		self.l_version.pack()
