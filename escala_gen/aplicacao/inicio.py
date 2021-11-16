'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk

from .componentes import *
from .base import Base

# Pagina de início
class Inicio(Base):
	
	def __init__(self, mestre, app):
		super().__init__(mestre, app)

		# Campos da janela
		# Titulo
		self.titulo = Container(self)
		Titulo(self.titulo, "Escala Gen")

