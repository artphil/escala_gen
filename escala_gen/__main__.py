from database import Dados
from aplicacao import App

print('Iniciando programa')
db = Dados()
app = App(db, None)

# print(db.estacoes.busca_tudo(ordem='codigo', reverso=True))
app.mainloop()