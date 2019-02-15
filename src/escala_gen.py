'''
Programa de geracao automatica de escala de postos de servico
Escalas mensais de bloqueio e bilheteria (PEQ/PEB) por estacao
autor: Arthur Phillip Silva
'''

import random
import json
import sys
import numpy as np
from planilha import gera_xls
from datetime import datetime, timedelta, date
import prob

class gen:
	
	def esc_auto(self):
	
		# Banco de dados
		with open("data/data.jnew", "r") as read_bd:
			self.bd = json.load(read_bd)

		print('Lendo arquivos')
		if len(sys.argv) <= 1: 
			print('Argumentos necessários')
			return
		if not self.le_dados_auto():
			return
		
		print(self.bd)

		# Escalas vigentes
		self.folgas()

		# Primeiro sabado
		self.sabado()

		# Gera tabela
		print('Gerando tabela')
		self.gera_tabela()

		print('Criando planilha')
		gera_xls(self.escala)

		print ("Arquivo gerado no diretorio: ", self.escala[0][0])

		

	def esc_int(self, bd, estacao, funcs, mes, ano, *msg):

		self.bd = bd
		self.estacao = estacao
		self.funcs = funcs
		self.mes = mes 
		self.ano = ano

		# Escalas vigentes
		self.folgas()

		# Primeiro sabado
		self.sabado()

		# Gera tabela
		self.gera_tabela()

		gera_xls(self.escala)

		return "Arquivo gerado no diretorio:\n"

	# Imprime dicionarios
	def print_dic(dic):
		print (json.dumps(dic, sort_keys=True, indent=4))

	# Importa as definições de estacao.dat
	def le_dados_auto(self):
		with open(sys.argv[1], "r") as entrada:
			# print (sys.argv[1])
			self.estacao = entrada.readline()[:-1]
			self.mes, self.ano = entrada.readline()[:-1].split(' ')
			self.funcs = entrada.readline()[:-1].split(' ')
			# print(self.data['func_nomes'])

		#  Tratamento de erro da entrada
		if not self.estacao in self.bd['est']:
			print("Estação não encontrada", '\n')
			print('error')
			return False
		if not self.mes in self.bd['mes']:
			print("Mes não encontrado", '\n')
			print('error')
			return False
		if len(self.funcs) != 2*len(self.bd['est'][self.estacao]['postos']):
			print("Numero de funcionarios difere dos postos", '\n')
			print('error')
			return False
		
		return True

	# Primeiro sabado do mes
	def sabado(self):
		for n in range(1,8):
			dia = date(int(self.ano), self.bd['mes'][self.mes]['id'], n)
			# Se sabado
			if dia.weekday() == 6 : 
				self.dia_inicio = n-1
				self.data_inicio = dia
				break

	# Escalas vigentes
	def folgas(self):
		with open("data/escala.dat", "r") as read_escala:
			self.esc42 = read_escala.readline().split('	')
			# print(esc42)
			self.esc31 = read_escala.readline().split('	')
			# print(esc31)
			self.esc42aj = read_escala.readline().split('	')
			# print(esc31)

			if not self.esc42 or not self.esc31 or not self.esc42aj:
				print('arquivo de escalas corrompido')

	# cria a matriz da escala
	def gera_tabela(self):

		self.escala = []
		# Titulo
		self.escala.append(["Escala ASO1 - "+self.bd['est'][self.estacao]['nome']+" - "+self.mes, ""])

		dias = self.bd['mes'][self.mes]['dias']

		# Sequencia de dias
		lista_dias = ["", "Dias"]
		for d in range(dias):
			lista_dias.append((self.dia_inicio+d-1)%dias+1)
		
		self.escala.append(lista_dias)

		# Sequencia de dias da semana
		lista_sem = ["", "Ps"]
		data_dia = datetime(int(self.ano), self.bd['mes'][self.mes]['id'], self.dia_inicio)
		
		for d in range(dias):
			lista_sem.append(self.bd['semana'][int(data_dia.strftime('%w'))])
			data_dia += timedelta(days=1)

		self.escala.append(lista_sem)

		# Distribuicao de postos e folgas
		distrib = self.aloca()

		# Transforma id em sigla; 1->F ; 2->B1 ; 3->Q1 ...
		# Relaciona nomes e escalas
		c = 0
		for f in range(len(self.funcs)):
			p = []
			f_nome = self.funcs[f]
			p.append(self.bd['aso'][f_nome]['alias'])
			p.append(self.bd['aso'][f_nome]['p'])

			for i in range(dias):
				if distrib[c][i] == 0:
					p.append("")
				elif distrib[c][i] == 1:
					p.append("F")
				elif (distrib[c][i]%2)==0:
					p.append("B"+str(int(distrib[c][i]/2)))
				else:
					p.append("Q"+str(int(distrib[c][i]/2)))

			c += 1
			self.escala.append(p)

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
		# print(balanc_postos)
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
			# print()
			for f in postos:
				# print(c, f[c], f[c-1])
				if f[c] > 1 and f[c] == f[c-1]:
					resultado = False
					break

		# Verifica se alguem trabalha 4 dias no mesmo tipo de podto (PEB/PEQ)
		if resultado and (c > 2):
			# print()
			for f in postos:
				# print(c, '->', f[c-3], f[c-2], f[c-1], f[c])
				if (f[c]>1 and f[c-1]>1 and f[c-2]>1 and f[c-2]>1):
					if (f[c]%2 == f[c-1]%2 and f[c]%2 == f[c-2]%2 and f[c]%2 == f[c-3]%2):
						resultado = False
						break
		# print(resultado, x)
		return resultado


'''                       Funcoes                              ''' '''
# Imprime dicionarios
def print_dic(dic):
	print (json.dumps(dic, sort_keys=True, indent=4))

# Importa as definições de estacao.dat
def le_dados_auto():
	with open(sys.argv[1], "r") as entrada:
		# print (sys.argv[1])
		data['estacao'] = entrada.readline()[:-1]
		data['mes'], data['ano'] = entrada.readline()[:-1].split(' ')
		data['func_nomes'] = entrada.readline()[:-1].split(' ')
		print(data['func_nomes'])

		for n in range(1,8):
			this_day = datetime(int(data['ano']), bd['mes'][data['mes']]['id'],n)
			if this_day.weekday() == 6:
				data['dia_inicio'] = n
				break

	#  Tratamento de erro da entrada
	if not data['estacao'] in bd['est']:
		print("Estação não encontrada", '\n')
		print('error')
		return False
	if not data['mes'] in bd['mes']:
		print("Mes não encontrado", '\n')
		print('error')
		return False
	if len(data['func_nomes']) != 2*len(bd['est'][data['estacao']]['postos']):
		print("Numero de funcionarios difere", '\n')
		print('error')
		return False
	
	return True

# cria a matriz da escala e exporta como xlsx
def gera_tabela():
	# Titulo
	escala.append(["Escala ASO1 - "+bd['est'][data['estacao']]['nome']+" - "+data['mes'], ""])

	dias = bd['mes'][data['mes']]['dias']

	# Sequencia de dias
	lista_dias = ["", "Dias"]
	for d in range(dias):
		lista_dias.append((data['dia_inicio']+d-1)%dias+1)
	escala.append(lista_dias)

	# Sequencia de dias da semana
	lista_sem = ["", "Ps"]
	data_dia = datetime(int(data['ano']),bd['mes'][data['mes']]['id'],data['dia_inicio'])
	for d in range(dias):
		lista_sem.append(bd['semana'][int(data_dia.strftime('%w'))])
		data_dia += timedelta(days=1)
	escala.append(lista_sem)

	# Distribuicao de postos e folgas
	distrib = aloca()

	# Transforma id em sigla; 1->F ; 2->B1 ; 3->Q1 ...
	# Relaciona nomes e escalas
	c = 0
	for f in range(len(data['func_nomes'])):
		p = []
		f_nome = data['func_nomes'][f]
		p.append(bd['aso'][f_nome]['alias'])
		p.append(bd['aso'][f_nome]['p'])

		for i in range(dias):
			if distrib[c][i] == 0:
				p.append("")
			elif distrib[c][i] == 1:
				p.append("F")
			elif (distrib[c][i]%2)==0:
				p.append("B"+str(int(distrib[c][i]/2)))
			else:
				p.append("Q"+str(int(distrib[c][i]/2)))

		c += 1
		escala.append(p)

# Coloca postos do dia a todos os funcionario
def insere_p(tabela, c, coluna, postos, vistos):
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
def remove_p(tabela, c, coluna, postos, vistos):
	func = len(tabela)
	fixos = int(func/2)
	for i in range(len(coluna)):
		if tabela[i][c] == 1:
			vistos[i+fixos][postos.index(coluna[i])] -= 1
		else:
			vistos[i][postos.index(coluna[i])] -= 1

# Verifica parametros especificados
def checksum(postos, c, tabela, x):
	resultado = True
	# Verifica se postos colocados estão balanceados
	for l in tabela:
		if max(l)-min(l) > x:
			resultado = False
			break

	# Verifica se alguem trabalha dois dias no mesmo posto
	if resultado and (c > 0):
		# print()
		for f in postos:
			# print(c, f[c], f[c-1])
			if f[c] > 1 and f[c] == f[c-1]:
				resultado = False
				break

	# Verifica se alguem trabalha 4 dias no mesmo tipo de podto (PEB/PEQ)
	if resultado and (c > 2):
		# print()
		for f in postos:
			# print(c, '->', f[c-3], f[c-2], f[c-1], f[c])
			if (f[c]>1 and f[c-1]>1 and f[c-2]>1 and f[c-2]>1):
				if (f[c]%2 == f[c-1]%2 and f[c]%2 == f[c-2]%2 and f[c]%2 == f[c-3]%2):
					resultado = False
					break
	# print(resultado, x)
	return resultado

# Distribui postos e folgas
def aloca():
	nomes = data['func_nomes']
	func = len(nomes)		# Quantidade de funcionarioa
	fixos = int(func/2)		# Quantidade de postos
	dias = bd['mes'][data['mes']]['dias']

	# Tabela de distribuicao de postos
	dist_postos = np.zeros((func,dias))
	# Tabela de balanceamento de postos
	balanc_postos = np.zeros((func,fixos))

	# Atribui as folgas do funcionario
	f=0
	ini42 = int(bd['folgas']['0']) + data['dia_inicio'] -1
	ini31 = int(bd['folgas']['00']) + data['dia_inicio'] -1
	for n in nomes:
		p = bd['aso'][n]['p']
		inip = int(bd['folgas'][p])
		# print(len(esc42), len(esc31))
		if p == '7' or p == '8' or p == '9':
			for d in range(dias):
				dist_postos[f][d] = int(esc31[(d+ini31+inip)%21])
			# print(n, p, (ini31+inip)%21, '= (', ini31, '+', inip,')')
		elif int(p) < 16:
			for d in range(dias):
				dist_postos[f][d] = int(esc42[(d+ini42+inip)%84])
			# print(n, p, (ini42+inip)%84, '= (', ini42, '+', inip,')')

		else:
			for d in range(dias):
				dist_postos[f][d] = int(esc42aj[(d+ini31+inip)%21])
		# print(dist_postos[f])
		f += 1

	# Cria a sequencia de postos a trabalhar
	postos = bd['est'][data['estacao']]['postos']
	# Lista todas as combinacoes possiveis de postos
	arranjos = prob.gera_p(postos)
	n_arranjos = len(arranjos)

	# Aloca os postos aos funcionarios
	d = a = t = 0
	limite = 1 # Nivel de erro no banlanco de postos
	while d < dias:
		# Coloca uma combinacao
		insere_p(dist_postos, d, arranjos[a], postos, balanc_postos)
		# print (dist_postos)
		# Testa parametros
		if checksum(dist_postos, d, balanc_postos, limite):
			d += 1
			a = (a+1)%n_arranjos
			t = 0
			# Reduz o erro do balanco
			if limite > 1:
				limite -= 1
		else:
			# Remove combinacao se nao passa no teste
			remove_p(dist_postos, d, arranjos[a], postos, balanc_postos)
			a = (a+1)%n_arranjos
			t += 1
			# Verifica se tentou todas a possibilidades
			if t == n_arranjos:
				t = 0
				# Aumenta o erro do balanço
				limite += 1
	# print(postos)
	# print(balanc_postos)
	return dist_postos

'''
'''                    Programa                           '''
'''
# Banco de dados
with open("data/data.jnew", "r") as read_json:
	bd = json.load(read_json)

# Escalas vigentes
with open("data/escala.dat", "r") as read_escala:
	esc42 = read_escala.readline().split('	')
	# print(esc42)
	esc31 = read_escala.readline().split('	')
	# print(esc31)
	esc42aj = read_escala.readline().split('	')
	# print(esc31)

# print_dic (bd)
escala = []
data = {}

print('Lendo arquivos')
if not le_dados_auto():
	pass

print('Gerando tabela')
gera_tabela()

for h in escala:
	print(h)

print('Criando planilha')
gera_xls(escala)

print ("Arquivo gerado no diretorio: ", escala[0][0])
'''
e = gen()

e.esc_auto()
