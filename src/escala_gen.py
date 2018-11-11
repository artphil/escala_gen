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
import prob


'''                       Funcoes                              '''
# Imprime dicionarios
def print_dic(dic):
	print (json.dumps(dic, sort_keys=True, indent=4))

# Importa as definições de estacao.dat
def le_dados_auto():
	with open(sys.argv[1], "r") as entrada:
		# print (sys.argv[1])
		data['estacao'] = entrada.readline()[:-1]
		data['mes'] = entrada.readline()[:-1]
		data['dia_inicio'] = int(entrada.readline())
		data['func_nomes'] = entrada.readline()[:-1].split(',')

# cria a matriz da escala e exporta como xlsx
def gera_tabela():
	# Titulo
	escala.append(["Escala ASO1 - " + data['estacao'] + " - " + data['mes'], ""])

	dias = bd['dias_mes'][data['mes']]

	# Sequencia de dias
	lista_dias = ["", "Dias"]
	for d in range(dias):
		lista_dias.append((data['dia_inicio']+d-1)%dias+1)
	escala.append(lista_dias)

	# Sequencia de dias da semana
	lista_sem = ["", "Ps"]
	for d in range(dias):
		lista_sem.append(bd['semana'][d%7])
	escala.append(lista_sem)

	# Distribuicao de postos e folgas
	distrib = aloca()

	# Transforma id em sigla; 1->F ; 2->B1 ; 3->Q1 ...
	# Relaciona nomes e escalas
	c = 0
	for f in range(len(data['func_nomes'])):
		p = []
		f_nome = data['func_nomes'][f]
		p.append(f_nome)
		p.append(bd['pessoal'][f_nome])

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


	print ("Arquivo gerado no diretorio: ")

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
	dias = bd['dias_mes'][data['mes']]

	# Tabela de distribuicao de postos
	dist_postos = np.zeros((func,dias))
	# Tabela de balanceamento de postos
	balanc_postos = np.zeros((func,fixos))

	# Atribui as folgas do funcionario
	f=0
	ini42 = int(bd['folgas']['0']) + data['dia_inicio'] -1
	ini31 = data['dia_inicio'] -1
	for n in nomes:
		p = bd['pessoal'][n]
		inip = int(bd['folgas'][p])
		# print(len(esc42), len(esc31))
		if p == '7' or p == '8' or p == '9':
			for d in range(dias):
				dist_postos[f][d] = int(esc31[(d+ini31+inip)%21])
			# print(n, p, (ini31+inip)%21, '= (', ini31, '+', inip,')')
		else:
			for d in range(dias):
				dist_postos[f][d] = int(esc42[(d+ini42+inip)%84])
			# print(n, p, (ini42+inip)%84, '= (', ini42, '+', inip,')')

		# print(dist_postos[f])
		f += 1

	# Cria a sequencia de postos a trabalhar
	postos = bd['estacao'][data['estacao']]['postos']
	# Lista todas as combinacoes possiveis de postos
	arranjos = prob.gera_p(postos)
	n_arranjos = len(arranjos)

	# Aloca os postos aos funcionarios
	d = a = t = 0
	limite = 1
	while d < dias:
		# Coloca uma combinacao
		insere_p(dist_postos, d, arranjos[a], postos, balanc_postos)
		# print (dist_postos)
		# Testa parametros
		if checksum(dist_postos, d, balanc_postos, limite):
			d += 1
			a = (a+1)%n_arranjos
			t = 0
		else:
			# remove combinacao se nao passa no teste
			remove_p(dist_postos, d, arranjos[a], postos, balanc_postos)
			a = (a+1)%n_arranjos
			t += 1
			if t == n_arranjos:
				t = 0
				limite += 1
	# print(postos)
	# print(balanc_postos)
	return dist_postos


'''                    Programa                           '''

# Banco de dados
with open("data/data.json", "r") as read_json:
	bd = json.load(read_json)

# Escalas vigentes
with open("data/escala.dat", "r") as read_escala:
	esc42 = read_escala.readline().split('	')
	# print(esc42)
	esc31 = read_escala.readline().split('	')
	# print(esc31)

# print_dic (bd)
escala = []
data = {}

le_dados_auto()

gera_tabela()

gera_xls(escala)
