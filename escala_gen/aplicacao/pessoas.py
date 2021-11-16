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

class Pessoas(Base):
	
	def __init__(self, mestre, app):
		super().__init__(mestre, app)
		self.pessoa = {}
		self.busca_pessoas()
		self.desenha_tela()
	
	def busca_pessoas(self):
		self.pessoas = self.app.db.pessoas.busca_tudo()

	def atualiza_pessoa(self):
		nome = self.pessoa_nome.get()
		apelido = self.pessoa_apelido.get()
		matricula = self.pessoa_matricula.get()
		posto = int(self.pessoa_posto.get())
		turno = int(self.pessoa_turno.get())
		dados = {}
		if self.pessoa['nome'] != nome:
			dados['nome'] = nome
		if self.pessoa['apelido'] != apelido:
			dados['apelido'] = apelido
		if self.pessoa['matricula'] != matricula:
			dados['matricula'] = matricula
		if self.pessoa['posto'] != posto:
			dados['posto'] = posto
		if self.pessoa['turno'] != turno:
			dados['turno'] = turno
		if dados:
			self.app.db.pessoas.atualiza(self.pessoa['id'], dados)
			self.limpa_campos()
			self.busca_pessoas()
			self.seletor_pessoas.set_completion_list(self.pessoas.keys())
			self.escreve_mensagem(f'Dados de {apelido} alterado com sucesso')
		else:
			self.escreve_mensagem(f'Nenhuma alteração encontrada')

	def remove_pessoa(self, id):
		pessoa = self.pessoa_secionada()
		self.app.db.pessoas.remove(pessoa['id'])

	def preenche_campos(self):
		self.pessoa = self.pessoa_secionada()
		self.pessoa_nome.texto(self.pessoa['nome'])
		self.pessoa_apelido.texto(self.pessoa['apelido'])
		self.pessoa_matricula.texto(self.pessoa['matricula'])
		self.pessoa_posto.texto(self.pessoa['posto'])
		self.pessoa_turno.texto(self.pessoa['turno'])

	def limpa_campos(self):
		self.pessoa_nome.texto('')
		self.pessoa_apelido.texto('')
		self.pessoa_matricula.texto('')
		self.pessoa_posto.texto('')
		self.pessoa_turno.texto('')

	def pessoa_secionada(self):
		return self.pessoas[self.seletor_pessoas.get()]

	def desenha_tela(self):
		# Campos da janela
		## Titulo
		self.titulo = Container(self.body)
		Titulo(self.titulo, "Pessoas")
		

		## Dados
		self.dados = Container(self.body)
		self.seletor = Container(self.dados, altura=30)
		self.seletor_pessoas = SeletorAutocomplete(self.seletor, self.pessoas.keys(), posicao=tk.LEFT)
		Botao(self.seletor, 'Buscar', lambda: self.preenche_campos(), posicao=tk.LEFT)
	
		self.nome = Container(self.dados)
		Texto(self.nome, "Nome", posicao=tk.LEFT, largura=20)
		self.pessoa_nome = Entrada(self.nome, posicao=tk.LEFT, largura=78)
		
		self.identificacao = Container(self.dados,altura=20)
		Texto(self.identificacao, "Apelido", posicao=tk.LEFT, largura=20)
		self.pessoa_apelido = Entrada(self.identificacao, posicao=tk.LEFT, largura=30)
		Texto(self.identificacao, "Matríula", posicao=tk.LEFT, largura=15)
		self.pessoa_matricula = Entrada(self.identificacao, posicao=tk.LEFT, largura=30)

		self.lotacao = Container(self.dados)
		Texto(self.lotacao, "Turno", posicao=tk.LEFT, largura=20)
		self.pessoa_turno = Entrada(self.lotacao, posicao=tk.LEFT, largura=30)
		Texto(self.lotacao, "P", posicao=tk.LEFT, largura=15)
		self.pessoa_posto = Entrada(self.lotacao, posicao=tk.LEFT, largura=30)
		
		## Botões
		self.botoes = Container(self.body, altura=30)
		Botao(self.botoes, 'Atualizar', lambda: self.atualiza_pessoa(), posicao=tk.LEFT)

