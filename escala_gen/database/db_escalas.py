from .db_base import DB_base

class DB_escalas(DB_base):
	
	def __init__(self, db):
		super().__init__(db, 'escalas', 'codigo')

	def busca_por_estacao(self, estacao, turno):
		return self.busca_por({'sigla': f"LIKE '%{estacao}%'", 'turno': turno}, 'sigla')