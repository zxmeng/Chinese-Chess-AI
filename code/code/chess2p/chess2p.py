from common1 import *

def on_a_response(*args):
    # get fen
    fen = args[0]

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
        # f.write(string + "," + fen[tempmove[0]*10 + tempmove[1]] + "\n")
        return None, fen[100]

    index = move_selection(fen,newboard)

    string = ''
    for x in xrange(0,4):
        string = string + str(move[index][x])


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

