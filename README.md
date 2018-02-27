# CUHK CS FYP, 2016 - 2017

## Intelligent Non-Player Character with Deep Learning

This project is to use Machine Learning techniques, such as CNN, Supervised Learning and Reinforcement Learning, to build and train a Game AI for Chinese Chess. Training data were collected via internet. Tensorflow was used to build the neural network models and Aliyun was used for cloud service.

1. run the server

    cd ./site/Sites

    npm start

2. run the python program

    cd ./code

    python server_new.py

if you want to use the evaluator from Eleeye, set the path in the common.py

File | Function
------------ | -------------
check.py | test check or checkmate
chess_new.py | play chess with itself
common.py | common functions
data_process.py | process data for NN
information.py | extract information from pgn  
information_eva.py | extract data for Evaluation network
information_ext.py | extract data for Policy network 
model_training_move.py | train move selector
model_training_piece.py | train piece selector
moveGeneration.py | generate possible moves
move_selector.py | move selector
piece_selector.py | piece selector
server_new.py | server program
train_eva_full.py | train evaluation network
trans.py | process PGN 
update_move.py | RL for move selector
update_piece.py | RL for piece selector
validation.py | move validation
chess2p\ | 2p chess for RL
