import time

import pygame
import random
from morpion_essentials import *

# Game Constants
WIDTH, HEIGHT = 300, 300
GRID_SIZE = WIDTH // 3
LINE_WIDTH = 5
CIRCLE_RADIUS = GRID_SIZE // 3
CROSS_WIDTH = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (28, 170, 156)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")

# Hash Dictionary (Precomputed Moves)
hash_dic = {}

# Alpha-Beta Pruning Function (From Your Existing Code)
def alpha_beta_pruning_hash(mx, mo, maximize):
    """Alpha-beta pruning with move storage (average of ~0.0122s)."""
    def alpha_beta_pruning(mx, mo, alpha, beta, maximize):
        if (value := check_winner(mx, mo)) is not None:
            return value, None

        hash_val, index = hash_transform_board(mx, mo)
        if hash_val in hash_dic:
            return hash_dic[hash_val]

        best_move = None
        if maximize:
            value = -1
            for action in actions(mx, mo):
                eval, _ = alpha_beta_pruning(mx | action, mo, alpha, beta, False)
                if eval > value:
                    value, best_move = eval, action
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        else:
            value = 1
            for action in actions(mx, mo):
                eval, _ = alpha_beta_pruning(mx, mo | action, alpha, beta, True)
                if eval < value:
                    value, best_move = eval, action
                beta = min(beta, eval)
                if beta <= alpha:
                    break

        if best_move is not None:
            best_move = transform(best_move, TRANSFORMATIONS[index])
        hash_dic[hash_val] = (value, best_move)
        return value, best_move

    eval, move = alpha_beta_pruning(mx, mo, -1, 1, maximize)
    return eval, move

# Game Logic
def get_ai_move(mx, mo, ai_turn):
    st = time.time()

    hash_val, index = hash_transform_board(mx, mo)
    print(f"Board hash: {hash_val}")
    print(f"Index of hash: {index}")

    if hash_val in hash_dic:
        print(hash_dic[hash_val])
        best_move = hash_dic[hash_val][1]
        best_move = inverse_transform(best_move, TRANSFORMATIONS[index])
        et = time.time()
        print(f"AI was thinking for: {et - st:.6f}s (cached)")
        return best_move

    _, best_move = alpha_beta_pruning_hash(mx, mo, ai_turn)


    et = time.time()
    print(f"AI was thinking for: {et - st:.6f}s (computed)")
    return best_move


# Drawing Functions
def draw_board():
    screen.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * GRID_SIZE, 0), (i * GRID_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), LINE_WIDTH)

def draw_pieces(mx, mo):
    for i in range(9):
        x, y = (i % 3) * GRID_SIZE, (i // 3) * GRID_SIZE
        mask = 1 << i
        if mx & mask:
            pygame.draw.line(screen, CROSS_COLOR, (x + 20, y + 20), (x + GRID_SIZE - 20, y + GRID_SIZE - 20), CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, (x + GRID_SIZE - 20, y + 20), (x + 20, y + GRID_SIZE - 20), CROSS_WIDTH)
        elif mo & mask:
            pygame.draw.circle(screen, CIRCLE_COLOR, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), CIRCLE_RADIUS, CROSS_WIDTH)


def display_ai_thinking(mx, mo, maximize):
    st = time.time()
    board = ['   '] * 9
    bit_map = 0b111111111 & (~(mx | mo))
    for i, action in enumerate(ALL_MOVES_ORDERED):
        if action & bit_map == 0:
            continue
        nx, no = play(mx, mo, action, not maximize)
        eval = get_ai_move(nx, no, not maximize)
        board[i] = eval if eval is not None else 0
    et = time.time()

    print(f"For board:")
    display_board(mx, mo)
    print(f"Here are its recommendations:")
    print(f"{board[0]:3} | {board[1]:3} | {board[2]:3}")
    print("----+-----+----")
    print(f"{board[3]:3} | {board[4]:3} | {board[5]:3}")
    print("----+-----+----")
    print(f"{board[6]:3} | {board[7]:3} | {board[8]:3}")
    print(f"It took: {et - st:.6f}s")



# Game Loop
def main():
    running = True
    mx, mo = 0, 0
    player_maximize = True
    player_turn = player_maximize
    game_over = False
    last = (-1, -1)

    while running:
        draw_board()
        draw_pieces(mx, mo)
        if last != (mx, mo):
            display_board(mx, mo)
            print()
            last = (mx, mo)
        pygame.display.flip()

        if not game_over:
            if player_turn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        mx, mo = 0, 0
                        player_maximize = random.choice([True, False])
                        player_turn = player_maximize
                        game_over = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        move = 1 << (y // GRID_SIZE * 3 + x // GRID_SIZE)
                        if move & (mx | mo) == 0:
                            mx, mo = (mx | move, mo) if player_maximize else (mx, mo | move)
                            player_turn = not player_turn
            else:
                display_ai_thinking(mx, mo, not player_maximize)
                move = get_ai_move(mx, mo, not player_maximize)
                if move:
                    mx, mo = (mx | move, mo) if not player_maximize else (mx, mo | move)
                player_turn = not player_turn
                print(f"Moved chosen: {move}")
                display_ai_thinking(mx, mo, player_maximize)

            result = check_winner(mx, mo)
            if result is not None:
                game_over = True
                string = ("draw", "win for player 1", "win for player 2")[result]
                print(f"Game has ended, it's a {string} !")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mx, mo = 0, 0
                player_turn = random.choice([True, False])
                game_over = False

    pygame.quit()

if __name__ == "__main__":
    main()