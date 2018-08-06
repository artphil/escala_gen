import xlwt
import numpy as np

escala = []

def imprime(tabela):
	cell_blk = xlwt.easyxf('pattern: pattern solid, fore_colour black;')

	# Definindo planilha
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Escala')

	# Definindo largura das células das sequência
	for i in range(1,34):
	    ws.col(i).width = 800
	    ws.row(i-1).height = 300

	# Preenchendo com dados da tabela
	i = 0;
	for linha in tabela:
		j = 0;
		for celula in linha:
			if celula == 'F':
				ws.write(i, j, celula, cell_blk)
			else:
				ws.write(i, j, celula)
			j += 1
		i += 1

	# Salvando
	wb.save('escala_ASO1.xls')



def gera_tabela():
	estacao = input("nome estacao: ")
	escala.append(["Escala ASO1 - " + estacao, ""])

	dia = int(input("dia da mudança: "))
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

	func_num = int(input("numero de funcionarios: "))
	func_nomes = []
	func_Ps = []
	for i in range(func_num):
		 func_nomes.append(input("nome: "))
		 func_Ps.append(int(input("P: ")))

	postos = []
	for f in range(func_num):
		p = []
		for i in range(31):
			if i%(4+f) == 0:
				p.append("F")
			else:
				p.append("B1")
		postos.append(p)

	for i in range(func_num):
		linha = postos[i][:]
		linha.insert(0,func_nomes[i])
		linha.insert(1,func_Ps[i])
		escala.append(linha)

	imprime(escala)

	print ("Arquivo gerado no diretorio: ")

gera_tabela()
