import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk
from datetime import datetime
import json
import os
# import difflib as df
from escala_gen import gen


# Gerenciador da aplicação
class application(tk.Tk):

	def __init__(self):
		tk.Tk.__init__(self)
		self.path_data 		= 'data/data'
		self.path_data_aso 	= 'data/data_aso'
		self.path_data_est 	= 'data/data_est'

		with open(self.path_data+'.json', "r") as arq:
			self.db = json.load(arq)
		
		with open(self.path_data_aso+'.json', "r") as arq:
			self.db_aso = json.load(arq)
		
		with open(self.path_data_est+'.json', "r") as arq:
			self.db_est = json.load(arq)
		
		# Fontes padrão
		self.font_title = tkfont.Font(family='Arial', size=12, weight="bold")
		self.font_body = tkfont.Font(family='Arial', size=10)

		self.title("** Escala ASO 1 **")

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

	# Salva banco de dados
	def save(self, db, file_name):
		with open(file_name+'.aux', "w") as arq:
			arq.write(json.dumps(db, sort_keys=True, indent=4))
			
			# orig = json.load(open(file_name+'.json', "r")
			# adiff = open(file_name+'.diff', "r+")
			# adiff.write(datetime)

			# print(df.Differ())
			os.system('date >> '+file_name+'.diff')
			os.system('diff '+file_name+'.json '+file_name+'.aux >> '+file_name+'.diff')
			os.remove(file_name+'.json')
			os.rename(file_name+'.aux', file_name+'.json')

		
		# with open(file_name+'.json', "r") as arq:
		# 	self.ctrl.db = json.load(arq)


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

		# ## Remover
		# self.button_delete = tk.Button(self.c_button)
		# self.button_delete['text'] = "Remover"
		# self.button_delete['command'] = lambda: self.delete()
		# self.button_delete.pack(side=tk.LEFT)

	# Procura Est
	def search(self):
		fid = self.fid.get().upper()

		if fid:
			self.fid.delete(0,tk.END)
			self.name.delete(0,tk.END)
			self.fpeb.delete(0,tk.END)
			self.fpeq.delete(0,tk.END)

			peb = 0
			peq = 0
			
			if fid in self.ctrl.db_est:
				self.fid.insert(0, fid)

				self.name.insert(0,self.ctrl.db_est[fid]['nome'])
				
				for p in self.ctrl.db_est[fid]['postos']:
					if p % 2 == 0:
						peb += 1
					else:
						peq += 1

				self.fpeb.insert(0,peb)
				self.fpeq.insert(0,peq)

				self.l_result['text'] = '** OK **'
			else:
				self.l_result['text'] = '** Estação não encontrada **'
		
		else:
			self.l_result['text'] = '** Digite ID **'

	# Atualiza Est
	def update(self):
		fid = self.fid.get()
		peb = int(self.fpeb.get())
		peq = int(self.fpeq.get())

		if not peb or peb < 1:
			self.l_result['text'] = '** PEB inválido **'
			return

		if not peq or peq < 1:
			self.l_result['text'] = '** PEQ inválido **'
			return

		if fid :
			if fid not in self.ctrl.db_est:
				self.ctrl.db_est[fid] = {}
			
			self.ctrl.db_est[fid]['nome'] = self.name.get()
			
			l = []

			a = 2
			for p in range(peb):
				l.append(a)
				a += 2

			a = 3
			for p in range(peq):
				l.append(a)
				a += 2

			self.ctrl.db_est[fid]['postos'] = l 

			self.l_result['text'] = '** Estação atualizada **'

			self.ctrl.save(self.ctrl.db_est, self.ctrl.path_data_est)

	# Remove ASO
	def delete(self):
		fid = self.fid.get()
		if fid and fid in ctrl.db_est:
			del self.ctrl.db_est[fid]
			self.ctrl.save(self.ctrl.db_est, self.ctrl.path_data_est)






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
			
			if fid in self.ctrl.db_aso:
				self.name.insert(0,self.ctrl.db_aso[fid]['nome'])
				
				self.alias.insert(0,self.ctrl.db_aso[fid]['alias'])
				
				self.fp.insert(0,self.ctrl.db_aso[fid]['p'])

				self.l_result['text'] = '** OK **'
			else:
				self.l_result['text'] = '** ASO não encontrado **'
		
		elif alias:
			self.name.delete(0,tk.END)
			self.fid.delete(0,tk.END)
			self.fp.delete(0,tk.END)
			self.alias.delete(0,tk.END)

			for f, v in self.ctrl.db_aso.items():
				if alias.lower() == v['alias'].lower():
					
					self.fid.insert(0,f)
	
					self.alias.insert(0,self.ctrl.db_aso[f]['alias'])
				
					self.name.insert(0,self.ctrl.db_aso[f]['nome'])
					
					self.fp.insert(0,self.ctrl.db_aso[f]['p'])

					self.l_result['text'] = '** OK **'
					return
			
			if not alias:
				self.l_result['text'] = '** ASO não encontrado **'
		
		else:
			self.l_result['text'] = '** Digite ID ou Alias **'

	# Atualiza ASO
	def update(self):
		fid = self.fid.get()
		if fid:
			if fid not in self.ctrl.db_aso:
				self.ctrl.db_aso[fid] = {}
			
			self.ctrl.db_aso[fid]['nome'] = self.name.get()
			
			self.ctrl.db_aso[fid]['alias'] = self.alias.get()
			
			self.ctrl.db_aso[fid]['p'] = self.fp.get()

			self.l_result['text'] = '** ASO atualizado **'

			self.ctrl.save(self.ctrl.db_aso, self.ctrl.path_data_aso)

	# Remove ASO
	def delete(self):
		fid = self.fid.get()
		if fid and fid in ctrl.db_aso:
			del self.ctrl.db_aso[fid]
			self.ctrl.save(self.ctrl.db_aso, self.ctrl.path_data_aso)






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

		## Mes e ano
		self.c_date = tk.Frame(self.c_data)
		self.c_date.pack()
		
		self.monthLabel = tk.Label(self.c_date)
		self.monthLabel['text'] ="Mes 		"
		self.monthLabel['font'] = self.ctrl.font_body
		self.monthLabel.pack(side=tk.LEFT)

		self.month = ttk.Combobox(self.c_date, state='readonly', values=[' ','Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
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

		self.c_asot = tk.Frame(self.c_data)
		self.c_asot.pack(side=tk.LEFT)

		self.l_data = tk.Label(self.c_asot)
		self.l_data['text'] = "Titulares" 
		self.l_data['font'] = self.ctrl.font_body
		self.l_data.pack()

		self.c_asor = tk.Frame(self.c_data)
		self.c_asor.pack(side=tk.RIGHT)

		self.l_data = tk.Label(self.c_asor)
		self.l_data['text'] = "Resesrvas" 
		self.l_data['font'] = self.ctrl.font_body
		self.l_data.pack()

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
		# self.button_update = tk.Button(self.c_button)
		# self.button_update['text'] = "Atualizar"
		# self.button_update['command'] = lambda: self.update()
		# self.button_update.pack(side=tk.LEFT)

		## Gerador
		self.button_search = tk.Button(self.c_button)
		self.button_search['text'] = "Gerar escala"
		self.button_search['command'] = lambda: self.generate()
		self.button_search.pack(side=tk.LEFT)

	# Procura estação
	def search(self):
		sid = self.sid.get().upper()

		if sid:
			self.sid.delete(0,tk.END)
			self.name.delete(0,tk.END)
			
			for a in self.asos:
				a.destroy()

			self.asos = []

			self.aso_alias()

			if sid in self.ctrl.db_est:
				self.sid.insert(0,sid)
				self.name.insert(0,self.ctrl.db_est[sid]['nome'])

				nf = len(self.ctrl.db_est[sid]['postos'])

				self.l_result['text'] = '** OK **'
				

				for n in range(nf):
					self.asos.append(ttk.Combobox(self.c_asot, state='readonly', values = self.alias_list))
					self.asos[n].set = self.alias_list[0]
					self.asos[n]["width"] = 20
					self.asos[n]["font"] = self.ctrl.font_body
					self.asos[n].pack()

				for n in range(nf):
					self.asos.append(ttk.Combobox(self.c_asor, state='readonly', values = self.alias_list))
					self.asos[n+nf].set = self.alias_list[0]
					self.asos[n+nf]["width"] = 20
					self.asos[n+nf]["font"] = self.ctrl.font_body
					self.asos[n+nf].pack()

			else:
				self.l_result['text'] = '** Estação não encontrada **'

	# # Atualiza ASO
	# def update(self):
	# 	with open('data/data.json', "r") as arq:
	# 		self.ctrl.db = json.load(arq)

	# Gera escala
	def generate(self):
		sid = self.sid.get()
		if sid not in self.ctrl.db_est:
			self.l_result['text'] = '** Estação não encontrada **'
			return

		month = self.month.get()
		if month not in self.ctrl.db['mes']:
			self.l_result['text'] = '** Mês inválido **'
			return

		year = self.year.get()
		if not year or int(year) < 2000 or int(year) > 2500:
			self.l_result['text'] = '** Ano inválido **'
			return
		
		asos = []
		for a in self.asos:
			found = False
			aname = a.get()
			for k, v in self.ctrl.db_aso.items():
				if aname == v['alias']:
					asos.append(k)
					found = True
					break
			if not found:
				self.l_result['text'] = '** ASO ' +aname+ ' não encontrado **'
				return

		with open('data/ests/'+sid, "w") as arq:
			arq.write(sid+'\n')
			arq.write(month+' '+year+'\n')
			# arq.write('1\n')
			for a in asos:
				arq.write(a)
				arq.write(' ')

		# os.system('python src/escala_gen.py data/ests/'+sid)
		
		db_gen = self.ctrl.db.copy()
		db_gen['aso'] = self.ctrl.db_aso.copy()
		db_gen['est'] = self.ctrl.db_est.copy()

		esc = gen()
		self.l_result['text'] = esc.esc_int(db_gen,sid,asos,month,year,self.l_result['text'])
		
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

# Criando aplicação
myapp = application()

# Iniciando programa
myapp.mainloop()