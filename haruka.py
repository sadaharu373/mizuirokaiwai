from kogi_canvas import play_othello, PandaAI
!pip install -U kogi-canvas
class EagerAI(object):
    def face(self):
        return "😎"  # 顔文字を変更

    def place(self, board, stone):
        best_x, best_y = -1, -1
        max_flipped = -1  # ひっくり返せる石の最大数を初期化

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    # 石を置いた場合にひっくり返せる石の数を計算
                    flipped_count = self.count_flipped_stones(board, stone, x, y)

                    # より多くの石をひっくり返せる場所が見つかったら更新
                    if flipped_count > max_flipped:
                        max_flipped = flipped_count
                        best_x, best_y = x, y

        # 最適な場所が見つかった場合はその座標を返す
        if best_x != -1:
            return best_x, best_y
        else:
            # 置ける場所がない場合は、random_place でランダムに置く
            return random_place(board, stone)

    def count_flipped_stones(self, board, stone, x, y):
            flipped_count = 0
            opponent = 3 - stone
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                stones_to_flip = []  # ひっくり返す石を一時的に保存

                while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                    stones_to_flip.append((nx, ny))
                    nx += dx
                    ny += dy

                if stones_to_flip and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                    flipped_count += len(stones_to_flip)  # ひっくり返せる石の数を合計

            return flipped_count
from kogi_canvas import play_othello, PandaAI

BLACK=1
WHITE=2

board = [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,1,2,0,0],
        [0,0,2,1,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
]

play_othello(PandaAI()) # ここを自分の作ったAIに変える
