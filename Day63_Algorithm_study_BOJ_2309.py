storage = [int(input()) for _ in range(9)]

for i in range(9):
    for j in range(i+1, 9):
        if sum(storage) - (storage[i] + storage[j]) == 100:
            one = storage[i]
            two = storage[j]
            break
storage.remove(one)
storage.remove(two)                    
print('\n'.join(map(str, sorted(storage))))