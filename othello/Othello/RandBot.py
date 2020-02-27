from GameBoard import get_legal_moves
import random

# return move coordinates or False if passing
def bot_move(board,player):
    legal_moves = get_legal_moves(board,player)
    if len(legal_moves)==0:
        return False
    random.shuffle(legal_moves)
    x,y = legal_moves[0]
    return [x,y]
