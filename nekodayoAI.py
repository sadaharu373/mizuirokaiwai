from kogi_canvas import play_othello

# 石の種類を定義 (1が黒石、2が白石)
BLACK = 1
WHITE = 2

# 6x6の初期状態のオセロボードを定義
board = [
    [0, 0, 0, 0, 0, 0],  # 0は空きマスを表す
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],  # 中央に黒石(1)と白石(2)が配置されている
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

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


def simulate_move(board, stone, x, y):
    new_board = [row[:] for row in board]
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    new_board[y][x] = stone

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flipped_positions = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == opponent:
            flipped_positions.append((nx, ny))
            nx += dx
            ny += dy

        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == stone:
            for fx, fy in flipped_positions:
                new_board[fy][fx] = stone

    return new_board

def evaluate_board(board, stone):
    opponent = 3 - stone
    my_score = sum(row.count(stone) for row in board)
    opponent_score = sum(row.count(opponent) for row in board)
    return my_score - opponent_score

def minimax(board, stone, depth, maximizing):
    if depth == 0:
        return evaluate_board(board, stone)

    opponent = 3 - stone
    best_score = float('-inf') if maximizing else float('inf')

    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone if maximizing else opponent, x, y):
                new_board = simulate_move(board, stone if maximizing else opponent, x, y)
                score = minimax(new_board, stone, depth - 1, not maximizing)
                if maximizing:
                    best_score = max(best_score, score)
                else:
                    best_score = min(best_score, score)

    return best_score

class EagarAI(object):
    """
    最も多くの石を裏返せる場所を選ぶAIクラス。
    """

    def face(self):
        # AIのシンボルとしての顔文字を返す
        return "🤖"

    def place(self, board, stone):
        """
        最も多くの石を裏返せる場所を選んで返す。
        board: 2次元配列のオセロボード
        stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
        return: 選んだ位置 (x, y)
        """
        max_flipped = -1
        best_move = None

        # ボード全体をチェックして最良の場所を探す
        for y in range(len(board)):
            for x in range(len(board[0])):
                flipped = count_flipped(board, stone, x, y)  # 裏返せる石の数を計算
                if flipped > max_flipped:
                    max_flipped = flipped
                    best_move = (x, y)  # 最良の位置を更新

        return best_move  # 最良の位置を返す

class MinimaxAI(EagarAI):
    def place(self, board, stone):
        best_score = float('-inf')
        best_move = None

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    new_board = simulate_move(board, stone, x, y)
                    score = minimax(new_board, stone, depth=2, maximizing=False)
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

play_othello(MinimaxAI())
