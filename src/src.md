### escala_gen

# Estrutura
```
interface.py <--- database.py <--- taso.csv
     |               |         +-- test.csv
     v               |         l
escala_gen.py <------- 

```


```python {cmd="/usr/local/bin/python3"}
	print("This will run python3 program")
```

```gnuplot {cmd=true output="html"}
set terminal svg
set title "Simple Plots" font ",20"
set key left box
set samples 50
set style data points

plot [-10:10] sin(x),atan(x),cos(atan(x))
```