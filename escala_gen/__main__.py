from database import Dados
from aplicacao import App
from gerador import GeradorEscala

print('Iniciando programa')
db = Dados()
ge = GeradorEscala(db)
app = App(db, ge)

# print(db.estacoes.busca_tudo(ordem='codigo', reverso=True))
app.mainloop()