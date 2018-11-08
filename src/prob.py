import numpy as np
from random import shuffle

p = []

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


def gera_p(vetor):
	global p
	tam = len(vetor)
	vistos = np.zeros(tam)
	aux = []
	final = []

	gerador(final, vetor, vistos, aux)

	shuffle(final)
	p = final
	return final
