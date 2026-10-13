# Task 2 - Tic-Tac-Toe against an unbeatable AI
# The computer uses minimax with alpha-beta pruning.
# Human plays X, computer plays O. Board positions are numbered 1-9.

import math

HUMAN = "X"
AI = "O"
EMPTY = " "

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


def show_board(board):
    print()
    for r in range(3):
        row = board[r * 3: r * 3 + 3]
        print(" " + " | ".join(row))
        if r < 2:
            print("---+---+---")
    print()


def show_help_board():
    print("Positions are numbered like this:")
    print(" 1 | 2 | 3")
    print("---+---+---")
    print(" 4 | 5 | 6")
    print("---+---+---")
    print(" 7 | 8 | 9")


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def free_cells(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def minimax(board, depth, is_ai_turn, alpha, beta):
    """Returns a score from the AI's point of view.
    Positive = good for AI, negative = good for human.
    depth is used so that quicker wins score higher than slow ones."""
    w = winner(board)
    if w == AI:
        return 10 - depth
    if w == HUMAN:
        return depth - 10
    if is_full(board):
        return 0

    if is_ai_turn:
        best = -math.inf
        for move in free_cells(board):
            board[move] = AI
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move] = EMPTY
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break          # this branch cannot improve the parent's choice
        return best
    else:
        best = math.inf
        for move in free_cells(board):
            board[move] = HUMAN
            score = minimax(board, depth + 1, True, alpha, beta)
            board[move] = EMPTY
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def best_move(board):
    best_score = -math.inf
    move_choice = None
    for move in free_cells(board):
        board[move] = AI
        score = minimax(board, 1, False, -math.inf, math.inf)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            move_choice = move
    return move_choice


def ask_human_move(board):
    while True:
        raw = input("Your move (1-9): ").strip()
        if len(raw) != 1 or raw not in "123456789":
            print("Please type a number between 1 and 9.")
            continue
        pos = int(raw) - 1
        if pos < 0 or pos > 8:
            print("That's outside the board.")
        elif board[pos] != EMPTY:
            print("That spot is already taken.")
        else:
            return pos


def play_one_game():
    board = [EMPTY] * 9
    show_help_board()

    first = input("Do you want to go first? (y/n): ").strip().lower()
    human_turn = first != "n"

    while True:
        if human_turn:
            move = ask_human_move(board)
            board[move] = HUMAN
        else:
            print("Computer is thinking...")
            move = best_move(board)
            board[move] = AI
            print(f"Computer plays {move + 1}")

        show_board(board)

        w = winner(board)
        if w == HUMAN:
            print("You win!")
            return
        if w == AI:
            print("Computer wins.")
            return
        if is_full(board):
            print("It's a draw.")
            return

        human_turn = not human_turn


def main():
    print("=== Tic-Tac-Toe ===")
    print("You are X, the computer is O.")
    while True:
        play_one_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGame ended.")
