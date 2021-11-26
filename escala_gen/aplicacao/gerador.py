'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk
from tkinter import ttk

import json

import aplicacao.autocompletion as atk

from .componentes import *
from .base import Base


class Gerador(Base):
	
	def __init__(self, mestre, app):
		super().__init__(mestre, app)
		self.lista_turnos = [
			'1 Turno',
			'2 Turno'
			]
		self.lista_info = []
		self.busca_escalas()
		self.desenha_tela()

	def busca_escalas(self):
		self.estacoes = self.app.db.estacoes.busca_tudo(ordem='codigo')
		self.lista_estacoes = ['Todos'] + list(self.estacoes.keys())
		self.meses = {mes['nome']:mes['numero'] for mes in self.app.db.meses}

	def estacao_secionada(self, texto=False):
		estacao = self.seletor_estacoes.get()
		if texto: 
			return estacao
		if estacao == 'Todos':
			return 0
		if not estacao:
			return 
		return self.estacoes[estacao]['id']

	def turno_secionado(self):
		turno = self.seletor_turnos.get()
		if turno == '1 Turno':
			return 1
		if turno == '2 Turno':
			return 2
		return 0
	
	def ano_secionado(self):
		ano = int(self.ano.get())
		if ano < 2019 or ano > 3000:
			return 0
		return ano

	def mes_secionado(self):
		mes = self.mes.get()
		if not mes:
			return 0
		return self.meses[mes]

	def gera_escala(self):
		estacao_id = self.estacao_secionada()
		turno_id = self.turno_secionado()
		ano = self.ano_secionado()
		mes = self.mes_secionado()
		if not ano or not mes: 
			self.escreve_mensagem(f'Ano ou Mes invalido')
			return

		print(estacao_id, turno_id)
		if estacao_id == 0:
			self.escreve_mensagem(f'Gerando todas as escalas')
			self.app.ge.gera_todas_escalas(ano, mes)
		elif estacao_id:
			if not turno_id:
				self.escreve_mensagem(f'Nenhum turno escolhido')
			else:
				estacao_sigla = self.estacao_secionada(True)
				self.escreve_mensagem(f'Gerando escala da estação {estacao_sigla}')
				self.app.ge.gera_escala(ano, mes, turno_id, estacao_id)
		else:
			self.escreve_mensagem(f'Nenhuma estação escolhida')

		# self.escala_codigo.texto(self.escala['codigo'])
		# self.escala_sigla.texto(self.escala['sigla'])
		# self.escala_turno.texto(self.escala['turno'])
		# self.escala_trecho.texto(self.escala['trecho'])
		# pessoa = self.app.db.pessoas.busca_por_id(self.escala['pessoa_id'])
		# self.escala_pessoa.texto(pessoa['apelido'])
		# estacao = self.app.db.estacoes.busca_por_id(self.escala['estacao_id'])
		# self.escala_estacao.texto(estacao['sigla'])

	def desenha_tela(self):
		# Campos da janela
		## Titulo
		self.titulo = Container(self.body)
		Titulo(self.titulo, "Gerador de Escalas")

		## Dados
		self.dados = Container(self.body)
		self.seletor = Container(self.dados, altura=30)
		Texto(self.seletor, "Ano", posicao=tk.LEFT, largura=10)
		self.ano = Entrada(self.seletor, posicao=tk.LEFT, largura=10)
		Texto(self.seletor, "Mes", posicao=tk.LEFT, largura=10)
		self.mes = Seletor(self.seletor, list(self.meses.keys()), posicao=tk.LEFT, largura=10)
		Texto(self.seletor, "Estação", posicao=tk.LEFT, largura=10)
		self.seletor_estacoes = SeletorAutocomplete(self.seletor, self.lista_estacoes, posicao=tk.LEFT, largura=10)
		Texto(self.seletor, "Turno", posicao=tk.LEFT, largura=10)
		self.seletor_turnos = SeletorAutocomplete(self.seletor, self.lista_turnos, posicao=tk.LEFT, largura=10)
		Botao(self.seletor, 'Visualizar', lambda: self.preenche_info(), posicao=tk.LEFT)

		## Informacao
		self.info = Container(self.body)
		self.info_esquerda = Container(self.info, posicao=tk.LEFT, largura=50)
		self.info_direita = Container(self.info, posicao=tk.LEFT, largura=50)

		## Botões
		self.botoes = Container(self.body, altura=30)
		Botao(self.botoes, 'Gerar escala', lambda: self.gera_escala(), posicao=tk.LEFT)
		# Botao(self.botoes, 'Limpar', lambda: self.gerar_escala(), posicao=tk.LEFT)

	def preenche_info(self):
		for item in self.lista_info:
			item.destroy()
		self.lista_info = []
		estacao = self.estacao_secionada(True)
		turno = self.turno_secionado()
		ano = self.ano_secionado()
		mes = self.mes_secionado()
		if not ano or not mes: 
			self.escreve_mensagem(f'Ano ou Mes invalido')
			return
		if not estacao or estacao=='Todos' or not turno: 
			self.escreve_mensagem(f'Muitos dados, não é possivel mostrar.')
			return
		escalas = self.app.db.escalas.busca_por_estacao(estacao,turno).values()
		n_postos = int(len(escalas)/2)
		for i, item in enumerate(escalas):
			pessoa = self.app.db.pessoas.busca_por_id(item['pessoa_id'])
			texto = f"{item['sigla']} - {pessoa['apelido']} ( P{pessoa['posto']} )"
			if i < n_postos:
				e = Texto(self.info_esquerda, texto, posicao=tk.TOP)
			else:
				e = Texto(self.info_direita, texto, posicao=tk.TOP)
			self.lista_info.append(e)