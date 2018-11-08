import random
import json
import sys
import numpy as np
from planilha import gera_xls
import prob


'''                       Funcoes                              '''

def print_dic(dic):
	print (json.dumps(dic, sort_keys=True, indent=4))

def le_dados():
	data['estacao'] = input("nome estacao: ")
	data['dia_inicio'] = int(input("dia da mudança: "))
	data['func_num'] = int(input("numero de funcionarios: "))
	data['mes'] = input("mes: ")

	func_nomes = []
	func_Ps = []
	for i in range(data['func_num']):
		func_nomes.append(input("nome: "))
		func_Ps.append(int(input("P: ")))

	data['func_nomes'] = func_nomes
	data['func_Ps'] = func_Ps


# Importa as definições de setup.dat
def le_dados_auto():
	with open(sys.argv[1], "r") as entrada:
		print (sys.argv[1])
		data['estacao'] = entrada.readline()[:-1]
		data['mes'] = entrada.readline()[:-1]
		data['dia_inicio'] = int(entrada.readline())
		data['func_nomes'] = entrada.readline()[:-1].split(',')

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

	distrib = aloca()
	postos = []
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

def remove_p(tabela, c, coluna, postos, vistos):
	func = len(tabela)
	fixos = int(func/2)
	for i in range(len(coluna)):
		if tabela[i][c] == 1:
			vistos[i+fixos][postos.index(coluna[i])] -= 1
		else:
			vistos[i][postos.index(coluna[i])] -= 1

def checksum(tabela, x):
	resultado = True
	for l in tabela:
		if max(l)-min(l) > x:
			resultado = False
			break

	'''
	if resultado:
		for i in range(int(len(tabela[0])/2)):
			if max([l[i] for l in tabela]) - min([l[i] for l in tabela]) > x:
				resultado = False
				break
	'''
	# print(resultado, x)
	return resultado

def aloca():
	nomes = data['func_nomes']
	func = len(nomes)
	fixos = int(func/2)
	dias = bd['dias_mes'][data['mes']]

	dist_postos = np.zeros((func,dias))
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
		else:
			for d in range(dias):
				dist_postos[f][d] = int(esc42[(d+ini42+inip)%84])

		print(n, p, (ini42+inip)%84)
		print(dist_postos[f])
		f += 1

	# Cria a sequencia de postos a trabalhar
	postos = bd['estacao'][data['estacao']]['postos']
	arranjos = prob.gera_p(postos)
	n_arranjos = len(arranjos)

	d = a = t = 0
	limite = 1
	while d < dias:
		insere_p(dist_postos, d, arranjos[a], postos, balanc_postos)
		# print (dist_postos)
		if checksum(balanc_postos, limite):
			d += 1
			a = (a+1)%n_arranjos
			t = 0
		else:
			remove_p(dist_postos, d, arranjos[a], postos, balanc_postos)
			a = (a+1)%n_arranjos
			t += 1
			if t == n_arranjos:
				t = 0
				limite += 1

	print(balanc_postos)
	return dist_postos

def preenche():
	nomes = data['func_nomes']
	func = len(nomes)
	func_fixos = int(func/2)
	dias = bd['dias_mes'][data['mes']]

	# postos_trab = np.zeros((func,func_fixos))

	dist_postos = np.zeros((func,dias))

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
		else:
			for d in range(dias):
				dist_postos[f][d] = int(esc42[(d+ini42+inip)%84])

		f += 1

	# Cria a sequencia de postos a trabalhar
	postos = bd['estacao'][data['estacao']]['postos']

	print (postos)

	pula = 0
	posto = 0
	for f in range(func_fixos):
		n_folgas = 0
		for d in range(dias):
			if dist_postos[f][d] == 1:
				n_folgas += 1
				pula += 1
				# print(f+d-n_folgas+pula)
				dist_postos[f+func_fixos][d] = postos[(f+d-n_folgas+pula)%len(postos)]
			else:
				pula = 0
				# print(f+d-n_folgas)
				dist_postos[f][d] = postos[(f+d-n_folgas)%len(postos)]

	# print (dist_postos)
	return dist_postos



'''                    Programa                           '''


with open("data/data.json", "r") as read_json:
	bd = json.load(read_json)

with open("data/escala.dat", "r") as read_escala:
	esc42 = read_escala.readline().split('	')
	print(esc42)
	esc31 = read_escala.readline().split('	')
	print(esc31)

# print_dic (bd)
escala = []
data = {}

le_dados_auto()

gera_tabela()

gera_xls(escala)
