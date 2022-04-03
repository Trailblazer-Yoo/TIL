# TIL(Today I Learned)

___

> Apr/3rd/2022_Multi campus_유선종 Day81

```python
n, k = map(int,input().split())
coin = [int(input()) for _ in range(n)]
coin = coin[::-1]
result = 0
for value in coin:
    num = k // value
    if num > 0:
        k -= value * num
        result += num
print(result)
```