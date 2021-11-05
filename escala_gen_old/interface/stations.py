'''
Programa de geracao automatica de escala de postos de servico
Interface
autor: Arthur Phillip Silva
''' 

import tkinter as tk

from .base import Base_page

class Stations_page(Base_page):
	
	def __init__(self, parent, ctrl):
		super().__init__(parent, ctrl)
		# tk.Frame.__init__(self, parent)
		# self.ctrl = ctrl

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
		self.c_button["pady"] = 10
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
		self.fidLabel["width"] = 10
		self.fidLabel['text'] ="ID"
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
		self.nameLabel["width"] = 10
		self.nameLabel['text'] ="Nome"
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
		self.fpebLabel["width"] = 10
		self.fpebLabel['text'] ="PEB"
		self.fpebLabel['font'] = self.ctrl.font_body
		self.fpebLabel.pack(side=tk.LEFT)
  
		self.fpeb = tk.Entry(self.c_fp)
		self.fpeb["width"] = 10
		self.fpeb["font"] = self.ctrl.font_body
		self.fpeb.pack(side=tk.LEFT)

		### PEQ
		self.fpeqLabel = tk.Label(self.c_fp)
		self.fpeqLabel["width"] = 8
		self.fpeqLabel['text'] ="PEQ"
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

			item = self.ctrl.data.stations.get(fid)
			
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

		if self.ctrl.data.stations.insert(item) :
			self.l_result['text'] = f'** Estação {fid} atualizada **'

		else:
			self.l_result['text'] = f'** Não foi possivel atualizar {fid} **'


	# Remove Est
	def delete(self):
		fid = self.fid.get()
		if fid and self.ctrl.data.stations.remove(fid):
			self.l_result['text'] = f'** Estação {fid} removida **'
		else:
			self.l_result['text'] = f'** Não foi possivel remover {fid} **'

