### escala_gen

# Source
O programa foi desenvolvido em Python3. 

## Execução
Na pasta raiz
```
python src/interface.py 
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

[interface.py](./interface.py) é o gerenciagor da interface. \
[escala_gen.py](./interface.py) é a parte que cria a escala comom uma matriz. \
[planilha.py](./interface.py) é quem transforma a matriz em uma planilha `.xls`. \
[prop.py](./interface.py) é o "gerador de improbabilidade infinita" coma as possiveis sequencias de postos de cada dia. \
[database.py](./interface.py) é o gerenciagor de arquivos de dados. \
[taso.csv](./interface.py) é o arquivo com os dados dos ASOs. \
[test.csv](./interface.py) é o arquivo com os dados das estações. \
Os demais arquivos da pasta [ests](./ests) são os dados volateis das estações como os ASOs escalados para determinado mês.