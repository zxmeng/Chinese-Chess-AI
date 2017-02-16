#coding=utf-8
import codecs

# chinese characters
# r for red, b for black
# king
k_r = "帅"
k_b = "将"
# advisor
a_r = "仕"
a_b = "士"
# bishop
b_r = "相"
b_b = "象"
# knight
n_r = "马"
n_b = "马"
# rock
r_r = "车"
r_b = "车"
# cannon
c_r = "炮"
c_b = "炮"
# pawn
p_r = "兵"
p_b = "卒"

piece_r = {'帅':'k', '仕':'a', '相':'b', '兵':'p'}
piece_b = {'将':'k', '士':'a', '象':'b', '卒':'p'}
piece_c = {'马':'n', '车':'r', '炮':'c'}

# move forward
x = "进"
# move backward
y = "退"
# move horizontally
z = "平"

movedir = {'进':'x', '退':'y', '平':'z'}

# front one
u = "前"
# middle one
v = "中"
# back one
w = "后"

position = {'前':'u', '中':'v', '后':'w', '一':'1', '二':'2', '三':'3', '四':'4', '五':'5'}

number = {'一':'1', '二':'2', '三':'3', '四':'4', '五':'5', '六':'6', '七':'7', '八':'8', '九':'9'}

one = "一"
two = "二"
three = "三"
four = "四"
five = "五"
six = "六"
seven = "七"
eight = "八"
nine = "九"

# decode the string in utf-8
def decode(str):
    str = str.decode("utf-8")
    return str

# open pgn file
pgn = open("pgn1","r")
# the translation output
output = ""
# the flag for searching
find_flag = 0

# read file line by line
for line in pgn:
    # decode the line
    line = decode(line)
    # split the string into two substrings
    subline = line.split()
    # for each substring
    for sub in subline:
        # for the four chars in one substring
        print sub
        output = ""
        for char in sub:
            #print char
            find_flag = 0
            if find_flag == 0:
                for tile in piece_r:
                    if char == decode(tile):
                        output += piece_r[tile]
                        find_flag = 1
                        break

            if find_flag == 0:
                for tile in piece_b:
                    if char == decode(tile):
                        output += piece_b[tile]
                        find_flag = 1
                        break

            if find_flag == 0:
                for tile in piece_c:
                    if char == decode(tile):
                        output += piece_c[tile]
                        find_flag = 1
                        break

            if find_flag == 0:
                for tile in movedir:
                    if char == decode(tile):
                        output += movedir[tile]
                        find_flag = 1
                        break

            if find_flag == 0:
                for tile in position:
                    if char == decode(tile):
                        output += position[tile]
                        find_flag = 1
                        break

            if find_flag == 0:
                for tile in number:
                    if char == decode(tile):
                        output += number[tile]
                        find_flag = 1
                        break

            if find_flag == 0:
                if int(char) > 0 and int(char) < 10:
                    output += str(int(char))
                    find_flag = 1

            # report error if not found
            if find_flag == 0:
                print "error: char not found!"

        # print ourput for each subline
        print output



