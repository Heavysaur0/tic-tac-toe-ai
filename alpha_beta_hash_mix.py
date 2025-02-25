import time

from morpion_essentials import *


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

def alpha_beta_pruning_hash(mx, mo, maximize):
    """average of 0.0124s"""
    hash_dic = {}

    def alpha_beta_pruning(mx, mo, alpha, beta, maximize):
        if (value := check_winner(mx, mo)) is not None:
            return value

        hash_val = hash_board(mx, mo)
        if hash_val in hash_dic:
            return hash_dic[hash_val]

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

        hash_dic[hash_val] = value
        return value

    return alpha_beta_pruning(mx, mo, -1, 1, maximize)

def alpha_beta_pruning_hash_moves(mx, mo, maximize):
    """Alpha-beta pruning with move storage (average of ~0.0122s)."""
    hash_dic = {}

    def alpha_beta_pruning(mx, mo, alpha, beta, maximize):
        if (value := check_winner(mx, mo)) is not None:
            return value, None

        hash_val = hash_board(mx, mo)
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

        hash_dic[hash_val] = (value, best_move)
        return value, best_move

    eval, move = alpha_beta_pruning(mx, mo, -1, 1, maximize)
    return eval, move, hash_dic


def test_time(mx, mo, maximize, iterations = 1000):
    print(f"Starting time evaluation for board:")
    display_board(mx, mo)
    times = 0
    values = []
    for _ in range(iterations):
        st = time.time()
        eval, move, _ = alpha_beta_pruning_hash_moves(mx, mo, maximize)
        et = time.time()
        values.append(eval)
        times += et - st
    print(f"Total time {times:.5f}s over {iterations} iterations.")
    print(f"That makes up for an average of {times / iterations:.6f}s.")
    print(len(values))


moves = 0
mx, mo = random_position(moves)
display_board(mx, mo)

st = time.time()
eval, move, _ = alpha_beta_pruning_hash_moves(mx, mo, moves % 2 == 0)
et = time.time()
print(f"Evaluation: {eval}, Best Move: {bin(move)}")
print(f"It took: {et - st:.6f}s")
test_time(mx, mo, moves % 2 == 0)