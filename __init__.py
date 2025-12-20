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
