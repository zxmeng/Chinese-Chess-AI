# check checking
# checkmate checking
# input: board and move
# output: bool

import validation
import moveGeneration

# board: 9 x 10
# player: red(r) or black(b)
piece_b = ['k','a','b','n','r','c','p']
piece_r = ['K','A','B','N','R','C','P']


# decide whether current player is in check
# 0 for no, 1 for yes
def check(board, player):
    k_row = 0
    k_col = 0

    if player == 'r':
        # first find the king of red
        for r in range(7,10):
            for c in range(3,6):
                if board[r][c] == 'K':
                    k_row = r
                    k_col = c
                    break
        # second, find whether there is valid move for black pieces to capture red king
        for r in range(10):
            for c in range(9):
                if board[r][c] in piece_b:
                    move = [r, c, k_row, k_col]
                    if validation.validate(board, move, 'b') == 1:
                        return 1,move

    elif player == 'b':
        # first find the king of black
        for r in range(3):
            for c in range(3,6):
                if board[r][c] == 'k':
                    k_row = r
                    k_col = c
                    break
        # second, find whether there is valid move for black pieces to capture red king
        for r in range(10):
            for c in range(9):
                if board[r][c] in piece_r:
                    move = [r, c, k_row, k_col]
                    if validation.validate(board, move, 'r') == 1:
                        return 1,move

    return 0,[0,0,0,0]


# return tuple (checkflag, moves(if any))
# whether player is checkmated
# 0 for no, 1 for yes
def checkmate(board, player):
    moves = moveGeneration.generatemoves(board, player)
    output = []
    checkflag = 1
    newboard = [[0 for x in range(9)] for y in range(10)]
    for move in moves:
        # execute the move
        for r in range(10):
            for c in range(9):
                newboard[r][c] = board[r][c]
        newboard[move[2]][move[3]] = newboard[move[0]][move[1]]
        newboard[move[0]][move[1]] = '1'
        if check(newboard, player) == 0:
            output.append(move)
            checkflag = 0

    return checkflag, output



