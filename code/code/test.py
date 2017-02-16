# for testing 

import moveGeneration
import validation
import check

initboard = "rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR/s,1234,p"

chessboard = [[0 for c in range(9)] for r in range(10)]

for r in range(10):
    for c in range(9):
        chessboard[r][c] = initboard[r*10 + c]

moves = moveGeneration.generatemoves(chessboard, 'r')

for line in chessboard:
    print line
print ""
for move in moves:
    print move

counter = 0
newboard = [[0 for x in range(9)] for y in range(10)]

while True:
    if counter == 0:
        choice = raw_input("Please input next move for red: ")
        if choice == 'q':
            break
        move[0] = int(choice[0])
        move[1] = int(choice[1])
        move[2] = int(choice[2])
        move[3] = int(choice[3])

        if validation.validate(chessboard, move, 'r') == 1:
            for r in range(10):
                for c in range(9):
                    newboard[r][c] = chessboard[r][c]
            newboard[move[2]][move[3]] = newboard[move[0]][move[1]]
            newboard[move[0]][move[1]] = '1'

            if check.check(newboard, 'r') == 1:
                print "Red will be in check!"
                continue

            chessboard[move[2]][move[3]] = chessboard[move[0]][move[1]]
            chessboard[move[0]][move[1]] = '1'
            for line in chessboard:
                print line
            counter = 1
            if check.check(chessboard, 'b') == 1:
                print "Red delivered a check!"
                checkflag, output = check.checkmate(chessboard, 'b')
                if checkflag == 1:
                    print "Black is checkmated!"
                else:
                    print "Black is not checkmated!"
                    for move in output:
                        print move
        else:
            print "Invalid move!"
        continue

    if counter == 1:
        choice = raw_input("Please input next move for black: ")
        if choice == 'q':
            break
        move[0] = int(choice[0])
        move[1] = int(choice[1])
        move[2] = int(choice[2])
        move[3] = int(choice[3])

        if validation.validate(chessboard, move, 'b') == 1:
            for r in range(10):
                for c in range(9):
                    newboard[r][c] = chessboard[r][c]
            newboard[move[2]][move[3]] = newboard[move[0]][move[1]]
            newboard[move[0]][move[1]] = '1'

            if check.check(newboard, 'b') == 1:
                print "Black will be in check!"
                continue

            chessboard[move[2]][move[3]] = chessboard[move[0]][move[1]]
            chessboard[move[0]][move[1]] = '1'
            for line in chessboard:
                print line
            counter = 0
            if check.check(chessboard, 'r') == 1:
                print "Black delivered a check!"
                checkflag, output = check.checkmate(chessboard, 'r')
                if checkflag == 1:
                    print "Red is checkmated!"
                else:
                    print "Red is not checkmated!"
                    for move in output:
                        print move
        else:
            print "Invalid move!"
        continue

