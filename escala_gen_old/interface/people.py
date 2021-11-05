'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk
from tkinter import ttk

import json

import interface.autocompletion as atk

from .base import Base_page

class People_page(Base_page):
	
	def __init__(self, parent, ctrl):
		super().__init__(parent, ctrl)

		# Campos da janela
		## Titulo
		self.c_title = tk.Frame(self)
		self.c_title["padx"] = 20
		self.c_title.pack()

		## Dados
		self.c_data = tk.Frame(self)
		self.c_data["padx"] = 40
		self.c_data.pack()

		## Botões
		self.c_button = tk.Frame(self)
		self.c_button["padx"] = 40
		self.c_button['pady'] = 10
		self.c_button.pack()

		# Campo do titulo
		self.label = tk.Label(self.c_title)
		self.label['text'] = "Banco de dados" 
		self.label['font'] = self.ctrl.font_title
		self.label['pady'] = 10
		self.label.pack()


		# Campo dos dados
		## Texto
		self.l_data = tk.Label(self.c_data)
		self.l_data['text'] = "Procure por ID ou Alias" 
		self.l_data['font'] = self.ctrl.font_body
		self.l_data.pack()

		## Id
		self.c_fid = tk.Frame(self.c_data)
		self.c_fid.pack()

		self.fidLabel = tk.Label(self.c_fid)
		self.fidLabel["width"] = 10
		self.fidLabel['text'] ="Matrícula"
		self.fidLabel['font'] = self.ctrl.font_body
		self.fidLabel.pack(side=tk.LEFT)
  
		self.fid = tk.Entry(self.c_fid)
		self.fid["width"] = 30
		self.fid["font"] = self.ctrl.font_body
		self.fid.pack(side=tk.RIGHT)

		## Alias
		self.c_alias = tk.Frame(self.c_data)
		self.c_alias.pack()
		
		self.aliasLabel = tk.Label(self.c_alias)
		self.aliasLabel["width"] = 10
		self.aliasLabel['text'] ="Alias"
		self.aliasLabel['font'] = self.ctrl.font_body
		self.aliasLabel.pack(side=tk.LEFT)
  
		self.alias =  atk.AutocompleteCombobox(self.c_alias)
		self.alias.set_completion_list(self.ctrl.data.people.get_list('alias'))
		self.alias["width"] = 28
		self.alias['text'] ="teste"
		self.alias["font"] = self.ctrl.font_body
		self.alias.pack()
		self.alias.focus_set()

		## Nome
		self.c_name = tk.Frame(self.c_data)
		self.c_name.pack()
		
		self.nameLabel = tk.Label(self.c_name)
		self.nameLabel["width"] = 10
		self.nameLabel['text'] ="Nome"
		self.nameLabel['font'] = self.ctrl.font_body
		self.nameLabel.pack(side=tk.LEFT)
  
		self.name = tk.Entry(self.c_name)
		self.name["width"] = 30
		self.name["font"] = self.ctrl.font_body
		self.name.pack(side=tk.RIGHT)

		## Posto
		self.c_fp = tk.Frame(self.c_data)
		self.c_fp.pack()
		
		self.fpLabel = tk.Label(self.c_fp)
		self.fpLabel["width"] = 10
		self.fpLabel['text'] ="Posto"
		self.fpLabel['font'] = self.ctrl.font_body
		self.fpLabel.pack(side=tk.LEFT)
  
		self.fp = tk.Entry(self.c_fp)
		self.fp["width"] = 30
		self.fp["font"] = self.ctrl.font_body
		self.fp.pack(side=tk.RIGHT)

		## Resultado 
		self.l_result = tk.Label(self)
		self.l_result['text'] = ''
		self.l_result['font'] = self.ctrl.font_body
		self.l_result.pack(side=tk.BOTTOM)

		# Campo dos botões
		
		## Busca
		self.button_search = tk.Button(self.c_button)
		self.button_search['text'] = "Buscar"
		self.button_search['command'] = lambda: self.search()
		self.button_search.pack(side=tk.LEFT)

		## Atualiza
		self.button_update = tk.Button(self.c_button)
		self.button_update['text'] = "Atualizar"
		self.button_update['command'] = lambda: self.update()
		self.button_update.pack(side=tk.LEFT)

		## Remover
		self.button_delete = tk.Button(self.c_button)
		self.button_delete['text'] = "Remover"
		self.button_delete['command'] = lambda: self.delete()
		self.button_delete.pack(side=tk.LEFT)

	# Procura ASO
	def search(self):
		fid = self.fid.get()
		alias = self.alias.get()

		if alias:
			self.name.delete(0,tk.END)
			self.fid.delete(0,tk.END)
			self.fp.delete(0,tk.END)
			self.alias.delete(0,tk.END)

			item = self.ctrl.data.people.get(alias, 'alias')

			if item:
				self.fid.insert(0,item['id'])

				self.name.insert(0,item['name'])
				
				self.alias.insert(0,item['alias'])
				
				self.fp.insert(0,item['p'])

				self.l_result['text'] = '** OK **'
			
			else:
				self.l_result['text'] = '** ASO não encontrado **'
		
		else:
			self.l_result['text'] = '** Digite Alias **'

	# Atualiza ASO
	def update(self):
		fid = self.fid.get()
		name = self.name.get()
		alias = self.alias.get()
		fp = self.fp.get()

		if not fid:
			self.l_result['text'] = '** ID inválido **'
			return

		item = {
			'id':	fid,
			'name':	name,
			'alias':alias,
			'p':	fp
		}	

		if self.ctrl.data.people.insert(item) :
			self.l_result['text'] = f'** ASO {fid} atualizado **'
			self.alias.set_completion_list(self.ctrl.data.people.get_list('alias'))

		else:
			self.l_result['text'] = f'** Não foi possivel atualizar {fid} **'

	# Remove ASO
	def delete(self):
		fid = self.fid.get()
		if fid and self.ctrl.data.people.remove(fid):
			self.l_result['text'] = f'** ASO {fid} removido **'
		else:
			self.l_result['text'] = f'** Não foi possivel remover {fid} **'

