# -------------------------------------------------------+
# get information of chessboard                          |
# used to extract information for evaluation model       |
# -------------------------------------------------------+

# --------------------------------------------------------------------+
# Ver 2.0    Apr 4 2017                                               |
# Based on information_ext.py                                         |
# Author: zxm                                                         |
# Summary: extract information for fully connected eva model          |
# --------------------------------------------------------------------+


# format
# [90 board places] , [player] , [score]
# evaluate this board state for the player to make a move
# init_board = "rnbakabnr/111111111/1111c11c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/b,2421,c"

from moveGeneration import *
from validation import *
import numpy as np
import os

piece_b = ['k', 'r', 'c', 'n', 'b', 'a', 'p']
piece_r = ['K', 'R', 'C', 'N', 'B', 'A', 'P']
pieces = ['K', 'R', 'C', 'N', 'B', 'A', 'P', 'k', 'r', 'c', 'n', 'b', 'a', 'p']
piece_mob = ['R', 'C', 'N', 'r', 'c', 'n']
piece_list = {'b': piece_b, 'r': piece_r}
piece_list_op = {'b': piece_r, 'r': piece_b}
piece_total = {'K': 1, 'R': 2, 'C': 2, 'N': 2, 'B': 2, 'A': 2, 'P': 5, 'k', 'r': 2, 'c': 2, 'n': 2, 'b': 2, 'a': 2, 'p': 5}


def fen_reader(fen):
    # input fen: [chessboard string], [player], [score]
    chessboard = [['\0' for c in range(9)] for r in range(10)]
    for r in range(10):
        for c in range(9):
            chessboard[r][c] = fen[r * 10 + c]

    player = fen[100]
    temp = fen.split(",")
    score = temp[-1]
    return chessboard, player, score


def ext_info_eva_full(fen):
    dic_count = {p: 0 for p in pieces }

    pl_k = np.zeros((2, 3), dtype=np.int8)
    pl_r = np.zeros((2, 3), dtype=np.int8)
    pl_c = np.zeros((2, 3), dtype=np.int8)
    pl_n = np.zeros((2, 3), dtype=np.int8)
    pl_b = np.zeros((2, 3), dtype=np.int8)
    pl_a = np.zeros((2, 3), dtype=np.int8)
    pl_p = np.zeros((5, 3), dtype=np.int8)

    pl_K = np.zeros((2, 3), dtype=np.int8)
    pl_R = np.zeros((2, 3), dtype=np.int8)
    pl_C = np.zeros((2, 3), dtype=np.int8)
    pl_N = np.zeros((2, 3), dtype=np.int8)
    pl_B = np.zeros((2, 3), dtype=np.int8)
    pl_A = np.zeros((2, 3), dtype=np.int8)
    pl_P = np.zeros((5, 3), dtype=np.int8)

    dic_pl = {'K': pl_K, 'R': pl_R, 'C': pl_C, 'N': pl_N, 'B': pl_B, 'A': pl_A, 'P': pl_P, 'k': pl_k, 'r': pl_r, 'c': pl_c, 'n': pl_n, 'b': pl_b, 'a': pl_a, 'p': pl_p}

    mob_r = np.zeros((2), dtype=np.float32)
    mob_c = np.zeros((2), dtype=np.float32)
    mob_n = np.zeros((2), dtype=np.float32)
    mob_R = np.zeros((2), dtype=np.float32)
    mob_C = np.zeros((2), dtype=np.float32)
    mob_N = np.zeros((2), dtype=np.float32)

    dic_mob = {'R': mob_R, 'C': mob_C, 'N': mob_N, 'r': mob_r, 'c': mob_c, 'n': mob_n}

    _chessboard, _player, _score = fen_reader(fen)

    output = ""
    if (_player == 'r'):
        output += '1,'
    else:
        output += '-1,'

    for r in range(10):
        for c in range(9):
            ptype = _chessboard[r][c]
            if ptype != '1':
                count = dic_count[ptype]
                dic_pl[ptype][count][0] = 1
                dic_pl[ptype][count][1] = r + 1
                dic_pl[ptype][count][2] = c + 1
                if ptype in piece_mob:
                    dic_mob[ptype][count] = count_mobility(_chessboard, [r, c]) / 4 
                dic_count[ptype] += 1

    for x in range(14):
        output += str(dic_count[pieces[x]])
        output += ','

    for x in range(14):
        ptype = pieces[x]
        for i in range(piece_total[ptype]):
            for j in range(3):
                output += str(dic_pl[ptype][i][j])
                output += ','

    for x in range(6):
        ptype = piece_mob[x]
        for i in range(piece_total[ptype]):
            output += str(dic_mob[ptype][i])
            output += ','

    output += '\n'
    output += _score
    output += '\n'
    return output

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


# -----------------------------------------+
# extract information for evaluation model |
# -----------------------------------------+
def info_ext_eva():
    path = '../eva_processed/'
    dt = open("../eva_train/pgninfo_ext_eva.txt", 'w')
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
                output = ext_info_eva_full(line)
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
