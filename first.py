import io

test = input().split()
r = int(test[0])
s = int(test[1])

bot = [0 for i in range(r)]
for i in range(s):
    idx = i % r
    bot[idx] = bot[idx] + 1

solve = 1
for c in bot:
    solve = solve * (1 + c) * 2

print(solve)