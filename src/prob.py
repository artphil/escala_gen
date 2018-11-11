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
	tam = len(vetor)
	vistos = np.zeros(tam)
	aux = []
	final = []

	# Gera combinacoes
	gerador(final, vetor, vistos, aux)

	# Embaralha resultado
	shuffle(final)

	p = final
	return final
