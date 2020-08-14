class Board:
    def __init__(self, H, W, C, balls):
        self.H = H
        self.W = W
        self.C = C
        self.balls = balls


class BoardController:
    def __init__(self, board: Board):
        self.board = board

    def gravity(self):
        for j in range(self.board.W):
            blank_beg = self.board.H
            blank_count = 0
            for i in range(self.board.H - 1, -1, -1):
                if self.board.balls[i][j] == '-':
                    break
                if self.board.balls[i][j] == '.':
                    if blank_count == 0:
                        blank_beg = i
                        blank_count += 1
                    else:
                        blank_count += 1
                elif blank_count > 0:
                    k = 0
                    while self.board.balls[i+k] not in ['.', '-']:
                        self.board.balls[blank_beg - k][j] = self.board.balls[i-k][j]
                        k += 1
                        if i+k >= self.board.H:
                            break
                    blank_count = 0
            k = 0
            while self.board.balls[k][j] in ['.', '-']:
                self.board.balls[k][j] = '-'
                k += 1
                if k >= self.board.H:
                    break

    def is_move_possible(self, x, y):
        col = self.board.balls[x][y]
        if x + 1 < self.board.H:
            if col == self.board.balls[x + 1][y]:
                return True
        if x - 1 >= 0:
            if col == self.board.balls[x - 1][y]:
                return True
        if y + 1 < self.board.W:
            if col == self.board.balls[x][y + 1]:
                return True
        if y - 1 >= 0:
            if col == self.board.balls[x][y - 1]:
                return True
        return False

    def make_move(self, x, y):
        visited_areas = [[False for _ in range(self.board.W)] for _ in range(self.board.H)]
        col = self.board.balls[x][y]
        n = self._destroy_neighbours(x, y, visited_areas, col)
        points = n * (n - 1)
        self.gravity()
        return points

    def _destroy_neighbours(self, x, y, visited_areas, col):
        if x < 0 or x >= self.board.H or \
                y < 0 or y >= self.board.W:
            return 0
        elif visited_areas[x][y] or \
                self.board.balls[x][y] != col:
            return 0
        else:
            visited_areas[x][y] = True
            self.board.balls[x][y] = '.'
            n = 1
            n += self._destroy_neighbours(x - 1, y, visited_areas, col)
            n += self._destroy_neighbours(x + 1, y, visited_areas, col)
            n += self._destroy_neighbours(x, y - 1, visited_areas, col)
            n += self._destroy_neighbours(x, y + 1, visited_areas, col)
            return n

#
# boards = []
# for _ in range(int(input())):
#     line = input().split()
#     H = int(line[0])
#     W = int(line[1])
#     C = int(line[2])
#     balls = [input().split() for _ in range(H)]
#     boards.append(BoardController(Board(H, W, C, balls)))
