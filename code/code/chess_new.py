from common import *

import sys
sys.path.insert(0,'chess2p')
import chess2p as game2p

f=open("../qipu/" + sys.argv[1],"a+")

def on_a_response(*args):
    # get fen
    fen = args[0]
    f.write(args[0])
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
    checkflag,tempmove = check(newboard, opp)
    if(checkflag == 1):
        string = ''
        for x in xrange(0,4):
            print string
            string = string + str(tempmove[x])
        f.write(string + "," + fen[tempmove[0]*10 + tempmove[1]] + "\n")
        return None, fen[100]

    index = move_selection(fen, newboard)

    string = ''
    for x in xrange(0,4):
        string = string + str(move[index][x])

    f.write(string + "," + fen[move[0][0] * 10 + move[0][1]] + "\n")

    newboard[int(string[2])][int(string[3])] = newboard[int(string[0])][int(string[1])]
    newboard[int(string[0])][int(string[1])] = '1';


    fen1 = ""
    for i in xrange(0,10):
        for j in xrange(0,9):
            fen1 += newboard[i][j]
        fen1 += "/"
    fen1 += opp 

    return fen1, None


# def minimax_search(chessboard, move, num, side):


def chess_loop(times,filename):
    f=open("../source/" + filename,"a+")
    fen = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/r"

    for x in xrange(1,times+1):
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

# if __name__ == "__main__":
   
#     # the default path is in "qipu"
#     # f=open("../qipu/" + sys.argv[1],"a+")
#     chess_loop(1000,sys.argv[1])

if __name__ == '__main__':
    
    init_version = sys.argv[1]
    new_version = int(init_version) + 1
    fileindex = 0
    while fileindex<100:
        chess_loop(1000,str(fileindex)+".txt")
        # if(fileindex%10 == 9):
        data_process(str(init_version),str(new_version),fileindex)
        init_version = new_version
        load_model(str(init_version))
        new_version = new_version + 1
        fileindex = fileindex + 1
        pass