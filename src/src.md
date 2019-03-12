### escala_gen

# Estrutura
```
interface.py <--- database.py <--- taso.csv
     |               |         +-- test.csv
     v               |         l
escala_gen.py <------- 

```


```python {hide=true}
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

```python {cmd=true matplotlib=true}
import matplotlib.pyplot as plt
plt.plot([1,2,3, 4])
plt.show() # show figure
```