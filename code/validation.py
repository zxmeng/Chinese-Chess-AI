# move validation
# input: board and move
# output: bool

# board: 9 x 10 
# move: [old_r][old_c][new_r][new_c]
# move[0]: original row
# move[1]: original col
# move[2]: new row
# move[3]: new col
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


def validate_k(board, move, player):
    if player == 'b':
        k = 'K'
        r_range = range(move[0] + 1, move[2])
        t = 0
    else:
        k = 'k'
        r_range = range(move[2] + 1, move[0])
        t = 7

    if board[move[2]][move[3]] == k and move[3] == move[1]:
        for r in r_range:
            if board[r][move[1]] != '1':
                return 0
    else:
        # king cant move out of the box, invalid
        if move[2] > 2+t or move[2] < t or move[3] > 5 or move[3] < 3:
            return 0
        # king can only move one cell horizontally or vertically, invalid
        if ((move[0] - move[2]) ** 2 + (move[1] - move[3]) ** 2) != 1:
            return 0
    return 1


def validate_a(_, move, player):
    if player == 'b':
        t = 0
    else:
        t = 7
    # adviser cant move out of the box, invalid
    if move[2] > 2+t or move[2] < t or move[3] > 5 or move[3] < 3:
        return 0
    # adviser can only move one cell diagonally, invalid
    if ((move[0] - move[2]) ** 2 + (move[1] - move[3]) ** 2) != 2:
        return 0
    return 1


def validate_b(board, move, player):
    # bishop cant cross the river
    if player == 'b' and move[2] > 4:
        return 0
    elif player == 'r' and move[2] < 5:
        return 0
    # bishop move like 'tian'
    if ((move[0] - move[2]) ** 2 + (move[1] - move[3]) ** 2) != 8:
        return 0
    # bishop cant move with a tile in the center of 'tian'
    r_center = (move[0] + move[2]) / 2
    c_center = (move[1] + move[3]) / 2
    if board[r_center][c_center] != '1':
        return 0
    return 1


def validate_n(board, move, _):
    # knight move like 'ri'
    if (move[0] - move[2]) ** 2 == 1 and (move[1] - move[3]) ** 2 == 4:
        # knight will be blocked by the tile nearby
        r_center = move[0]
        c_center = (move[1] + move[3]) / 2
        if board[r_center][c_center] != '1':
            return 0
    elif (move[0] - move[2]) ** 2 == 4 and (move[1] - move[3]) ** 2 == 1:
        # knight will be blocked by the tile nearby
        r_center = (move[0] + move[2]) / 2
        c_center = move[1]
        if board[r_center][c_center] != '1':
            return 0
    # not moving like 'ri', invalid
    else:
        return 0
    return 1


def validate_r(board, move, _):
    # move horizontally
    if (move[0] - move[2]) ** 2 == 0 and (move[1] - move[3]) ** 2 != 0:
        if move[1] > move[3]:
            c_range = range(move[3] + 1, move[1])
        else:
            c_range = range(move[1] + 1, move[3])
        # rock cant cross other pieces
        for c in c_range:
            if board[move[0]][c] != '1':
                return 0
    # move vertically
    elif (move[0] - move[2]) ** 2 != 0 and (move[1] - move[3]) ** 2 == 0:
        if move[0] > move[2]:
            r_range = range(move[2] + 1, move[0])
        else:
            r_range = range(move[0] + 1, move[2])
        # rock cant cross other pieces
        for r in r_range:
            if board[r][move[1]] != '1':
                return 0
    # rock can only move horizontally or vertically
    else:
        return 0
    return 1


def validate_c(board, move, player):
    # cannon capture the opposite tile
    capture = 0
    if player == 'b' and board[move[2]][move[3]] in piece_r:
        capture = 1
    elif player == 'r' and board[move[2]][move[3]] in piece_b:
        capture = 1
    # move horizontally
    if (move[0] - move[2]) ** 2 == 0 and (move[1] - move[3]) ** 2 != 0:
        # cannon cant cross pieces if not capturing opposite tile
        # cannon can only cross one piece if capturing opposite tile
        if move[1] > move[3]:
            c_range = range(move[3] + 1, move[1])
        else:
            c_range = range(move[1] + 1, move[3])
        # count the pieces in the middle
        counter = 0
        for c in c_range:
            if board[move[0]][c] != '1':
                counter += 1
        # when capture = 1, counter should be 1
        # when capture = 0, counter should be 0
        if (counter - capture) != 0:
            return 0
    # move vertically
    elif (move[0] - move[2]) ** 2 != 0 and (move[1] - move[3]) ** 2 == 0:
        # cannon cant cross pieces if not capturing opposite tile
        # cannon can only cross one piece if capturing opposite tile
        if move[0] > move[2]:
            r_range = range(move[2] + 1, move[0])
        else:
            r_range = range(move[0] + 1, move[2])
        # count the pieces in the middle
        counter = 0
        for r in r_range:
            if board[r][move[1]] != '1':
                counter += 1
        # when capture = 1, counter should be 1
        # when capture = 0, counter should be 0
        if (counter - capture) != 0:
            return 0
    # cannon can only move horizontally or vertically
    else:
        return 0
    return 1


def validate_p(_, move, player):
    # move more than one step
    if ((move[0] - move[2]) ** 2 + (move[1] - move[3]) ** 2) != 1:
        return 0

    # before crossing the river, can only move forward one step
    if player == 'b' and move[0] < 5:
        if (move[2] - move[0]) != 1 or move[3] != move[1]:
            return 0
    elif player == 'r' and move[0] > 4:
        if (move[2] - move[0]) != -1 or move[3] != move[1]:
            return 0

    # after crossing the river, can move forward/left/right one step but not backward
    if player == 'b' and move[0] > 4 and move[2] < move[0]:
        return 0
    elif player == 'r' and move[0] < 5 and move[2] > move[0]:
        return 0
    return 1


options = {'k':validate_k,'a':validate_a,'b':validate_b,'n':validate_n,'r':validate_r,'c':validate_c,'p':validate_p}


# move validation
# 0 for invalid, 1 for valid
def validate(board, move, player):
    if move[2] < 0 or move[2] > 9 or move[3] < 0 or move[3] > 8:
        return 0

    if player == 'b':
        # only can move black tile
        # can't suicide, invalid
        if board[move[0]][move[1]] not in piece_b or board[move[2]][move[3]] in piece_b:
            return 0

        return options[board[move[0]][move[1]]](board, move, player)

    elif player == 'r':
        # only can move red tile
        # can't suicide, invalid
        if board[move[0]][move[1]] not in piece_r or board[move[2]][move[3]] in piece_r:
            return 0

        return options[board[move[0]][move[1]].lower()](board, move, player)

    return 0
