n = int(input())

space = [[i,n] for i in range(1, n+1)]
   
for index in range(n//2, n):
    while True:
        if space[index][1] - space[index][0] > -1:
            num = space[index][1] - space[index][0]
            space[index].insert(0, num)
        else:
            break

        
len = [len(space[i]) for i in range(n)]
len_max = max(len)
print(len_max)
print(' '.join(map(str,space[len.index(len_max)][::-1])))
# print(' '.join(space[len.index(len_max)]))
    