import sqlite3 as sql
import os


class DB: 
	def __init__(self):
		caminho = 'DB/database.db'
		if os.path.exists(caminho):
			self.abrir(caminho)
		else:
			pasta, _ = caminho.split('/')
			if not os.path.exists(pasta):
				print(f'Criando pasta \'{pasta}\'')
				os.makedirs(pasta)
			self.abrir(caminho)
			self.criar_tabelas()

	def abrir(self, caminho):
		print(f'Abrindo Banco de Dados {caminho}.')
		self.conexao = sql.connect(caminho)
		self.cursor = self.conexao.cursor()

	def criar_tabelas(self):
		print('Criando tabelas...')
		with open('data/database/tabelas') as file:
			for create in file.readlines():
				# print(create)
				tabela = create.split()[2]
				print(f'Criando tabela {tabela}')
				self.cursor.execute(create)
				self.conexao.commit()
				# caminho = f'data/database/{tabela}.csv'
				caminho = f'data/database/{tabela}'
				with open(caminho, encoding="utf-8") as f:
					contador = 0
					for data in f.readlines():
						contador += 1
						insert = f"INSERT INTO {tabela} VALUES ({data.strip()})"
						# print(insert)
						self.cursor.execute(insert)
						self.conexao.commit()
					print(f'Inseridos {contador} registros.')
