import random
import copy
import tensorflow as tf
import os
import numpy as np
from socketIO_client import SocketIO
import time
from piece_selector import *
from move_selector import *
from check import *
from evaluate import *

fileadd = "../qipu/1.txt"

# fen: not flipped
# prediction: flipped

def get_max(prediction):
    temp = np.amax(prediction)
    for i in range(10):
        for j in range(9):
            if (temp == prediction[i][j]):
                return i, j


def process1(prediction,fen):
    print prediction
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

    temp = np.amax(prediction)
    for i in range(10):
        for j in range(9):
            if (temp == prediction[i][j]):
                return i,j


def printstat(prediction):
    temp = np.zeros((10,9))
    np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    for i in range(10):
        for j in range(9):
            temp[i][j] = prediction[9-i][8-j]
        # print temp[i]


def flip(fen, x,y):
    if fen[100] =='b':
        x = 9 - x
        y = 8 - y
    return x, y


def on_a_response(*args):
    f = open(fileadd,"a")

    f.write(time.strftime("%Y-%m-%d %H:%M:%S,", time.localtime()))
    # print args
    temp = args[0]
    message = temp.split(",")
    fen = message[0]
    f.write(fen)
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
            print string
            string = string + str(tempmove[x])
        f.write(string+","+ fen[tempmove[0]*10+tempmove[1]] +"\n")
        socketIO.emit("chat1",string+","+message[1])
        return

    prediction = piece_selector_nn(fen)
    process1(prediction,fen)
    for i in range(precision):
        move[i][0], move[i][1] = get_max(prediction)
        if prediction[move[i][0]][move[i][1]] == 0:
            break
        temp1 = move[i][0]
        temp2 = move[i][1]
        move[i][0], move[i][1] = flip(fen, move[i][0], move[i][1])

        # move selector
        prediction_m = move_selector_nn(fen, [move[i][0], move[i][1]])
        printstat(prediction_m)
        # process prediction
        move[i][2], move[i][3] = process(prediction_m)
        move[i][2], move[i][3] = flip(fen, move[i][2], move[i][3])

        prediction[temp1][temp2] = 0.0


    j = eval_move(newboard,move[:i+1],i+1,fen[100])

    string = ''
    for x in xrange(0,4):
        string = string + str(move[j][x])
    # print string

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
    print message[1]
    # return fen1,None
    socketIO.emit('chat1',string+","+message[1])
    f.write(string)
    f.write("\n")

# move = np.zeros((3, 4), dtype=np.int)
# fen = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/r"
# # fen = "111a1ab11/11R111111/111k11111/p11Nn111p/111111111/111111111/111C1111c/111111R11/111111111/11BAKAB11,b"
# # fen = "11bakab11/111111111/11R111111/C111c1111/111111111/111111111/P111Nn11P/11111K111/111111r11/11BA1A111,r"
# print fen
# # on_a_response(fen)
# for i in xrange(1,100):
#     fen, win = on_a_response(fen)
#     print win
#     if(win == "r"):
#         print "r"
#         print i
#         break
#     elif(win == "b"):
#         print "b"
#         print i
#         break
#     print fen
#     pass

# socket.gethostbyaddr('localhost:3000')
# import socket
precision = 10
move = np.zeros((precision, 4), dtype=np.int)
host = 'localhost'
port = 3001
socketIO = SocketIO('localhost', port)
# socketIO.on('chat',on_a_response)
# socketIO.wait(seconds=10)

#chat_namespace = socketIO.define(AA, '/chat')
while True:
    socketIO.on('chat',on_a_response)
    socketIO.wait(seconds=10)

    pass
