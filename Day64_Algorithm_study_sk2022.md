# TIL(Today I Learned)

___

> Mar/16th/2022_Multi campus_유선종 Day64

```python
def solution(money, costs):
    costs_dict = {}
    efficient = []
    unit = [1, 5, 10, 50, 100, 500]
    for key, value in zip(unit, costs):
        costs_dict[key] = value
        efficient.append((key - value) / key)
    
    efficient_min = list(reversed(sorted(efficient)))
    idx_list = [unit[efficient.index(idx)] for idx in efficient_min]

    money_iter = money
    quantity_list = []
    for efficient in idx_list:
        dup = 0
        while True:
            money_iter -= efficient
            if money_iter < 0:
                break 
            dup += 1
        money_iter = money_iter + efficient
        quantity_list.append(dup)

    
    values = [costs_dict[key] * quantity_list[i]  for i, key in enumerate(idx_list)]
    
    return sum(values)

print(solution(1999,[2, 11, 20, 100, 200, 600]))
```