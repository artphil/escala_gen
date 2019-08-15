'''
Programa de geracao automatica de escala de postos de servico
Testes unitarios
autor: Arthur Phillip Silva
'''
# Bibliotecas Python
import unittest
from random import random
from pymongo import MongoClient

# Bibliotecas do programa
from db import db


class Test_db_class(unittest.TestCase):

	# Carregamento do banco dde dados
	def test_db(self):
		database = db()
		
		self.assertTrue(database.client.server_info())

	def test_insert(self):
		database = db()

		data = {"data":"data", "teste":"teste"}
		count_DB_before = database.test.count_documents({}) 
		data["_id"] = count_DB_before+1

		database.insert(database.test, data)
		count_DB_after = database.test.count_documents({}) 

		self.assertTrue(count_DB_before+1 == count_DB_after)

	def test_get(self):
		database = db()
		data_1 = database.get(database.test, {})
		data_2 = MongoClient().test.test.find_one({"data":"data"})

		self.assertDictEqual(data_1,data_2)

	def test_update(self):
		database = db()
		data_1 = MongoClient().test.test.find_one({"data":"data"})
		data_1["update"] = random()

		database.update(database.test, data_1)
		data_2 = MongoClient().test.test.find_one({"_id":data_1["_id"]})

		self.assertDictEqual(data_1,data_2)

	def test_delete(self):
		database = db()
		count_DB = database.test.count_documents({}) 
		data = MongoClient().test.test.find_one({"_id":count_DB})

		while not data:
			count_DB -= 1
			data = MongoClient().test.test.find_one({"_id":count_DB})

		database.delete(database.test, data)
		data = MongoClient().test.test.find_one({"_id":count_DB})

		self.assertFalse(data)
	def test_get_all(self):
		database = db()
		data_1 = database.get_all(database.test, {"data":"data"})
		data_2 = MongoClient().test.test.count_documents({})

		self.assertEqual(len(data_1),data_2)

	def test_employer(self):
		database = db()

		data = {"_id":123, "name":"data", "teste":"teste"}
		
		self.assertFalse(database.get_employer(data))

		count_1 = database.people.count_documents({}) 
		self.assertTrue(database.insert_employer(data))
		count_2 = database.people.count_documents({}) 
		self.assertTrue(count_1+1 == count_2)

		test = database.get_employer(data)
		self.assertDictEqual(data,test)

		self.assertTrue(database.delete_employer(data))

		self.assertFalse(database.get_employer(data))

		count_3 = len(database.get_all_employers())
		self.assertTrue(count_1 == count_3)




# Execucao
if __name__ == '__main__':
    unittest.main()
