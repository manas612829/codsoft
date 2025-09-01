#!/usr/bin/env python3
"""
Tic-Tac-Toe (Human vs Unbeatable AI)
------------------------------------
- Human plays 'X' (goes first by default).
- AI plays 'O' and uses Minimax (with optional Alpha-Beta pruning) to be unbeatable.
- Run: python tictactoe_ai.py
- Toggle options at the top (HUMAN_FIRST, USE_ALPHA_BETA).
"""

from typing import List, Optional, Tuple
import math

# ====== Configuration ======
HUMAN = 'X'
AI = 'O'
EMPTY = ' '
HUMAN_FIRST = True          # Set False if you want the AI to start
USE_ALPHA_BETA = True       # Minimax with alpha-beta pruning for speed


# ====== Game Utilities ======
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),    # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),    # cols
    (0, 4, 8), (2, 4, 6)                # diagonals
]


def print_board(board: List[str]) -> None:
    """Pretty-print the current board."""
    rows = [board[i:i+3] for i in range(0, 9, 3)]
    def cell(c): return c if c != EMPTY else '·'
    print("\n  1   2   3")
    for r, row in enumerate(rows, start=1):
        print(f"{r} {cell(row[0])} | {cell(row[1])} | {cell(row[2])}")
        if r < 3:
            print("  ---+---+---")
    print()


def winner(board: List[str]) -> Optional[str]:
    """Return 'X' or 'O' if someone won, else None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def available_moves(board: List[str]) -> List[int]:
    return [i for i, v in enumerate(board) if v == EMPTY]


def is_terminal(board: List[str]) -> bool:
    return winner(board) is not None or not available_moves(board)


def score(board: List[str]) -> int:
    w = winner(board)
    if w == AI:
        return 1
    if w == HUMAN:
        return -1
    return 0  # draw


# ====== Minimax (with optional Alpha-Beta) ======
def minimax(board: List[str],
            maximizing: bool,
            alpha: float = -math.inf,
            beta: float = math.inf) -> Tuple[int, Optional[int]]:
    if is_terminal(board):
        return score(board), None

    best_move = None
    order = move_order(board)  # heuristic order

    if maximizing:
        best_score = -math.inf
        for m in order:
            board[m] = AI
            s, _ = minimax(board, False, alpha, beta)
            board[m] = EMPTY
            if s > best_score:
                best_score, best_move = s, m
            if USE_ALPHA_BETA:
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score, best_move
    else:
        best_score = math.inf
        for m in order:
            board[m] = HUMAN
            s, _ = minimax(board, True, alpha, beta)
            board[m] = EMPTY
            if s < best_score:
                best_score, best_move = s, m
            if USE_ALPHA_BETA:
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score, best_move


def move_order(board: List[str]) -> List[int]:
    """Heuristic move ordering: center, corners, then edges."""
    center = [4] if board[4] == EMPTY else []
    corners = [i for i in [0, 2, 6, 8] if board[i] == EMPTY]
    edges = [i for i in [1, 3, 5, 7] if board[i] == EMPTY]
    return center + corners + edges


def best_ai_move(board: List[str]) -> int:
    _, move = minimax(board, maximizing=True)
    return move


# ====== Input Handling ======
def parse_move(s: str) -> Optional[int]:
    """Parse inputs like '1 3' or '23' into board index."""
    s = s.strip().replace(',', ' ')
    parts = [p for p in s.split() if p.isdigit()]
    if len(parts) == 2:
        r, c = int(parts[0]), int(parts[1])
    elif len(s) == 2 and all(ch.isdigit() for ch in s):
        r, c = int(s[0]), int(s[1])
    else:
        return None
    if 1 <= r <= 3 and 1 <= c <= 3:
        return (r - 1) * 3 + (c - 1)
    return None


def human_turn(board: List[str]) -> None:
    while True:
        raw = input("Your move (row col, e.g., '2 3'): ").strip()
        m = parse_move(raw)
        if m is None or board[m] != EMPTY:
            print("Invalid move. Try again.")
            continue
        board[m] = HUMAN
        break


# ====== Game Flow ======
def game_loop() -> None:
    board = [EMPTY] * 9
    turn_is_human = HUMAN_FIRST

    print("\nTic-Tac-Toe — Human (X) vs AI (O)")
    print("Enter your move as 'row col' (e.g., 1 3).")
    print_board(board)

    while True:
        if turn_is_human:
            human_turn(board)
        else:
            print("AI is thinking...")
            m = best_ai_move(board)
            board[m] = AI
            print(f"AI chose: row {(m // 3) + 1}, col {(m % 3) + 1}")
        print_board(board)

        w = winner(board)
        if w == HUMAN:
            print("You win! (Nice job!)")
            break
        elif w == AI:
            print("AI wins. Better luck next time.")
            break
        elif not available_moves(board):
            print("It's a draw.")
            break

        turn_is_human = not turn_is_human


if __name__ == "__main__":
    game_loop()
