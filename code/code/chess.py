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

import sys
sys.path.insert(0,'chess2p')
import chess2p as game2p

# os.environ['TF_CPP_MIN_VLOG_LEVEL']='3'

# the default path is in "qipu"

f=open("../qipu/"+sys.argv[1],"a+")

#for piece selector inorder not to select an empty block
def process1(prediction,fen):
#    print prediction
    for i in range(10):
	for j in range(9):
	    temp_r, temp_c = flip(fen, i, j)	
	    if (fen[temp_r*10+temp_c]=='1'):
	    	prediction[i][j]=0.0
#    prediction[prediction<0.001] = 0.0
    # prediction = np.power(prediction, 2)
    total = np.sum(prediction)
    prediction = prediction / total

    rand = np.random.uniform(0,1)

    # temp = np.amax(prediction)
    temp = 0
    for i in range(10):
        for j in range(9):
            temp += prediction[i][j]
            temp_r, temp_c = flip(fen, i, j)
            if (temp >= rand) and (fen[temp_r*10+temp_c]!='1'):
                return i, j

    temp = np.amax(prediction)
    for i in range(10):
        for j in range(9):
            if (temp == prediction[i][j]):
                return i, j

def process(prediction):
#    prediction[prediction<0.001] = 0.0
    # prediction = np.power(prediction, 2)
    total = np.sum(prediction)
    prediction = prediction / total

    rand = np.random.uniform(0,1)

    # temp = np.amax(prediction)
    temp = 0
    for i in range(10):
        for j in range(9):
            temp += prediction[i][j]
            if (temp > rand):
                return i, j


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
    temp = np.zeros((3),dtype=np.float32)
    temp_m = 0.0
    # piece selector
    prediction = fuck.piece_selector_nn(fen)
    # printstat(prediction)
    # process prediction
    for i in range(3):
        move[i][0], move[i][1] = process1(prediction,fen)
# keep the value before flip
        temp1 = move[i][0]
        temp2 = move[i][1]
        move[i][0], move[i][1] = flip(fen, move[i][0], move[i][1])
        # print move[i][0], move[i][1]

        # move selector
        # prediction_m = move_selector_nn(fen, [move[i][0], move[i][1]])
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
#        printstat(prediction_m)
        prediction_m[temp1][temp2] = 0
# not select own piece

        # process prediction
        move[i][2], move[i][3] = process(prediction_m)
        
        move[i][2], move[i][3] = flip(fen, move[i][2], move[i][3])
        # print move[i][2], move[i][3]

        temp[i] = prediction[9 - move[i][0]][8 - move[i][1]] * prediction_m[9 - move[i][2]][8 - move[i][3]]
        prediction[9 - move[i][0]][8 - move[i][1]] = 0.0

        if temp[i] > temp_m:
            temp_m = temp[i]

    j = 0
    for i in range(3):
        if temp[i] == temp_m:
            j = i
            break

    string = ''
    for x in xrange(0,4):
        string = string + str(move[j][x])
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
    # socketIO.emit('chat1',string)
    

move = np.zeros((3, 4), dtype=np.int)


fen = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/r"
# fen = "111a1ab11/11R111111/111k11111/p11Nn111p/111111111/111111111/111C1111c/111111R11/111111111/11BAKAB11,b"
# fen = "11bakab11/111111111/11R111111/C111c1111/111111111/111111111/P111Nn11P/11111K111/111111r11/11BA1A111,r"
#print fen
# on_a_response(fen)

# the part is for self training

# for x in xrange(1,500):
#     print x
#     f.write("Game "+str(x)+"\n")
#     for i in xrange(1,1000):
#         fen, win = on_a_response(fen)
#         # print win
#         if(win == "r"):
#             f.write("r wins\n")
#             # print "r"
#             print i
#             break
#         elif(win == "b"):
#             f.write("b wins\n")
#             # print "b"
#             print i
#             break
#         # print fen
#         pass
#     fen = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/r"
#     pass


# end of part

# training with 2p

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
