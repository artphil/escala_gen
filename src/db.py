'''
Programa de geracao automatica de escala de postos de servico
Gerenciador de Banco de Dados
autor: Arthur Phillip Silva
'''

import json
from pymongo import MongoClient

class db:
	# Mensagens padrao
	DB_NOT_FOUND = "Banco de dados não encontrado"
	INVALID_PARAMETERS = "Parametros invalidos"
	NOT_ID = "Item sem ID"
	
	# Inicializa a classe
	def __init__(self,HOST='localhost',PORT=27017):
		try:
			self.client = MongoClient(HOST, PORT) # conecta num cliente do MongoDB rodando na sua máquina
		except:
			print(self.DB_NOT_FOUND)
			quit()
	
	# Recupera um item do DB
	def get(self, db, item):
		if not db or type(item) != type(dict()):
			print(self.INVALID_PARAMETERS)
			return
		return db.find_one(item)
	
	# Recupera vários itens do DB
	def get_all(self, db, item):
		if not db or type(item) != type(dict()):
			print(self.INVALID_PARAMETERS)
			return
		return db.find_many(item)
	
	# Insere um item do DB
	def insert(self, db, item):
		if not db or type(item) != type(dict()):
			print(self.INVALID_PARAMETERS)
			return
		if not "_id" in item:
			print(self.NOT_ID)
			return
		db.insert_one(item)	

	# Atualisa um item do DB
	def update(self, db, item):
		if not db or type(item) != type(dict()):
			print(self.INVALID_PARAMETERS)
			return
		if not "_id" in item:
			print(self.NOT_ID)
			return
		old = self.get(db, {"_id":item["_id"]})
		if not old:
			return
		new = {}
		for data in item:
			if (data not in old) or (old[data] != item[data]):
				new[data] = item[data]
		db.update_one({"_id":item["_id"]}, {'$set': new})

	# Remove um item do DB
	def delete(self, db, item):
		if not db or type(item) != type(dict()):
			print(self.INVALID_PARAMETERS)
			return
		if not "_id" in item:
			print(self.NOT_ID)
			return
		album.delete_one({"_id": item["_id"]})




		# ''' ------------------- ^^^ Updated ^^^ ------------------- '''
				
				
				
				
				
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
		


