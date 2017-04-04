# move generation
# input: borad, player
# output: array of moves

from validation import validate

# board: 9 x 10
# player: red(r) or black(b)
# lower case for black, upper case for red
# k king
# a adviser
# b bishop
# n knight
# r rock
# c cannon
# p pawn
piece_b = ['k','a','b','n','r','c','p']
piece_r = ['K','A','B','N','R','C','P']
piece = {'b': piece_b, 'r': piece_r}
piece_op = {'b': piece_r, 'r': piece_b}


def validate_k(board, r, c, player):
    count = 0
    for x in [-1, 1]:
        count += validate(board, [r, c, r + x, c], player)
    for y in [-1, 1]:
        count += validate(board, [r, c, r, c + y], player)
    if player == 'b':
        y_range = range(7, 10)
    else:
        y_range = range(3)
    for y in y_range:
        count += validate(board, [r, c, y, c], player)
    return count


def validate_a(board, r, c, player):
    count = 0
    for x in [-1, 1]:
        for y in [-1, 1]:
            count += validate(board, [r, c, r + x, c + y], player)
    return count


def validate_b(board, r, c, player):
    count = 0
    for x in [-2, 2]:
        for y in [-2, 2]:
            count += validate(board, [r, c, r + x, c + y], player)
    return count


def validate_n(board, r, c, player):
    count = 0
    for x in [-1, 1]:
        for y in [-2, 2]:
            count += validate(board, [r, c, r + x, c + y], player)
    for x in [-2, 2]:
        for y in [-1, 1]:
            count += validate(board, [r, c, r + x, c + y], player)
    return count


def validate_r(board, r, c, player):
    count = 0
    # left
    for x in range(c):
        count += validate(board, [r, c, r, x], player)
    # right
    for x in range(c, 9):
        count += validate(board, [r, c, r, x], player)
    # up
    for y in range(r):
        count += validate(board, [r, c, y, c], player)
    # down
    for y in range(r, 10):
        count += validate(board, [r, c, y, c], player)
    return count


def validate_c(board, r, c, player):
    count = 0
    # left
    for x in range(9):
        count += validate(board, [r, c, r, x], player)
        if board[r][x] == '1':
            board[r][x] = piece_op[player][-1]
            count += validate(board, [r, c, r, x], player)
            board[r][x] = '1'
    # right
    # for x in range(c, 9):
    #     count += validate(board, [r, c, r, x], player)
    #     newboard = board
    #     newboard[r][x] = piece_op[player][-1]
    #     count += validate(newboard, [r, c, r, x], player)
    # up
    for y in range(10):
        count += validate(board, [r, c, y, c], player)
        if board[y][c] == '1':
            board[y][c] = piece_op[player][-1]
            count += validate(board, [r, c, y, c], player)
            board[y][c] = '1'
    # down
    # for y in range(r, 10):
    #     count += validate(board, [r, c, y, c], player)
    #     newboard = board
    #     newboard[r][x] = piece_op[player][-1]
    #     count += validate(newboard, [r, c, r, x], player)
    return count


def validate_p(board, r, c, player):
    count = 0
    if player == 'b':
        t = 1
    else:
        t = -1
    # forward
    count += validate(board, [r, c, r + t, c], player)
    # right
    count += validate(board, [r, c, r, c + 1], player)
    # left
    count += validate(board, [r, c, r, c - 1], player)
    return count

options = {'k':validate_k,'a':validate_a,'b':validate_b,'n':validate_n,'r':validate_r,'c':validate_c,'p':validate_p}
options_gen = {'k':validate_k,'a':validate_a,'b':validate_b,'n':validate_n,'r':validate_r,'c':validate_c,'p':validate_p}


def generatemoves(board, player):
    output = []
    if player == 'b':
        for r in range(10):
            for c in range(9):
                if board[r][c] == 'k':
                    if validate(board, [r, c, r+1, c], 'b') == 1:
                        output.append([r, c, r+1, c])
                    if validate(board, [r, c, r-1, c], 'b') == 1:
                        output.append([r, c, r-1, c])
                    if validate(board, [r, c, r, c+1], 'b') == 1:
                        output.append([r, c, r, c+1])
                    if validate(board, [r, c, r, c-1], 'b') == 1:
                        output.append([r, c, r, c-1])
                    for y in range(7,10):
                        if validate(board, [r, c, y, c], 'b') == 1:
                            output.append([r, c, y, c])

                elif board[r][c] == 'a':
                    if validate(board, [r, c, r+1, c+1], 'b') == 1:
                        output.append([r, c, r+1, c+1])
                    if validate(board, [r, c, r+1, c-1], 'b') == 1:
                        output.append([r, c, r+1, c-1])
                    if validate(board, [r, c, r-1, c+1], 'b') == 1:
                        output.append([r, c, r-1, c+1])
                    if validate(board, [r, c, r-1, c-1], 'b') == 1:
                        output.append([r, c, r-1, c-1])

                elif board[r][c] == 'b':
                    if validate(board, [r, c, r+2, c+2], 'b') == 1:
                        output.append([r, c, r+2, c+2])
                    if validate(board, [r, c, r+2, c-2], 'b') == 1:
                        output.append([r, c, r+2, c-2])
                    if validate(board, [r, c, r-2, c+2], 'b') == 1:
                        output.append([r, c, r-2, c+2])
                    if validate(board, [r, c, r-2, c-2], 'b') == 1:
                        output.append([r, c, r-2, c-2])

                elif board[r][c] == 'n':
                    if validate(board, [r, c, r+1, c+2], 'b') == 1:
                        output.append([r, c, r+1, c+2])
                    if validate(board, [r, c, r+1, c-2], 'b') == 1:
                        output.append([r, c, r+1, c-2])
                    if validate(board, [r, c, r-1, c+2], 'b') == 1:
                        output.append([r, c, r-1, c+2])
                    if validate(board, [r, c, r-1, c-2], 'b') == 1:
                        output.append([r, c, r-1, c-2])
                    if validate(board, [r, c, r+2, c+1], 'b') == 1:
                        output.append([r, c, r+2, c+1])
                    if validate(board, [r, c, r+2, c-1], 'b') == 1:
                        output.append([r, c, r+2, c-1])
                    if validate(board, [r, c, r-2, c+1], 'b') == 1:
                        output.append([r, c, r-2, c+1])
                    if validate(board, [r, c, r-2, c-1], 'b') == 1:
                        output.append([r, c, r-2, c-1])

                elif board[r][c] == 'r':
                    # left
                    for x in range(c):
                        if validate(board, [r, c, r, x], 'b') == 1:
                            output.append([r, c, r, x])
                    # right
                    for x in range(c, 9):
                        if validate(board, [r, c, r, x], 'b') == 1:
                            output.append([r, c, r, x])
                    # up
                    for y in range(r):
                        if validate(board, [r, c, y, c], 'b') == 1:
                            output.append([r, c, y, c])
                    # down
                    for y in range(r, 10):
                        if validate(board, [r, c, y, c], 'b') == 1:
                            output.append([r, c, y, c])

                elif board[r][c] == 'c':
                    # left
                    for x in range(c):
                        if validate(board, [r, c, r, x], 'b') == 1:
                            output.append([r, c, r, x])
                    # right
                    for x in range(c, 9):
                        if validate(board, [r, c, r, x], 'b') == 1:
                            output.append([r, c, r, x])
                    # up
                    for y in range(r):
                        if validate(board, [r, c, y, c], 'b') == 1:
                            output.append([r, c, y, c])
                    # down
                    for y in range(r, 10):
                        if validate(board, [r, c, y, c], 'b') == 1:
                            output.append([r, c, y, c])

                elif board[r][c] == 'p':
                    # forward
                    if validate(board, [r, c, r+1, c], 'b') == 1:
                        output.append([r, c, r+1, c])
                    # right
                    if validate(board, [r, c, r, c+1], 'b') == 1:
                        output.append([r, c, r, c+1])
                    # left
                    if validate(board, [r, c, r, c-1], 'b') == 1:
                        output.append([r, c, r, c-1])

    elif player == 'r':
        for r in range(10):
            for c in range(9):
                if board[r][c] == 'K':
                    if validate(board, [r, c, r+1, c], 'r') == 1:
                        output.append([r, c, r+1, c])
                    if validate(board, [r, c, r-1, c], 'r') == 1:
                        output.append([r, c, r-1, c])
                    if validate(board, [r, c, r, c+1], 'r') == 1:
                        output.append([r, c, r, c+1])
                    if validate(board, [r, c, r, c-1], 'r') == 1:
                        output.append([r, c, r, c-1])
                    for y in range(3):
                        if validate(board, [r, c, y, c], 'r') == 1:
                            output.append([r, c, y, c])

                elif board[r][c] == 'A':
                    if validate(board, [r, c, r+1, c+1], 'r') == 1:
                        output.append([r, c, r+1, c+1])
                    if validate(board, [r, c, r+1, c-1], 'r') == 1:
                        output.append([r, c, r+1, c-1])
                    if validate(board, [r, c, r-1, c+1], 'r') == 1:
                        output.append([r, c, r-1, c+1])
                    if validate(board, [r, c, r-1, c-1], 'r') == 1:
                        output.append([r, c, r-1, c-1])

                elif board[r][c] == 'B':
                    if validate(board, [r, c, r+2, c+2], 'r') == 1:
                        output.append([r, c, r+2, c+2])
                    if validate(board, [r, c, r+2, c-2], 'r') == 1:
                        output.append([r, c, r+2, c-2])
                    if validate(board, [r, c, r-2, c+2], 'r') == 1:
                        output.append([r, c, r-2, c+2])
                    if validate(board, [r, c, r-2, c-2], 'r') == 1:
                        output.append([r, c, r-2, c-2])

                elif board[r][c] == 'N':
                    if validate(board, [r, c, r+1, c+2], 'r') == 1:
                        output.append([r, c, r+1, c+2])
                    if validate(board, [r, c, r+1, c-2], 'r') == 1:
                        output.append([r, c, r+1, c-2])
                    if validate(board, [r, c, r-1, c+2], 'r') == 1:
                        output.append([r, c, r-1, c+2])
                    if validate(board, [r, c, r-1, c-2], 'r') == 1:
                        output.append([r, c, r-1, c-2])
                    if validate(board, [r, c, r+2, c+1], 'r') == 1:
                        output.append([r, c, r+2, c+1])
                    if validate(board, [r, c, r+2, c-1], 'r') == 1:
                        output.append([r, c, r+2, c-1])
                    if validate(board, [r, c, r-2, c+1], 'r') == 1:
                        output.append([r, c, r-2, c+1])
                    if validate(board, [r, c, r-2, c-1], 'r') == 1:
                        output.append([r, c, r-2, c-1])

                elif board[r][c] == 'R':
                    # left
                    for x in range(c):
                        if validate(board, [r, c, r, x], 'r') == 1:
                            output.append([r, c, r, x])
                    # right
                    for x in range(c, 9):
                        if validate(board, [r, c, r, x], 'r') == 1:
                            output.append([r, c, r, x])
                    # up
                    for y in range(r):
                        if validate(board, [r, c, y, c], 'r') == 1:
                            output.append([r, c, y, c])
                    # down
                    for y in range(r, 10):
                        if validate(board, [r, c, y, c], 'r') == 1:
                            output.append([r, c, y, c])

                elif board[r][c] == 'C':
                    # left
                    for x in range(c):
                        if validate(board, [r, c, r, x], 'r') == 1:
                            output.append([r, c, r, x])
                    # right
                    for x in range(c, 9):
                        if validate(board, [r, c, r, x], 'r') == 1:
                            output.append([r, c, r, x])
                    # up
                    for y in range(r):
                        if validate(board, [r, c, y, c], 'r') == 1:
                            output.append([r, c, y, c])
                    # down
                    for y in range(r, 10):
                        if validate(board, [r, c, y, c], 'r') == 1:
                            output.append([r, c, y, c])

                elif board[r][c] == 'P':
                    # forward
                    if validate(board, [r, c, r-1, c], 'r') == 1:
                        output.append([r, c, r-1, c])
                    # right
                    if validate(board, [r, c, r, c+1], 'r') == 1:
                        output.append([r, c, r, c+1])
                    # left
                    if validate(board, [r, c, r, c-1], 'r') == 1:
                        output.append([r, c, r, c-1])

    return output


def generatemoves_fortile(board, player, tile):
    output = []
    r = tile[0]
    c = tile[1]

    if player == 'b':
        if board[r][c] == 'k':
            if validate(board, [r, c, r+1, c], 'b') == 1:
                output.append([r, c, r+1, c])
            if validate(board, [r, c, r-1, c], 'b') == 1:
                output.append([r, c, r-1, c])
            if validate(board, [r, c, r, c+1], 'b') == 1:
                output.append([r, c, r, c+1])
            if validate(board, [r, c, r, c-1], 'b') == 1:
                output.append([r, c, r, c-1])
            for y in range(7,10):
                if validate(board, [r, c, y, c], 'b') == 1:
                    output.append([r, c, y, c])

        elif board[r][c] == 'a':
            if validate(board, [r, c, r+1, c+1], 'b') == 1:
                output.append([r, c, r+1, c+1])
            if validate(board, [r, c, r+1, c-1], 'b') == 1:
                output.append([r, c, r+1, c-1])
            if validate(board, [r, c, r-1, c+1], 'b') == 1:
                output.append([r, c, r-1, c+1])
            if validate(board, [r, c, r-1, c-1], 'b') == 1:
                output.append([r, c, r-1, c-1])

        elif board[r][c] == 'b':
            if validate(board, [r, c, r+2, c+2], 'b') == 1:
                output.append([r, c, r+2, c+2])
            if validate(board, [r, c, r+2, c-2], 'b') == 1:
                output.append([r, c, r+2, c-2])
            if validate(board, [r, c, r-2, c+2], 'b') == 1:
                output.append([r, c, r-2, c+2])
            if validate(board, [r, c, r-2, c-2], 'b') == 1:
                output.append([r, c, r-2, c-2])

        elif board[r][c] == 'n':
            if validate(board, [r, c, r+1, c+2], 'b') == 1:
                output.append([r, c, r+1, c+2])
            if validate(board, [r, c, r+1, c-2], 'b') == 1:
                output.append([r, c, r+1, c-2])
            if validate(board, [r, c, r-1, c+2], 'b') == 1:
                output.append([r, c, r-1, c+2])
            if validate(board, [r, c, r-1, c-2], 'b') == 1:
                output.append([r, c, r-1, c-2])
            if validate(board, [r, c, r+2, c+1], 'b') == 1:
                output.append([r, c, r+2, c+1])
            if validate(board, [r, c, r+2, c-1], 'b') == 1:
                output.append([r, c, r+2, c-1])
            if validate(board, [r, c, r-2, c+1], 'b') == 1:
                output.append([r, c, r-2, c+1])
            if validate(board, [r, c, r-2, c-1], 'b') == 1:
                output.append([r, c, r-2, c-1])

        elif board[r][c] == 'r':
            # left
            for x in range(c):
                if validate(board, [r, c, r, x], 'b') == 1:
                    output.append([r, c, r, x])
            # right
            for x in range(c, 9):
                if validate(board, [r, c, r, x], 'b') == 1:
                    output.append([r, c, r, x])
            # up
            for y in range(r):
                if validate(board, [r, c, y, c], 'b') == 1:
                    output.append([r, c, y, c])
            # down
            for y in range(r, 10):
                if validate(board, [r, c, y, c], 'b') == 1:
                    output.append([r, c, y, c])

        elif board[r][c] == 'c':
            # left
            for x in range(c):
                if validate(board, [r, c, r, x], 'b') == 1:
                    output.append([r, c, r, x])
            # right
            for x in range(c, 9):
                if validate(board, [r, c, r, x], 'b') == 1:
                    output.append([r, c, r, x])
            # up
            for y in range(r):
                if validate(board, [r, c, y, c], 'b') == 1:
                    output.append([r, c, y, c])
            # down
            for y in range(r, 10):
                if validate(board, [r, c, y, c], 'b') == 1:
                    output.append([r, c, y, c])

        elif board[r][c] == 'p':
            # forward
            if validate(board, [r, c, r+1, c], 'b') == 1:
                output.append([r, c, r+1, c])
            # right
            if validate(board, [r, c, r, c+1], 'b') == 1:
                output.append([r, c, r, c+1])
            # left
            if validate(board, [r, c, r, c-1], 'b') == 1:
                output.append([r, c, r, c-1])

    elif player == 'r':
        if board[r][c] == 'K':
            if validate(board, [r, c, r+1, c], 'r') == 1:
                output.append([r, c, r+1, c])
            if validate(board, [r, c, r-1, c], 'r') == 1:
                output.append([r, c, r-1, c])
            if validate(board, [r, c, r, c+1], 'r') == 1:
                output.append([r, c, r, c+1])
            if validate(board, [r, c, r, c-1], 'r') == 1:
                output.append([r, c, r, c-1])
            for y in range(3):
                if validate(board, [r, c, y, c], 'r') == 1:
                    output.append([r, c, y, c])

        elif board[r][c] == 'A':
            if validate(board, [r, c, r+1, c+1], 'r') == 1:
                output.append([r, c, r+1, c+1])
            if validate(board, [r, c, r+1, c-1], 'r') == 1:
                output.append([r, c, r+1, c-1])
            if validate(board, [r, c, r-1, c+1], 'r') == 1:
                output.append([r, c, r-1, c+1])
            if validate(board, [r, c, r-1, c-1], 'r') == 1:
                output.append([r, c, r-1, c-1])

        elif board[r][c] == 'B':
            if validate(board, [r, c, r+2, c+2], 'r') == 1:
                output.append([r, c, r+2, c+2])
            if validate(board, [r, c, r+2, c-2], 'r') == 1:
                output.append([r, c, r+2, c-2])
            if validate(board, [r, c, r-2, c+2], 'r') == 1:
                output.append([r, c, r-2, c+2])
            if validate(board, [r, c, r-2, c-2], 'r') == 1:
                output.append([r, c, r-2, c-2])

        elif board[r][c] == 'N':
            if validate(board, [r, c, r+1, c+2], 'r') == 1:
                output.append([r, c, r+1, c+2])
            if validate(board, [r, c, r+1, c-2], 'r') == 1:
                output.append([r, c, r+1, c-2])
            if validate(board, [r, c, r-1, c+2], 'r') == 1:
                output.append([r, c, r-1, c+2])
            if validate(board, [r, c, r-1, c-2], 'r') == 1:
                output.append([r, c, r-1, c-2])
            if validate(board, [r, c, r+2, c+1], 'r') == 1:
                output.append([r, c, r+2, c+1])
            if validate(board, [r, c, r+2, c-1], 'r') == 1:
                output.append([r, c, r+2, c-1])
            if validate(board, [r, c, r-2, c+1], 'r') == 1:
                output.append([r, c, r-2, c+1])
            if validate(board, [r, c, r-2, c-1], 'r') == 1:
                output.append([r, c, r-2, c-1])

        elif board[r][c] == 'R':
            # left
            for x in range(c):
                if validate(board, [r, c, r, x], 'r') == 1:
                    output.append([r, c, r, x])
            # right
            for x in range(c, 9):
                if validate(board, [r, c, r, x], 'r') == 1:
                    output.append([r, c, r, x])
            # up
            for y in range(r):
                if validate(board, [r, c, y, c], 'r') == 1:
                    output.append([r, c, y, c])
            # down
            for y in range(r, 10):
                if validate(board, [r, c, y, c], 'r') == 1:
                    output.append([r, c, y, c])

        elif board[r][c] == 'C':
            # left
            for x in range(c):
                if validate(board, [r, c, r, x], 'r') == 1:
                    output.append([r, c, r, x])
            # right
            for x in range(c, 9):
                if validate(board, [r, c, r, x], 'r') == 1:
                    output.append([r, c, r, x])
            # up
            for y in range(r):
                if validate(board, [r, c, y, c], 'r') == 1:
                    output.append([r, c, y, c])
            # down
            for y in range(r, 10):
                if validate(board, [r, c, y, c], 'r') == 1:
                    output.append([r, c, y, c])

        elif board[r][c] == 'P':
            # forward
            if validate(board, [r, c, r-1, c], 'r') == 1:
                output.append([r, c, r-1, c])
            # right
            if validate(board, [r, c, r, c+1], 'r') == 1:
                output.append([r, c, r, c+1])
            # left
            if validate(board, [r, c, r, c-1], 'r') == 1:
                output.append([r, c, r, c-1])

    return output


def count_movesnum(board, player, tile):
    count = 0
    r = tile[0]
    c = tile[1]
    if player == 'b' and board[r][c] in piece_b:
        count = options[board[r][c]](board, r, c, player)
    elif player == 'r' and board[r][c] in piece_r:
        count = options[board[r][c].lower()](board, r, c, player)
    return count


def count_mobility(board, tile):
    count = 0
    r = tile[0]
    c = tile[1]
    if board[r][c] in piece_b:
        player == 'b'
        count = options[board[r][c]](board, r, c, player)
    elif board[r][c] in piece_r:
        player == 'r' 
        count = options[board[r][c].lower()](board, r, c, player)
    return count

