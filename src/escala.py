from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, PatternFill
from openpyxl.utils import column_index_from_string

import numpy as np

escala = []

def imprime(tabela):
	# Definindo planilha
	wb = Workbook()
	ws = wb.active
	ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE

	# Titulo da aba
	ws.title = 'Escala'

	# Definindo largura das células das sequência
	for i in range(1,34):
	    # ws.col(i).width = 800
	    # ws.row(i-1).height = 300
		pass

	# Preenchendo com dados da tabela
	i = 0;
	for linha in tabela:
		ws.append(linha)

	# Aplica merge as celulas do titulo
	ws.merge_cells("A1:AG1")

	ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

	for linha in ws['A2:AG15']:
		ws.row_dimensions[linha[0].row].height = 20.0
		for celula in linha:
			celula.alignment = Alignment(horizontal='center', vertical='center')
			if celula.col_idx < 3 or celula.row < 4:
				# print (column_index_from_string[celula.column])
				celula.font = Font(bold=True)
			if celula.value == 'F':
				celula.fill = PatternFill("solid", fgColor="000000")
				celula.font = Font(color='FFFFFF')

	ws.row_dimensions[ws['A1'].row].height = 30.0

	for col in ws['B:AG']:
	     ws.column_dimensions[col[0].column].width = 4.0

	# Salvando
	wb.save(filename='escala_ASO1.xlsx')



def gera_tabela():

	estacao = "Central" #input("nome estacao: ")
	escala.append(["Escala ASO1 - " + estacao, ""])

	dia = 3 #int(input("dia da mudança: "))
	lista_dias = []
	lista_dias.append("Dias")
	lista_dias.append("P")
	for d in range(31):
		lista_dias.append((dia+d-1)%31+1)
	escala.append(lista_dias)

	semana = ["D", "S", "T", "Q", "Q", "S", "S", "D"]
	lista_sem = []
	lista_sem.append(" ")
	lista_sem.append(" ")
	for d in range(31):
		lista_sem.append(semana[d%7])
	escala.append(lista_sem)

	func_num = 4 #int(input("numero de funcionarios: "))
	func_nomes = []
	func_Ps = []
	for i in range(func_num):
		 func_nomes.append("Ana") #input("nome: "))
		 func_Ps.append( 1 ) #int(input("P: ")))

	distrib = preenche(4, 31)
	postos = []
	c = 0
	for f in range(func_num):
		p = []
		for i in range(31):
			if distrib[c][i] == 1:
				p.append("F")
			elif distrib[c][i] == 2:
				p.append("B1")
			elif distrib[c][i] == 3:
				p.append("B2")
			elif distrib[c][i] == 5:
				p.append("Q1")
			else:
				p.append("Q2")
		c += 1
		postos.append(p)

	for i in range(func_num):
		linha = postos[i][:]
		linha.insert(0,func_nomes[i])
		linha.insert(1,func_Ps[i])
		escala.append(linha)

	imprime(escala)

	print ("Arquivo gerado no diretorio: ")

def preenche(func=4, dias=15):
	dist_postos = np.zeros((func,dias))

	for i in range(func):
		for j in range(dias):
			if (i-j)%5 == 0:
				dist_postos[i][j] = 1

	postos = [2,3,5,7]

	for j in range(dias):
		k = j%func;
		for i in range(func):
			if dist_postos[i][j] != 1:
				dist_postos[i][j] = postos[k]
				k = (k+1)%func

	print (dist_postos)
	return dist_postos


gera_tabela()
# preenche()
