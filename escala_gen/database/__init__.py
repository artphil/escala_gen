import json

from .database import DB 
from .db_estacoes import DB_estacoes 
from .db_pessoas import DB_pessoas 
from .db_postos import DB_postos 
from .db_escalas import DB_escalas 

caminho_escalas = 'data/database/escalas.json'
caminho_meses = 'data/database/meses.json'

class Dados:
	def __init__(self):
		db = DB()
		self.estacoes = DB_estacoes(db)
		self.postos = DB_postos(db)
		self.escalas = DB_escalas(db)
		self.pessoas = DB_pessoas(db)
		self.dias_semana = ["D","S","T","Q","Q","S","S"]
		# with open(caminho_escalas) as f:
		# 	self.escalas = json.load(f)
		try: 
			print('Carregando escalas ...')
			with open(caminho_escalas) as f:
				self.escala_p = json.load(f)
		except:
			print('Escalas não encontradas.')
			quit()
		try: 
			print('Carregando meses ...')
			with open(caminho_meses, encoding='utf8') as f:
				self.meses = json.load(f)
		except:
			print('Meses não encontrados.')
			quit()
