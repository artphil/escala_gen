'''
Programa de geracao automatica de escala de postos de servico
gerenciador de Banco de Dados
autor: Arthur Phillip Silva
'''

import os

class db:
	def __init__(self):
		self.aso = data('data/taso.csv')
		self.est = data('data/test.csv')


class data:
	def __init__(self, path):
		self.path = path
		self.read()

	def read(self):
		try:
			file = open(self.path, 'r').readlines()
		except:
			print('Arquivo {} não encontrado'.format(path))
			return

		self.titles = file[0][:-1].split(';')
		self.db = {}

		for line in file[1:]:
			item = {}
			data = line[:-1].split(';')
			for i in range(1, len(data)):
				item[self.titles[i]] = data[i]
			self.db[data[0]] = item
		
		return self

	def write(self):
		p_tmp = self.path+'.tmp'

		with open(p_tmp, 'w') as file:

			file.write(';'.join(self.titles)+'\n')

			for item in self.db:
				
				file.write(item)
				for value in self.db[item]:
					file.write(';'+self.db[item][value])
			
				file.write('\n')
		
		
		os.remove(self.path)
		os.rename(p_tmp, self.path)

	def insert(self, jdata):
		for title in self.titles:
			if title not in jdata:
				return False
		item = {}
		for title in self.titles[1:]:
			item[title] = jdata[title]

		self.db[self.titles[0]] = item

		return True

	def remove(self, item):
		if item in self.db:
			del self.db[item]
		else:
			return False

		return True

	def get_list(self, title):
		if title not in self.titles:
			return
		
		colum = []
		for item in self.db:
			colum.append(self.db[item][title])

		return colum

	def get(self, item, title=''):
		if title:
			for data in self.db:
				pass
		elif item in self.db:
			i = self.db[item].copy()
			i[self.titles[0]] = item
			return i


			


			

			 
			 		