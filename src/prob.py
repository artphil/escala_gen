'''
Programa de geracao automatica de escala de postos de servico
Gerador de probabilidades
autor: Arthur Phillip Silva
'''

import numpy as np
from random import shuffle

p = []

# Arranja e lista todas as combinacoes
def gerador(final, vetor, vistos, aux):
	tam = len(vetor)

	if len(aux) == tam:
		# print(aux)
		final.append(aux)
	else:
		for i in range(tam):
			if vistos[i] == 0:
				a = aux.copy()
				v = vistos.copy()
				a.append(vetor[i])
				v[i] = 1
				gerador(final, vetor, v, a)

# Lista de combinacoes de um vetor
def gera_p(vetor):
	global p
	v_name = ""
	for i in vetor:
		v_name += str(i)
	
	print(v_name)
	f_name = "data/seqs/"+v_name
	print(f_name)
	try:
		final = []
		# recupera uma sequencia gravada
		file = open(f_name,"r")
		for line in file.readlines():
			final.append([int(x) for x in line.split(',')])
	except:
		tam = len(vetor)
		vistos = np.zeros(tam)
		aux = []
		final = []

		# Gera combinacoes
		gerador(final, vetor, vistos, aux)

		# Embaralha resultado
		shuffle(final)

		# Grava a sequencia
		file = open(f_name,"w")
		for line in final:
			file.write(str(line)[1:-1]+"\n")
		
	p = final
	return final
