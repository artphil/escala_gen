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

class Escalas(Base):
	
	def __init__(self, mestre, app):
		super().__init__(mestre, app)
		self.escala = {}
		self.pessoa = {}
		self.estacao = {}
		self.busca_escalas()
		self.desenha_tela()
	
	def busca_escalas(self):
		self.escalas = self.app.db.escalas.busca_tudo()
		self.pessoas = self.app.db.pessoas.nomes()
		self.estacoes = self.app.db.estacoes.busca_tudo(ordem='codigo')

	def salva_escala(self):
		campos = self.le_campos()
		dados = {}
		print(self.escala)
		print(campos)
		for chave in campos:
			if not self.escala or self.escala[chave] != campos[chave]:
				dados[chave] = campos[chave]
		if dados:
			if 'id' in self.escala:
				self.app.db.escalas.atualiza(self.escala['id'], dados)
			else:
				self.app.db.escalas.insere(dados)
			self.limpa_campos()
			self.busca_escalas()
			self.seletor_escalas.set_completion_list(self.escalas.keys())
			self.escreve_mensagem(f"Dados de {dados['codigo']} salvo com sucesso")
		else:
			self.escreve_mensagem(f'Nenhuma alteração encontrada')

	def remove_escala(self):
		escala = self.escala_secionada()
		if escala:
			self.app.db.escalas.remove(escala['id'])
			self.limpa_campos()
			self.busca_escalas()
			self.seletor_escalas.set_completion_list(self.escalas.keys())

	def le_campos(self):
		dados = {}
		dados['codigo'] = self.escala_codigo.get().upper()
		dados['sigla'] =  self.escala_sigla.get().upper()
		dados['turno'] = int(self.escala_turno.get())
		dados['trecho'] = int(self.escala_trecho.get())
		dados['ordem'] = int(self.escala_ordem.get())
		dados['pessoa_id'] = self.pessoa_secionada()
		return dados

	def preenche_campos(self):
		self.escala = self.escala_secionada()
		self.escala_codigo.texto(self.escala['codigo'])
		self.escala_sigla.texto(self.escala['sigla'])
		self.escala_turno.texto(self.escala['turno'])
		self.escala_trecho.texto(self.escala['trecho'])
		self.escala_ordem.texto(self.escala['ordem'])
		pessoa = self.app.db.pessoas.busca_por_id(self.escala['pessoa_id'])
		self.escala_pessoa.texto(pessoa['apelido'])

	def limpa_campos(self):
		self.escala = {}
		self.escala_codigo.texto('')
		self.escala_trecho.texto('')
		self.escala_sigla.texto('')
		self.escala_turno.texto('')
		self.escala_pessoa.texto('')
		self.escala_estacao.texto('')

	def escreve_mensagem(self, msg):
		self.msg.set(msg)

	def escala_secionada(self):
		return self.escalas[self.seletor_escalas.get()]

	def pessoa_secionada(self):
		pessoa = self.pessoas[self.escala_pessoa.get()]
		return pessoa['id']

	def desenha_tela(self):
		# Campos da janela
		## Titulo
		self.titulo = Container(self.body)
		Titulo(self.titulo, "Escalas")
		

		## Dados
		self.dados = Container(self.body)
		self.seletor = Container(self.dados, altura=30)
		self.seletor_escalas = SeletorAutocomplete(self.seletor, self.escalas.keys(), posicao=tk.LEFT)
		Botao(self.seletor, 'Buscar', lambda: self.preenche_campos(), posicao=tk.LEFT)
	
		self.identificacao = Container(self.dados)
		Texto(self.identificacao, "Código", posicao=tk.LEFT, largura=20)
		self.escala_codigo = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		Texto(self.identificacao, "Sigla", posicao=tk.LEFT, largura=10)
		self.escala_sigla = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		Texto(self.identificacao, "Turno", posicao=tk.LEFT, largura=10)
		self.escala_turno = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		Texto(self.identificacao, "Trecho", posicao=tk.LEFT, largura=10)
		self.escala_trecho = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		Texto(self.identificacao, "Ordem", posicao=tk.LEFT, largura=10)
		self.escala_ordem = Entrada(self.identificacao, posicao=tk.LEFT, largura=10)
		
		self.ocupante = Container(self.dados, altura=20)
		Texto(self.ocupante, "Pessoa", posicao=tk.LEFT, largura=20)
		self.escala_pessoa = SeletorAutocomplete(self.ocupante, self.pessoas.keys(), posicao=tk.LEFT, largura=30)
		
		## Botões
		self.botoes = Container(self.body, altura=30)
		Botao(self.botoes, 'Salvar', lambda: self.salva_escala(), posicao=tk.LEFT)
		Botao(self.botoes, 'Remove', lambda: self.remove_escala(), posicao=tk.LEFT)
		Botao(self.botoes, 'Limpar', lambda: self.limpa_campos(), posicao=tk.LEFT)
