# -------------------------------------------------------+
# get information of chessboard                          |
# used to extract information in reinforcement learning  |
# -------------------------------------------------------+

# -------------------------------------------------------------+
# Ver 1.0    Feb 16 2017                                       |
# Based on information.py                                      |
# Author: zxm                                                  |
# Summary: add function info_ext_move() and info_ext_piece()   |
# -------------------------------------------------------------+

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
    move = [0 for x in range(4)]
    for x in range(4):
        move[x] = int(fen[102 + x])
    piece_type = fen[107]
    winner = fen[109]
    return chessboard, player, move, piece_type, winner


def flip(chessboard, player, move, piece_type):
    # assume player is always the lower side of chessboard, in uppercase
    # fip the board if player is black
    if player == 'b':
        move[0] = 9 - move[0]
        move[1] = 8 - move[1]
        move[2] = 9 - move[2]
        move[3] = 8 - move[3]
        piece_type = piece_type.upper()
        newboard = [['1' for c in range(9)] for r in range(10)]
        for r in range(10):
            for c in range(9):
                if chessboard[9-r][8-c] in piece_b:
                    newboard[r][c] = chessboard[9-r][8-c].upper()
                elif chessboard[9-r][8-c] in piece_r:
                    newboard[r][c] = chessboard[9-r][8-c].lower()
        return newboard, move, piece_type
    else:
        return chessboard, move, piece_type


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

# label reward for 
def label_chosen_piece(move, player, winner):
    newboard = np.zeros((10, 9), dtype=np.int8)
    if player == winner:
        newboard[move[0]][move[1]] = 1
    else:
        newboard[move[0]][move[1]] = -1
    return np.reshape(newboard, 90)


def label_chosen_dest(move, player, winner):
    newboard = np.zeros((10, 9), dtype=np.int8)
    if player == winner:
        newboard[move[2]][move[3]] = 1
    else:
        newboard[move[2]][move[3]] = -1
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
    _chessboard, _player, _move, _piece_type, _winner = fen_reader(fen)
    _chessboard, _move, _piece_type = flip(_chessboard, _player, _move, _piece_type)

    side_label = label_board_side(_chessboard)
    # print side_label
    type_label = np.zeros((7, 90), dtype=np.int8)
    for x in range(7):
        ptype = piece_b[x]
        type_label[x] = label_board_type(_chessboard, ptype)

    # liberties_label = label_liberties(_chessboard)
    # atkdfd_label = label_attack_defend(_chessboard)
    chosen_piece_label = label_chosen_piece(_move, _player, _winner)

    chnl_option = {0: side_label, 1: type_label[0], 2: type_label[1], 3: type_label[2], 4: type_label[3],
                   5: type_label[4], 6: type_label[5], 7: type_label[6]}
    output = ""
    for r in range(10):
        for c in range(9):
            for x in range(8):
                output += str(chnl_option[x][r*9 + c])
                output += ','
    output += '\n'
    for r in range(10):
        for c in range(9):
            output += str(chosen_piece_label[r*9 + c])
            output += ','
    output += '\n'
    return output


def extract_features_dest(fen):
    _chessboard, _player, _move, _piece_type, _winner = fen_reader(fen)
    _chessboard, _move, _piece_type = flip(_chessboard, _player, _move, _piece_type)

    side_label = label_board_side(_chessboard)
    type_label = np.zeros((7, 90), dtype=np.int8)
    for x in range(7):
        ptype = piece_b[x]
        type_label[x] = label_board_type(_chessboard, ptype)

    # liberties_label = label_liberties(_chessboard)
    # atkdfd_label = label_attack_defend(_chessboard)
    chosen_dest_label = label_chosen_dest(_move, _player, _winner)
    validmoves_label = label_valid_moves_tile(_chessboard, _move[:2])

    chnl_option = {0: side_label, 1: type_label[0], 2: type_label[1], 3: type_label[2], 4: type_label[3],
                   5: type_label[4], 6: type_label[5], 7: type_label[6], 8: validmoves_label}
    output = ""
    for r in range(10):
        for c in range(9):
            for x in range(9):
                output += str(chnl_option[x][r*9 + c])
                output += ','
    output += '\n'
    for r in range(10):
        for c in range(9):
            output += str(chosen_dest_label[r*9 + c])
            output += ','
    output += '\n'
    # print output
    return output, _piece_type.lower()

# def extract_features_predict(fen):
#     _chessboard, _player, _move, _piece_type = fen_reader(fen)
#     _chessboard, _move, _piece_type = flip(_chessboard, _player, _move, _piece_type)

#     side_label = label_board_side(_chessboard)
#     # print side_label
#     type_label = np.zeros((7, 90), dtype=np.int8)
#     for x in range(7):
#         ptype = piece_b[x]
#         type_label[x] = label_board_type(_chessboard, ptype)

#     # liberties_label = label_liberties(_chessboard)
#     # atkdfd_label = label_attack_defend(_chessboard)
#     # chosen_piece_label = label_chosen_piece(_move)

#     chnl_option = {0: side_label, 1: type_label[0], 2: type_label[1], 3: type_label[2], 4: type_label[3],
#                    5: type_label[4], 6: type_label[5], 7: type_label[6]}
#     output = ""
#     for r in range(10):
#         for c in range(9):
#             for x in range(8):
#                 output += str(chnl_option[x][r*9 + c])
#                 output += ','
#     output += '\n'
#     return output

# ---------------------------------------+
# extract information for move selector  |
# ---------------------------------------+
def info_ext_move():
    path = '../processed/'
    dt = ["" for x in range(7)]
    for x in range(7):
        dt[x] = open("../update_move_" + piece_b[x] + "/pgninfo_ext_" + piece_b[x] + ".txt", 'w')

    count = 0
    for filename in os.listdir(path):
        if filename[0] == '.':
            continue
        pgn = open(path + filename, 'r')
        output = ""
        for line in pgn:
            count+=1
            if count%1000 == 0:
                print count
            # line = line.decode("utf-8")
            # print line
            try:
                output, piece = extract_features_dest(line)
                dt[piece_b.index(piece)].write(output)
            except:
                print 'error! ' + line
        pgn.close()
    for x in range(7):
        dt[x].close()
    print count


# ---------------------------------------+
# extract information for piece selector |
# ---------------------------------------+
def info_ext_piece():
    path = '../processed/'
    dt = open("../update_piece/pgninfo_ext_piece.txt", 'w')
    count = 0
    for filename in os.listdir(path):
        if filename[0] == '.':
            continue
        pgn = open(path + filename, 'r')
        output = ""
        for line in pgn:
            count+=1
            if count%1000 == 0:
                print count
            # line = line.decode("utf-8")
            # print line
            try:
                output = extract_features_piece(line)
                dt.write(output)
            except:
                print 'error! ' + line
        pgn.close()
    dt.close()
    print count

# ------------------------------------------+
# used to extract information in prediction |
# ------------------------------------------+
# path = '../train/'
# dt = open("dataset_piece_predict", 'a+')
# count = 0
# for filename in os.listdir(path):
#     if filename[0] == '.':
#         continue
#     pgn = open(path + filename, 'r')
#     for line in pgn:
#         count+=1
#         if count%1000 == 0:
#             print count
#         # line = line.decode("utf-8")
#         # print line
#         try:
#             output = extract_features_predict(line)
#             dt.write(output)
#         except:
#             print 'error! ' + line
#     pgn.close()
# dt.close()
