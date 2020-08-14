import math


def triangle_area(a, b, c):
    a_b = b - a
    a_c = c - a
    return a_b.dot(a_c) / 2


def sign(a):
    if a > 0:
        return 1
    elif a == 0:
        return 0
    else:
        return -1


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x:{self.x}   y:{self.y}"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def orient(self, c):
        return sign(triangle_area(self.a, self.b, c))

    def normal(self):
        return Vector(self.b.y - self.a.y, self.b.x - self.a.x) / len(self.a - self.b)

    def dist(self, c):
        area = triangle_area(self.a, self.b, c)
        l = len(self.a - self.b)
        return abs(2 * area / l)


class Circle:
    def __init__(self, x, y, z):
        self.center = Vector(x, y)
        self.r = z


class Algorithm:
    def __init__(self, disks):
        self.circles = disks
        self.boundary_disks = []

    def find_solution(self):
        self.boundary_disks = self._find_disks(self.circles)

    def _find_disks(self, D):
        if len(D) == 1:
            return D
        p, q, d_p, d_q = self._find_extream_points_and_disks(D)
        print(f"p:[{p}] q:[{q}]")
        # D_L, D_R = self._divide_disks(p, q)
        # hull_L = self._find_hull(D_L, d_p, d_q)
        # hull_R = self._find_hull(D_R, d_q, d_p)
        # return hull_R + hull_L

    def _find_extream_points_and_disks(self, D):
        p = Vector(float('inf'), float('-inf'))
        q = Vector(float('-inf'), float('inf'))
        d_p = None
        d_q = None
        for disk in D:
            c_p = disk.center - Vector(disk.r, 0)
            c_q = disk.center + Vector(disk.r, 0)
            if c_p.x < p.x or c_p.x == p.x and c_p.y < p.y:
                p = c_p
                d_p = disk
            elif c_q.x > q.x or c_q.x == q.x and c_q.y > q.y:
                q = c_q
                d_q = disk
        return p, q, d_p, d_q

    def _divide_disks(self, p, q):
        pass

    def _find_hull(self, D_R, d_q, d_p):
        return []


circles = []
t = int(input())
for _ in range(t):
    n = int(input())
    for _ in range(n):
        line = input().split()
        circles.append(Circle(int(line[0]), int(line[1]), int(line[2])))
    alg = Algorithm(circles)
    alg.find_solution()
