from seven import Board, BoardController


class BoardVisualizer(BoardController):
    def print(self):
        for i in range(self.board.H):
            for j in range(self.board.W):
                print(self.board.balls[i][j], end=' ')
            print()


H = 3
W = 2
C = 2
balls = [
    ['1', '1'],
    ['1', '2'],
    ['1', '1'],
]


controller = BoardVisualizer(Board(H, W, C, balls))
print(controller.is_move_possible(1, 1))
controller.print()
print()
x, y = 0, 1
if controller.is_move_possible(x, y):
    points = controller.make_move(x, y)
    print(points)
controller.print()


