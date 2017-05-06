from common import *
from socketIO_client import SocketIO
fileadd = "../qipu/1.txt"
f = open(fileadd,"a")

# fen: not flipped
# prediction: flipped


def on_a_response(*args):
    f.write(time.strftime("%Y-%m-%d %H:%M:%S,", time.localtime()))

    # get fen
    temp = args[0]
    message = temp.split(",")
    fen = message[0]
    f.write(fen)
    f.write(",")

    # reshape fen
    newboard = [[0 for x in range(9)] for y in range(10)]
    for i in xrange(0,10):
        for j in xrange(0,9):
            newboard[i][j] = fen[i*10 + j]

    # get player sides
    side = fen[100]
    if(side == "r"):
        opp = "b"
    else:
        opp = "r"

    # detect whether being checked
    checkflag,tempmove = check(newboard,opp)
    if(checkflag == 1):
        string = ''
        for x in xrange(0,4):
            print string
            string = string + str(tempmove[x])
        f.write(string + "," + fen[tempmove[0]*10 + tempmove[1]] + "\n")
        socketIO.emit("chat1", string + "," + message[1])
        return

    index = move_selection(fen,newboard)

    string = ''
    for x in xrange(0,4):
        string = string + str(move[index][x])

    # update chess board
    newboard[int(string[2])][int(string[3])] = newboard[int(string[0])][int(string[1])]
    newboard[int(string[0])][int(string[1])] = '1';

    # convert board to fen
    fen1 = ""
    for i in xrange(0,10):
        for j in xrange(0,9):
            fen1 += newboard[i][j]
        fen1 += "/"
    fen1 += opp	

    # output
    print message[1]
    socketIO.emit('chat1', string + "," + message[1])
    f.write(string)
    f.write("\n")


# socket.gethostbyaddr('localhost:3000')
host = 'localhost'
port = 3001
socketIO = SocketIO('localhost', port)

#chat_namespace = socketIO.define(AA, '/chat')
while True:
    socketIO.on('chat',on_a_response)
    socketIO.wait(seconds=10)
    pass
