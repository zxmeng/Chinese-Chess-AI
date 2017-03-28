# origin version of chess, the move will be record by 
# the text file in the argument 

import random
import copy
import os
import numpy as np
import time
from piece_selector import *
from move_selector import *
from check import *
from evaluate import *

import sys
sys.path.insert(0,'chess2p')
import chess2p as game2p

# os.environ['TF_CPP_MIN_VLOG_LEVEL']='3'

# the default path is in "qipu"

f=open("../qipu/"+sys.argv[1],"a+")

#for piece selector inorder not to select an empty block
def get_max(prediction):
    temp = np.amax(prediction)
    for i in range(10):
        for j in range(9):
            if (temp == prediction[i][j]):
                return i, j


def process1(prediction,fen):
    # print prediction
    for i in range(10):
        for j in range(9):
            temp_r, temp_c = flip(fen, i, j)    
            if (fen[i*10+j]=='1'):
                prediction[temp_r][temp_c]=0.0

    prediction[prediction<0.01] = 0.0
    total = np.sum(prediction)
    prediction = prediction / total

    

def process(prediction):
    prediction[prediction<0.01] = 0.0
    # prediction = np.power(prediction, 2)
    total = np.sum(prediction)
    prediction = prediction / total

    # temp = np.amax(prediction)
    # for i in range(10):
    #     for j in range(9):
    #         if (temp == prediction[i][j]):
    #             return i,j


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


def on_a_response(*args):
    # print args
    fen = args[0]
    f.write(args[0])
    f.write(",")
    newboard = [[0 for x in range(9)] for y in range(10)]
    for i in xrange(0,10):
            for j in xrange(0,9):
                newboard[i][j]=fen[i*10 + j]
    if(fen[100]=="r"):
        opp="b"
    else:
        opp="r"

    checkflag,tempmove=check(newboard,opp)
    if(checkflag==1):
        string = ''
        for x in xrange(0,4):
            string = string + str(tempmove[x])
        f.write(string+","+ fen[tempmove[0]*10+tempmove[1]] +"\n")
        # print tempmove
        return None, fen[100]

    prediction = fuck.piece_selector_nn(fen)
    process1(prediction, fen)

    for i in range(int(precision/3)):
        move[i][0], move[i][1] = get_max(prediction)
        if prediction[move[i][0]][move[i][1]] == 0:
            break

        temp0 = move[i][0]
        temp1 = move[i][1]
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
        # printstat(prediction_m)
        # process prediction
        # move[i][2], move[i][3] = random_select(prediction_m)
        process(prediction_m)
        for j in range(3):
            move[i+j][0] = move[i][0]
            move[i+j][1] = move[i][1]

            move[i+j][2], move[i+j][3] = get_max(prediction_m)
            if prediction_m[move[i+j][2]][move[i+j][3]] == 0:
                break

            temp2 = move[i+j][2]
            temp3 = move[i+j][3]
            move[i+j][2], move[i+j][3] = flip(fen, move[i+j][2], move[i+j][3])

            prediction_m[temp2][temp3] = 0.0

        i = i + j
        prediction[temp0][temp1] = 0.0


    index = eval_move(newboard,move[:i],i,fen[100])
    # index = minimax_search(newboard, move[:i], i, fen[100])

    string = ''
    for x in xrange(0,4):
        string = string + str(move[index][x])
    # print string

    f.write(string+","+fen[move[0][0]*10+move[0][1]]+"\n")

    newboard[int(string[2])][int(string[3])]=newboard[int(string[0])][int(string[1])]
    newboard[int(string[0])][int(string[1])]='1';

    # print newboard

    fen1=""
    for i in xrange(0,10):
        for j in xrange(0,9):
            fen1 += newboard[i][j]
        fen1 += "/"
    if(fen[100]=="r"):
        fen1+="b"
    else:
        fen1+="r"
    # print fen1

    return fen1,None


def move_selection(fen):
    # transfer fen to array board
    newboard = [[0 for x in range(9)] for y in range(10)]
    for i in xrange(0, 10):
            for j in xrange(0,9):
                newboard[i][j] = fen[i*10 + j]

    # get opponent
    if (fen[100] == "r"):
        opp = "b"
    else:
        opp = "r"

    # detect whether it's checkmated
    checkflag, tempmove = check(newboard, opp)
    if(checkflag == 1):
        return [-1, -1, -1, -1]

    # piece selector make prediction
    prediction = fuck.piece_selector_nn(fen)
    process1(prediction, fen)

    for i in range(int(precision/3)):
        move[i][0], move[i][1] = get_max(prediction)
        if prediction[move[i][0]][move[i][1]] == 0:
            break

        temp0 = move[i][0]
        temp1 = move[i][1]
        move[i][0], move[i][1] = flip(fen, move[i][0], move[i][1])

        # move selector make prediction
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
        process(prediction_m)
        
        for j in range(3):
            move[i+j][0] = move[i][0]
            move[i+j][1] = move[i][1]

            move[i+j][2], move[i+j][3] = get_max(prediction_m)
            if prediction_m[move[i+j][2]][move[i+j][3]] == 0:
                break

            temp2 = move[i+j][2]
            temp3 = move[i+j][3]
            move[i+j][2], move[i+j][3] = flip(fen, move[i+j][2], move[i+j][3])

            prediction_m[temp2][temp3] = 0.0

        i = i + j
        prediction[temp0][temp1] = 0.0


    index = eval_move(newboard,move[:i],i,fen[100])

    return move[index]



def minimax_search(chessboard, move, num, side):


    
precision = 15
move = np.zeros((precision, 4), dtype=np.int)


fen = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/r"


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

for x in xrange(1,1000):
    print x
    f.write("Game "+str(x)+"\n")
    for i in xrange(1,1000):
        if(i%2==1):
            fen, win = on_a_response(fen)
        else:
            fen, win = game2p.on_a_response(fen)
        # print win
        if(win == "r"):
            f.write("r wins\n")
            # print "r"
            print i
            break
        elif(win == "b"):
            f.write("b wins\n")
            # print "b"
            print i
            break
        # print fen
        pass
    fen = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/r"
    pass
