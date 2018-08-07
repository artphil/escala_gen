from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, PatternFill
from openpyxl.utils import column_index_from_string

import numpy as np

def imprime(tabela):
	# Definindo a planilha
	wb = Workbook()
	ws = wb.active
	ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
	ws.page_setup.paperSize = ws.PAPERSIZE_A4
	ws.page_setup.fitToPage = True
	ws.print_area = 'A1:AG15'

	# Titulo da aba
	ws.title = 'Escala'

	# Preenchendo com dados da tabela
	i = 0;
	for linha in tabela:
		ws.append(linha)

	# Aplica merge e formata as celulas do titulo
	ws.merge_cells("A1:AG1")
	ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
	ws['A1'].font = Font(bold=True)

	# Aplica formatacao as demais celulas
	for linha in ws['A2:AG15']:
		ws.row_dimensions[linha[0].row].height = 20.0
		for celula in linha:
			celula.alignment = Alignment(horizontal='center', vertical='center')
			if celula.col_idx < 3 or celula.row < 4:
				celula.font = Font(bold=True)
			if celula.value == 'F':
				celula.fill = PatternFill("solid", fgColor="000000")
				celula.font = Font(color='FFFFFF')

	# Definindo largura das células das sequência
	ws.row_dimensions[ws['A1'].row].height = 30.0
	for col in ws['B:AG']:
	     ws.column_dimensions[col[0].column].width = 4.0

	# Salvando
	nome_arquivo = tabela[0][0]+'.xlsx'
	wb.save(filename=nome_arquivo)


def le_dados():
	data = {}

	data['estacao'] = input("nome estacao: ")
	data['dia_inicio'] = int(input("dia da mudança: "))
	data['func_num'] = int(input("numero de funcionarios: "))

	func_nomes = []
	func_Ps = []
	for i in range(func_num):
		func_nomes.append(input("nome: "))
		func_Ps.append(int(input("P: ")))

	data['func_nomes'] = func_nomes
	data['func_Ps'] = func_Ps

	return data

def gera_tabela():
	escala = []
	dias_mes = {
	'Janeiro' : 31,
	'Fevereiro' : 28,
	'Marco' : 31,
	'Abril' : 30,
	'Maio' : 31,
	'Junho' : 30,
	'Julho' : 31,
	'Agosto' : 31,
	'Setembro' : 30,
	'Outubro' : 31,
	'Novembro' : 30,
	'Dezembro' : 31
	}
	semana = ["D", "S", "T", "Q", "Q", "S", "S", "D"]


	data = {}
	data['estacao'] = "Central"
	data['dia_inicio'] = 3
	data['mes'] = 'Julho'
	data['func_num'] = 4
	data['func_nomes'] = ['Artphil', 'D.Maia', 'Waguim', 'Zeze']
	data['func_Ps'] = [7, 8, 9, 4]

	# data = le_dados()

	escala.append(["Escala ASO1 - " + data['estacao'] + " - " + data['mes'], ""])

	lista_dias = ["Dias", "P"]
	for d in range(dias_mes[data['mes']]):
		lista_dias.append((data['dia_inicio']+d-1)%dias_mes[data['mes']]+1)
	escala.append(lista_dias)

	lista_sem = ["", ""]
	for d in range(dias_mes[data['mes']]):
		lista_sem.append(semana[d%7])
	escala.append(lista_sem)

	distrib = preenche(data['func_num'], dias_mes[data['mes']])
	postos = []
	c = 0
	for f in range(data['func_num']):
		p = []
		p.append(data['func_nomes'][f])
		p.append(data['func_Ps'][f])
		for i in range(dias_mes[data['mes']]):
			if distrib[c][i] == 1:
				p.append("F")
			elif distrib[c][i] == 2:
				p.append("B1")
			elif distrib[c][i] == 3:
				p.append("Q1")
			elif distrib[c][i] == 4:
				p.append("B2")
			elif distrib[c][i] == 5:
				p.append("Q2")
			else:
				p.append("")
		c += 1
		escala.append(p)

	imprime(escala)

	print ("Arquivo gerado no diretorio: ")

def preenche(func=4, dias=15):
	dist_postos = np.zeros((func,dias))

	for i in range(func):
		for j in range(dias):
			if (i-j)%5 == 0:
				dist_postos[i][j] = 1

	postos = [2,3,4,5]

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
