import moveGeneration
import validation
import check
import random
import copy

max_depth = 20

newboard = [[0 for x in range(9)] for y in range(10)]
class Chess(object):
    """docstring for Chess"""
    turn = 0
    fen = ""
    side = ''
    chessboard =  [[1 for i in range(9)] for i in range(10)]
    def __init__(self):
        super(Chess, self).__init__()
    
    #initialize the chess board
    def initialize(self):
        self.fen_set("rnbakabnr/111111111/1c11111c1/p1p1p1p1p/111111111/111111111/P1P1P1P1P/1C11111C1/111111111/RNBAKABNR r");
        self.turn = 0;
        self.side = 'r';

    #set the board with fen
    def fen_set(self,fen):
        for i in xrange(0,10):
            for j in xrange(0,9):
                self.chessboard[i][j]=fen[i*10 + j]
        self.side=fen[100]

    def output_fen(self):
        fen=""
        for i in xrange(0,10):
            for j in xrange(0,9):
                fen += self.chessboard[i][j]
            fen += "/"
        fen+=self.side
        return fen
    
    #print the board
    def printBoard(self):
        print "It's turn for %c" % self.side
        print "It's turn for %d" % self.turn
        for i in xrange(0,10):
            print self.chessboard[i]
        pass

    def outputBoard(self):
        return copy.deepcopy(self.chessboard), self.side
        pass

    def inputBoard(self,newboard,side,turn):
        self.chessboard=copy.deepcopy(newboard)
        self.side=side
        self.turn=turn
        pass

    def movement(self,choice,side):
        move=[0,0,0,0]
        move[0] = int(choice[0])
        move[1] = int(choice[1])
        move[2] = int(choice[2])
        move[3] = int(choice[3])
        self.chessboard[move[2]][move[3]] = self.chessboard[move[0]][move[1]]
        self.chessboard[move[0]][move[1]] = '1'
        self.turn += 1
        if side == 'r':
            self.side = 'b'
        else:
            self.side = 'r'

    def demovement(self,choice,tile):
        move=[0,0,0,0]
        move[0] = int(choice[0])
        move[1] = int(choice[1])
        move[2] = int(choice[2])
        move[3] = int(choice[3])
        self.chessboard[move[0]][move[1]] = self.chessboard[move[2]][move[3]]
        self.chessboard[move[2]][move[3]] = tile
        self.turn -= 1
        if self.side == 'r':
            self.side = 'b'
        else:
            self.side = 'r'
        pass

    #search the special piece, x and y is the position of the chess
    def eval(self):
        score=0;
        for i in xrange(0,10):
            for j in xrange(0,9):
                if self.chessboard[i][j]=='a':
                    score = score - 2
                    pass
                elif self.chessboard[i][j]=='b':
                    score = score - 2
                    pass
                elif self.chessboard[i][j]=='n':
                    score = score - 4
                    pass
                elif self.chessboard[i][j]=='r':
                    score = score - 9
                    pass
                elif self.chessboard[i][j]=='c':
                    score = score - 5
                    pass
                elif self.chessboard[i][j]=='p':
                    if i>5:
                        score = score - 2
                    else:
                        score = score - 1
                    pass
                #elif self.chessboard[i][j]=='k':
                    score = score - 100
                #elif self.chessboard[i][j]=='K':
                    score = score + 100
                elif self.chessboard[i][j]=='A':
                    score = score + 2
                    pass
                elif self.chessboard[i][j]=='B':
                    score = score + 2
                    pass
                elif self.chessboard[i][j]=='N':
                    score = score + 4
                    pass
                elif self.chessboard[i][j]=='R':
                    score = score + 9
                    pass
                elif self.chessboard[i][j]=='C':
                    score = score + 5
                    pass
                elif self.chessboard[i][j]=='P':
                    if i>5:
                        score = score + 1
                    else:
                        score = score + 2
                    pass
        return score

    def evalution(self,side):
        posmov=moveGeneration.generatemoves(self.chessboard,side)
        backupboard, backupside=self.outputBoard()
        backupturn = self.turn
        #posmov = improved_generation(self,side,posmov)
        pos = random.randint(0,len(posmov)-1)
        newboard = Chess()   
        print posmov
        score = [0 for i in range(len(posmov))]
        for x in xrange(0,len(posmov)):
            for i in range(20):
                self.inputBoard(backupboard,backupside,backupturn)
                self.movement(posmov[x],side)
                if(check.check(self.chessboard,backupside)== 0):
                    a=search_ver2(self,self.side,max_depth)
                    #print a
                    score[x] += a
                elif(side=='r'):
                    score[x]=-1
                else:
                    score[x]=1
        self.inputBoard(backupboard,backupside,backupturn)
        print score
        if(side=='r'):
            return (sum(score)/len(score) )/20
        elif(side=='b'):
            return (sum(score)/len(score) )/20
        pass

    #to be continued
    def nextmove(self,side):
        posmov=moveGeneration.generatemoves(self.chessboard,side)
        backupboard, backupside=self.outputBoard()
        backupturn = self.turn
        pos = random.randint(0,len(posmov)-1)

        return posmov[pos]

    def nextmove1(self,side):
        posmov=moveGeneration.generatemoves(self.chessboard,side)
        backupboard, backupside=self.outputBoard()
        backupturn = self.turn
        #posmov = improved_generation(self,side,posmov)
        pos = random.randint(0,len(posmov)-1)
        newboard = Chess()   
        print posmov
        eval_cur=self.eval()
        score = [0 for i in range(len(posmov))]
        for x in xrange(0,len(posmov)):
            for i in range(0,10):
                self.inputBoard(backupboard,backupside,backupturn)
                           
                #newboard.inputBoard(backupboard,backupside,backupturn)
                self.movement(posmov[x],side)
                if(check.check(self.chessboard,backupside)== 0):

                    score[x] += search(self,self.side,max_depth)
                else:
                    if(side=='b'):
                        score[x]=9999
                        i = i + 1
                    if(side=='r'):
                        score[x]=-9999
                        i = i + 1

            #score[x] += newchess.eval()
        pos = 0
        print score,side
        self.inputBoard(backupboard,backupside,backupturn)
        if side == 'r':
            max=-9999
            for x in range(len(score)):
                if score[x]>max:
                    max=score[x]
                    pos=x
        else:
            min=9999
            for x in range(len(score)):
                if score[x]<min:
                    min=score[x]
                    pos=x


        return posmov[pos]

def search(chess,side,depth):
    if(check.check(chess.chessboard,side)==1):
        if side == 'b':
            #print depth/50
            return chess.eval() + (max_depth - depth)/2
        else:
            return chess.eval() - (max_depth - depth)/2
    posmov=moveGeneration.generatemoves(chess.chessboard,side)
    #posmov = improved_generation(chess,side,posmov)
    if len(posmov) == 0 or depth == 0:
        return 0
    pass
    if side == 'r':
        newside = 'b'
    else:
        newside = 'r'
    pos = random.randint(0,len(posmov)-1)
    chess.movement(posmov[pos],side);
    return search(chess,newside,depth-1) 

def search_ver2(chess,side,depth):
    #print chess.eval()
    if side == 'r':
        newside = 'b'
    else:
        newside = 'r'
    if(check.check(chess.chessboard,side)==1):
        #print depth
        #chess.printBoard()
        #print 
        if side == 'r':
            #print depth/50
            return depth/float(max_depth) + chess.eval()/200.0
        else:
            return (-depth)/float(max_depth) + chess.eval()/200.0
    posmov=moveGeneration.generatemoves(chess.chessboard,side)
    #posmov = improved_generation(chess,side,posmov)
    if len(posmov) == 0 or depth == 0:
        return chess.eval()/500.0
    pass

    pos = random.randint(0,len(posmov)-1)
    chess.movement(posmov[pos],side);
    newtile= chess.chessboard[posmov[pos][2]][posmov[pos][3]]
    while (check.check(chess.chessboard,side)):
        chess.demovement(posmov[pos],newtile)
        posmov.pop(pos)
        if(len(posmov)==0):
            return chess.eval()/200.0
        pos = random.randint(0,len(posmov)-1)
        chess.movement(posmov[pos],side);

        pass
    #chess.printBoard()
    if side  == 'b':
        return search_ver2(chess,newside,depth-1) - len(posmov)/2000.0
    else:
        return search_ver2(chess,newside,depth-1) + len(posmov)/2000.0

def improved_generation(chess,side,moves):
    list1 = []
    backupboard, backupside=chess.outputBoard()
    backupturn = chess.turn
    for m in moves:
        chess.inputBoard(backupboard,backupside,backupturn)
        chess.movement(m,side)
        if(check.check(chess.chessboard,side)==0):
            list1.append(m)
    chess.inputBoard(backupboard,backupside,backupturn)
    return list1

def on_a_response(*args):
    print args
    print type(args)
    b = Chess()
    b.fen_set(args[0]);
    print b.side
    #b.printBoard()
    move = b.nextmove1(b.side)
    string = ''
    for x in xrange(0,4):
        print move
        print x
        string = string + str(move[x])
        print string
    socketIO.emit('chat1',string)


#socket.gethostbyaddr('localhost:3000')
# import socket
move = []
host = 'localhost'
port = 3000
from socketIO_client import SocketIO
import time
socketIO = SocketIO('localhost', port)
# socketIO.on('chat',on_a_response)
# socketIO.wait(seconds=10)

#chat_namespace = socketIO.define(AA, '/chat')
while True:
    socketIO.on('chat',on_a_response)
    socketIO.wait(seconds=5)

    pass

b = Chess()
