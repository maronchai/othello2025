import numpy as np

# 盤面のサイズ
SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = 2

def get_valid_moves(board, color):
    moves = []
    for r in range(SIZE):
        for c in range(SIZE):
            if can_put(board, color, r, c):
                moves.append((r, c))
    return moves

def can_put(board, color, r, c):
    if board[r, c] != EMPTY: return False
    opponent = 3 - color
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE and board[nr, nc] == opponent:
            nr += dr
            nc += dc
            while 0 <= nr < SIZE and 0 <= nc < SIZE:
                if board[nr, nc] == EMPTY: break
                if board[nr, nc] == color: return True
                nr += dr
                nc += dc
    return False

def apply_move(board, color, r, c):
    new_board = board.copy()
    new_board[r, c] = color
    opponent = 3 - color
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dr, dc in directions:
        path = []
        nr, nc = r + dr, c + dc
        while 0 <= nr < SIZE and 0 <= nc < SIZE and new_board[nr, nc] == opponent:
            path.append((nr, nc))
            nr += dr
            nc += dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE and new_board[nr, nc] == color:
            for pr, pc in path:
                new_board[pr, pc] = color
    return new_board

# --- ここに myai 関数を定義します ---
def myai(board, color):
    """
    盤面の重み付け（角を優先）に基づいた戦略をとるAI
    """
    valid_moves = get_valid_moves(board, color)
    if not valid_moves:
        return None

    # 盤面の場所ごとの価値（重み付け）
    weights = np.array([
        [ 100, -20,  10,   5,   5,  10, -20, 100],
        [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
        [  10,  -2,   5,   1,   1,   5,  -2,  10],
        [   5,  -2,   1,   0,   0,   1,  -2,   5],
        [   5,  -2,   1,   0,   0,   1,  -2,   5],
        [  10,  -2,   5,   1,   1,   5,  -2,  10],
        [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
        [ 100, -20,  10,   5,   5,  10, -20, 100]
    ])

    best_score = -float('inf')
    best_move = valid_moves[0]

    for r, c in valid_moves:
        # 重みが高い場所を優先的に選ぶ
        score = weights[r, c]
        if score > best_score:
            best_score = score
            best_move = (r, c)

    return best_move

def myai(board, color):
    """
    オセロAIのメイン関数。
    ボードの状態と、自分が打つべき色を受け取り、次に打つべき手の座標を返す。
    """

    # Determine board dimensions dynamically
    rows = len(board)
    if rows == 0:
        return None # Cannot make a move on an empty board

    # Assuming all rows have the same number of columns
    cols = len(board[0])
    if cols == 0:
        return None # Cannot make a move if rows are empty

    # --- ヘルパー関数: 指定されたセルに石を置いた場合に裏返る石のリストを返す ---
    def get_flipped_stones(r, c, board, color):
        # 盤外、または空でないセルであれば無効
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != 0:
            return []

        opponent_color = 3 - color # 相手の色 (1 -> 2, 2 -> 1)
        all_flipped_in_all_directions = []

        # 8方向を定義 (上下左右、斜め)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            current_flipped_in_direction = []
            nr, nc = r + dr, c + dc # 探索開始位置

            # 相手の石が連続しているかチェック
            found_opponent = False
            while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == opponent_color:
                current_flipped_in_direction.append((nr, nc))
                nr += dr
                nc += dc
                found_opponent = True

            # 相手の石の後に自分の石があるかチェック
            if found_opponent and 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == color:
                all_flipped_in_all_directions.extend(current_flipped_in_direction)

        return all_flipped_in_all_directions

    # --- 1. 現状で打てる手のリストを取得 (裏返せる石がある手のみ) ---
    valid_moves_with_flips_count = {} # キー: (r, c), 値: 裏返せる石の数

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 0: # 空きマスのみを対象
                flipped_stones = get_flipped_stones(r, c, board, color)
                if flipped_stones: # 裏返せる石がある場合のみ有効な手とみなす
                    valid_moves_with_flips_count[(r, c)] = len(flipped_stones)

    # ----------------------------------------

    # --- 2. 打てる手の中から、最適/次に打つ手を決定 ---

    if not valid_moves_with_flips_count:
        # 打てる手がない場合（パス）
        return None

    # 【現在の選択ロジック（最も多く石を裏返せる手を選ぶ）】
    # より高度なAIロジックはここに実装します（例：ミニマックス法や評価関数）。

    best_move = None
    max_flips = -1

    for move, flips_count in valid_moves_with_flips_count.items():
        if flips_count > max_flips:
            max_flips = flips_count
            best_move = move

    # --- 3. 決定した手を返す ---
    return best_move
