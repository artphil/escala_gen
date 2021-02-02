### escala_gen

# Requisitos
O programa foi desenvolvido em [Python3](https://www.python.org/downloads/).<br/>
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) é a biblioteca utilizada para a criar da planilha (A criação autoática dos PDFs só acontece no Linux com OpenOffice instalado).<br/>
Todas as biblliotecas utilizadas estão no arquivo [requeriments.txt](https://github.com/artphil/escala_gen/tree/master/requeriments.txt).

## Preparando o ambiente
Criando o ambiente com venv
``` 
python3 -m venv env
```

Ativando o ambiente
Windows
```
env\Scripts\activate
```
Linux
```
env/bin/activate
```

Desativando o ambiente
```
deactivate
```

## Execução
Na pasta raiz executar o comando após ativar o ambiente
```
python escala_gen
```

 
## Estrutura
```
                                     +------------+
> interface.py <--- database.py <--- |  taso.csv  |
     |               |               |  test.csv  |
     v               |               |  UEL1      |
> escala_gen.py <-----+              |  ...       |
     |               |               +------------+
     v             prop.py
  planilha.py
```

[interface.py](./interface.py) é o gerenciagor da interface. <br />
[escala_gen.py](./interface.py) é a parte que cria a escala comom uma matriz. <br />
[planilha.py](./interface.py) é quem transforma a matriz em uma planilha `.xls`. <br />
[prop.py](./interface.py) é o "gerador de improbabilidade infinita" coma as possiveis sequencias de postos de cada dia. <br />
[database.py](./interface.py) é o gerenciagor de arquivos de dados. <br />
[taso.csv](./interface.py) é o arquivo com os dados dos ASOs.<br />
[test.csv](./interface.py) é o arquivo com os dados das estações. <br />
Os demais arquivos da pasta [ests](./ests) são os dados volateis das estações como os ASOs escalados para determinado mês.