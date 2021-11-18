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
		self.busca_escalas()
		self.desenha_tela()

	def busca_escalas(self):
		self.estacoes = self.app.db.estacoes.busca_tudo(ordem='codigo')
		self.lista_estacoes = ['Todos'] + list(self.estacoes.keys())

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

	def preenche_campos(self):
		estacao_id = self.estacao_secionada()
		turno_id = self.turno_secionado()
		print(estacao_id, turno_id)
		if estacao_id == 0:
			self.escreve_mensagem(f'Gerando todas as escalas')
		elif estacao_id:
			if not turno_id:
				self.escreve_mensagem(f'Nenhum turno escolhido')
			else:
				estacao = self.estacao_secionada(True)
				self.app.ge.gera_escala(2021, 1, turno_id, estacao_id)
				self.escreve_mensagem(f'Gerando escala da estação {estacao}')
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
		Texto(self.seletor, "Estação", posicao=tk.LEFT, largura=10)
		self.seletor_estacoes = SeletorAutocomplete(self.seletor, self.lista_estacoes, posicao=tk.LEFT)
		Texto(self.seletor, "Turno", posicao=tk.LEFT, largura=10)
		self.seletor_turnos = SeletorAutocomplete(self.seletor, self.lista_turnos, posicao=tk.LEFT)
		Botao(self.seletor, 'Buscar', lambda: self.preenche_campos(), posicao=tk.LEFT)

		## Botões
		self.botoes = Container(self.body, altura=30)
		Botao(self.botoes, 'Gerar', lambda: self.preenche_campos(), posicao=tk.LEFT)
		# Botao(self.botoes, 'Limpar', lambda: self.gerar_escala(), posicao=tk.LEFT)

	# 	## ASOs
	# 	self.asos = []
	# 	self.lines = []
	# 	self.ps = []

	# 	### ASOs titulares
	# 	self.c_asos = tk.Frame(self.c_data)
	# 	self.c_asos.pack()

	# 	self.l_asos = tk.Label(self.c_asos)
	# 	self.l_asos['text'] = "Titulares                        Reservsa" 
	# 	self.l_asos['font'] = self.app.font_body
	# 	self.l_asos.pack()

	# 	## Texto
	# 	self.l_data2 = tk.Label(self.c_data)
	# 	self.l_data2['text'] = " ------------------------------------------------------- " 
	# 	self.l_data2['font'] = self.app.font_body
	# 	self.l_data2.pack()

	# 	## Resultado 
	# 	self.l_result = tk.Label(self)
	# 	self.l_result['text'] = ''
	# 	self.l_result['font'] = self.app.font_body
	# 	self.l_result.pack(side=tk.BOTTOM)
		
	# 	# Campo dos botões
	# 	self.button_start = tk.Button(self.c_button)
	# 	self.button_start['text'] = "Inicio"
	# 	self.button_start['command'] = lambda: self.app.show_frame("Start_page")
	# 	self.button_start.pack(side=tk.LEFT)

	# 	# ## Atualiza
	# 	self.button_update = tk.Button(self.c_button)
	# 	self.button_update['text'] = "Atualizar"
	# 	self.button_update['command'] = lambda: self.update()
	# 	# self.button_update.pack(side=tk.LEFT)

	# 	## Gerador
	# 	self.button_search = tk.Button(self.c_button)
	# 	self.button_search['text'] = "Gerar escala"
	# 	self.button_search['command'] = lambda: self.generate()
	# 	self.button_search.pack(side=tk.LEFT)

	# # Procura estação
	# def search(self):
	# 	sid = self.sid.get().upper()

	# 	print(self.asos)

	# 	for a in self.asos:
	# 		a.destroy()

	# 	for l in self.lines:
	# 		l.destroy()

	# 	for p in self.ps:
	# 		p.destroy()
		
	# 	self.asos = []
	# 	self.ps = []
		
	# 	if sid:
	# 		self.sid.delete(0,tk.END)
	# 		self.name.delete(0,tk.END)

	# 		alias_list = self.app.data.people.get_list('alias')

	# 		aso_list = []
	# 		try:
	# 			station = json.load(open('data/ests/'+sid, "r"))
	# 			for aso in station['asos']:
	# 				aso_list.append(self.app.data.people.get(aso)) 
	# 		except:
	# 			print('Arquivo invalido estação')

	# 		station = self.app.data.stations.get(sid)

	# 		if station:
	# 			self.sid.insert(0,sid)
	# 			self.name.insert(0,station['name'])

	# 			nf = int(station['peb']) + int(station['peq'])

	# 			self.l_result['text'] = '** OK **'

	# 			asot = []
	# 			asor = []
	# 			for n in range(nf):
	# 				dupla = tk.Frame(self.c_asos)
	# 				dupla.pack()
	# 				self.lines.append(dupla)

	# 				item = atk.AutocompleteCombobox(dupla)
	# 				item.set_completion_list(alias_list)
	# 				item["width"] = 20
	# 				item["font"] = self.app.font_body
	# 				item.pack(side=tk.LEFT, padx=30)
	# 				item.focus_set()
	# 				asot.append(item)

	# 				if aso_list and n < len(aso_list):
	# 					item.insert(0,aso_list[n]['alias'])

	# 				item = atk.AutocompleteCombobox(dupla)
	# 				item.set_completion_list(alias_list)
	# 				item["width"] = 20
	# 				item["font"] = self.app.font_body
	# 				item.pack(side=tk.RIGHT, padx=30)
	# 				item.focus_set()
	# 				asor.append(item)

	# 				if aso_list and (n+nf) < len(aso_list):
	# 					item.insert(0,aso_list[n+nf]['alias'])
				
	# 			self.asos = asot+asor
	# 		else:
	# 			self.l_result['text'] = '** Estação não encontrada **'

	# def generate(self):
	# 	self.l_result['text'] = 'Trabalhando.. Aguarde.'

	# 	sid = self.sid.get()
	# 	item = self.app.data.stations.get(sid)
	# 	if not item:
	# 		self.l_result['text'] = '** Estação não encontrada **'
	# 		return

	# 	month = self.month.get()
	# 	if month not in self.app.data.months:
	# 		self.l_result['text'] = '** Mês inválido **'
	# 		return

	# 	year = self.year.get()
	# 	if not year or int(year) < 2000 or int(year) > 2500:
	# 		self.l_result['text'] = '** Ano inválido **'
	# 		return
		
	# 	asos = []
	# 	for a in self.asos:
	# 		aname = a.get()
	# 		if not aname:
	# 			self.l_result['text'] = '** Necessario preencher todos ASOs **'
	# 			return

	# 		item = self.app.data.people.get(aname, 'alias')
	# 		if item:
	# 			asos.append(item['id'])
	# 		else:
	# 			self.l_result['text'] = '** ASO ' +aname+ ' não encontrado **'
	# 			return

	# 	dat = {
	# 		'station':sid,
	# 		'month':month,
	# 		'year':year,
	# 		'asos':asos
	# 	}
		
	# 	try:
	# 		arq = open('data/ests/'+sid, "w")
	# 		arq.write(json.dumps(dat, indent=4))
	# 	except:
	# 		print('Arquivo invalido')

	# 	self.l_result['text'] = self.app.gen.gen(dat)
		
	# 	self.app.gen.pdf()

	# def aso_alias(self):
	# 	self.alias_list = ['  ']
	# 	for k,v in self.app.db_aso.items():
	# 		self.alias_list.append(v['alias'])

	# 	self.alias_list.sort()