'''
Programa de geracao automatica de escala de postos de servico
Gerenciador de Banco de Dados
autor: Arthur Phillip Silva
'''

import os
import json

class db:
	def __init__(self):
		print('empty')
		self.aso = data('data/taso.csv')
		print(self.aso)
		self.est = data('data/test.csv')
		print(self.est)
		self.scl = scale('data/scale.json')
		print(self.scl)
		self.pds = places('data/tpos.json')
		print(self.pds)
		# print(json.dumps(self.pds.db))

		self.folgas = {
				"0": 55, 	"00": 9,
				"1": 0,		"2": 28,	"3": 56,
				"4": 21,	"5": 49,	"6": 77,
				"7": 0,		"8": 7,		"9": 14,
				"10": 42,	"11": 70,	"12": 14,
				"13": 63,	"14": 7,	"15": 35,
				"16": 0,	"17": 7,	"18": 14,
				"19": 0,	"20": 7,	"21": 14
		}

		self.mes = {
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
			"Novembro": {'name':"Novembro",	"dias": 31,"id": 11},
			"Dezembro": {'name':"Dezembro",	"dias": 31,"id": 12}
		}

		self.semana = ["D","S","T","Q","Q","S","S"]


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
			for i in range(len(data)):
				item[self.titles[i]] = data[i]
			self.db[data[0]] = item

	def write(self):
		p_tmp = self.path+'.tmp'

		with open(p_tmp, 'w') as file:

			file.write(';'.join(self.titles)+'\n')

			for item in self.db:
				
				# file.write(item)
				# for value in self.db[item]:
					# file.write(';'+self.db[item][value])

				file.write(';'.join([ self.db[item][value] for value in self.titles ]))
			
				file.write('\n')
		
		
		os.remove(self.path)
		os.rename(p_tmp, self.path)

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

	def get_list(self, title):
		if title not in self.titles:
			return
		
		colum = []
		for item in self.db:
			colum.append(self.db[item][title])

		return colum

	def get(self, item, title=None):
		if title and title in self.titles:
			for data in self.db:
				if self.db[data][title] == item:
					i = self.db[data].copy()
					# i[self.titles[0]] = data
					return i
		elif item in self.db:
			i = self.db[item].copy()
			# i[self.titles[0]] = item
			return i
		else:
			return

	def get_by(self, title):
		if title and title in self.titles:
			colum = {}
			for data in self.db:
				colum[self.db[data][title]] = self.db[data].copy()
				# colum[self.db[data]][self.titles[0]] = data
			
			return colum
		
		else:
			return

	def get_tree(self):
		tree = {
			"1":{
				"a":{},
				"b":{},
				"c":{}
			},
			"2":{
				"a":{},
				"b":{},
				"c":{}
			}
		}
		for data in self.db:
			if self.db[data]["turno"] == "1":
				if self.db[data]["trecho"] == "a":
					tree["1"]["a"][self.db[data]["posto"]] = self.db[data].copy()
				elif self.db[data]["trecho"] == "b":
					tree["1"]["b"][self.db[data]["posto"]] = self.db[data].copy()
				elif self.db[data]["trecho"] == "c":
					tree["1"]["c"][self.db[data]["posto"]] = self.db[data].copy()

			elif self.db[data]["turno"] == "2":
				if self.db[data]["trecho"] == "a":
					tree["2"]["a"][self.db[data]["posto"]] = self.db[data].copy()
				elif self.db[data]["trecho"] == "b":
					tree["2"]["b"][self.db[data]["posto"]] = self.db[data].copy()
				elif self.db[data]["trecho"] == "c":
					tree["2"]["c"][self.db[data]["posto"]] = self.db[data].copy()
			
		return tree

	def set_posto(self,ano,mes,data):
		posicao = (ano-2000)*12 + mes
		print (posicao)

		for a in self.db:
			if self.db[a]["trecho"] == 'd': continue
			j = self.db[a]
			list_size = len(data[ j["turno"] ][ j["trecho"] ][ 0 ])

			# Encontra o posto pela posicao
			if j["pos"]:
				# self.db[a]["posto"] = data[ j["turno"] ][ j["trecho"] ][ (int(j["p"]))%3 ][ (int(j["pos"])+posicao)%list_size ]
				print (data[ j["turno"] ][ j["trecho"] ][ (int(j["p"]))%3 ][ (int(j["pos"])+posicao)%list_size ])
			
		self.save()

	def set_pos(self,ano,mes,data):
		posicao = (ano-2000)*12 + mes
		print (posicao)

		for a in self.db:
			if self.db[a]["trecho"] == 'd': continue
			j = self.db[a]
			list_size = len(data[ j["turno"] ][ j["trecho"] ][ 0 ])

			# Encontra a posicao do posto na lista
			print( j["turno"], j["trecho"], j["p"], (int(j["p"]))%3)
			print(j["posto"],)
			try: print(data[ j["turno"] ][ j["trecho"] ][ (int(j["p"]))%3 ].index(j["posto"]))
			except: print('-')

			if self.db[a]["posto"] in data[ j["turno"] ][ j["trecho"] ][ (int(j["p"]))%3 ]:
				self.db[a]["pos"] = str(list_size + data[ j["turno"] ][ j["trecho"] ][ (int(j["p"]))%3 ].index(j["posto"]) - posicao%list_size)
			
		self.save()

	def save(self):
		self.write()
			
class scale:
	def __init__(self, path):
		self.path = path
		self.read()

	def read(self):
		try:
			file = open(self.path, 'r')
			self.db = json.load(file)
			file.close()
		except:
			print('Arquivo {} não encontrado'.format(path))
			return

class places:
	def __init__(self, path):
		self.path = path
		self.read()

	def read(self):
		try:
			file = open(self.path, 'r')
			self.db = json.load(file)
			file.close()
		except:
			print('Arquivo {} não encontrado'.format(path))
			return

		# print(json.dumps(self.db))
		


