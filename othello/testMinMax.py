from GameBoard import getBoard, game_over, move, count_score
from minimaxBot import BotClass
import math
import RandBot
import time
import random
import copy

def compete(n,depth,bot):
    maxBot,randBot,tie=0,0,0
    for _ in range(n):
        botColor = random.randint(1,2)
        bot.changeColor(botColor)
        (x,y) = oneRound(copy.copy(depth),bot)
        if x==y:
            tie+=1
        elif bot.player==1:
            if x>y:
                maxBot += 1
            else:
                randBot +=1
        else:
            if x<y:
                maxBot += 1
            else:
                randBot +=1
    return (maxBot,randBot,tie)

def nextTurn(turn):
    if turn==1:
        return 2
    else:
        return 1

def oneRound(depth,bot):
    board = getBoard()
    turn = 1
    #print('Minimaxbot playing as: {}'.format(bot.player))
    while not game_over(board):
        if turn == bot.player:
            coords = bot.getmove(board,copy.copy(bot.player),depth)
            #print(v,x+1,y+1)
            if coords!=None:
                x,y = coords
                move(board,bot.player,x,y)
        else:
            coords = RandBot.bot_move(board,bot.opponent)
            if coords!=False:
                x,y = coords
                move(board,bot.opponent,x,y)
        turn = nextTurn(turn)
        #time.sleep(0.1)
        #print_board(board)
        #print('\n')
        
    p1, p2 = count_score(board)
    return (p1,p2)

if __name__ == "__main__":

    _botColor = random.randint(1,2)
    _bot = BotClass(_botColor)
    _opponent=nextTurn(_botColor)
    

    #tally = [None]*13
    #for i in range(1,5):
    #    print('Using depth: {}'.format(i))
    #    (p1,p2,tie)=compete(100,i,_bot)
    #    print('MinimaxBot wins: {}\nRandBot wins: {}\nTies: {}\n\n'.format(p1,p2,tie))
    #    tally[i-2]=(p1,i)
    #print(tally)
    (p1,p2,tie)=compete(100,4,_bot)
    print('MinimaxBot wins: {}\nRandBot wins: {}\nTies: {}'.format(p1,p2,tie))

