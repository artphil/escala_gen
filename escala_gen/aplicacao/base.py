'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk
from .componentes import *

class Base(tk.Frame):
	
	def __init__(self, mestre, app):
		tk.Frame.__init__(self, mestre)
		self.app = app
		self.msg = tk.StringVar()

		# Navbar
		self.navbar = Container(self)

		# Campo dos botões
		Botao(self.navbar, 'Inicio', lambda: self.app.ir_para("Inicio"))
		Botao(self.navbar, 'Gerar escala', lambda: self.app.ir_para("Gerador"))
		Botao(self.navbar, 'Postos', lambda: self.app.ir_para("Postos"))
		Botao(self.navbar, 'Pessoas', lambda: self.app.ir_para("Pessoas"))
		Botao(self.navbar, 'Escalas', lambda: self.app.ir_para("Escalas"))
		Botao(self.navbar, 'Estações', lambda: self.app.ir_para("Estacoes"))
		Botao(self.navbar, 'Créditos', lambda: self.app.ir_para("Creditos"))

		self.body = Container(self)
		
		self.footer = Container(self, posicao=tk.BOTTOM)
		Texto(self.footer, variavel=self.msg)

	def escreve_mensagem(self, msg):
		self.msg.set(msg)