'''
Programa de geracao automatica de escala de postos de servico
Gerador de probabilidades
autor: Arthur Phillip Silva
'''

import numpy as np
from random import shuffle
import sys

p = []

# Arranja e lista todas as combinacoes
# Gera uma matriz das permutacoes como listas
def permut(rlist):
    if len(rlist) <=1 : 
        return rlist
    if len(rlist) == 2 :
        return [rlist, rlist[::-1]]

    result = []
    for i in range(len(rlist)):
        aux = rlist[:i] + rlist[i+1:] 
        a=rlist[i]
        for b in permut(aux):
            result.append([a]+b) 
    
    return result

# Lista de combinacoes de um vetor
def gera_p(vetor, f_name="data/seqs/"):

	v_name = "".join(map(str,vetor))
	
	f_name += v_name

	try:
		final = []
		# recupera uma sequencia gravada
		with open(f_name,'r') as file: 
			for line in file.readlines():
				final.append(list(map(int,line[:-1].split(','))))
	except:
		# Gera combinacoes
		final = permut(vetor)

		# Embaralha resultado
		shuffle(final)

		# Grava a sequencia
		with open(f_name,'w') as file: 
			for line in final:
				file.write(str(line)[1:-1]+'\n')
		
	return final

if __name__ == "__main__":
	klist = sys.argv[1:]
	gera_p(klist, f_name="")
