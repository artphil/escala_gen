'''
Programa de geracao automatica de escala de postos de servico
Escalas mensais de bloqueio e bilheteria (PEQ/PEB) por estacao
autor: Arthur Phillip Silva
'''

import sys
import os
import json
from database import db


class gen:
	def __init__(self):
		try: 
			self.data = db()
		except:
			print("Erro no Banco de Dados")
			quit()

		if len(sys.argv) <= 2: 
			self.read_input()
		else:
			self.read_input(sys.argv[1],int(sys.argv[2]))


	def read_input(self,mes="",ano=0):
		if mes in self.data.mes and ano > 2000:
			self.mes = mes
			self.ano = ano
			print(self.mes, self.ano)
		else:
			print("valores invalidos")
			try:
				mes = input("Digite o mês: ")
				ano = int(input("Digite o ano: "))
			except:
				print("valores invalidos")
			self.read_input(mes,ano)

	def stations(self):
		asos = self.data.aso.get_by("posto")
		print([a for a in asos])


		for st in self.data.est.db:
			print(st)
			if st == "TST": continue

			estacao = st[:-1]
			turno = st[-1]

			file = {}
			file["station"] = st
			file["month"] = self.mes
			file["year"] = str(self.ano)

			aso_list = []
			for p in self.data.pds.db[turno][estacao]:
				# print("-- ",p)
				# a = self.data.pds.db[turno]["postos"][p]
				# print( "-- ", a,  type(a))
				# print( "-- ", asos[a])
				aso_list.append(asos[self.data.pds.db[turno]["postos"][p]]["id"])
			
			file["asos"] = aso_list

			print(json.dumps(file))

			with open('data/ests/a'+st, "w") as new_file:
				new_file.write(json.dumps(file, indent=4))


if __name__ == '__main__':
	
	e = gen()
	e.stations()

