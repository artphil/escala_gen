'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk

from .componentes import *
from .base import Base

class Estacoes(Base):
	
	def __init__(self, mestre, app):
		super().__init__(mestre, app)
		self.estacoes = app.db.estacoes.busca_tudo(ordem='codigo')
		self.desenha_tela()

	def desenha_tela(self):
		# Campos da janela
		## Titulo
		self.titulo = Container(self)
		Titulo(self.titulo, "Estações")

		## Dados
		self.dados = Container(self)
		for sigla, estacao in self.estacoes.items():
			caixa = Container(self.dados, largura=80)
			texto = f"{sigla}	{estacao['nome']}		"
			Texto(caixa, texto, posicao=tk.LEFT)
			postos = self.app.db.postos.busca_por_estacao(estacao['id'], 1)
			Texto(caixa, '1T:', posicao=tk.LEFT)
			for p in postos:
				Texto(caixa, postos[p]['posto'], posicao=tk.LEFT)
			postos = self.app.db.postos.busca_por_estacao(estacao['id'], 2, 'posto')
			Texto(caixa, '	2T:', posicao=tk.LEFT)
			for p in postos:
				Texto(caixa, postos[p]['posto'], posicao=tk.LEFT)


		## Botões
		self.botoes = Container(self)


	