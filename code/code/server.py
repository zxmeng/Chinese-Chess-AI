import common

fileadd = "../qipu/1.txt"
f = open(fileadd,"a")


def on_a_response(*args):
    

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
#        return None, fen[100]
    temp = np.zeros((3),dtype=np.float32)
    temp_m = 0.0
    # piece selector
    prediction = piece_selector_nn(fen)
    # printstat(prediction)
    # process prediction
    for i in range(3):
        move[i][0], move[i][1] = process1(prediction,fen)
        move[i][0], move[i][1] = flip(fen, move[i][0], move[i][1])
        # print move[i][0], move[i][1]

        # move selector
        prediction_m = move_selector_nn(fen, [move[i][0], move[i][1]])
        printstat(prediction_m)
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

# socket.gethostbyaddr('localhost:3000')
move = np.zeros((3, 4), dtype=np.int)
host = 'localhost'
port = 3001
socketIO = SocketIO('localhost', port)

#chat_namespace = socketIO.define(AA, '/chat')
while True:
    socketIO.on('chat',on_a_response)
    socketIO.wait(seconds=5)

    pass
