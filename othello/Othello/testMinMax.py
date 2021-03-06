from GameBoard import getBoard, game_over, move, count_score
from minimaxBot import BotClass
import math
import RandBot
import time
import random
import copy
from statistics import mean

def compete(n,depth,bot):
    maxBot,randBot,tie=0,0,0
    maxBot_dark, maxBot_light = 0,0
    gametimes=[]
    for _ in range(n):
        botColor = random.randint(1,2)
        bot.changeColor(botColor)
        startTime = time.time()
        (x,y) = oneRound(copy.copy(depth),bot)
        gametimes.append(time.time()-startTime)
        if x==y:
            tie+=1
        elif bot.player==1:
            if x>y:
                maxBot += 1
                maxBot_dark +=1
            else:
                randBot +=1
        else:
            if x<y:
                maxBot += 1
                maxBot_light += 1
            else:
                randBot +=1
    return (maxBot,randBot,tie,gametimes, maxBot_dark, maxBot_light)

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
            coords = bot.getmove(board,copy.copy(bot.player),depth,time.time()+time_limit)
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
    games = int(input('Input number of games to play: '))
    time_limit=float(input('Input bot timelimit: '))
    print('Please stand by while bots play.')
    (p1,p2,tie,gameTimes, maxBot_dark, maxBot_light)=compete(games,4,_bot)
    print('MinimaxBot wins: {}\nRandBot wins: {}\nTies: {}\nWin percentage: {}%\nMean gametime: {}s\nWins as dark and light: {} dark/{} light'.format(p1,p2,tie,100*(p1/games),mean(gameTimes),maxBot_dark, maxBot_light))

