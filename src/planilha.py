from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, PatternFill, Border
from openpyxl.utils import column_index_from_string
from openpyxl.formula import Tokenizer

# Cria a planilha excel
def gera_xls(tabela):
	# Definindo a planilha
	wb = Workbook()
	ws = wb.active
	ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
	ws.page_setup.paperSize = ws.PAPERSIZE_A4
	ws.page_setup.fitToPage = True
	ws.print_area = 'A1:AG15'

	# Titulo da aba
	ws.title = 'tabela'

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
				# celula.style.borders.all_borders = Border.BORDER_MEDIUM
			if celula.value == 'F':
				celula.fill = PatternFill("solid", fgColor="000000")
				celula.font = Font(color='FFFFFF')

	# Definindo largura das células das sequência
	ws.row_dimensions[ws['A1'].row].height = 30.0
	ws.column_dimensions[ws['A1'].column].width = 11.0
	ws.column_dimensions[ws['B1'].column].width = 5.0
	for col in ws['B:AG']:
	     ws.column_dimensions[col[0].column].width = 4.0

	ws["AI3"] = "B1"
	ws["AJ3"] = "B2"
	ws["AK3"] = "B3"
	ws["AL3"] = "B4"
	ws["AM3"] = "Q1"
	ws["AN3"] = "Q2"

	for i in range(4,11):
		ws["AI"+str(i)] = '=CONT.SE(B'+str(i)+':AG'+str(i)+'; "B1")'
		ws["AJ"+str(i)] = '=CONT.SE(B'+str(i)+':AG'+str(i)+'; "B2")'
		ws["AK"+str(i)] = '=CONT.SE(B'+str(i)+':AG'+str(i)+'; "B3")'
		ws["AL"+str(i)] = '=CONT.SE(B'+str(i)+':AG'+str(i)+'; "B4")'
		ws["AM"+str(i)] = '=CONT.SE(B'+str(i)+':AG'+str(i)+'; "Q1")'
		ws["AN"+str(i)] = '=CONT.SE(B'+str(i)+':AG'+str(i)+'; "Q2")'

	# Salvando
	nome_arquivo = tabela[0][0]+'.xlsx'
	wb.save(filename=nome_arquivo)
