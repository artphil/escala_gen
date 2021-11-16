'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk

from .componentes import *
from .base import Base

class Creditos(Base):
	
	def __init__(self, mestre, app):
		super().__init__(mestre, app)
		self.desenha_tela()

	def desenha_tela(self):
		# Campos da janela
		## Titulo
		self.titulo = Container(self)
		Titulo(self.titulo, "Créditos")
		
		## Dados
		self.dados = Container(self)
		Texto(self.dados, "Gerador automático de escala PEB/PEQ")
		Texto(self.dados, "Desenvolvedor: Arthur Phillip Silva")
		Texto(self.dados, "Versão 3.0")