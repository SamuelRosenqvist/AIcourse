from GameBoard import getBoard, get_legal_moves, print_board, move, legal, game_over, count_score
from RandBot import bot_move
import time
from minimaxBot import BotClass
import copy

def get_player_move(board, player):
    # Let the player type in their move.
    # Returns the move as [x, y]
    allowed_inputs = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move ')
        move = input().lower()
        if len(move) == 2 and move[0] in allowed_inputs and move[1] in allowed_inputs:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if legal(board, player, x, y) == False:
                print('Illegal move, try another one')
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the bottom left corner.')
    return [x, y]

def next_turn(turn):
    if turn == 1:
        return 2
    else: 
        return 1


# Game start
if __name__ == "__main__":
    print('--- Othello ---\n')
    player = int(input('Choose your side, dark goes first (dark=1, light=2): '))
    if player==1:
        bot = 2
    else:
        bot = 1
    time_limit = int(input('Choose bot timelimit in seconds: '))

    board = getBoard()
    turn = 1
    bot = BotClass(bot)
    bot_used_Time=0

    # Main game loop
    while not game_over(board):
        if turn == player:
            print_board(board)
            print('\n')
            legal_moves = get_legal_moves(board,player)
            if len(legal_moves) == 0:
                print('No legal moves, passing player turn')
            else:
                print('Legal moves are %a\n' % ([[x+1 for x in m] for m in legal_moves]))
                x,y = get_player_move(board,player)
                move(board,player,x,y)
        else:
            coords = bot.getmove(board,copy.copy(bot.player),4,time.time()+time_limit)
            if coords!=None:
                x,y = coords
                move(board,bot.player,x,y)
        turn = next_turn(turn)
    p1, p2 = count_score(board)
    print('Final score:\n Light player: {} points\n Dark player: {} points'.format(p1,p2))
    if p1==p2:
        print('Game is a tie!')
    elif (player==1 and p1>p2) or (player==2 and p2>p1):
        print('You win!')
    else:
        print('Bot wins!')