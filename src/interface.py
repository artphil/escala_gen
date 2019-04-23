'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk
import autocompletion as atk
from datetime import datetime
import json
import os
from escala_gen import gen
from database import db


# Gerenciador da aplicação
class application(tk.Tk):

	def __init__(self):
		tk.Tk.__init__(self)
		try: 
			self.data = db()
		except:
			print("Erro no Banco de Dados")
			quit()

		# Fontes padrão
		self.font_title = tkfont.Font(family='Arial', size=12, weight="bold")
		self.font_body = tkfont.Font(family='Arial', size=10)

		self.title("** Gerador de Escala PEB/PEQ **")

		# Tamanho da tela
		wsize = 500
		hsize = 400
		self.minsize(wsize, hsize)
		# self.maxsize(wsize, hsize)

		# Corpo da aplicação
		container = tk.Frame(self)
		container.pack()

		# Gerenciador de janelas
		self.frames = {}
		for func in (	start_page, 
						aso_page, 
						est_page, 
						gen_page, 
						help_page):
			
			page_name = func.__name__
			frame = func(parent=container, ctrl=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("start_page")

	# Mostra a janela selecionada
	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

# Pagina de início
class start_page(tk.Frame):
	
	def __init__(self, parent, ctrl):
		tk.Frame.__init__(self, parent)
		self.ctrl = ctrl

		# Campos da janela
		# Titulo
		self.c_title = tk.Frame(self)
		self.c_title["padx"] = 20
		self.c_title["pady"] = 40
		self.c_title.pack()

		# Botões
		self.c_button = tk.Frame(self)
		self.c_button["padx"] = 40
		self.c_title["pady"] = 80
		self.c_button.pack(side=tk.BOTTOM)

		# Campo do titulo
		label = tk.Label(self.c_title)
		label['text'] = "Inicio" 
		label['font'] = self.ctrl.font_title
		# label['pady'] = 10
		label.pack(side=tk.TOP)

		# Campo dos botões
		button_gen = tk.Button(self.c_button)
		button_gen['text'] = "Gerar escala"
		button_gen['command'] = lambda: self.ctrl.show_frame("gen_page")

		button_aso = tk.Button(self.c_button)
		button_aso['text'] = "Alterar ASO"
		button_aso['command'] = lambda: self.ctrl.show_frame("aso_page")

		button_est = tk.Button(self.c_button)
		button_est['text'] = "Alterar EST"
		button_est['command'] = lambda: self.ctrl.show_frame("est_page")

		button_help = tk.Button(self.c_button)
		button_help['text'] = "Ajuda"
		button_help['command'] = lambda: self.ctrl.show_frame("help_page")

		button_help.pack(side=tk.LEFT)
		button_gen.pack(side=tk.LEFT)
		button_aso.pack(side=tk.RIGHT)
		button_est.pack(side=tk.RIGHT)

class est_page(tk.Frame):
	
	def __init__(self, parent, ctrl):
		tk.Frame.__init__(self, parent)
		self.ctrl = ctrl

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
		self.c_button.pack()

		# Campo do titulo
		self.label = tk.Label(self.c_title)
		self.label['text'] = "Estações" 
		self.label['font'] = self.ctrl.font_title
		self.label['pady'] = 10
		self.label.pack()


		# Campo dos dados
		## Texto
		self.l_data = tk.Label(self.c_data)
		self.l_data['text'] = "Procure por ID - exemplo: Central 1º turno = UCT1" 
		self.l_data['font'] = self.ctrl.font_body
		self.l_data.pack()

		## Id
		self.c_fid = tk.Frame(self.c_data)
		self.c_fid.pack()

		self.fidLabel = tk.Label(self.c_fid)
		self.fidLabel['text'] ="ID 	"
		self.fidLabel['font'] = self.ctrl.font_body
		self.fidLabel.pack(side=tk.LEFT)
  
		self.fid = tk.Entry(self.c_fid)
		self.fid["width"] = 30
		self.fid["font"] = self.ctrl.font_body
		self.fid.pack(side=tk.RIGHT)

		## Nome
		self.c_name = tk.Frame(self.c_data)
		self.c_name.pack()
		
		self.nameLabel = tk.Label(self.c_name)
		self.nameLabel['text'] ="Nome 	"
		self.nameLabel['font'] = self.ctrl.font_body
		self.nameLabel.pack(side=tk.LEFT)
  
		self.name = tk.Entry(self.c_name)
		self.name["width"] = 30
		self.name["font"] = self.ctrl.font_body
		self.name.pack(side=tk.RIGHT)

		## Postos
		self.c_fp = tk.Frame(self.c_data)
		self.c_fp.pack()
		
		### PEB
		self.fpebLabel = tk.Label(self.c_fp)
		self.fpebLabel['text'] ="PEB 	"
		self.fpebLabel['font'] = self.ctrl.font_body
		self.fpebLabel.pack(side=tk.LEFT)
  
		self.fpeb = tk.Entry(self.c_fp)
		self.fpeb["width"] = 10
		self.fpeb["font"] = self.ctrl.font_body
		self.fpeb.pack(side=tk.LEFT)

		### PEQ
		self.fpeqLabel = tk.Label(self.c_fp)
		self.fpeqLabel['text'] ="   PEQ 	"
		self.fpeqLabel['font'] = self.ctrl.font_body
		self.fpeqLabel.pack(side=tk.LEFT)
  
		self.fpeq = tk.Entry(self.c_fp)
		self.fpeq["width"] = 10
		self.fpeq["font"] = self.ctrl.font_body
		self.fpeq.pack(side=tk.LEFT)

		## Resultado 
		self.l_result = tk.Label(self)
		self.l_result['text'] = ''
		self.l_result['font'] = self.ctrl.font_body
		self.l_result.pack(side=tk.BOTTOM)

		# Campo dos botões
		## Inicio
		self.button_start = tk.Button(self.c_button)
		self.button_start['text'] = "Inicio"
		self.button_start['command'] = lambda: self.ctrl.show_frame("start_page")
		self.button_start.pack(side=tk.LEFT)

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

	# Procura Est
	def search(self):
		fid = self.fid.get().upper()

		if fid:
			self.fid.delete(0,tk.END)
			self.name.delete(0,tk.END)
			self.fpeb.delete(0,tk.END)
			self.fpeq.delete(0,tk.END)

			item = self.ctrl.data.est.get(fid)
			
			if item:
				self.fid.insert(0, fid)

				self.name.insert(0,item['name'])
				self.fpeb.insert(0,item['peb'])
				self.fpeq.insert(0,item['peq'])

				self.l_result['text'] = '** OK **'
			else:
				self.l_result['text'] = '** Estação não encontrada **'
		
		else:
			self.l_result['text'] = '** Digite ID **'

	# Atualiza Est
	def update(self):
		fid = self.fid.get()
		name = self.name.get()
		try: 
			peb = int(self.fpeb.get())
		except:
			self.l_result['text'] = '** PEB inválido **'
			return
			
		try: 
			peq = int(self.fpeq.get())
		except:
			self.l_result['text'] = '** PEQ inválido **'
			return

		if not fid:
			self.l_result['text'] = '** ID inválido **'
			return

		if peb < 1:
			self.l_result['text'] = '** PEB inválido **'
			return

		if peq < 1:
			self.l_result['text'] = '** PEQ inválido **'
			return

		item = {
			'id': fid,
			'name': name,
			'peb': str(peb),
			'peq': str(peq)
		}

		if self.ctrl.data.est.insert(item) :
			self.l_result['text'] = '** Estação '+fid+' atualizada **'

		else:
			self.l_result['text'] = '** Não foi possivel atualizar {} **'.format(fid)


	# Remove Est
	def delete(self):
		fid = self.fid.get()
		if fid and self.ctrl.data.est.remove(fid):
			self.l_result['text'] = '** Estação '+fid+' removida **'
		else:
			self.l_result['text'] = '** Não foi possivel remover {} **'.format(fid)







class aso_page(tk.Frame):
	
	def __init__(self, parent, ctrl):
		tk.Frame.__init__(self, parent)
		self.ctrl = ctrl

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
		self.fidLabel['text'] ="ID 	"
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
		self.aliasLabel['text'] ="Alias 	"
		self.aliasLabel['font'] = self.ctrl.font_body
		self.aliasLabel.pack(side=tk.LEFT)
  
		self.alias = tk.Entry(self.c_alias)
		self.alias["width"] = 30
		self.alias['text'] ="teste"
		self.alias["font"] = self.ctrl.font_body
		self.alias.pack(side=tk.RIGHT)

		## Nome
		self.c_name = tk.Frame(self.c_data)
		self.c_name.pack()
		
		self.nameLabel = tk.Label(self.c_name)
		self.nameLabel['text'] ="Nome 	"
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
		self.fpLabel['text'] ="P 	"
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
		## Inicio
		self.button_start = tk.Button(self.c_button)
		self.button_start['text'] = "Inicio"
		self.button_start['command'] = lambda: self.ctrl.show_frame("start_page")
		self.button_start.pack(side=tk.LEFT)

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

		if fid:
			self.name.delete(0,tk.END)
			self.alias.delete(0,tk.END)
			self.fp.delete(0,tk.END)
			
			item = self.ctrl.data.aso.get(fid)

			if item:
				self.name.insert(0,item['name'])
				
				self.alias.insert(0,item['alias'])
				
				self.fp.insert(0,item['p'])

				self.l_result['text'] = '** OK **'
			else:
				self.l_result['text'] = '** ASO não encontrado **'
		
		elif alias:
			self.name.delete(0,tk.END)
			self.fid.delete(0,tk.END)
			self.fp.delete(0,tk.END)
			self.alias.delete(0,tk.END)

			item = self.ctrl.data.aso.get(alias, 'alias')

			if item:
				self.fid.insert(0,item['id '])

				self.name.insert(0,item['name'])
				
				self.alias.insert(0,item['alias'])
				
				self.fp.insert(0,item['p'])

				self.l_result['text'] = '** OK **'
			
			else:
				self.l_result['text'] = '** ASO não encontrado **'
		
		else:
			self.l_result['text'] = '** Digite ID ou Alias **'

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

		if self.ctrl.data.aso.insert(item) :
			self.l_result['text'] = '** ASO '+fid+' atualizado **'

		else:
			self.l_result['text'] = '** Não foi possivel atualizar {} **'.format(fid)

	# Remove ASO
	def delete(self):
		fid = self.fid.get()
		if fid and self.ctrl.data.aso.remove(fid):
			self.l_result['text'] = '** ASO '+fid+' removido **'
		else:
			self.l_result['text'] = '** Não foi possivel remover {} **'.format(fid)






class gen_page(tk.Frame):
	
	def __init__(self, parent, ctrl):
		tk.Frame.__init__(self, parent)
		self.ctrl = ctrl

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
		self.c_button.pack()

		# Campo do titulo
		label = tk.Label(self.c_title)
		label['text'] = "Gerador de escala" 
		label['font'] = self.ctrl.font_title
		label['pady'] = 10
		label.pack()

		# Campo dos dados
		## Texto
		self.l_data = tk.Label(self.c_title)
		self.l_data['text'] = "Procure por ID - exemplo: Central 1º turno = UCT1" 
		self.l_data['font'] = self.ctrl.font_body
		self.l_data.pack()

		## Id
		self.c_sid = tk.Frame(self.c_data)
		self.c_sid.pack()

		self.sidLabel = tk.Label(self.c_sid)
		self.sidLabel['text'] ="ID estação 	"
		self.sidLabel['font'] = self.ctrl.font_body
		self.sidLabel.pack(side=tk.LEFT)
  
		self.sid = tk.Entry(self.c_sid)
		self.sid["width"] = 30
		self.sid["font"] = self.ctrl.font_body
		self.sid.pack(side=tk.RIGHT)

		## Estação
		self.c_name = tk.Frame(self.c_data)
		self.c_name.pack()
		
		self.nameLabel = tk.Label(self.c_name)
		self.nameLabel['text'] ="Nome 		"
		self.nameLabel['font'] = self.ctrl.font_body
		self.nameLabel.pack(side=tk.LEFT)
  
		self.name = tk.Entry(self.c_name)
		self.name["width"] = 30
		self.name["font"] = self.ctrl.font_body
		self.name.pack(side=tk.RIGHT)

		## Mes e Ano
		self.c_date = tk.Frame(self.c_data)
		self.c_date.pack()
		
		self.monthLabel = tk.Label(self.c_date)
		self.monthLabel['text'] ="Mes 		"
		self.monthLabel['font'] = self.ctrl.font_body
		self.monthLabel.pack(side=tk.LEFT)

		self.month = ttk.Combobox(self.c_date, values=[' ','Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])#, state='readonly')
		self.month["width"] = 12
		self.month["font"] = self.ctrl.font_body
		self.month.pack(side=tk.LEFT)

		self.yearLabel = tk.Label(self.c_date)
		self.yearLabel['text'] ="	Ano"
		self.yearLabel['font'] = self.ctrl.font_body
		self.yearLabel.pack(side=tk.LEFT)
  
		self.year = tk.Entry(self.c_date)
		self.year["width"] = 4
		self.year["font"] = self.ctrl.font_body
		self.year.pack(side=tk.LEFT)

		## Texto
		self.l_data = tk.Label(self.c_data)
		self.l_data['text'] = " ------------------------------------------------------- " 
		self.l_data['font'] = self.ctrl.font_body
		self.l_data.pack()

		## ASOs
		self.asos = []
		self.ps = []

		### ASOs titulares
		self.c_asot = tk.Frame(self.c_data)
		self.c_asot.pack(side=tk.LEFT)

		self.l_asot = tk.Label(self.c_asot)
		self.l_asot['text'] = "Titulares" 
		self.l_asot['font'] = self.ctrl.font_body
		self.l_asot.pack()

		# self.c_pt = tk.Frame(self.c_data)
		# self.c_pt.pack(side=tk.LEFT)

		# self.l_pt = tk.Label(self.c_pt)
		# self.l_pt['text'] = "Ps  " 
		# self.l_pt['font'] = self.ctrl.font_body
		# self.l_pt.pack()

		### ASOs reservas
		# self.c_pr = tk.Frame(self.c_data)
		# self.c_pr.pack(side=tk.RIGHT)

		# self.l_pr = tk.Label(self.c_pr)
		# self.l_pr['text'] = "Ps  " 
		# self.l_pr['font'] = self.ctrl.font_body
		# self.l_pr.pack()

		self.c_asor = tk.Frame(self.c_data)
		self.c_asor.pack(side=tk.RIGHT)

		self.l_asor = tk.Label(self.c_asor)
		self.l_asor['text'] = "Resesrvas" 
		self.l_asor['font'] = self.ctrl.font_body
		self.l_asor.pack()

		## Resultado 
		self.l_result = tk.Label(self)
		self.l_result['text'] = ''
		self.l_result['font'] = self.ctrl.font_body
		self.l_result.pack(side=tk.BOTTOM)
		
		# Campo dos botões
		self.button_start = tk.Button(self.c_button)
		self.button_start['text'] = "Inicio"
		self.button_start['command'] = lambda: self.ctrl.show_frame("start_page")
		self.button_start.pack(side=tk.LEFT)

		## Busca
		self.button_search = tk.Button(self.c_button)
		self.button_search['text'] = "Buscar"
		self.button_search['command'] = lambda: self.search()
		self.button_search.pack(side=tk.LEFT)

		# ## Atualiza
		self.button_update = tk.Button(self.c_button)
		self.button_update['text'] = "Atualizar"
		self.button_update['command'] = lambda: self.update()
		# self.button_update.pack(side=tk.LEFT)

		## Gerador
		self.button_search = tk.Button(self.c_button)
		self.button_search['text'] = "Gerar escala"
		self.button_search['command'] = lambda: self.generate()
		self.button_search.pack(side=tk.LEFT)

	# Procura estação
	def search(self):
		sid = self.sid.get().upper()

		print(self.asos)

		for a in self.asos:
			a.destroy()

		for p in self.ps:
			p.destroy()
		
		self.asos = []
		self.ps = []
		
		if sid:
			self.sid.delete(0,tk.END)
			self.name.delete(0,tk.END)

			alias_list = self.ctrl.data.aso.get_list('alias')

			aso_list = []
			try:
				station = json.load(open('data/ests/'+sid, "r"))
				for aso in station['asos']:
					aso_list.append(self.ctrl.data.aso.get(aso)) 
			except:
				print('Arquivo invalido estação')

			station = self.ctrl.data.est.get(sid)

			if station:
				self.sid.insert(0,sid)
				self.name.insert(0,station['name'])

				nf = int(station['peb']) + int(station['peq'])

				self.l_result['text'] = '** OK **'
				

				for n in range(nf):
					item = atk.AutocompleteCombobox(self.c_asot)
					item.set_completion_list(alias_list)
					item["width"] = 20
					item["font"] = self.ctrl.font_body
					item.pack()
					item.focus_set()
					self.asos.append(item)

					# p = tk.Entry(self.c_pt)
					# p["width"] = 3
					# p["font"] = self.ctrl.font_body
					# p.pack()
					# self.ps.append(p)
				
					if aso_list and n < len(aso_list):
						item.insert(0,aso_list[n]['alias'])
						# p.insert(0,aso_list[n]['p'])
						# p.configure(state='readonly')

				for n in range(nf):
					item = atk.AutocompleteCombobox(self.c_asor)
					item.set_completion_list(alias_list)
					item["width"] = 20
					item["font"] = self.ctrl.font_body
					item.pack()
					item.focus_set()
					self.asos.append(item)

					# p = tk.Entry(self.c_pr)
					# p["width"] = 3
					# p["font"] = self.ctrl.font_body
					# p.pack()
					# self.ps.append(p)
					
					if aso_list and (n+nf) < len(aso_list):
						item.insert(0,aso_list[n+nf]['alias'])
						# p.insert(0,aso_list[n+nf]['p'])
						# p.configure(state='readonly')

			else:
				self.l_result['text'] = '** Estação não encontrada **'

	# # Atualiza ASO
	# def update(self):
	# 	with open('data/data.json', "r") as arq:
	# 		self.ctrl.db = json.load(arq)

	# Gera escala
	def generate(self):
		self.l_result['text'] = 'Trabalhando.. Aguarde.'

		sid = self.sid.get()
		item = self.ctrl.data.est.get(sid)
		if not item:
			self.l_result['text'] = '** Estação não encontrada **'
			return

		month = self.month.get()
		if month not in self.ctrl.data.mes:
			self.l_result['text'] = '** Mês inválido **'
			return

		year = self.year.get()
		if not year or int(year) < 2000 or int(year) > 2500:
			self.l_result['text'] = '** Ano inválido **'
			return
		
		asos = []
		for a in self.asos:
			aname = a.get()
			if not aname:
				self.l_result['text'] = '** Necessario preencher todos ASOs **'
				return

			item = self.ctrl.data.aso.get(aname, 'alias')
			if item:
				asos.append(item['id'])
			else:
				self.l_result['text'] = '** ASO ' +aname+ ' não encontrado **'
				return

		dat = {
			'station':sid,
			'month':month,
			'year':year,
			'asos':asos
		}
		
		try:
			arq = open('data/ests/'+sid, "w")
			arq.write(json.dumps(dat, indent=4))
		except:
			print('Arquivo invalido')

		# os.system('python src/escala_gen.py data/ests/'+sid)
		
		esc = gen()
		self.l_result['text'] = esc.esc_int(self.ctrl.data, dat)
		
		esc.pdf()

	def aso_alias(self):
		self.alias_list = ['  ']
		for k,v in self.ctrl.db_aso.items():
			self.alias_list.append(v['alias'])

		self.alias_list.sort()

		
class help_page(tk.Frame):
	
	def __init__(self, parent, ctrl):
		tk.Frame.__init__(self, parent)
		self.ctrl = ctrl

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
		self.c_button.pack()

		# Campo do titulo
		label = tk.Label(self.c_title)
		label['text'] = "AJUDA" 
		label['font'] = self.ctrl.font_title
		label['pady'] = 10
		label.pack()

		# Campo dos dados
		## Texto
		self.l_data = tk.Label(self.c_data)
		self.l_data['text'] = "Perguntas frequentes" 
		self.l_data['font'] = self.ctrl.font_body
		self.l_data.pack()

		self.l_q1 = tk.Label(self.c_data)
		self.l_q1['text'] = "Perguntas frequentes" 
		self.l_q1['font'] = self.ctrl.font_body
		self.l_q1.pack()

		# Campo dos botões
		button_back = tk.Button(self.c_button)
		button_back['text'] = "Inicio"
		button_back['command'] = lambda: self.ctrl.show_frame("start_page")

		button_back.pack()

if __name__ == '__main__':
	
	# Criando aplicação
	myapp = application()

	# Iniciando programa
	myapp.mainloop()