n = int(input())
num = [int(i) for i in input().split()]

ans1 = [1]*n
ans2 = [1]*n
print(ans1)
print(ans2)

for i in range(1,n):
    if num[i-1] <= num[i]:
        ans1[i] = max(ans1[i], ans1[i-1] + 1)
        print(ans1)
    if num[i] <= num[i-1]:
        ans2[i] = max(ans2[i], ans2[i-2] + 1)
        print(ans2)
        
        
print(max(max(ans1), max(ans2)))