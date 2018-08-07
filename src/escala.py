from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, PatternFill
from openpyxl.utils import column_index_from_string

import numpy as np

def imprime(tabela):
	# Definindo planilha
	wb = Workbook()
	ws = wb.active
	ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
	ws.page_setup.paperSize = ws.PAPERSIZE_A4
	ws.page_setup.fitToPage = True
	ws.print_area = 'A1:AG15'

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

	ws.row_dimensions[ws['A1'].row].height = 30.0

	for col in ws['B:AG']:
	     ws.column_dimensions[col[0].column].width = 4.0

	# Salvando
	nome_arquivo = tabela[0][0]+'.xlsx'
	wb.save(filename=nome_arquivo)


def le_dados():
	estacao = input("nome estacao: ")
	dia = int(input("dia da mudança: "))
	func_num = int(input("numero de funcionarios: "))
	func_nomes = []
	func_Ps = []
	for i in range(func_num):
		func_nomes.append(input("nome: "))
		func_Ps.append(int(input("P: ")))

	data = {}
	data['estacao'] = estacao
	data['dia_inicio'] = dias
	data['func_num'] = func_num
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


	estacao = "Central"
	dia = 3
	mes = 'Agosto'
	func_num = 4
	func_nomes = ['Artphil', 'D.Maia', 'Waguim', 'Zeze']
	func_Ps = [7, 8, 9, 4]


	escala.append(["Escala ASO1 - " + estacao + " - " + mes, ""])

	lista_dias = ["Dias", "P"]
	for d in range(dias_mes[mes]):
		lista_dias.append((dia+d-1)%dias_mes[mes]+1)
	escala.append(lista_dias)

	lista_sem = ["", ""]
	for d in range(dias_mes[mes]):
		lista_sem.append(semana[d%7])
	escala.append(lista_sem)

	distrib = preenche(func_num, dias_mes[mes])
	postos = []
	c = 0
	for f in range(func_num):
		p = []
		p.append(func_nomes[f])
		p.append(func_Ps[f])
		for i in range(dias_mes[mes]):
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
