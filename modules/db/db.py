import json
from pymongo import MongoClient

# Mensagens padrao
DB_NOT_FOUND = "Banco de dados não encontrado"
INVALID_PARAMETERS = "Parametros invalidos"
NOT_ID = "Item sem ID"

# Inicializa a classe
client = MongoClient('localhost', 27017) # conecta num cliente do MongoDB rodando na sua máquina

test = client['test']['test']
people = client['data']['people']
places = client['data']['places']
scale = client['data']['scale']
time = client['data']['time']

# Insere um funcionario no banco
def insert_employer(employer):
	return insert(people, employer)

# Recupera um funcionario do banco
def get_employer(employer):
	return get(people, employer)

# Recupera todos os funcionarios
def get_all_employers():
	return get_all(people, {})

# Remove um funcionario do banco
def delete_employer(employer):
	return delete(people, employer)






# Recupera um item do DB
def get(db, item):
	if not db or type(item) is not dict:
		print(INVALID_PARAMETERS)
		return
	return db.find_one(item)

# Recupera vários itens do DB
def get_all(db, item):
	if not db or type(item) is not dict:
		print(INVALID_PARAMETERS)
		return
	return list (db.find(item))

# Insere um item do DB
def insert(db, item):
	if not db or type(item) is not dict:
		print(INVALID_PARAMETERS)
		return False
	if not "_id" in item:
		print(NOT_ID)
		return False
	db.insert_one(item)	
	return True

# Atualisa um item do DB
def update(db, item):
	if not db or type(item) is not dict:
		print(INVALID_PARAMETERS)
		return False
	if not "_id" in item:
		print(NOT_ID)
		return False
	old = get(db, {"_id":item["_id"]})
	if not old:
		return False
	new = {}
	for data in item:
		if (data not in old) or (old[data] != item[data]):
			new[data] = item[data]

	if new:
		db.update_one({"_id":item["_id"]}, {'$set': new})
		
	return True
		
# Remove um item do DB
def delete(db, item):
	if not db or type(item) is not dict:
		print(INVALID_PARAMETERS)
		return
	if not "_id" in item:
		print(NOT_ID)
		return
	db.delete_one({"_id": item["_id"]})
	return True


