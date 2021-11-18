import tkinter as tk

from tkinter import font, ttk


from .autocompletion import AutocompleteCombobox


FONTE_TEXTO = lambda: font.Font(family='Arial', size=10)

FONTE_TITULO = lambda: font.Font(family='Arial', size=12, weight="bold")


class Botao(tk.Button):
	def __init__(self, mestre, texto, comando, posicao=tk.LEFT, altura=None, largura=15, margem_vertical=None,):
		param = {}
		param['master'] = mestre
		param['text'] = texto
		param['command'] = comando
		param['width'] = largura
		if altura:
			param['height'] = altura	
		if margem_vertical:
			param['pady'] = margem_vertical

		super().__init__(**param)

		self.pack(side=posicao)


class Container(tk.Frame):

	def __init__(self, mestre, posicao=None, largura=None, altura=None, preenche=None):
		param = {}
		param['master'] = mestre
		if largura:
			param['padx'] = largura
		if altura:
			param['pady'] = altura

		super().__init__(**param)
		attr = {}
		if posicao:
			attr['side'] = posicao
		if preenche:
			attr['fill'] = preenche
		self.pack(**attr)

class Entrada(tk.Entry):
	def __init__(self, mestre, posicao=None, largura=None, altura=None):
		param = {}
		param['master'] = mestre
		param['font'] = FONTE_TEXTO()
		if largura:
			param['width'] = largura
		if altura:
			param['height'] = altura

		super().__init__(**param)
		self.pack(side=posicao)

	def texto(self, texto):
		self.delete(0,tk.END)
		self.insert(0,texto)

class Titulo(tk.Label):
	def __init__(self, mestre, texto, posicao=tk.TOP, largura=None, altura=None):
		param = {}
		param['master'] = mestre
		param['text'] = texto
		param['font'] = FONTE_TITULO()
		if largura:
			param['width'] = largura
		if altura:
			param['height'] = altura

		super().__init__(**param)
		self.pack(side=posicao)

class Texto(tk.Label):
	def __init__(self, mestre, texto='', variavel=None, posicao=None, largura=None, altura=None):
		param = {}
		param['master'] = mestre
		param['font'] = FONTE_TEXTO()
		if texto:
			param['text'] = texto
		if variavel:
			param['textvariable'] = variavel
		if largura:
			param['width'] = largura
		if altura:
			param['height'] = altura

		super().__init__(**param)
		self.pack(side=posicao)
	
	def texto(self, texto):
		self.text = texto

class Seletor(ttk.Combobox):
	def __init__(self, mestre, valores, largura=30, altura=None, posicao=None):
		param = {}
		param['master'] = mestre
		param['values'] = valores
		param['font'] = FONTE_TEXTO()
		if largura:
			param['width'] = largura
		if altura:
			param['height'] = altura

		super().__init__(**param)
		self.pack(side=posicao)
		self.valores = valores
	
	def selecionado(self):
		return self.valores[self.get()]

	def texto(self, texto):
		self.delete(0,tk.END)
		self.insert(0,texto)

class SeletorAutocomplete(AutocompleteCombobox):
	def __init__(self, mestre, valores, largura=30, altura=None, posicao=None):
		param = {}
		param['master'] = mestre
		param['font'] = FONTE_TEXTO()
		if largura:
			param['width'] = largura
		if altura:
			param['height'] = altura
		super().__init__(**param)
		self.set_completion_list(valores)
		self.pack(side=posicao)
		self.focus_set()

	def texto(self, texto):
		self.delete(0,tk.END)
		self.insert(0,texto)