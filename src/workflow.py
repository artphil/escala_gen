'''
Programa de geracao automatica de escala de postos de servico
Alocador de postos de estacao
autor: Arthur Phillip Silva
''' 
from database import db

class flow:
	def __init__(self):

		# Banco de dados
		try: 
			self.data = db()
		except:
			print("Erro no Banco de Dados")
			quit()