# ----------------------------------------+
# preprocess the source pgn data          |
# pass the data to information extractor  |
# used in reinforcement learning  		  |
# ----------------------------------------+

# -------------------------------------------------------------+
# Ver 1.0    Feb 16 2017                                       |
# Author: zxm                                                  |
# Summary: to train existing model by reinforcement            |
#          using processed source data                         |
#                                                              |
# Update 1    Feb 21 2017                                      |
# Summary: 1. modify to accept command line arguments          |
# -------------------------------------------------------------+

import os
import sys
from information_ext import *
from update_piece import *
from update_move import *

if len(sys.argv) != 3:
	print "Wrong number of arguments!"
	exit(1)
else:
	print "***** Start Training *****"
	print "Old Version: " + str(sys.argv[1])
	print "New Version: " + str(sys.argv[2])


# --------------------------------------------------------+
# open source data files and preprocess the data          |
# get the game results and assign rewards accordingly     |
# save the processed data to folder processed             |
# --------------------------------------------------------+
path = '../source/'
dt = open("../processed/processed.txt", 'w')
count = 0
for filename in os.listdir(path):
	if filename[0] == '.':
		continue
	pgn = open(path + filename, 'r')
	output = ""
	for line in pgn:
		count+=1
		if count%1000 == 0:
			print count
		# line = line.decode("utf-8")
		# print line
		if "Game" in line:
			continue
		elif "wins" in line:
			winner = line[0]
			output = output.replace("\n", "," + winner + "\n")
			dt.write(output)
			
			output = ""
			continue
		else:
			output += line

	pgn.close()
dt.close()
print count


# --------------------------------------------------------------------+
# call information_ext functions to extract pgn info for training     |
# extract for piece selector first                                    |
# then for different move selectors                                   |
# save the extracted info to folder update_xxx                        |
# --------------------------------------------------------------------+
info_ext_piece()
info_ext_move()


# --------------------------------------------------+
# call update functions to train the old models     |
# --------------------------------------------------+
over = str(sys.argv[1])
nver = str(sys.argv[2])

update_piece_selector(over, nver)
update_move_selector("r", over, nver)
update_move_selector("c", over, nver)
update_move_selector("b", over, nver)
update_move_selector("a", over, nver)
update_move_selector("n", over, nver)
update_move_selector("k", over, nver)
update_move_selector("p", over, nver)

