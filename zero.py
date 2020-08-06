for i in range(int(input())):
    test = input().split()
    if int(test[1]) >= int(test[0]) * int(test[2]):
        print('yes')
    else:
        print('no')