<hr>
MOWNIT 2 (12.03.2019)<br>
Maciej Mionskowski | nr albumu: 296628
<hr>

# II Laboratoria

## Gauss Jordan

Usprawnienia względem standardowego algorytmu:

- Partial pivoting
- Scaling

### Porównanie

Size | Our gauss Jordan | Numpy solve
---|---|---
5 | 0.0006504058837890625 | 0.0000858306884765
300 | 0.35778236389160156 | 0.06560730934143066
1000 | 7.49634051322937 |   0.2636873722076416

### Wnioski

Gauss Jordan nie jest zbyt efektywnym algorytmem rozwiązywania układów równań.
Funkcje biblioteczne są rząd wielkości szybsze.

## LU Decomposition

Zgodnie z instrukcjami podanymi na laboratoriach zrezygnowałem z pivotingu i scalingu.

### Porównanie

Size | Our LU Decomp | Scipy LU Decom
---|---|---
5 | 0.00011491775512695312 | 0.0010249614715576173
10 | 0.0002892017364501953 | 0.0021255016326904297
300 | 0.2748112678527832 | 0.19040608406066895
1000 | 3.4280920028686523 | 0.35529518127441406
2000 | 14.292314529418945 | 1.0336315631866455

### Wnioski

Dla bardzo niewielkich macierzy nasz algorytm dekompozycji potrafi być szybszy niż ten zawarty w bibliotece scipy.
Dla obszerniejszych danych scipy jest znacznie wydajniejszy.
