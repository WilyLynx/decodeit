import io

t = int(input())
for _ in range(t):
    l = int(input())
    k = [c for c in input()]
    for i in range(l):
        print(chr( int(k[4*i]+k[4*i+2]) + int(k[4*i+1]+k[4*i+3])), end='')
    print()