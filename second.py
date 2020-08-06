def tab_2_int(tab):
    return int(''.join(tab))


def int_2_tab(num):
    return [c for c in str(num).zfill(4)]


def test_zero(tab):
    return all([t == '0' for t in tab])


def get_solution(tab):
    tab_int = tab_2_int(tab)
    if tab_int == 6174:
        return 0
    elif tab_int == 0:
        return -1
    else:
        tab_asc = sorted(tab)
        int_asc = tab_2_int(tab_asc)
        sol = solutions.get(int_asc)
        if sol is not None:
            return sol
        else:
            tab_des = list(reversed(tab_asc))
            diff = tab_2_int(tab_des) - int_asc
            sub_solution = get_solution(int_2_tab(diff))
            if sub_solution == -1:
                curr_solution = sub_solution
            else:
                curr_solution = sub_solution + 1
            solutions[int_asc] = curr_solution
            return curr_solution


solutions = dict()
solutions[6174] = 0
t = int(input())
for i in range(t):
    tab = [c for c in input()]
    if test_zero(tab):
        print(-1)
    else:
        solve = get_solution(tab)
        print(solve)
