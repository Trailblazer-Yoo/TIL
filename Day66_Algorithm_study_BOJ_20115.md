# TIL(Today I Learned)

___

> Mar/18th/2022_Multi campus_유선종 Day66

```python
n = int(input())
x = list(map(int,input().split()))
max_x = max(x)
x.remove(max_x)

print(max_x + sum(x) / 2)
```