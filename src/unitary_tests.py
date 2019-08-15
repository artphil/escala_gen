'''
Programa de geracao automatica de escala de postos de servico
Testes unitarios
autor: Arthur Phillip Silva
'''
# Bibliotecas Python
import unittest
from pymongo import MongoClient

# Bibliotecas do programa
from db import db


class Test_db_class(unittest.TestCase):
	# Carregamento do banco dde dados
	def test_db(self):
		self.client = MongoClient('localhost', 27017)
		self.db = db()
		self.assertTrue(self.client.server_info())
		self.assertTrue(self.db.client.server_info())


# Execucao
if __name__ == '__main__':
    unittest.main()
