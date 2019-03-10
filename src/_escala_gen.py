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
import os
from database import db

class gen:
	
	def esc_auto(self):
		
		# Banco de dados
		try: 
			self.data = db()
		except:
			print("Erro no Banco de Dados")
			quit()
		
		print('Lendo arquivos')
		if len(sys.argv) <= 1: 
			print('Falta arquivo "estação"')
			quit()

		if not self.read_auto():
			quit()
		
		# Escalas vigentes
		self.folgas()

		# Primeiro sabado
		self.sabado()

		# Gera tabela
		print('Gerando tabela')
		self.gera_tabela()

		print('Criando planilha')
		gera_xls(self.escala)

		print ("\nArquivo gerado no diretorio: ", self.escala[0][0])

		self.pdf()

		print ("PDF criado")
		

	def esc_int(self, bd, estacao, fids, mes, ano, *msg):

		self.data = bd
		self.estacao = self.data.get(estacao)
		self.funcs = []
		for fid in fids:
			self.funcs.append(self.data.aso.get(fid))
		self.mes = self.data.mes[mes] 
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
	def read_auto(self):
		with open(sys.argv[1], "r") as entrada:
			# print (sys.argv[1])
			self.estacao = self.data.est.get(entrada.readline()[:-1])
			mes, self.ano = entrada.readline()[:-1].split(' ')
			self.mes = self.data.mes[mes] 
			self.funcs = []
			for fid in entrada.readline()[:-1].split(' '):
				self.funcs.append(self.data.aso.get(fid))

		#  Tratamento de erro da entrada
		if not self.estacao:
			print("Estação não encontrada", '\n')
			print('error')
			return False
		if not self.mes:
			print("Mes não encontrado", '\n')
			print('error')
			return False, 
		postos = int(self.estacao['peb'])+int(self.estacao['peq'])
		if len(self.funcs) != 2*postos:
			print("Numero de funcionarios difere do numero de postos", '\n')
			print('error')
			return False
		
		return True

	# Primeiro sabado do mes
	def sabado(self):
		for n in range(1,8):
			dia = date(int(self.ano), self.mes['id'], n)
			# Se sabado
			if dia.weekday() == 6 : 
				self.dia_inicio = n-1
				self.data_inicio = dia
				break

	# cria a matriz da escala
	def gera_tabela(self):

		self.escala = []
		# Titulo
		self.escala.append(["Escala ASO1 - "+self.estacao['name']+" - "+self.mes['name'], ""])

		dias = self.mes['dias']

		# Sequencia de dias
		lista_dias = ["", "Dias"]
		for d in range(dias):
			lista_dias.append((self.dia_inicio+d-1)%dias+1)
		
		self.escala.append(lista_dias)

		# Sequencia de dias da semana
		lista_sem = ["", "Ps"]
		data_dia = datetime(int(self.ano), self.mes['id'], self.dia_inicio)
		
		for d in range(dias):
			lista_sem.append(self.data.semana[int(data_dia.strftime('%w'))])
			data_dia += timedelta(days=1)

		self.escala.append(lista_sem)

		# Distribuicao de postos e folgas
		distrib = self.aloca()

		# Transforma id em sigla; 1->F ; 2->B1 ; 3->Q1 ...
		# Relaciona nomes e escalas
		c = 0
		for f in self.funcs:
			p = []
			p.append(f['alias'])
			p.append(f['p'])

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
		dias = self.mes['dias']

		# Tabela de distribuicao de postos
		dist_postos = np.zeros((func,dias))

		# Tabela de balanceamento de postos
		balanc_postos = np.zeros((func,fixos))

		# Atribui as folgas do funcionario
		f=0
		
		print(date(2019,1,1).day)

		for func in self.funcs:
			p = func['p']
			initp = int(self.data.folgas[p])
			if p == '7' or p == '8' or p == '9':
				scale = self.data.scl['3x1']
				init = self.data.folgas['00'] + abs(self.data_inicio - date(2019,1,1)).days 
			elif int(p) < 16:
				scale = self.data.scl['4x2']
				init = self.data.folgas['0'] + abs(self.data_inicio - date(2019,1,1)).days 
			elif int(p) < 19:
				scale = self.data.scl['4x2a']
				init = self.data.folgas['00'] + abs(self.data_inicio - date(2019,1,1)).days 
			elif int(p) < 22:
				scale = self.data.scl['4x2b']
				init = self.data.folgas['00'] + abs(self.data_inicio - date(2019,1,1)).days 
			else:
				print('P fora do escopo')
				exit()

			for d in range(dias):
				dist_postos[f][d] = int(scale[(d+init+initp)%len(scale)])

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
		while d < dias:
			print ("\nTentando dia", d)

			# Coloca uma combinacao
			if self.insere_p(dist_postos, d, arranjos[a], postos, balanc_postos):

				# Testa parametros
				if self.checksum(dist_postos, d, balanc_postos, limite):
					print ("\nDia {} alocado\n".format(d+1))
					d += 1
					t = 0

					# Reduz o erro do balanco
					if limite > 1:
						limite -= 1
				else:
					# Remove combinacao se nao passa no teste
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

		print('\nsoffice --convert-to pdf planilha/'+file_name+'.xls --outdir pdf/ \n')

		# Codigo valido para LibreOffife
		os.system('soffice --convert-to pdf planilha/'+file_name+'.xls --outdir pdf/ ')
		os.system('gvfs-open pdf/'+file_name+'.pdf')


if __name__ == '__main__':
	
	e = gen()

	e.esc_auto()
