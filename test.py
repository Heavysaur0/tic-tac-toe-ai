import random

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

def display_board(x_mask: int, o_mask: int):
    symbols = [' '] * 9  # Initialize board with empty spaces

    for i in range(9):
        if (x_mask >> (8 - i)) & 1:
            symbols[i] = 'X'
        elif (o_mask >> (8 - i)) & 1:
            symbols[i] = 'O'

    board = f"""
     {symbols[0]} | {symbols[1]} | {symbols[2]} 
    ---+---+---
     {symbols[3]} | {symbols[4]} | {symbols[5]} 
    ---+---+---
     {symbols[6]} | {symbols[7]} | {symbols[8]} 
    """
    print(board)



def hashes_transform(mx, mo, t):
    return sum(((((mx >> i) & 1) << 9) | ((mo >> i) & 1)) << t[i] for i in range(9))

def hash_mask(m, t):
    return sum(((m >> i) & 1) << t[i] for i in range(9))

def hash_board(mx, mo):
    return min(hashes_transform(mx, mo, t) for t in TRANSFORMATIONS)


mx, mo = 0b001001001, 0b010001000
mx, mo = random.randrange(256), random.randrange(256)
values = []
for trsf in TRANSFORMATIONS:
    h = hashes_transform(mx, mo, trsf)
    values.append(h)
    print(h)
print()
print(hash_board(mx, mo))
print(min(values))