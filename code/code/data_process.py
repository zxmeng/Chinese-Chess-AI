# ----------------------------------------+
# preprocess the source pgn data          |
# pass the data to information extractor  |
# used in reinforcement learning  		  |
# ----------------------------------------+

from moveGeneration import *
from validation import *
import numpy as np
import os

path = '../source/'
dt = open("../test/test.txt", 'w')
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
			print winner
			output = output.replace("\n", "," + winner + "\n")
			dt.write(output)
			output = ""
			continue
		else:
			output += line

	pgn.close()
dt.close()