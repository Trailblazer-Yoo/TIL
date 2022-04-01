# TIL(Today I Learned)

___

> Apr/1st/2022_Multi campus_유선종 Day79

```python
n = int(input())
x = list(map(int,input().split()))
max_x = max(x)
x.remove(max_x)

print(max_x + sum(x) / 2)
```