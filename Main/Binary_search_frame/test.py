memo=[]
for i in range(1,8):
    memo.append([i,i+1,i+2])


for i in memo:
    print(i)

print(memo[-1])
memo.pop(-1)
print(memo[-1])

for i in memo:
    print(i)