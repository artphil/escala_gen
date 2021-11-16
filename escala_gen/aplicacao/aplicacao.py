'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk
from tkinter import font  as tkfont

from .estacoes import Estacoes


from .inicio import Inicio
from .pessoas import Pessoas
from .postos import Postos
from .escalas import Escalas
from .gerador import Gerador
from .creditos import Creditos


# Gerenciador da aplicação
class App(tk.Tk):

	def __init__(self, db, gen):
		tk.Tk.__init__(self)
		self.db = db
		self.gen = gen

		# Fontes padrão
		self.font_title = tkfont.Font(family='Arial', size=12, weight="bold")
		self.font_body = tkfont.Font(family='Arial', size=10)

		self.title("Escala Gen - Gerador de Escala PEB/PEQ")

		# Tamanho da tela
		wsize = 800
		hsize = 600
		self.minsize(wsize, hsize)
		# self.maxsize(wsize, hsize)

		# Corpo da aplicação
		container = tk.Frame(self)
		container.pack()

		# Gerenciador de janelas
		self.janelas = {}
		for func in (	Inicio, 
						Pessoas, 
						Postos, 
						Escalas, 
						Estacoes, 
						Gerador, 
						Creditos ):
			
			page_name = func.__name__
			frame = func(container, self)
			self.janelas[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.ir_para("Inicio")

	# Mostra a janela selecionada
	def ir_para(self, page_name):
		frame = self.janelas[page_name]
		frame.tkraise()
