from random import choice

# Winning patterns as bitmasks
WIN_PATTERNS = (56, 146, 273, 84, 448, 7, 292, 73)
ALL_MOVES = (16, 1, 4, 64, 256, 2, 8, 32, 128)
ALL_MOVES_ORDERED = tuple(1 << p for p in range(9))
TRANSFORMATIONS = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8),  # Identity
    (2, 5, 8, 1, 4, 7, 0, 3, 6),  # Rotate 90
    (8, 7, 6, 5, 4, 3, 2, 1, 0),  # Rotate 180
    (6, 3, 0, 7, 4, 1, 8, 5, 2),  # Rotate 270
    (2, 1, 0, 5, 4, 3, 8, 7, 6),  # Mirror vertical
    (6, 7, 8, 3, 4, 5, 0, 1, 2),  # Mirror horizontal
    (0, 3, 6, 1, 4, 7, 2, 5, 8),  # Mirror diagonal \
    (8, 5, 2, 7, 4, 1, 6, 3, 0),  # Mirror diagonal /
)

def to_bit_format(number):
    if number < 0:
        number = 2**9 - number
    string = ""
    while number:
        rest = number & 1
        number >>= 1
        string += str(rest)
    return string[::-1]

def check_winner(board_x, board_o):
    for pattern in WIN_PATTERNS:
        if board_x & pattern == pattern:
            return 1
        if board_o & pattern == pattern:
            return -1
    if board_x | board_o == 0b111111111:
        return 0
    return None

def actions(board_x, board_o):
    bit_map = 0b111111111 & (~(board_x | board_o))

    for move in ALL_MOVES:
        action = bit_map & move
        if action == 0:
            continue
        yield action

def random_action(board_x, board_o):
    possible_choice = [action for action in actions(board_x, board_o)]
    return choice(possible_choice)

def play(mx, mo, action, maximize):
    return (mx | action, mo) if maximize else (mx, mo | action)

def random_position(moves):
    mx, mo = 0, 0
    for counter in range(moves):
        action = random_action(mx, mo)
        mx, mo = play(mx, mo, action, counter % 2 == 0)
    return mx, mo

def transform(mask, t):
    return sum(((mask >> i) & 1) << t[i] for i in range(9))

def inverse_transform(mask, t):
    return sum(((mask >> t[i]) & 1) << i for i in range(9))

def hashes_transform(mx, mo, t):
    return sum(((((mx >> i) & 1) << 9) | ((mo >> i) & 1)) << t[i] for i in range(9))

def hash_board(mx, mo):
    return min(hashes_transform(mx, mo, t) for t in TRANSFORMATIONS)

def hash_transform_board(mx, mo):
    return min(((hashes_transform(mx, mo, TRANSFORMATIONS[i]), i) for i in range(8)), key=lambda lst: lst[0])



def display_board(board_x, board_o):
    board = [' '] * 9
    for i in range(9):
        v = ALL_MOVES_ORDERED[i]
        if board_x & v:
            board[i] = 'X'
            if board_o & v:
                board[i] = '#'
        elif board_o & v:
            board[i] = 'O'
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")

if __name__ == "__main__":
    mx, mo = 0b100110000, 0b010000110
    bm = 0b000001000
    print(mx, mo, bm)
    display_board(mx, mo)
    _hash, _index = hash_transform_board(mx, mo)
    hashed_bm = transform(bm, TRANSFORMATIONS[_index])
    print(f"The hash of board: {_hash}")
    print(f"The index of hash: {_index}")
    print(f"The hashed best moved: {hashed_bm}")
    print(f"The inverse hashed move: {inverse_transform(hashed_bm, TRANSFORMATIONS[_index])}")
    index = 7
    a, b = transform(mx, TRANSFORMATIONS[index]), transform(mo, TRANSFORMATIONS[index])
    print(f"Changed board:")
    display_board(a, b)
    _hash, _index = hash_transform_board(a, b)
    print(f"Hash: {_hash}")
    print(f"Hashed at index: {_index}")
    print(f"Changed best move: {inverse_transform(hashed_bm, TRANSFORMATIONS[_index])}")