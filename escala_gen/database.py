'''
Programa de geracao automatica de escala de postos de servico
Gerenciador de Banco de Dados
autor: Arthur Phillip Silva
'''

import os
import json

path_source = r'data/'
file_people = 'pessoas.csv'
file_stations = 'estacoes.csv'
file_scales = 'escalas.json'

class DB:
	def __init__(self):
		try: 
			print('Carregando dados de pessoas ...')
			self.people = Data(path_source+file_people)
		except:
			print('Dados de pessoas não encontrado.')
			quit()

		try: 
			print('Carregando dados de estações ...')
			self.stations = Data(path_source+file_stations)
		except:
			print('Dados de estações não encontrado.')
			quit()

		try: 
			print('Carregando escalas ...')
			with open(path_source+file_scales, 'r') as f:
				self.scales = json.load(f)
		except:
			print('Escalas não encontradas.')
			quit()

		self.folgas = {
				# "0": 55, 	"00": 9,
				# "1": 0,		"2": 28,	"3": 56,
				# "4": 21,	"5": 49,	"6": 77,
				"0": 7, 	"00": 9,
				"1": 1,		"2": 8,		"3": 15,
				"4": 0,		"5": 7,		"6": 14,
				"7": 0,		"8": 7,		"9": 14,
				"10": 42,	"11": 70,	"12": 14,
				"13": 63,	"14": 7,	"15": 35,
				"16": 0,	"17": 7,	"18": 14,
				"19": 0,	"20": 7,	"21": 14
		}

		self.months = {
			"Janeiro": 	{'name':"Janeiro",	"dias": 31,"id": 1},
			"Fevereiro":{'name':"Fevereiro","dias": 28,"id": 2},
			"Março": 	{'name':"Março",	"dias": 31,"id": 3},
			"Abril": 	{'name':"Abril",	"dias": 30,"id": 4},
			"Maio": 	{'name':"Maio",		"dias": 31,"id": 5},
			"Junho": 	{'name':"Junho",	"dias": 30,"id": 6},
			"Julho": 	{'name':"Julho",	"dias": 31,"id": 7},
			"Agosto": 	{'name':"Agosto",	"dias": 31,"id": 8},
			"Setembro": {'name':"Setembro",	"dias": 30,"id": 9},
			"Outubro": 	{'name':"Outubro",	"dias": 31,"id": 10},
			"Novembro": {'name':"Novembro",	"dias": 30,"id": 11},
			"Dezembro": {'name':"Dezembro",	"dias": 31,"id": 12}
		}

		self.weekdays = ["D","S","T","Q","Q","S","S"]


class Data:
	def __init__(self, path):
		self.path = path
		self.load()

	def load(self):
		try:
			file = open(self.path, 'r', encoding="utf-8").readlines()
		except:
			print(f'Arquivo {self.path} não encontrado')
			return

		self.titles = file[0][:-1].split(';')
		
		self.db = {}

		for line in file[1:]:
			item = {}
			data = line[:-1].split(';')
			for i in range(len(data)):
				item[self.titles[i]] = data[i]
			self.db[data[0]] = item

	def save(self):
		p_tmp = self.path+'.tmp'

		with open(p_tmp, 'w') as file:

			file.write(';'.join(self.titles)+'\n')

			for item in self.db:

				file.write(';'.join([ self.db[item][value] for value in self.titles ]))
			
				file.write('\n')
		
		
		os.remove(self.path)
		os.rename(p_tmp, self.path)

	def get(self, item, title=None):
		if title and title in self.titles:
			for data in self.db:
				if self.db[data][title] == item:
					i = self.db[data].copy()
					return i
		elif item in self.db:
			i = self.db[item].copy()
			return i
		else:
			return

	def get_list(self, title):
		if title not in self.titles:
			return
		
		colum = []
		for item in self.db:
			colum.append(self.db[item][title])

		return colum

	def insert(self, jdata):
		for title in self.titles:
			if title not in jdata:
				return False
		item = {}
		for title in self.titles:
			item[title] = jdata[title]

		self.db[jdata[self.titles[0]]] = item

		print(item)
		self.save()
		return True

	def remove(self, item):
		if item in self.db:
			del self.db[item]
		else:
			return False

		self.save()
		return True