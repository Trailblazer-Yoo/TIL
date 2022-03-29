# TIL(Today I Learned)

___

> Mar/29th/2022_Multi campus_유선종 Day76

```python
n = int(input())

customer = [tuple(input().split()) for _ in range(n)]
customer.sort(key=lambda x:int(x[0]))

for i in customer:
    print(i[0], i[1])
```