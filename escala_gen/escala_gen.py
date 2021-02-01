'''
Programa de geracao automatica de escala de postos de servico
Escalas mensais de bloqueio e bilheteria (PEQ/PEB) por estacao
autor: Arthur Phillip Silva
'''

import random
import json
import sys
import numpy as np
from xls import Gen_xls
from datetime import datetime, timedelta, date
import prob
import os

from database import DB

class Generator:

	def __init__(self, db):
		self.data = db

	def gen(self, station):

		self.estacao = self.data.stations.get(station['station'])
		self.ano = station['year']
		self.mes = self.data.months[station['month']] 
		
		self.funcs = []
		for aso in station['asos']:
			self.funcs.append(self.data.people.get(aso))

		# Primeiro sabado
		self.sabado()
		
		# Gera tabela
		self.gera_tabela()

		Gen_xls(self.escala)

		return "Arquivo gerado no diretorio:\n"

	# Imprime dicionarios
	def print_dic(dic):
		print (json.dumps(dic, sort_keys=True, indent=4))

	# Primeiro sabado do meses
	def sabado(self):
		self.dia_inicio = 1
		self.data_inicio = date(int(self.ano), self.mes['id'], 1)

		# Recupera o primeiro sábado do mês
		# for n in range(1,8):
			# dia_i = date(int(self.ano), self.mes['id'], n)
			# Se sabado
			# if dia_i.weekday() == 5 : 
				# self.dia_inicio = n
				# self.data_inicio = dia_i
				# break

		next_month = self.mes['id']+1
		next_year = int(self.ano)
		if next_month > 12: 
			next_month = 1
			next_year += 1

		# dia_f = date(next_year, next_month, 1)
		# self.data_fim = dia_f + timedelta(days=-1)
		self.data_fim = date(next_year, next_month, 1)
		self.dias = (self.data_fim - self.data_inicio).days

		# Recupera o primeiro sábado do mês seguinte
		# for n in range(1,8):
			# dia_f = date(next_year, next_month, n)
			# Se sabado
			# if dia_f.weekday() == 5 : 
				# self.dias = (dia_f-dia_i).days
				# self.data_fim = dia_f
				# break

	# cria a matriz da escala
	def gera_tabela(self):

		self.escala = []
		# Titulo
		self.escala.append([f"Escala ASO1 - {self.estacao['name']} - {self.mes['name']}", ""])

		# dias = self.mes['dias']

		# Sequencia de dias
		lista_dias = ["", "Dias"]
		for d in range(self.dias):
			lista_dias.append((self.dia_inicio+d-1)%self.mes['dias']+1)
		
		self.escala.append(lista_dias)

		print("inicia em",  self.dia_inicio)
		# Sequencia de dias da semana
		lista_sem = ["", "Ps"]
		data_dia = datetime(int(self.ano), self.mes['id'], self.dia_inicio)
		
		for d in range(self.dias):
			lista_sem.append(self.data.weekdays[int(data_dia.strftime('%w'))])
			data_dia += timedelta(days=1)

		self.escala.append(lista_sem)

		# Distribuicao de postos e folgas
		distrib = self.aloca()

		# Transforma id em sigla; 1->F ; 2->B1 ; 3->Q1 ...
		# Relaciona nomes e escalas
		c = 0
		for f in self.funcs:
			p = []
			f_nome = ' ' if f['alias'][0] == '*' else f['alias']
			p.append(f_nome)
			p.append(f['p'])

			for i in range(self.dias):
				if distrib[c][i] == 0:
					p.append("")
				elif distrib[c][i] == 1:
					p.append("F")
				elif distrib[c][i] == 99:
					p.append("R")
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
		# dias = self.mes['dias']

		# Tabela de distribuicao de postos
		dist_postos = np.zeros((func,self.dias))

		# Tabela de balanceamento de postos
		balanc_postos = np.zeros((func,fixos))

		# Atribui as folgas do funcionario
		f=0
		
		print(date(2019,1,1).day)

		for func in self.funcs:
			print (func)
			
			p = func['p']
			initp = int(self.data.folgas[p])
			if 	int(p) < 4:
				scale = self.data.scales['4x2a']
				init = self.data.folgas['0'] + abs(self.data_inicio - date(2019,1,1)).days 
			elif int(p) < 7:
				scale = self.data.scales['4x2a']
				init = self.data.folgas['00'] + abs(self.data_inicio - date(2019,1,1)).days 
			# elif int(p) < 22:
			# 	scale = self.data.scales['4x2b']
			# 	init = self.data.folgas['00'] + abs(self.data_inicio - date(2019,1,1)).days 
			else:
				print('P fora do escopo')
				exit()

			for d in range(self.dias):
				dist_postos[f][d] = int(scale[(d+init+initp+1)%len(scale)])

			f += 1

		# Cria a sequencia de postos a trabalhar
		postos = []
		i = 2
		for x in range(int(self.estacao['peb'])):
			postos.append(i)
			i += 2
		i = 3
		for x in range(int(self.estacao['peq'])):
			postos.append(i)
			i += 2

		# Lista todas as combinacoes possiveis de postos
		arranjos = prob.gera_p(postos)
		n_arranjos = len(arranjos)

		# Aloca os postos aos funcionarios
		d = a = t = 0
		limite = 1 # Nivel de erro no banlanco de postos
		dtd = 0
		s = 0
		simb = ['|','/','-','\\','-','/'] 
		limite_atual = 0
		while d < self.dias:
			if dtd != d:
				dtd = d
				print ("\nTentando dia", d)
			
			# print('''simb[s]''' '|', '''flush=True,''' end = '')
			s = (s+1)%len(simb)

			# Coloca uma combinacao
			if self.insere_p(dist_postos, d, arranjos[a], postos, balanc_postos):

				# Testa parametros
				if self.checksum(dist_postos, d, balanc_postos, limite):
					limite_atual = 0
					print ("\nDia {} alocado\n".format(d+1))
					d += 1
					t = 0

					# Reduz o erro do balanco
					if limite > 1:
						limite -= 1
				# Remove combinacao se nao passa no teste
				else:
					if limite != limite_atual:
						limite_atual = limite
						print (limite, end=' ')
					self.remove_p(dist_postos, d, arranjos[a], postos, balanc_postos)
					t += 1
			else: 
				t += 1


			# Verifica se tentou todas a possibilidades
			if t == n_arranjos:
				t = 0

				# Aumenta o erro do balanço
				limite += 1
		
			a = (a+1)%n_arranjos

		return dist_postos
	
	# Coloca postos do dia a todos os funcionario
	def insere_p(self, tabela, c, coluna, postos, vistos):
		func = len(tabela)
		fixos = int(func/2)

		# Filtro para evitar repetir posto
		if (c > 0):
			for i in range(len(coluna)):
				if tabela[i][c] == 1:
					if tabela[i+fixos][c-1] == coluna[i]:
						return False
				else:
					if tabela[i][c-1] == coluna[i]:
						return False
		
		for i in range(len(coluna)):
			if tabela[i][c] == 1:
				tabela[i+fixos][c] = coluna[i]
				vistos[i+fixos][postos.index(coluna[i])] += 1
			else:
				tabela[i][c] = coluna[i]
				vistos[i][postos.index(coluna[i])] += 1

		return True

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
			for f in postos:
				if f[c] > 1 and f[c] == f[c-1]:
					resultado = False
					break

		# Verifica se alguem trabalha dois dias intercalados no mesmo posto
		if resultado and (len(postos) > 8) and (c > 1): #and (len(postos) < 12) 
			for f in postos:
				if f[c] > 1 and f[c] == f[c-2]:
					resultado = False
					break

		# Verifica se alguem trabalha 4 dias no mesmo tipo de podto (PEB/PEQ)
		if resultado and (len(postos) > 2) and (c > 2):
			for f in postos:
				if (f[c]>1 and f[c-1]>1 and f[c-2]>1 and f[c-2]>1):
					if (f[c]%2 == f[c-1]%2 and f[c]%2 == f[c-2]%2 and f[c]%2 == f[c-3]%2):
						resultado = False
						break
		return resultado

	# Gera o PDF a partir da planilha
	def pdf(self):
		file_name = ''
		for a in self.escala[0][0]:
			if a == ' ':
				file_name += "\\"

			file_name += a

		print('\nsoffice --convert-to pdf planilha/'+file_name+'.xlsx --outdir pdf/ \n')

		# Codigo valido para LibreOffife
		os.system('soffice --convert-to pdf planilha/'+file_name+'.xlsx --outdir pdf/ ')
		os.system('gvfs-open pdf/'+file_name+'.pdf')


if __name__ == '__main__':

	data = DB()

	e = Generator(data)

	e.esc_auto()
