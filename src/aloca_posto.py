'''
Programa de geracao automatica de escala de postos de servico
Alocador de postos
autor: Arthur Phillip Silva
''' 


class alocador:

	def__init__(self, bd):
		self.bd = bd
		
	# Distribui postos e folgas
	def aloca(self):
		func = len(self.funcs)	# Quantidade de funcionarios
		fixos = int(func/2)		# Quantidade de postos
		dias = self.bd['mes'][self.mes]['dias']

		# Tabela de distribuicao de postos
		dist_postos = np.zeros((func,dias))

		# Tabela de balanceamento de postos
		balanc_postos = np.zeros((func,fixos))

		# Atribui as folgas do funcionario
		f=0
		ini42 = self.bd['folgas']['0'] + abs(self.data_inicio - date(2019,1,1)).days 
		ini31 = self.bd['folgas']['00'] + abs(self.data_inicio - date(2019,1,1)).days 
		
		print(date(2019,1,1).day)

		for n in self.funcs:
			p = self.bd['aso'][n]['p']
			inip = int(self.bd['folgas'][p])
			# print(len(esc42), len(self.esc31))
			if p == '7' or p == '8' or p == '9':
				for d in range(dias):
					dist_postos[f][d] = int(self.esc31[(d+ini31+inip)%21])
				# print(n, p, (ini31+inip)%21, '= (', ini31, '+', inip,')')
			elif int(p) < 16:
				for d in range(dias):
					dist_postos[f][d] = int(self.esc42[(d+ini42+inip)%84])
				# print(n, p, (ini42+inip)%84, '= (', ini42, '+', inip,')')
			else:
				for d in range(dias):
					dist_postos[f][d] = int(self.esc42aj[(d+ini31+inip)%21])
			# print(dist_postos[f])
			f += 1

		# Cria a sequencia de postos a trabalhar
		postos = self.bd['est'][self.estacao]['postos']

		# Lista todas as combinacoes possiveis de postos
		arranjos = prob.gera_p(postos)
		n_arranjos = len(arranjos)

		# Aloca os postos aos funcionarios
		d = a = t = 0
		limite = 1 # Nivel de erro no banlanco de postos
		while d < dias:
			# Coloca uma combinacao
			self.insere_p(dist_postos, d, arranjos[a], postos, balanc_postos)
			# print (dist_postos)
			print ("\nTentando dia", d)
			print ("Teste:", t, '/', n_arranjos,'\n')
			# Testa parametros
			if self.checksum(dist_postos, d, balanc_postos, limite):
				d += 1
				a = (a+1)%n_arranjos
				t = 0
				# Reduz o erro do balanco
				if limite > 1:
					limite -= 1
			else:
				# Remove combinacao se nao passa no teste
				self.remove_p(dist_postos, d, arranjos[a], postos, balanc_postos)
				a = (a+1)%n_arranjos
				t += 1
				# Verifica se tentou todas a possibilidades
				if t == n_arranjos:
					t = 0
					# Aumenta o erro do balanço
					limite += 1
			# print(postos)
			print(balanc_postos)
		return dist_postos
	
	# Coloca postos do dia a todos os funcionario
	def insere_p(self, tabela, c, coluna, postos, vistos):
		func = len(tabela)
		fixos = int(func/2)
		for i in range(len(coluna)):
			if tabela[i][c] == 1:
				tabela[i+fixos][c] = coluna[i]
				vistos[i+fixos][postos.index(coluna[i])] += 1
			else:
				tabela[i][c] = coluna[i]
				vistos[i][postos.index(coluna[i])] += 1

	# Retira postos do dia de todos os funcionario
	def remove_p(self, tabela, c, coluna, postos, vistos):
		func = len(tabela)
		fixos = int(func/2)
		for i in range(len(coluna)):
			if tabela[i][c] == 1:
				vistos[i+fixos][postos.index(coluna[i])] -= 1
			else:
				vistos[i][postos.index(coluna[i])] -= 1

	# Verifica parametros especificados
	def checksum(self, postos, c, tabela, x):
		resultado = True
		# Verifica se postos colocados estão balanceados
		for l in tabela:
			if max(l)-min(l) > x:
				resultado = False
				break

		# Verifica se alguem trabalha dois dias no mesmo posto
		if resultado and (c > 0):
			print('		dup')
			for f in postos:
				# print(c, f[c], f[c-1])
				if f[c] > 1 and f[c] == f[c-1]:
					resultado = False
					break

		# Verifica se alguem trabalha dois dias intercalados no mesmo posto
		if resultado and (len(postos) > 4) and (c > 1):
			print('		inter')
			for f in postos:
				# print(c, f[c], f[c-1])
				if f[c] > 1 and f[c] == f[c-2]:
					resultado = False
					break

		# Verifica se alguem trabalha 4 dias no mesmo tipo de podto (PEB/PEQ)
		if resultado and (len(postos) > 2) and (c > 2):
			print('		4 dias')
			for f in postos:
				# print(c, '->', f[c-3], f[c-2], f[c-1], f[c])
				if (f[c]>1 and f[c-1]>1 and f[c-2]>1 and f[c-2]>1):
					if (f[c]%2 == f[c-1]%2 and f[c]%2 == f[c-2]%2 and f[c]%2 == f[c-3]%2):
						resultado = False
						break
		print(resultado, x)
		return resultado

