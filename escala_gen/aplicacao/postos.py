'''
Programa de geracao automatica de posto de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk
from tkinter import ttk

import json

import aplicacao.autocompletion as atk

from .componentes import *
from .base import Base

class Postos(Base):
	
	def __init__(self, mestre, app):
		super().__init__(mestre, app)
		self.posto = {}
		self.pessoa = {}
		self.estacao = {}
		self.busca_postos()
		self.desenha_tela()
	
	def busca_postos(self):
		self.postos = self.app.db.postos.busca_tudo()
		self.pessoas = self.app.db.pessoas.nomes()
		self.estacoes = self.app.db.estacoes.busca_tudo(ordem='codigo')

	def salva_posto(self):
		dados = {}
		campos = self.le_campos()
		print('campos lidos:', campos)
		for chave in campos:
			if not self.posto or self.posto[chave] != campos[chave]:
				dados[chave] = campos[chave]
		if dados:
			if 'id' in self.posto:
				self.app.db.postos.atualiza(self.posto['id'], dados)
			else:
				self.app.db.postos.insere(dados)
			self.limpa_campos()
			self.busca_postos()
			self.seletor_postos.set_completion_list(self.postos.keys())
			self.escreve_mensagem(f"Dados de {campos['codigo']} alterado com sucesso")
		else:
			self.escreve_mensagem(f'Nenhuma alteração encontrada')

	def remove_posto(self):
		posto = self.posto_secionado()
		if posto:
			self.app.db.postos.remove(posto['id'])
			self.limpa_campos()
			self.busca_postos()
			self.seletor_postos.set_completion_list(self.postos.keys())

	def preenche_campos(self):
		self.posto = self.posto_secionado()
		self.posto_codigo.texto(self.posto['codigo'])
		self.posto_turno.texto(self.posto['turno'])
		self.posto_ordem.texto(self.posto['ordem'])
		self.posto_posto.texto(self.posto['posto'])
		self.posto_descricao.texto(self.posto['desc'])
		estacao = self.app.db.estacoes.busca_por_id(self.posto['estacao_id'])
		self.posto_estacao.texto(estacao['sigla'])

	def limpa_campos(self):
		self.posto = {}
		self.posto_codigo.texto('')
		self.posto_descricao.texto('')
		self.posto_posto.texto('')
		self.posto_ordem.texto('')
		self.posto_turno.texto('')
		self.posto_estacao.texto('')

	def le_campos(self):
		dados = {}
		dados['codigo'] = self.posto_codigo.get().upper()
		dados['posto'] = self.posto_posto.get().upper()
		dados['desc'] = self.posto_descricao.get()
		dados['turno'] = int(self.posto_turno.get())
		dados['ordem'] = int(self.posto_ordem.get())
		dados['estacao_id'] = self.estacao_secionada()
		return dados

	def escreve_mensagem(self, msg):
		self.msg.set(msg)

	def posto_secionado(self):
		return self.postos[self.seletor_postos.get()]

	def pessoa_secionada(self):
		pessoa = self.pessoas[self.posto_pessoa.get()]
		return pessoa['id']

	def estacao_secionada(self):
		estacao = self.estacoes[self.posto_estacao.get()]
		return estacao['id']

	def desenha_tela(self):
		# Campos da janela
		## Titulo
		self.titulo = Container(self.body)
		Titulo(self.titulo, "postos")
		

		## Dados
		self.dados = Container(self.body)
		self.seletor = Container(self.dados, altura=30)
		self.seletor_postos = SeletorAutocomplete(self.seletor, self.postos.keys(), posicao=tk.LEFT)
		Botao(self.seletor, 'Buscar', lambda: self.preenche_campos(), posicao=tk.LEFT)
	
		self.identificacao = Container(self.dados)
		Texto(self.identificacao, "Código", posicao=tk.LEFT, largura=20)
		self.posto_codigo = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		Texto(self.identificacao, "Posto", posicao=tk.LEFT, largura=10)
		self.posto_posto = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		Texto(self.identificacao, "Turno", posicao=tk.LEFT, largura=10)
		self.posto_turno = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		Texto(self.identificacao, "Estacao", posicao=tk.LEFT, largura=10)
		self.posto_estacao = SeletorAutocomplete(self.identificacao, self.estacoes.keys(), posicao=tk.LEFT, largura=10)
		
		self.descricao = Container(self.dados, altura=20)
		Texto(self.descricao, "Descrição", posicao=tk.LEFT, largura=20)
		self.posto_descricao = Entrada(self.descricao, posicao=tk.LEFT, largura=58)
		Texto(self.descricao, "Ordem", posicao=tk.LEFT, largura=10)
		self.posto_ordem = Entrada(self.descricao, posicao=tk.LEFT, largura=10)

		## Botões
		self.botoes = Container(self.body, altura=30)
		Botao(self.botoes, 'Salvar', lambda: self.salva_posto(), posicao=tk.LEFT)
		Botao(self.botoes, 'Remove', lambda: self.remove_posto(), posicao=tk.LEFT)
		Botao(self.botoes, 'Limpar', lambda: self.limpa_campos(), posicao=tk.LEFT)