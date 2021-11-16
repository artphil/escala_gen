from .db_base import DB_base

class DB_estacoes(DB_base):
	
	def __init__(self, db):
		super().__init__(db, 'estacoes', 'sigla')

