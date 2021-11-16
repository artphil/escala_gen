from .db_base import DB_base

class DB_pessoas(DB_base):
	
	def __init__(self, db):
		super().__init__(db, 'pessoas', 'apelido')

	def nomes(self,turno=None,trecho=None):
		parametros={}
		if trecho:
			parametros['trecho'] = trecho
		if turno:
			parametros['turno'] = turno
		return self.busca(campos=['apelido'],parametros=parametros, ordem='apelido')