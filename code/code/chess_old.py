import random
import copy
import tensorflow as tf
import os
import numpy as np
from socketIO_client import SocketIO
import time
from piece_selector import *
from move_selector import *


def process(prediction):
    prediction[prediction<0.001] = 0.0
    # prediction = np.power(prediction, 2)
    # total = np.sum(prediction)
    # prediction = prediction / total

    # rand = np.random.uniform(0,1)

    temp = np.amax(prediction)
    for i in range(10):
        for j in range(9):
            if temp == prediction[i][j]:
                return i, j


def printstat(prediction):
    temp = np.zeros((10,9))
    np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    for i in range(10):
        for j in range(9):
            temp[i][j] = prediction[9-i][8-j]
        print temp[i]


def flip(fen, x,y):
    if fen[100] =='b':
        x = 9 - x
        y = 8 - y
    return x, y


def on_a_response(*args):
    print args
    fen = args[0]

    # piece selector
    prediction = piece_selector_nn(fen)
    # process prediction
    printstat(prediction)
    move[0], move[1] = process(prediction)
    move[0], move[1] = flip(fen, move[0], move[1])
    print move[0], move[1]

    # move selector
    prediction_m = move_selector_nn(fen, [move[0], move[1]])
    printstat(prediction_m)
    # process prediction
    move[2], move[3] = process(prediction_m)
    move[2], move[3] = flip(fen, move[2], move[3])
    print move[2], move[3]

    string = ''
    for x in xrange(0,4):
        string = string + str(move[x])
        # print string
    socketIO.emit('chat1',string)

# fen = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR,r"
# print fen
# prediction = piece_selector_nn(fen)
# print prediction

#socket.gethostbyaddr('localhost:3000')
# import socket
move = np.zeros((4), dtype=np.int)
host = 'localhost'
port = 3000
socketIO = SocketIO('localhost', port)
# socketIO.on('chat',on_a_response)
# socketIO.wait(seconds=10)

#chat_namespace = socketIO.define(AA, '/chat')
while True:
    socketIO.on('chat',on_a_response)
    socketIO.wait(seconds=5)
    pass
