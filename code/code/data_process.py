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
# -------------------------------------------------------------+

import os
from information_ext import *
from update_piece import *
from update_move import *


# --------------------------------------------------------+
# open source data files and preprocess the data          |
# get the game results and assign rewards accordingly     |
# save the processed data to folder processed             |
# --------------------------------------------------------+
# path = '../source/'
# dt = open("../processed/processed.txt", 'w')
# count = 0
# for filename in os.listdir(path):
# 	if filename[0] == '.':
# 		continue
# 	pgn = open(path + filename, 'r')
# 	output = ""
# 	for line in pgn:
# 		count+=1
# 		if count%1000 == 0:
# 			print count
# 		# line = line.decode("utf-8")
# 		# print line
# 		if "Game" in line:
# 			continue
# 		elif "wins" in line:
# 			winner = line[0]
# 			print winner
# 			output = output.replace("\n", "," + winner + "\n")
# 			dt.write(output)
# 			output = ""
# 			continue
# 		else:
# 			output += line

# 	pgn.close()
# dt.close()
# print count


# --------------------------------------------------------------------+
# call information_ext functions to extract pgn info for training     |
# extract for piece selector first                                    |
# then for different move selectors                                   |
# save the extracted info to folder update_xxx                        |
# --------------------------------------------------------------------+
# info_ext_piece()
# info_ext_move()


# --------------------------------------------------+
# call update functions to train the old models     |
# --------------------------------------------------+
# update_piece_selector()
update_move_selector("r")
update_move_selector("c")
update_move_selector("b")
update_move_selector("a")
update_move_selector("n")
update_move_selector("k")
update_move_selector("p")