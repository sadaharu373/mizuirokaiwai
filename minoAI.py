from kogi_canvas import play_othello, PandaAI
import math
import random

BLACK = 1
WHITE = 2

class Board:
    def __init__(self, board=None):
        if board:
            self.board = [row[:] for row in board]
        else:
            self.board = [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,1,2,0,0],
        [0,0,2,1,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
]

    def clone(self):
        return Board(self.board)

    def place_stone(self, stone, x, y):
        if not can_place_x_y(self.board, stone, x, y):
            return False

        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.board[y][x] = stone

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []

            while 0 <= nx < len(self.board[0]) and 0 <= ny < len(self.board):
                if self.board[ny][nx] == opponent:
                    stones_to_flip.append((nx, ny))
                elif self.board[ny][nx] == stone:
                    for fx, fy in stones_to_flip:
                        self.board[fy][fx] = stone
                    break
                else:
                    break

                nx += dx
                ny += dy

        return True

    def get_valid_moves(self, stone):
        moves = []
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if can_place_x_y(self.board, stone, x, y):
                    moves.append((x, y))
        return moves

    def is_full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def count_stones(self):
        black = sum(row.count(BLACK) for row in self.board)
        white = sum(row.count(WHITE) for row in self.board)
        return black, white

    def display(self):
        print("  " + " ".join(map(str, range(len(self.board[0])))))
        for y, row in enumerate(self.board):
            print(f"{y} " + " ".join(str(cell) if cell != 0 else "." for cell in row))


def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False


class MCTSNode:
    def __init__(self, board, stone, parent=None):
        self.board = board
        self.stone = stone
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.board.get_valid_moves(self.stone))

    def best_child(self, exploration_weight=1.0):
        return max(
            self.children,
            key=lambda child: child.wins / child.visits + exploration_weight * math.sqrt(math.log(self.visits) / child.visits),
        )

    def expand(self):
        untried_moves = [move for move in self.board.get_valid_moves(self.stone) if move not in [child.move for child in self.children]]
        move = random.choice(untried_moves)
        next_board = self.board.clone()
        next_board.place_stone(self.stone, move[0], move[1])
        child_node = MCTSNode(next_board, 3 - self.stone, parent=self)
        child_node.move = move
        self.children.append(child_node)
        return child_node

    def simulate(self):
        current_board = self.board.clone()
        current_stone = self.stone

        while not current_board.is_full() and current_board.get_valid_moves(current_stone):
            move = random.choice(current_board.get_valid_moves(current_stone))
            current_board.place_stone(current_stone, move[0], move[1])
            current_stone = 3 - current_stone

        black, white = current_board.count_stones()
        if self.stone == BLACK:
            return 1 if black > white else 0
        else:
            return 1 if white > black else 0

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)


class PandaMCTS:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def face(self):
        return "🐼"

    def place(self, board, stone):
        root = MCTSNode(Board(board), stone)

        for _ in range(self.iterations):
            node = root

            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            if not node.is_fully_expanded():
                node = node.expand()

            result = node.simulate()
            node.backpropagate(result)

        best_move = root.best_child(exploration_weight=0).move
        return best_move

# Game loop
board = Board()
panda_ai = PandaMCTS(iterations=1000)
current_player = BLACK

while not board.is_full():
    board.display()
    print(f"Current player: {'BLACK' if current_player == BLACK else 'WHITE'}")

    if current_player == BLACK:
        while True:
            try:
                x, y = map(int, input("Enter your move (x y): ").split())
                if board.place_stone(current_player, x, y):
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter two numbers separated by a space.")
    else:
        x, y = panda_ai.place(board.board, current_player)
        board.place_stone(current_player, x, y)
        print(f"AI places at ({x}, {y})")

    current_player = 3 - current_player

board.display()
black, white = board.count_stones()
print(f"Game over! Black: {black}, White: {white}")
if black > white:
    print("Black wins!")
elif white > black:
    print("White wins!")
else:
    print("It's a tie!")
