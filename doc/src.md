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
 escala_gen
     |               
     v                               +----------------+
> interface <------ database.py <--- |  pessoas.csv   |
     |               |               |  estacoes.csv  |
     v               |               |  UEL1          |
>   gen.py <---------+               |  ...           |
     |               |               +----------------+
     v             prop.py
  planilha.py
```

[interface](https://github.com/artphil/escala_gen/tree/master/escala_gen/interface) é o gerenciagor da interface. <br />
[gen.py](https://github.com/artphil/escala_gen/tree/master/escala_gen/gen.py) é a parte que cria a escala comom uma matriz. <br />
[xls.py](https://github.com/artphil/escala_gen/tree/master/escala_gen/xls.py) é quem transforma a matriz em uma planilha `.xls`. <br />
[prob.py](https://github.com/artphil/escala_gen/tree/master/escala_gen/prob.py) é o "gerador de improbabilidade infinita" coma as possiveis sequencias de postos de cada dia. <br />
[database.py](https://github.com/artphil/escala_gen/tree/master/escala_gen/database.py) é o gerenciagor de arquivos de dados. <br />
[pessoas.csv](https://github.com/artphil/escala_gen/tree/master/data/pessoas.csv) é o arquivo com os dados dos ASOs.<br />
[estacoes.csv](https://github.com/artphil/escala_gen/tree/master/data/estacoes.csv) é o arquivo com os dados das estações. <br />
[escalas.json](https://github.com/artphil/escala_gen/tree/master/data/escalas.json) é o arquivo com os dados das escalas. <br />
Os demais arquivos da pasta [ests](https://github.com/artphil/escala_gen/tree/master/data/ests) são os dados volateis das estações como os ASOs escalados para determinado mês.