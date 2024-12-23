import random

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False

def count_flippable_stones(board, stone, x, y):
    """
    指定した場所に石を置いた場合にひっくり返せる石の数を計算する関数。
    """
    if board[y][x] != 0:
        return 0

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    total_flips = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flips = 0

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            flips += 1

        if flips > 0 and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            total_flips += flips

    return total_flips

def get_possible_moves(board, stone):
    """
    石を置ける座標と、それぞれの座標でひっくり返せる石の数を返す。
    """
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                flips = count_flippable_stones(board, stone, x, y)
                moves.append((x, y, flips))
    return moves

class SmartEagerAI(object):
    def face(self):
        return "🦉"  # SmartEagerAIの顔文字

    def place(self, board, stone):
        # 手順1: 石を置ける座標とそれぞれのポイントを取得
        possible_moves = get_possible_moves(board, stone)

        if not possible_moves:
            return None  # 合法手がない場合はパス

        # 手順2: 四隅のチェック
        corners = [(0, 0), (0, len(board) - 1), (len(board[0]) - 1, 0), (len(board[0]) - 1, len(board) - 1)]
        corner_moves = [move for move in possible_moves if (move[0], move[1]) in corners]

        if corner_moves:
            # 四隅に置ける場合はその中で最大ポイントの場所を選ぶ
            max_flips = max(corner_moves, key=lambda move: move[2])[2]
            best_corner_moves = [move for move in corner_moves if move[2] == max_flips]
            return random.choice(best_corner_moves)[:2]

        # 手順1で取得した座標の中で最大ポイントの場所を選ぶ
        max_flips = max(possible_moves, key=lambda move: move[2])[2]
        best_moves = [move for move in possible_moves if move[2] == max_flips]

        # ポイントが同じ場合はランダムに選択
        return random.choice(best_moves)[:2]

# 動作確認
from kogi_canvas import play_othello

BLACK = 1
WHITE = 2

board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

play_othello(SmartEagerAI())
