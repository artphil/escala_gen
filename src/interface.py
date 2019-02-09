import tkinter as tk
from tkinter import font  as tkfont
import json
import os


# Gerenciador da aplicação
class application(tk.Tk):

	def __init__(self):
		tk.Tk.__init__(self)
		
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
		for func in (start_page, data_page, gen_page, help_page):
			page_name = func.__name__
			frame = func(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("start_page")

	# Mostra a janela selecionada
	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

# Pagina de início
class start_page(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

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
		label['font'] = controller.font_title
		# label['pady'] = 10
		label.pack(side=tk.TOP)

		# Campo dos botões
		button_gen = tk.Button(self.c_button)
		button_gen['text'] = "Gerar escala"
		button_gen['command'] = lambda: controller.show_frame("gen_page")

		button_data = tk.Button(self.c_button)
		button_data['text'] = "Alterar dados"
		button_data['command'] = lambda: controller.show_frame("data_page")

		button_help = tk.Button(self.c_button)
		button_help['text'] = "Ajuda"
		button_help['command'] = lambda: controller.show_frame("help_page")

		button_help.pack(side=tk.LEFT)
		button_gen.pack(side=tk.LEFT)
		button_data.pack(side=tk.RIGHT)

class data_page(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		with open('data/data.jnew', "r") as arq:
			self.db = json.load(arq)

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
		self.label['font'] = controller.font_title
		self.label['pady'] = 10
		self.label.pack()


		# Campo dos dados
		## Texto
		self.l_data = tk.Label(self.c_data)
		self.l_data['text'] = "Procure por ID ou Alias" 
		self.l_data['font'] = controller.font_body
		self.l_data.pack()

		## Id
		self.c_fid = tk.Frame(self.c_data)
		self.c_fid.pack()

		self.fidLabel = tk.Label(self.c_fid)
		self.fidLabel['text'] ="ID 	"
		self.fidLabel['font'] = controller.font_body
		self.fidLabel.pack(side=tk.LEFT)
  
		self.fid = tk.Entry(self.c_fid)
		self.fid["width"] = 30
		self.fid["font"] = controller.font_body
		self.fid.pack(side=tk.RIGHT)

		## Nome
		self.c_name = tk.Frame(self.c_data)
		self.c_name.pack()
		
		self.nameLabel = tk.Label(self.c_name)
		self.nameLabel['text'] ="Nome 	"
		self.nameLabel['font'] = controller.font_body
		self.nameLabel.pack(side=tk.LEFT)
  
		self.name = tk.Entry(self.c_name)
		self.name["width"] = 30
		self.name["font"] = controller.font_body
		self.name.pack(side=tk.RIGHT)

		## Alias
		self.c_alias = tk.Frame(self.c_data)
		self.c_alias.pack()
		
		self.aliasLabel = tk.Label(self.c_alias)
		self.aliasLabel['text'] ="Alias 	"
		self.aliasLabel['font'] = controller.font_body
		self.aliasLabel.pack(side=tk.LEFT)
  
		self.alias = tk.Entry(self.c_alias)
		self.alias["width"] = 30
		self.alias['text'] ="teste"
		self.alias["font"] = controller.font_body
		self.alias.pack(side=tk.RIGHT)

		## Posto
		self.c_fp = tk.Frame(self.c_data)
		self.c_fp.pack()
		
		self.fpLabel = tk.Label(self.c_fp)
		self.fpLabel['text'] ="P 	"
		self.fpLabel['font'] = controller.font_body
		self.fpLabel.pack(side=tk.LEFT)
  
		self.fp = tk.Entry(self.c_fp)
		self.fp["width"] = 30
		self.fp["font"] = controller.font_body
		self.fp.pack(side=tk.RIGHT)

		## Resultado 
		self.l_result = tk.Label(self)
		self.l_result['text'] = ''
		self.l_result['font'] = controller.font_body
		self.l_result.pack(side=tk.BOTTOM)

		# Campo dos botões
		## Inicio
		self.button_start = tk.Button(self.c_button)
		self.button_start['text'] = "Inicio"
		self.button_start['command'] = lambda: controller.show_frame("start_page")
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
			
			if fid in self.db['aso']:
				self.name.insert(0,self.db['aso'][fid]['nome'])
				
				self.alias.insert(0,self.db['aso'][fid]['alias'])
				
				self.fp.insert(0,self.db['aso'][fid]['p'])

				self.l_result['text'] = '** OK **'
			else:
				self.l_result['text'] = '** ASO não encontrado **'
		
		elif alias:
			self.name.delete(0,tk.END)
			self.fid.delete(0,tk.END)
			self.fp.delete(0,tk.END)

			for f, v in self.db['aso'].items():
				if alias == v['alias']:
					self.fid.insert(0,f)
				
					self.name.insert(0,self.db['aso'][fid]['nome'])
					
					self.fp.insert(0,self.db['aso'][fid]['p'])
					self.l_result['text'] = '** OK **'
					return

	# Atualiza ASO
	def update(self):
		fid = self.fid.get()
		if fid:
			if fid not in self.db['aso']:
				self.db['aso'][fid] = {}
			
			self.db['aso'][fid]['nome'] = self.name.get()
			
			self.db['aso'][fid]['alias'] = self.alias.get()
			
			self.db['aso'][fid]['p'] = self.fp.get()

			self.l_result['text'] = '** ASO atualizado **'

			self.save()

	# Remove ASO
	def delete(self):
		fid = self.fid.get()
		if fid and fid in self.db['aso']:
			del self.db['aso'][fid]
			self.save()


	def save(self):
		with open('data/data.jnew', "w") as arq:
			arq.write(json.dumps(self.db, sort_keys=True, indent=4))
		
		with open('data/data.jnew', "r") as arq:
			self.db = json.load(arq)





class gen_page(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		with open('data/data.jnew', "r") as arq:
			self.db = json.load(arq)

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
		label['font'] = controller.font_title
		label['pady'] = 10
		label.pack()

		# Campo dos dados
		## Texto
		self.l_data = tk.Label(self.c_title)
		self.l_data['text'] = "Procure por ID - exemplo: Central 1º turno = UCT1" 
		self.l_data['font'] = controller.font_body
		self.l_data.pack()

		## Id
		self.c_sid = tk.Frame(self.c_data)
		self.c_sid.pack()

		self.sidLabel = tk.Label(self.c_sid)
		self.sidLabel['text'] ="ID estação 	"
		self.sidLabel['font'] = controller.font_body
		self.sidLabel.pack(side=tk.LEFT)
  
		self.sid = tk.Entry(self.c_sid)
		self.sid["width"] = 30
		self.sid["font"] = controller.font_body
		self.sid.pack(side=tk.RIGHT)

		## Estação
		self.c_name = tk.Frame(self.c_data)
		self.c_name.pack()
		
		self.nameLabel = tk.Label(self.c_name)
		self.nameLabel['text'] ="Nome 		"
		self.nameLabel['font'] = controller.font_body
		self.nameLabel.pack(side=tk.LEFT)
  
		self.name = tk.Entry(self.c_name)
		self.name["width"] = 30
		self.name["font"] = controller.font_body
		self.name.pack(side=tk.RIGHT)

		## Mes e ano
		self.c_date = tk.Frame(self.c_data)
		self.c_date.pack()
		
		self.monthLabel = tk.Label(self.c_date)
		self.monthLabel['text'] ="Mes 		"
		self.monthLabel['font'] = controller.font_body
		self.monthLabel.pack(side=tk.LEFT)
  
		self.month = tk.Entry(self.c_date)
		self.month["width"] = 14
		self.month["font"] = controller.font_body
		self.month.pack(side=tk.LEFT)

		self.yearLabel = tk.Label(self.c_date)
		self.yearLabel['text'] ="	Ano"
		self.yearLabel['font'] = controller.font_body
		self.yearLabel.pack(side=tk.LEFT)
  
		self.year = tk.Entry(self.c_date)
		self.year["width"] = 4
		self.year["font"] = controller.font_body
		self.year.pack(side=tk.LEFT)

		## Texto
		self.l_data = tk.Label(self.c_data)
		self.l_data['text'] = " ---------------------------------- " 
		self.l_data['font'] = controller.font_body
		self.l_data.pack()

		## ASOs
		self.asos = []

		self.c_asot = tk.Frame(self.c_data)
		self.c_asot.pack(side=tk.LEFT)

		self.l_data = tk.Label(self.c_asot)
		self.l_data['text'] = "Titulares (Alias)" 
		self.l_data['font'] = controller.font_body
		self.l_data.pack()

		self.c_asor = tk.Frame(self.c_data)
		self.c_asor.pack(side=tk.RIGHT)

		self.l_data = tk.Label(self.c_asor)
		self.l_data['text'] = "Resesrvas (Alias)" 
		self.l_data['font'] = self.controller.font_body
		self.l_data.pack()

		## Resultado 
		self.l_result = tk.Label(self)
		self.l_result['text'] = ''
		self.l_result['font'] = self.controller.font_body
		self.l_result.pack(side=tk.BOTTOM)
		
		# Campo dos botões
		self.button_start = tk.Button(self.c_button)
		self.button_start['text'] = "Inicio"
		self.button_start['command'] = lambda: self.controller.show_frame("start_page")
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

			if sid in self.db['est']:
				self.sid.insert(0,sid)
				self.name.insert(0,self.db['est'][sid]['nome'])

				nf = len(self.db['est'][sid]['postos'])

				self.l_result['text'] = '** OK **'

				for n in range(nf):
					self.asos.append(tk.Entry(self.c_asot))
					self.asos[n]["width"] = 30
					self.asos[n]["font"] = self.controller.font_body
					self.asos[n].pack()

				for n in range(nf):
					self.asos.append(tk.Entry(self.c_asor))
					self.asos[n+nf]["width"] = 30
					self.asos[n+nf]["font"] = self.controller.font_body
					self.asos[n+nf].pack()

			else:
				self.l_result['text'] = '** Estação não encontrada **'

	# Atualiza ASO
	def update(self):
		with open('data/data.jnew', "r") as arq:
			self.db = json.load(arq)

	def generate(self):
		sid = self.sid.get()
		if sid not in self.db['est']:
			self.l_result['text'] = '** Estação não encontrada **'
			return

		month = self.month.get()
		if month not in self.db['mes']:
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
			for k, v in self.db['aso'].items():
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

		os.system('python src/escala_gen.py data/ests/'+sid)

		
class help_page(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

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
		label['font'] = controller.font_title
		label['pady'] = 10
		label.pack()

		# Campo dos dados
		## Texto
		self.l_data = tk.Label(self.c_data)
		self.l_data['text'] = "Perguntas frequentes" 
		self.l_data['font'] = controller.font_body
		self.l_data.pack()

		self.l_q1 = tk.Label(self.c_data)
		self.l_q1['text'] = "Perguntas frequentes" 
		self.l_q1['font'] = controller.font_body
		self.l_q1.pack()

		# Campo dos botões
		button_back = tk.Button(self.c_button)
		button_back['text'] = "Inicio"
		button_back['command'] = lambda: controller.show_frame("start_page")

		button_back.pack()

# Criando aplicação
myapp = application()

# Iniciando programa
myapp.mainloop()