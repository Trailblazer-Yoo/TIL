# TIL(Today I Learned)

___

> Mar/27th/2022_Multi campus_유선종 Day74

```python
n, m = map(int, input().split())

pokemon = {num : input() for num in range(1, n+1)}
pokemon_reverse  = dict(map(reversed, pokemon.items()))
sol = [input() for _ in range(m)]

for finder in sol:
    try: 
        bool(int(finder)) == True
        print(pokemon[int(finder)])
    except:
        print(pokemon_reverse[finder])
```