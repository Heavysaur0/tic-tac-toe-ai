def check_winner(mx, mo):
    if mx | mo == 0x1FF:
        return 0
    for pattern in (56, 146, 273, 84, 448, 7, 292, 73):
        if pattern & mx == pattern:
            return 1
        if pattern & mo == pattern:
            return -1
    return None


def actions(mx, mo):
    bit_map = 0x1FF & (~(mx | mo))
    for action in (16, 1, 4, 64, 256, 2, 8, 32, 128):
        if bit_map & action:
            yield action


def negamax(mx, mo, player):
    def recursive_function(mx, mo):
        if (value := check_winner(mx, mo)) is not None:
            return value
        
        return max(- recursive_function(mo, mx | action) for action in actions(mx, mo))
    
    if player == 1:
        return recursive_function(mx, mo)
    return - recursive_function(mo, mx)

def negamax_best_move(mx, mo, player):
    def recursive_function(mx, mo):
        if (value := check_winner(mx, mo)) is not None:
            return value, None
        
        best_move = None
        best_score = -1
        for action in actions(mx, mo):
            score, _ = recursive_function(mo, mx | action)
            if best_score <= - score:
                best_score = - score
                best_move = action

        return best_score, best_move
    
    if player == 1:
        return recursive_function(mx, mo)
    value, best_move = recursive_function(mo, mx)
    return - value, best_move

def negamax_alpha_beta(mx, mo, player):
    def recursive_function(mx, mo, alpha, beta):
        if (value := check_winner(mx, mo)) is not None:
            return value

        best_score = -1
        for action in actions(mx, mo):
            score = - recursive_function(mo, mx | action, - beta, - alpha) / 2
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return best_score

    if player == 1:
        return recursive_function(mx, mo, -1, 1)
    return -recursive_function(mo, mx, -1, 1)

def negamax_alpha_beta_best_move(mx, mo, player):
    def recursive_function(mx, mo, alpha, beta):
        if (value := check_winner(mx, mo)) is not None:
            return value, None

        best_move = None
        best_score = -1
        for action in actions(mx, mo):
            score, _ = recursive_function(mo, mx | action, - beta, - alpha)
            score = - score / 2
            if score >= best_score:
                best_score = score
                best_move = action
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_score, best_move

    if player == 1:
        return recursive_function(mx, mo, -1, 1)
    value, best_move = recursive_function(mo, mx, -1, 1)
    return - value, best_move

def display(board_x, board_o):
    board = [' '] * 9
    for i in range(9):
        v = 0x100 >> i
        if board_x & v:
            board[i] = 'X'
            if board_o & v:
                board[i] = '#'
        elif board_o & v:
            board[i] = 'O'
    
    for i in range(3):
        print(f"{board[3*i]} | {board[3*i+1]} | {board[3*i+2]}")


def display_eval(mx, mo, player):
    board = ['  ' for _ in range(9)]
    bit_map = 0x1FF & (~(mx | mo))
    for i in range(9):
        action = 0x100 >> i
        if not bit_map & action:
            continue
        nx = mx | action if player == 1 else mx
        no = mo if player == 1 else mo | action
        board[i] = negamax_alpha_beta(nx, no, - player)
    
    for i in range(3):
        print(f"{board[3*i]:2} | {board[3*i+1]:2} | {board[3*i+2]:2}")



def main():
    mx = 0b100100000
    mo = 0b000000110
    player = 1
    print("Current board:")
    display(mx, mo)
    print("Negamax evaluation of each move:")
    display_eval(mx, mo, player)
    value, best_move = negamax_alpha_beta_best_move(mx, mo, player)
    print(f"Evaluation: {value}")
    print(f"Best move: {best_move}")
    nx = mx | best_move if player == 1 else mx
    no = mo if player == 1 else mo | best_move
    print("Situation after move")
    display(nx, no)

if __name__ == '__main__':
    main()