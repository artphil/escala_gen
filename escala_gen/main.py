from interface import Application
from database import DB
from generate.gen import Generator


# Criando aplicação
data = DB()
esc = Generator(data)
myapp = Application(data, esc)

# Iniciando programa
myapp.mainloop()