from seven import Board, BoardController, ROP
import random


class BoardVisualizer(BoardController):
    def print(self):
        for i in range(self.board.H):
            for j in range(self.board.W):
                print(self.board.balls[i][j], end=' ')
            print()


class ROPVisualizer(ROP):
    def _submit_move(self, x, y):
        score = super(ROPVisualizer, self)._submit_move(x, y)
        self.controller.print()
        print()
        return score


class BoardCreator:
    def __init__(self, H_range, W_range, C_range):
        self.H_low = H_range[0]
        self.H_high = H_range[1]
        self.W_low = W_range[0]
        self.W_high = W_range[1]
        self.C_low = C_range[0]
        self.C_high = C_range[1]

    def create_board(self, H, W, C):
        return [[random.randint(0, C) for _ in range(W)] for _ in range(H)]

    def create_series(self, length):
        for l in range(length):
            H = random.randint(self.H_low, self.H_high)
            W = random.randint(self.W_low, self.W_high)
            C = random.randint(self.C_low, self.C_high)
            balls = self.create_board(H, W, C)
            yield Board(H, W, C, balls)


H = 4
W = 4
C = 3
balls = [
    ['0', '0', '1', '1'],
    ['1', '1', '2', '2'],
    ['0', '1', '2', '0'],
    ['0', '1', '1', '2'],
]

H_range = (2, 10)
W_range = (2, 10)
C_range = (2, 5)

creator = BoardCreator(H_range, W_range, C_range)

for b in creator.create_series(1):
    controller = BoardVisualizer(b)
    player = ROPVisualizer(controller)
    controller.print()
    score = player.play()
    print(score)
    print()
