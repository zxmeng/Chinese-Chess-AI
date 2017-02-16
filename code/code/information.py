# -------------------------------------------------------+
# get information of chessboard                          |
# used to extract information in prediction              |
# -------------------------------------------------------+

from moveGeneration import *
from validation import *
import numpy as np
import os

piece_b = ['k', 'a', 'b', 'n', 'r', 'c', 'p']
piece_r = ['K', 'A', 'B', 'N', 'R', 'C', 'P']
piece_list = {'b': piece_b, 'r': piece_r}
piece_list_op = {'b': piece_r, 'r': piece_b}


def fen_reader(fen):
    # input fen: [chessboard string],x,x,x,x,[type]
    chessboard = [['\0' for c in range(9)] for r in range(10)]
    for r in range(10):
        for c in range(9):
            chessboard[r][c] = fen[r * 10 + c]
    player = fen[100]
    return chessboard, player


def flip(chessboard, player):
    # assume player is always the lower side of chessboard, in uppercase
    # fip the board if player is black
    if player == 'b':
        newboard = [['1' for c in range(9)] for r in range(10)]
        for r in range(10):
            for c in range(9):
                if chessboard[9-r][8-c] in piece_b:
                    newboard[r][c] = chessboard[9-r][8-c].upper()
                elif chessboard[9-r][8-c] in piece_r:
                    newboard[r][c] = chessboard[9-r][8-c].lower()
        return newboard
    else:
        return chessboard


def flip_dest(chessboard, player, move):
    # assume player is always the lower side of chessboard, in uppercase
    # fip the board if player is black
    if player == 'b':
        move[0] = 9 - move[0]
        move[1] = 8 - move[1]
        newboard = [['1' for c in range(9)] for r in range(10)]
        for r in range(10):
            for c in range(9):
                if chessboard[9-r][8-c] in piece_b:
                    newboard[r][c] = chessboard[9-r][8-c].upper()
                elif chessboard[9-r][8-c] in piece_r:
                    newboard[r][c] = chessboard[9-r][8-c].lower()
        return newboard, move
    else:
        return chessboard, move


def label_board_side(chessboard):
    # 1 for player, -1 for opponent, 0 for empty
    newboard = np.zeros((10, 9), dtype=np.int8)
    for r in range(10):
        for c in range(9):
            if chessboard[r][c] in piece_b:
                newboard[r][c] = -1
            elif chessboard[r][c] in piece_r:
                newboard[r][c] = 1
    return np.reshape(newboard, 90)


def label_board_type(chessboard, piece_type):
    # 1 for player, -1 for opponent, 0 for empty
    newboard = np.zeros((10, 9), dtype=np.int8)
    for r in range(10):
        for c in range(9):
            if chessboard[r][c] == piece_type.lower():
                newboard[r][c] = -1
            elif chessboard[r][c] == piece_type.upper():
                newboard[r][c] = 1
    # print np.reshape(newboard, 90)
    return np.reshape(newboard, 90)


def label_liberties(chessboard):
    # positive for player, negative for opponent, 0 for empty
    newboard = np.zeros((10, 9), dtype=np.int8)
    for r in range(10):
        for c in range(9):
            if chessboard[r][c] in piece_b:
                newboard[r][c] = -1 * count_movesnum(chessboard, 'b', [r, c])
            elif chessboard[r][c] in piece_r:
                newboard[r][c] = count_movesnum(chessboard, 'r', [r, c])
    return np.reshape(newboard, 90)


def label_attack_defend(chessboard):
    # positive for under defence, negative for under attack
    newboard = np.zeros((10, 9), dtype=np.int8)
    for r in range(10):
        for c in range(9):
            newboard[r][c] = count_defend(chessboard, 'r', [r, c]) - count_defend(chessboard, 'b', [r, c])
    return np.reshape(newboard, 90)


def label_valid_moves_tile(chessboard, tile):
    # -1 for invalid moves, 0 for this piece, 1 for valid moves
    newboard = -1 * np.ones((10, 9), dtype=np.int8)
    newboard[tile[0]][tile[1]] = 1
    moves = generatemoves_fortile(chessboard, 'r', tile)
    for move in moves:
        newboard[move[2]][move[3]] = 2
    return np.reshape(newboard, 90)


def label_chosen_piece(move):
    newboard = np.zeros((10, 9), dtype=np.int8)
    newboard[move[0]][move[1]] = 1
    return np.reshape(newboard, 90)


def label_chosen_dest(move):
    newboard = np.zeros((10, 9), dtype=np.int8)
    newboard[move[2]][move[3]] = 1
    return np.reshape(newboard, 90)


def count_defend(board, player, tile):
    count = 0
    flag = 0
    if board[tile[0]][tile[1]] == '1':
        board[tile[0]][tile[1]] = piece_list_op[player][-1]
        flag = 1
    for r in range(10):
        for c in range(9):
            if board[r][c] in piece_list[player]:
                move = [r, c, tile[0], tile[1]]
                count += validate(board, move, player)
    if flag == 1:
        board[tile[0]][tile[1]] = '1'
    return count


# init_board = "rnbakabnr/111111111/1111c11c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/b,2421,c"


def extract_features_piece(fen):
    _chessboard, _player = fen_reader(fen)
    _chessboard = flip(_chessboard, _player)

    side_label = label_board_side(_chessboard)
    # print side_label
    type_label = np.zeros((7, 90), dtype=np.int8)
    for x in range(7):
        ptype = piece_b[x]
        type_label[x] = label_board_type(_chessboard, ptype)

    # liberties_label = label_liberties(_chessboard)
    # atkdfd_label = label_attack_defend(_chessboard)

    chnl_option = {0: side_label, 1: type_label[0], 2: type_label[1], 3: type_label[2], 4: type_label[3],
                   5: type_label[4], 6: type_label[5], 7: type_label[6]}
    output = ""
    for r in range(10):
        for c in range(9):
            for x in range(8):
                output += str(chnl_option[x][r*9 + c])
                output += ','
    return output


def extract_features_dest(fen, move):
    _chessboard, _player = fen_reader(fen)
    _piece_type = _chessboard[move[0]][move[1]]
    # print "flip"
    _chessboard, _move = flip_dest(_chessboard, _player, move)

    side_label = label_board_side(_chessboard)
    type_label = np.zeros((7, 90), dtype=np.int8)
    for x in range(7):
        ptype = piece_b[x]
        type_label[x] = label_board_type(_chessboard, ptype)

    # liberties_label = label_liberties(_chessboard)
    # atkdfd_label = label_attack_defend(_chessboard)
    validmoves_label = label_valid_moves_tile(_chessboard, _move)

    chnl_option = {0: side_label, 1: type_label[0], 2: type_label[1], 3: type_label[2], 4: type_label[3],
                   5: type_label[4], 6: type_label[5], 7: type_label[6], 8: validmoves_label}
    output = ""
    for r in range(10):
        for c in range(9):
            for x in range(9):
                output += str(chnl_option[x][r*9 + c])
                output += ','
    # print output
    return output, _piece_type.lower()

