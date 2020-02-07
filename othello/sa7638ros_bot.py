from minimaxBot import BotClass
import socket
import random
from GameBoard import getBoard, move, game_over
import copy
# Implementatopn of an interaction with Othellio server 0.95
# I haven't the slightest idea...  

if __name__ == "__main__":
    # d = 1
    # w = 2
    _botColor = random.randint(1,2)
    if _botColor == 1:
        botcolor= 'd'
        opponent = 2
    else:
        botcolor= 'w'
        opponent = 1
    turn = 1
    bot = BotClass(_botColor)
    depth = 4
    board = getBoard()

    # change to correct one
    IDSTRING = 123

    HOST = 'vm33.cs.lth.se'    # The remote host
    PORT = 9035
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(IDSTRING)  # send id
    data = s.recv(1024)  # Helloyourid!  Your current win count is #
    data = s.recv(1024)  # choose colour, ’d’ for dark, ’w’ for white.
    print(repr(data))    
    s.sendall(botcolor)  # d|w
    data = s.recv(1024)  # you are dark|white   or: E: You provided wrong colour. Bye
    print(repr(data))
    if data == 'E: You provided wrong colour. Bye!':
        s.close
        print('Provided wrong color\n')
        quit()

    # game begins
    while not game_over(board):
        data = s.recv(1024)  # if server has to pass its turn it should know and send 'your move' again 
        if data[0:7]=='my move':
            turn = opponent
        else:
            turn = bot.player

        if turn == bot.player:
            coords = bot.getmove(board,copy.copy(bot.player),depth)
            if coords!=None:  # passes turn if no legal moves
                x,y = coords
                move(board,bot.player,x,y)
                s.send(intToChar(x)+str(y))
        else:
            data = s.recv(1024)
            x,y = charToInt(data[-2]),data[-1]
            move(board,bot.opponent,x,y)

    data = s.recv(1024)  # server: The game is finished
                         # server: White: #  
                         # server: Dark: #
                         # server: White won | Dark won | Draw
    s.close()



def intToChar(x):
    chars=['a','b','c','d','e','f','g','h']
    return chars[x]

def charToInt(c):
    chars=['a','b','c','d','e','f','g','h']
    return chars.index(c)