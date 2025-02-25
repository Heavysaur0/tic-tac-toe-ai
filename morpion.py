from random import choice
import time

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

def actions(board_x, board_o, all_moves = ALL_MOVES):
    bit_map = 0b111111111 & (~(board_x | board_o))

    for move in all_moves:
        action = bit_map & move
        if action == 0:
            continue
        yield action

def random_action(board_x, board_o):
    possible_choice = [action for action in actions(board_x, board_o)]
    return choice(possible_choice)

def random_position(moves):
    mx, mo = 0, 0
    for counter in range(moves):
        action = random_action(mx, mo)
        if counter % 2 == 0:
            mx |= action
        else:
            mo |= action
    return mx, mo





def minimax(mx, mo, maximize):
    if (value := check_winner(mx, mo)) is not None:
        return value

    if maximize:
        value = -1
        for action in actions(mx, mo):
            value = max(value, minimax(mx | action, mo, False))
    else:
        value = 1
        for action in actions(mx, mo):
            value = min(value, minimax(mx, mo | action, True))
    return value

def alpha_beta_pruning(mx, mo, alpha, beta, maximize):
    """average of 0.014s"""
    if (value := check_winner(mx, mo)) is not None:
        return value

    if maximize:
        value = -1
        for action in actions(mx, mo):
            eval = alpha_beta_pruning(mx | action, mo, alpha, beta, False)
            value = max(value, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
    else:
        value = 1
        for action in actions(mx, mo):
            eval = alpha_beta_pruning(mx, mo | action, alpha, beta, True)
            value = min(value, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
    return value


def hashes_transform(mx, mo, t):
    return sum(((((mx >> i) & 1) << 9) | ((mo >> i) & 1)) << t[i] for i in range(9))

def hash_board(mx, mo):
    return min(hashes_transform(mx, mo, t) for t in TRANSFORMATIONS)


def alpha_beta_pruning_hash(mx, mo, maximize):
    """average of 0.0124s"""
    hash_dic = {}

    def alpha_beta_pruning(mx, mo, alpha, beta, maximize):
        if (value := check_winner(mx, mo)) is not None:  # Check winner first!
            return value

        hash_val = hash_board(mx, mo)  # Compute hash only if no winner
        if hash_val in hash_dic:
            return hash_dic[hash_val]

        if maximize:
            value = -1
            for action in actions(mx, mo):
                eval = alpha_beta_pruning(mx | action, mo, alpha, beta, False)
                value = max(value, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:  # Alpha-beta pruning
                    break
        else:
            value = 1
            for action in actions(mx, mo):
                eval = alpha_beta_pruning(mx, mo | action, alpha, beta, True)
                value = min(value, eval)
                beta = min(beta, eval)
                if beta <= alpha:  # Alpha-beta pruning
                    break

        hash_dic[hash_val] = value  # Store only necessary values
        return value

    return alpha_beta_pruning(mx, mo, -1, 1, maximize)

def test_time(eval_function, iterations = 1000):
    mx, mo = 0, 0
    print(f"Starting time evaluation for board:")
    display_board(mx, mo)
    times = 0
    for _ in range(iterations):
        st = time.time()
        eval_function(mx, mo, True)
        et = time.time()
        times += et - st
    print(f"Total time {times:.5f}s over {iterations} iterations.")
    print(f"That makes up for an average of {times / iterations:.6f}s.")

def display_ai_move(mx, mo, maximize, eval_function):
    print(f"For board:")
    display_board(mx, mo)
    print(f"Here are its recommendations:")
    st = time.time()
    board = ['  '] * 9
    bit_map = 0b111111111 & (~(mx | mo))
    for i, action in enumerate(ALL_MOVES_ORDERED):
        if action & bit_map == 0:
            continue
        if maximize:
            eval = eval_function(mx | action, mo, False)
        else:
            eval = eval_function(mx, mo | action, True)
        board[i] = eval
    et = time.time()

    print(f"{board[0]:2} | {board[1]:2} | {board[2]:2}")
    print("---+----+---")
    print(f"{board[3]:2} | {board[4]:2} | {board[5]:2}")
    print("---+----+---")
    print(f"{board[6]:2} | {board[7]:2} | {board[8]:2}")
    print(f"It took: {et - st:.6f}s")

def recursive_display(mx, mo, maximize):
    if maximize:
        for action in actions(mx, mo):
            display_ai_move(mx | action, mo, False)
            print("==============")
    else:
        for action in actions(mx, mo):
            display_ai_move(mx, mo | action, True)
            print("==============")


def eval_foo(type):
    if type == 0:
        return lambda mx, mo, maximize: minimax(mx, mo, maximize)
    if type == 1:
        return lambda mx, mo, maximize: alpha_beta_pruning(mx, mo, -1, 1, maximize)
    if type == 2:
        return lambda mx, mo, maximize: alpha_beta_pruning_hash(mx, mo, maximize)

type = 0
eval_function = eval_foo(type)
moves = 0
mx, mo = random_position(moves)

display_board(mx, mo)
st = time.time()
value = eval_function(mx, mo, moves % 2 == 0)
et = time.time()
print(f"AI result: {value}")
print(f"It took: {et - st:.6f}s")
display_ai_move(mx, mo, moves % 2 == 0, eval_function)