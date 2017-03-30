import random
import copy
import tensorflow as tf
import os
import numpy as np
# from socketIO_client import SocketIO
import time
from piece_selector import *
from move_selector import *
from check import *
import copy as cp
import ctypes
import check as ck
evaluator = ctypes.CDLL('/root/code/example.so')
# evaluator = ctypes.CDLL('/data/ssd/public/hzzhang5/code/example.so')

# from evaluate import *

piece_b = ['k', 'a', 'b', 'n', 'r', 'c', 'p']
piece_r = ['K', 'A', 'B', 'N', 'R', 'C', 'P']
piece_list = {'b': piece_b, 'r': piece_r}
piece_list_op = {'b': piece_r, 'r': piece_b}


precision = 18
move = np.zeros((precision, 4), dtype=np.int)

# load NN models
fuck = Fuck()
fuck.init_piece_selector()
fuck_a = Fuck_m("a")
fuck_a.init_move_selector()
fuck_b = Fuck_m("b")
fuck_b.init_move_selector()
fuck_c = Fuck_m("c")
fuck_c.init_move_selector()
fuck_k = Fuck_m("k")
fuck_k.init_move_selector()
fuck_p = Fuck_m("p")
fuck_p.init_move_selector()
fuck_r = Fuck_m("r")
fuck_r.init_move_selector()
fuck_n = Fuck_m("n")
fuck_n.init_move_selector()


# get max value index from prediction
def get_max(prediction):
    temp = np.amax(prediction)
    for i in range(10):
        for j in range(9):
            if (temp == prediction[i][j]):
                return i, j

# process piece selector prediction
def process_piece(prediction, fen, player):
    for i in range(10):
        for j in range(9):
            temp_r, temp_c = flip(fen, i, j)    
            if (fen[i*10+j] == '1'):
                prediction[temp_r][temp_c]=0.0
            elif (fen[i*10+j] in piece_list_op[player]):
                prediction[temp_r][temp_c]=0.0

    prediction[prediction<0.01] = 0.0
    total = np.sum(prediction)
    prediction = prediction / total

    
# process move selector prediction
def process_move(prediction):
    prediction[prediction<0.01] = 0.0
    total = np.sum(prediction)
    prediction = prediction / total


def random_select(prediction):
    prediction[prediction<0.01] = 0.0
    total = np.sum(prediction)
    prediction = prediction / total

    rand = np.random.uniform(0,1)
    temp = 0
    for i in range(10):
        for j in range(9):
            temp += prediction[i][j]
            if (temp > rand):
                return i,j


def printstat(prediction):
    temp = np.zeros((10,9))
    np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    for i in range(10):
        for j in range(9):
            temp[i][j] = prediction[9-i][8-j]
            print temp[i]


def flip(fen, x, y):
    if fen[100] =='b':
        x = 9 - x
        y = 8 - y
    return x, y


def move_selection(fen,newboard):
    prediction = fuck.piece_selector_nn(fen)
    process_piece(prediction,fen,fen[100])
    for i in range(precision):
        move[i][0], move[i][1] = get_max(prediction)
        if prediction[move[i][0]][move[i][1]] == 0:
            break
        temp1 = move[i][0]
        temp2 = move[i][1]
        move[i][0], move[i][1] = flip(fen, move[i][0], move[i][1])

        # move selector
        output, piece_type = extract_features_dest(fen, [move[i][0], move[i][1]])
        if piece_type == "a":
            prediction_m = fuck_a.move_selector_nn(output)
        elif piece_type == "b":
            prediction_m = fuck_b.move_selector_nn(output)
        elif piece_type == "c":
            prediction_m = fuck_c.move_selector_nn(output)
        elif piece_type == "n":
            prediction_m = fuck_n.move_selector_nn(output)
        elif piece_type == "k":
            prediction_m = fuck_k.move_selector_nn(output)
        elif piece_type == "p":
            prediction_m = fuck_p.move_selector_nn(output)
        elif piece_type == "r":
            prediction_m = fuck_r.move_selector_nn(output)
        pass
        # process prediction
        move[i][2], move[i][3] = get_max(prediction_m)
        move[i][2], move[i][3] = flip(fen, move[i][2], move[i][3])

        prediction[temp1][temp2] = 0.0


    index = eval_move(newboard,move[:i],i,fen[100])

    return index

def eval_move(board, move,size,side):
    score = np.zeros(size)
    # print "oppo move"
    # print move
    for x in xrange(0,size):
        newboard = cp.deepcopy(board)
        string = move[x]
        newboard[int(string[2])][int(string[3])]=newboard[int(string[0])][int(string[1])]
        newboard[int(string[0])][int(string[1])]='1';


        fen=""
        for i in xrange(0,10):
            for j in xrange(0,9):
                fen += newboard[i][j]
            fen += "/"
        # fen += side
        if side=='r':
            fen += "b"
        else:
            fen += 'r'
            pass

        # print fen
        isChecked, _ = ck.check(newboard,side)
        if isChecked == 1:
            score[x] = -9999
            continue
        # evaluator.evaluate.argtypes = [ctypes.c_char_p]
        # score[x]=evaluator.evaluate(fen)
        score[x] = eval_minimax(fen,fen[100])
        # score[x] = evaluate(fen)


    index = np.argmax(score)
    print score
    print index
    return index

    pass

def eval_minimax(fen,side):
    newboard = [[0 for x in range(9)] for y in range(10)]
    for i in xrange(0,10):
        for j in xrange(0,9):
            newboard[i][j] = fen[i*10 + j]
    if(side == "r"):
        opp = "b"
    else:
        opp = "r"
    pass
    temp_move = np.zeros((precision, 4), dtype=np.int)
    score = move_selection_temp(fen,newboard,temp_move)
    return score

def move_selection_temp(fen,newboard,move):
    prediction = fuck.piece_selector_nn(fen)
    process_piece(prediction,fen,fen[100])
    for i in range(precision):
        move[i][0], move[i][1] = get_max(prediction)
        if prediction[move[i][0]][move[i][1]] == 0:
            break
        temp1 = move[i][0]
        temp2 = move[i][1]
        move[i][0], move[i][1] = flip(fen, move[i][0], move[i][1])

        # move selector
        output, piece_type = extract_features_dest(fen, [move[i][0], move[i][1]])
        if piece_type == "a":
            prediction_m = fuck_a.move_selector_nn(output)
        elif piece_type == "b":
            prediction_m = fuck_b.move_selector_nn(output)
        elif piece_type == "c":
            prediction_m = fuck_c.move_selector_nn(output)
        elif piece_type == "n":
            prediction_m = fuck_n.move_selector_nn(output)
        elif piece_type == "k":
            prediction_m = fuck_k.move_selector_nn(output)
        elif piece_type == "p":
            prediction_m = fuck_p.move_selector_nn(output)
        elif piece_type == "r":
            prediction_m = fuck_r.move_selector_nn(output)
        pass
        # process prediction
        move[i][2], move[i][3] = get_max(prediction_m)
        move[i][2], move[i][3] = flip(fen, move[i][2], move[i][3])

        prediction[temp1][temp2] = 0.0


    # index = eval_move(newboard,move[:i],i,fen[100])

    move = move[:i]
    size = i
    side = fen[100]
    score = np.zeros(size)
    # print "prediction move"
    # print move
    for x in xrange(0,size):
        tempboard = cp.deepcopy(newboard)
        string = move[x]
        tempboard[int(string[2])][int(string[3])]=tempboard[int(string[0])][int(string[1])]
        tempboard[int(string[0])][int(string[1])]='1';


        fen=""
        for i in xrange(0,10):
            for j in xrange(0,9):
                fen += tempboard[i][j]
            fen += "/"
        # fen += side
        if side=='r':
            fen += "b"
        else:
            fen += 'r'
            pass

        # print fen
        isChecked, _ = ck.check(tempboard,side)
        if isChecked == 1:
            score[x] = 9999
            continue
        evaluator.evaluate.argtypes = [ctypes.c_char_p]
        score[x]=evaluator.evaluate(fen)
    # print score
    # print "score is %d" % np.amin(score)
    return np.amin(score)