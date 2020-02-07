from GameBoard import get_legal_moves_with_scores_and_flipped_tiles,move_with_list,undo_move, eval_board, count_player_lead
import math
from operator import itemgetter

class BotClass:
    def __init__(self, player=1):
        self.player=player
        if self.player == 1:
            self.opponent=2
        else:
            self.opponent=1

    def changeColor(self, player):
        self.player=player
        if self.player==1:
            self.opponent=2
        else:
            self.opponent=1

    # returns the best move
    def getmove(self, board, player, depth, time_remaining=None):
        _, bestmove = self._minimax(board, player, time_remaining, depth)
        return bestmove

    def _minimax(self, board, player, time_remaining, depth):
        moves = get_legal_moves_with_scores_and_flipped_tiles(board,player)
        moves = sorted(moves,key=itemgetter(2),reverse=True)
        if len(moves)==0:
            score = count_player_lead(board,player)
            return score, None
        bestmove = (moves[0][0],moves[0][1])
        bestscore = - math.inf
        for x,y,_,flip_tiles in moves:
            old_tiles = move_with_list(board,player,x,y,flip_tiles)
            score = self._minimizing_player(board, self.otherColor(player), depth-1, -math.inf, math.inf)
            undo_move(board,player,old_tiles)
            if score > bestscore:
                bestscore = score
                bestmove = [x,y]
        return (bestscore,bestmove)

    def _maximizing_player(self, board, player, depth, alpha, beta):
        if depth == 0:
            return eval_board(board,player)
        bestscore = -math.inf
        moves = get_legal_moves_with_scores_and_flipped_tiles(board,player)
        moves = sorted(moves,key=itemgetter(2),reverse=True)
        for x,y,_,flip_tiles in moves:
            old_tiles = move_with_list(board,player,x,y,flip_tiles)
            score = self._minimizing_player(board, self.otherColor(player), depth-1, alpha, beta)
            undo_move(board,player,old_tiles)
            if score > bestscore:
                bestscore = score
            if bestscore >= beta:
                return bestscore
            alpha = max (alpha,bestscore)
        return bestscore

    def _minimizing_player(self, board, player, depth, alpha, beta):
        if depth == 0:
            return eval_board(board,player)
        bestscore = math.inf
        moves = get_legal_moves_with_scores_and_flipped_tiles(board,player)
        moves = sorted(moves,key=itemgetter(2),reverse=True)
        for x,y,_,flip_tiles in moves:
            old_tiles = move_with_list(board,player,x,y,flip_tiles)
            score = self._maximizing_player(board, self.otherColor(player), depth-1, alpha, beta)
            undo_move(board,player,old_tiles)
            if score < bestscore:
                bestscore = score
            if bestscore <= alpha:
                return bestscore
            beta = min(beta,bestscore)
        return bestscore

    def otherColor(self,color):
        if color == 1:
            return 2
        else:
            return 1