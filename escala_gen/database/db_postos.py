from .db_base import DB_base

class DB_postos(DB_base):
	
	def __init__(self, db):
		super().__init__(db, 'postos', 'codigo')

	def busca_por_estacao(self, estacao_id, turno, ordem=''):
		return self.busca_por({'estacao_id': estacao_id, 'turno': turno}, ordem)

