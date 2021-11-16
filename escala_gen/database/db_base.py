class DB_base:

	def __init__(self, db, tabela, chave):
		self.db = db
		self.tabela = tabela
		self.chave = chave

	def to_json(self, one=False):
		linhas = self.db.cursor.fetchall()
		colunas = self.colunas()
		data = {}
		for l in linhas:
			d = {}
			for i, c in enumerate(colunas):
				d[c] = l[i] 
			data[str(d[self.chave])] = d
		return data
	
	def colunas(self):
		return [c[0] for c in self.db.cursor.description]

	def busca(self, campos=[], parametros={}, ordem='', reverso=False, grupos=[]):
		colunas = '*' if not campos else 'id,'+','.join(campos)
		ordenacao = ''
		condicao = ''
		primeiro = True
		for chave, valor in parametros.items():
			if primeiro:
				primeiro = False
				condicao += f'WHERE {chave}={valor}'
			else:
				condicao += f' AND {chave}={valor}'
		if ordem:
			ordenacao = f'ORDER BY {ordem}'
			if reverso:
				ordenacao += ' DESC'
		agrupamento = ''
		if grupos:
			agrupamento = 'GROUP BY '+ ','.join(grupos)

		query = f'SELECT {colunas} FROM {self.tabela} {condicao} {agrupamento} {ordenacao};'
		self.db.cursor.execute(query)
		return self.to_json()

	def busca_tudo(self, ordem='', reverso=False):
		return self.busca(ordem=ordem, reverso=reverso)
		
	def busca_por_id(self, id):
		item = self.busca(parametros={'id':id})
		return list(item.values())[0]

	def busca_por(self, parametros, ordem='', reverso=False):
		return self.busca(parametros=parametros, ordem=ordem, reverso=reverso)
	
	def atualiza(self, id, dados):
		campos = []
		for chave, valor in dados.items():
			if type(valor) == str:
				valor = f"'{valor}'"
			campos.append(f'{chave} = {valor}')
		campos_alterados = ','.join(campos)

		query = f'UPDATE {self.tabela} SET {campos_alterados} WHERE id = {id};'
		self.db.cursor.execute(query)
		self.db.conexao.commit()

	def insere(self, dados):
		self.busca()
		colunas = self.colunas()
		colunas.remove('id')
		colunas.remove('ordem')
		valores = []
		print('col:', colunas)
		for chave in colunas:
			valor = "'"+dados[chave]+"'" if type(dados[chave]) == str else str(dados[chave])
			valores.append(valor)
		query =  f"INSERT INTO {self.tabela} ({','.join(colunas)}) VALUES ({','.join(valores)})"
		self.db.cursor.execute(query)
		self.db.conexao.commit()

	def remove(self, id):
		query = f'DELETE FROM {self.tabela} WHERE id = {id};'
		self.db.cursor.execute(query)
		self.db.conexao.commit()
