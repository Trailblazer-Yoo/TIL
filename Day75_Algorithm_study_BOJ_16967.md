# TIL(Today I Learned)

___

> Mar/28th/2022_Multi campus_유선종 Day75

```python
h, w, x, y = map(int, input().split())

layer_row = h - x

matrix = [list(map(int, input().split())) for _ in range(h + x)]
layer_matrix = [matrix[x + idx][y:] for idx in range(layer_row)]

for idx in range(layer_row):
    matrix[x + idx][y:] = [x-y for x,y in zip(layer_matrix[idx], matrix[idx][:len(matrix[idx])-y])]

for inner_row in matrix[:h]:
    print(*inner_row[:len(inner_row)-y])
```