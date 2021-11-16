from .database import DB 
from .db_estacoes import DB_estacoes 
from .db_pessoas import DB_pessoas 
from .db_postos import DB_postos 
from .db_escalas import DB_escalas 


class Dados:
	def __init__(self):
		db = DB()
		self.estacoes = DB_estacoes(db)
		self.postos = DB_postos(db)
		self.escalas = DB_escalas(db)
		self.pessoas = DB_pessoas(db)
