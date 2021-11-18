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
		self.detalhes_estacoes = []
		self.estacoes = app.db.estacoes.busca_tudo(ordem='codigo')
		self.desenha_tela()

	def atualiza_tela(self):
		for item in self.detalhes_estacoes:
			item.destroy()
		self.detalhes_estacoes.clear()
		self.preenche_detalhes()


	def desenha_tela(self):
		# Campos da janela
		## Titulo
		self.titulo = Container(self.body)
		Titulo(self.titulo, "Estações")

		## Dados
		self.dados = Container(self.body)
		self.preenche_detalhes()

		## Botões
		self.botoes = Container(self.body, altura=20)
		Botao(self.botoes, 'Atualizar', lambda: self.atualiza_tela(), posicao=tk.LEFT)

	def preenche_detalhes(self):
		for sigla, estacao in self.estacoes.items():
			caixa = Container(self.dados, largura=80, preenche='x')
			texto = f"{sigla:<15}{estacao['nome']:<25}	"
			Texto(caixa, texto, posicao=tk.LEFT)
			postos = self.app.db.postos.busca_por_estacao(estacao['id'], turno=1, ordem='posto')
			Texto(caixa, '1T:', posicao=tk.LEFT)
			for p in postos:
				Texto(caixa, postos[p]['posto'], posicao=tk.LEFT)
			postos = self.app.db.postos.busca_por_estacao(estacao['id'], turno=2, ordem='posto')
			Texto(caixa, '	2T:', posicao=tk.LEFT)
			for p in postos:
				Texto(caixa, postos[p]['posto'], posicao=tk.LEFT)
			self.detalhes_estacoes.append(caixa)
