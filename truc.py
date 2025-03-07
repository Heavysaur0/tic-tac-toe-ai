from morpion_essentials import ALL_MOVES_ORDERED, play, display_board, random_position
from morpion import negamax_alpha_beta_pruning


def full_board_value(mx, mo, player) -> tuple[int | str, ...]:
    """
    Returns a tuple representing the evaluation of each cell.
    -1 for bad moves, 0 for neutral moves, 1 for good moves.
    """
    board_value = [None for _ in range(9)]  # Initialize all cells as None
    
    bit_map = 0b111111111 & (~(mx | mo))  # Find available moves

    for i, action in enumerate(ALL_MOVES_ORDERED):
        if action & bit_map == 0:
            continue
        nx, no = play(mx, mo, action, player == 1)
        result = negamax_alpha_beta_pruning(nx, no, player == 1)
        board_value[i] = result
    
    return board_value

def display_eval(mx, mo, board):
    print(f"For board:")
    display_board(mx, mo)
    print(f"Here are its recommendations:")
    print(f"{board[0]:2} | {board[1]:2} | {board[2]:2}")
    print("---+----+---")
    print(f"{board[3]:2} | {board[4]:2} | {board[5]:2}")
    print("---+----+---")
    print(f"{board[6]:2} | {board[7]:2} | {board[8]:2}")


moves = 0
mx, mo = random_position(moves)
board_value = full_board_value(mx, mo, (-1) ** moves)
display_eval(mx, mo, board_value)