#include <stdio.h>
#include <stdint.h>
#include <time.h>

u_int16_t WIN_PATTERNS[8] = {56, 146, 273, 84, 448, 7, 292, 73};

int negamaxAlphaBeta(u_int16_t mx, u_int16_t mo, int alpha, int beta) {
    if ((mx | mo) == 0x1FF) return 0;
    for (int i = 0; i < 8; i++) {
        u_int16_t pattern = WIN_PATTERNS[i];
        if ((mx & pattern) == pattern) return 1;
        if ((mo & pattern) == pattern) return -1;
    }

    int value = -1;
    u_int16_t bitMap = 0x1FF & (~(mx | mo));
    for (int i = 0; i < 9; i++) {
        u_int16_t action = 1 << i;
        if ((bitMap & action) == 0) continue;

        int negamaxValue = - negamaxAlphaBeta(mo, mx | action, - beta, - alpha);

        value = (negamaxValue > value) ? negamaxValue : value;
        alpha = (value > alpha) ? value : alpha;
        if (beta <= alpha) break;
    }
    return value;
}

int negamaxEvaluate(u_int16_t mx, u_int16_t mo, int player) {
    if (player == 1) return negamaxAlphaBeta(mx, mo, -1, 1);
    return - negamaxAlphaBeta(mo, mx, -1, 1);
}


typedef struct {
    int eval;
    int best_move;
} NegamaxResult;

NegamaxResult negamaxAlphaBetaMove(u_int16_t mx, u_int16_t mo, int alpha, int beta, int is_top_level) {
    if ((mx | mo) == 0x1FF) return (NegamaxResult){0, -1}; // Draw case

    static u_int16_t patterns[8] = {56, 146, 273, 84, 448, 7, 292, 73};
    for (int i = 0; i < 8; i++) {
        u_int16_t pattern = patterns[i];
        if ((mx & pattern) == pattern) return (NegamaxResult){1, -1};  // Player wins
        if ((mo & pattern) == pattern) return (NegamaxResult){-1, -1}; // Opponent wins
    }

    int value = -1;
    int best_move = -1; // Store the best move in the local scope

    u_int16_t bitMap = 0x1FF & (~(mx | mo));
    for (int i = 0; i < 9; i++) {
        u_int16_t action = 1 << i;
        if ((bitMap & action) == 0) continue;

        NegamaxResult negamaxValue = negamaxAlphaBetaMove(mo, mx | action, -beta, -alpha, 0);
        negamaxValue.eval = -negamaxValue.eval; // Negate value for minimax switch

        if (negamaxValue.eval >= value) {
            value = negamaxValue.eval;
            best_move = i; // Store the best move found
        }

        alpha = (value > alpha) ? value : alpha;
        if (beta <= alpha) break;
    }

    return (NegamaxResult){value, best_move};
}

NegamaxResult negamaxEvaluateWithMove(u_int16_t mx, u_int16_t mo, int player) {
    if (player == 1) return negamaxAlphaBetaMove(mx, mo, -1, 1, 1);
    NegamaxResult result = negamaxAlphaBetaMove(mo, mx, -1, 1, 1);
    result.eval = -result.eval; // Negate because we're switching perspective
    return result;
}



void displayBoard(u_int16_t mx, u_int16_t mo) {
    char board[9];

    for (int i = 0; i < 9; i++) {
        u_int16_t action = 0x100 >> i;
        if ((action & mx) != 0) {
            if ((action & mo) == 0) {
                board[i] = 'X';
            } else {
                board[i] = '#';
            }
        } else if ((action & mo) != 0) {
            board[i] = 'O';
        } else {
            board[i] = ' ';
        }
    }
    
    printf("Current board:\n");
    for (int i = 0; i < 3; i++) {
        printf(" %c | %c | %c \n", board[3*i], board[3*i+1], board[3*i+2]);
    }
}

void displayNegamaxBoard(u_int16_t mx, u_int16_t mo, int player) {
    int board[9];
    u_int16_t bitMap = 0x1FF & (~(mx | mo));
    
    for (int i = 0; i < 9; i++) {
        u_int16_t action = 0x100 >> i;
        if ((bitMap & action) == 0) { 
            board[i] = 2;
        } else {
            u_int16_t nx = (player == 1) ? mx | action : mx;
            u_int16_t no = (player == 1) ? mo : mo | action;
            board[i] = negamaxEvaluate(nx, no, -player);
        }
    }

    printf("Negamax evaluation of each move:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            int value = board[3 * i + j];
            if (value == 2) {
                printf("    ");
            } else {
                printf(" %2d ", value);
            }
            if (j < 2) printf("|");
        }
        printf("\n");
    }
}



int main() {
    u_int16_t mx = 0b000000000;
    u_int16_t mo = 0b000000000;
    int player = 1;

    displayBoard(mx, mo);
    int value = negamaxEvaluate(mx, mo, player);
    displayNegamaxBoard(mx, mo, player);
    printf("Negamax value: %d\n", value);
    printf("\n");


    // Start timing
    clock_t start_time = clock();

    // Call your function
    NegamaxResult result = negamaxEvaluateWithMove(mx, mo, player);

    // End timing
    clock_t end_time = clock();

    // Calculate elapsed time
    double time_taken = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;

    printf("Best move: %d, Evaluation: %d\n", result.best_move, result.eval);
    printf("Time taken: %f seconds\n", time_taken);

    return 0;
}