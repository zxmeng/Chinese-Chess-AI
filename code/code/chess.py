import commmon

import sys
sys.path.insert(0,'chess2p')
import chess2p as game2p


# the default path is in "qipu"
f=open("../qipu/"+sys.argv[1],"a+")


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
