import moveGeneration
import validation
import check
import random
import copy

# execute the move and update the chess board
def executemove(chessboard, choice):
    move = [0, 0, 0, 0]
    move[0] = int(choice[0])
    move[1] = int(choice[1])
    move[2] = int(choice[2])
    move[3] = int(choice[3])
    chessboard[move[2]][move[3]] = chessboard[move[0]][move[1]]
    chessboard[move[0]][move[1]] = '1'
    return

def deexecutemove(chessboard, choice, tile):
    move = [0, 0, 0, 0]
    move[0] = int(choice[0])
    move[1] = int(choice[1])
    move[2] = int(choice[2])
    move[3] = int(choice[3])
    chessboard[move[0]][move[1]] = chessboard[move[2]][move[3]]
    chessboard[move[2]][move[3]] = tile
    return


# search the special piece, x and y is the position of the chess
# the policy for evaluateuating the score if chessboard, need to be modified
def evaluate(chessboard):
    score = 0
    for i in xrange(0, 10):
        for j in xrange(0, 9):
            if chessboard[i][j] == 'a':
                score = score - 2
                pass
            elif chessboard[i][j] == 'b':
                score = score - 2
                pass
            elif chessboard[i][j] == 'n':
                score = score - 4
                pass
            elif chessboard[i][j] == 'r':
                score = score - 9
                pass
            elif chessboard[i][j] == 'c':
                score = score - 5
                pass
            elif chessboard[i][j] == 'p':
                if i > 5:
                    score = score - 2
                else:
                    score = score - 1
                pass
            elif chessboard[i][j] == 'A':
                score = score + 2
                pass
            elif chessboard[i][j] == 'B':
                score = score + 2
                pass
            elif chessboard[i][j] == 'N':
                score = score + 4
                pass
            elif chessboard[i][j] == 'R':
                score = score + 9
                pass
            elif chessboard[i][j] == 'C':
                score = score + 5
                pass
            elif chessboard[i][j] == 'P':
                if i > 5:
                    score = score + 1
                else:
                    score = score + 2
                pass
    return score

# choose next move
def nextmove(chessboard, side):
    # get current all possible movemetns
    posmov = moveGeneration.generatemoves(chessboard, side)
    print posmov

    scoret = [0 for i in range(len(posmov))]
    for t in range(0, len(posmov)):
        otile = chessboard[posmov[t][2]][posmov[t][3]]
        executemove(chessboard, posmov[t])
        if side == 'r':
            side == 'b'
            moves = moveGeneration.generatemoves(chessboard, side)
        else:
            side = 'r'
            moves = moveGeneration.generatemoves(chessboard, side)

        # evaluateuate the moves by monte carlo
        if side == 'b':
            scoret[t] = -9999
        else:
            scoret[t] = 9999
        evaluate_cur = evaluate(chessboard)

        for x in range(0, len(moves)):
            score = 0
            for i in range(0, 1):
                tile = chessboard[moves[x][2]][moves[x][3]]
                executemove(chessboard, moves[x])
                score -= evaluate_cur
                score += search(chessboard, side, 10, moves[x], tile)
            # find the best move
            if side == 'b':
                if score > scoret[t]:
                    scoret[t] = score
            else:
                if score < scoret[t]:
                    scoret[t] = score

        deexecutemove(chessboard, posmov[t], otile)

    # find the best move
    if side == 'b':
        max = -9999
        for x in range(len(scoret)):
            if scoret[x] > max:
                max = scoret[t]
                pos = t

    else:
        min = 9999
        for x in range(len(scoret)):
            if scoret[t] < min:
                min = scoret[t]
                pos = t
    print scoret

    return posmov[pos]


# monte carlo searching, return score of the board
def search(chessboard, side, depth, move, tile):
    posmov = moveGeneration.generatemoves(chessboard, side)
    if len(posmov) == 0 or depth == 0:
        score = evaluate(chessboard)
        deexecutemove(chessboard, move, tile)
        return score
    pass

    if side == 'r':
        newside = 'b'
    else:
        newside = 'r'

    # randomly pick a move
    pos = random.randint(0, len(posmov) - 1)
    newtile = chessboard[posmov[pos][2]][posmov[pos][3]]
    executemove(chessboard, posmov[pos])
    score = search(chessboard, newside, depth - 1, posmov[pos], newtile) + evaluate(chessboard)
    deexecutemove(chessboard, move, tile)

    return score


initboard = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR"

chessboard = [[0 for c in range(9)] for r in range(10)]

for r in range(10):
    for c in range(9):
        chessboard[r][c] = initboard[r*10 + c]


for i in range(5):
    executemove(chessboard, nextmove(chessboard, 'r'))
    for line in chessboard:
        print line
    print evaluate(chessboard)
    executemove(chessboard, nextmove(chessboard, 'b'))
    for line in chessboard:
        print line
    print evaluate(chessboard)
