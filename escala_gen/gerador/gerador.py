'''
Programa de geracao automatica de escala de postos de servico
Escalas mensais de bloqueio e bilheteria (PEQ/PEB) por estacao
autor: Arthur Phillip Silva
'''

import os
import sys
import platform

import json
import random
import numpy as np
from datetime import datetime, timedelta, date

from .xls import Gen_xls

OS_ = platform.system()

if OS_ == 'Windows':
	import win32api
	from win32com import client


class GeradorEscala:

	def __init__(self, db):
		self.db = db
		self.data_base = date(2019,1,1)

	def gera_todas_escalas(self, ano, mes_id):
		lista_estacoes = self.db.estacoes.busca_tudo().values()
		for turno in [1,2]:
			for estacao in lista_estacoes:
				self.gera_escala(ano, mes_id, turno, estacao['id'])

	
	def gera_escala(self, ano, mes_id, turno, estacao_id):
		estacao = self.db.estacoes.busca_por_id(estacao_id)
		escalas = self.db.escalas.busca_por_estacao(estacao['sigla'], turno)
		lista_escalas = list(escalas.values())
		postos = self.db.postos.busca_por_estacao(estacao_id, turno)
		lista_postos = [p['posto'] for p in postos.values()]
		quantidade_postos = len(postos)
		mes = self.db.meses[mes_id-1]
		
		pwd = os.path.abspath('.')
		caminho_xls = os.path.join(pwd, 'planilha', str(ano))
		if not os.path.isdir(caminho_xls):
			os.mkdir(caminho_xls)
		caminho_xls = os.path.join(caminho_xls, mes['nome'])
		if not os.path.isdir(caminho_xls):
			os.mkdir(caminho_xls)

		caminho_pdf = os.path.join(pwd, 'pdf', str(ano))
		if not os.path.isdir(caminho_pdf):
			os.mkdir(caminho_pdf)
		caminho_pdf = os.path.join(caminho_pdf, mes['nome'])
		if not os.path.isdir(caminho_pdf):
			os.mkdir(caminho_pdf)

		pessoas = []
		for escala in lista_escalas:
			pessoa_id = escala['pessoa_id']
			pessoa = self.db.pessoas.busca_por_id(pessoa_id)
			pessoas.append(pessoa)
			
		quantidade_pessoas = len(escalas)
		tabela_folgas = self.tabela_folgas(pessoas, ano, mes)
		tabela_postos = self.tabela_postos(tabela_folgas, lista_postos)



		matriz_escala = self.gera_tabela(pessoas, tabela_postos, estacao, mes, ano)
		for p in postos.values():
			matriz_escala.append(['',p['posto'], p['desc']])

		nome_arquivo =f"{estacao['sigla']}-{turno}T-{mes['abrev']}{ano}"
		Gen_xls(matriz_escala, caminho_xls, nome_arquivo)
		
		self.gera_pdf(nome_arquivo, caminho_xls, caminho_pdf)

		return "Arquivo gerado no diretorio:\n"

	def tabela_folgas(self, pessoas, ano, mes):
		inicio = date(ano, mes['numero'], 1)
		ano_fim = ano
		mes_fim = mes['numero']+1
		if mes_fim > 12:
			ano_fim += 1
			mes_fim = 1
		fim = date(ano_fim, mes_fim, 1)
		dias_mes = ( fim - inicio ).days
		dias_escala = len(self.db.escala_p['a'])
		dia_padrao = (inicio - self.data_base).days % dias_escala
		quantidade_pessoas = len(pessoas)
		tabela = np.zeros((quantidade_pessoas,dias_mes))
		for i, pessoa in enumerate(pessoas):
			pessoa_p = pessoa['posto']
			if pessoa_p < 4:
				escala_folga = self.db.escala_p['a']
				dia = ( pessoa_p - 1 ) * 7 + dia_padrao
			else: 
				escala_folga = self.db.escala_p['b']
				dia = ( pessoa_p - 4 ) * 7 + dia_padrao


			for j in range(dias_mes):
				d = (dia + j) % dias_escala
				tabela[i][j] = escala_folga[d]
		return tabela
	
	def tabela_postos(self, folgas, postos):
		titulares = []
		reservas = []
		quantidade_titulares = int(len(folgas) / 2)
		quantidade_dias = len(folgas[0])
		quantidade_postos = len(postos)
		for i in range(quantidade_titulares):
			titular = []
			reserva = []
			for j in range(quantidade_dias):
				k = (i + j) % quantidade_postos
				if folgas[i][j] > 0:
					titular.append('F')
					reserva.append(postos[k])
				else:
					titular.append(postos[k])
					if folgas[quantidade_titulares+i][j] > 0:
						reserva.append('F')
					else:
						reserva.append('')
			titulares.append(titular)
			reservas.append(reserva)
		return titulares + reservas


	# # cria a matriz da escala
	def gera_tabela(self, pessoas, postos, estacao, mes, ano):
		inicio = date(ano, mes['numero'], 1)
		ano_fim = ano
		mes_fim = mes['numero']+1
		if mes_fim > 12:
			ano_fim += 1
			mes_fim = 1
		fim = date(ano_fim, mes_fim, 1)
		dias_mes = ( fim - inicio ).days

		escala = []
		# Titulo
		escala.append([f"Escala ASO1 - {estacao['nome']} - {mes['nome']}/{ano}", ""])

		# Sequencia de dias
		lista_dias = ["", "Dias"] + [str(d+1) for d in range(dias_mes)]
		
		escala.append(lista_dias)

		# Sequencia de dias da semana
		lista_semana = ["", "Ps"]
		m = mes['numero']
		for d in range(1, dias_mes+1):
			data_dia = date(ano, m, d)
			lista_semana.append(self.db.dias_semana[int(data_dia.strftime('%w'))])

		escala.append(lista_semana)

		quantidade_pessoas = len(pessoas)
		for i in range(quantidade_pessoas):
			p = [pessoas[i]['apelido'], str(pessoas[i]['posto'])]
			p += postos[i]

			escala.append(p)
		return escala

	# Gera o PDF a partir da planilha
	def gera_pdf(self, filename, caminho_xls, caminho_pdf):
		xls_file = os.path.join(caminho_xls, f'{filename}.xlsx')
		pdf_file = os.path.join(caminho_pdf, f'{filename}.pdf')

		if OS_ == 'Linux':

			print(f'\nsoffice --convert-to pdf {xls_file} --outdir {caminho_pdf} \n')

			# Codigo valido para LibreOffife
			os.system(f'soffice --convert-to pdf {xls_file} --outdir {caminho_pdf} ')
			os.system(f'gvfs-open {pdf_file}')
	
		elif OS_ == 'Windows':

			#give valid output file nome and path
			app = client.Dispatch("Excel.Application")
			# app = client.DispatchEx("Excel.Application")
			app.Interactive = False
			app.Visible = False
			Workbook = app.Workbooks.Open(xls_file)
			work_sheets = Workbook.Worksheets[0]
			try:
				# Workbook.ActiveSheet.ExportAsFixedFormat(0, pdf_file)
				work_sheets.ExportAsFixedFormat(0, pdf_file)
				# os.system(pdf_file)
			except Exception as e:
				print("Failed to convert in PDF format.Please confirm environment meets all the requirements  and try again")
				print(str(e))
			finally:
				Workbook.Close()
				# app.Exit()


