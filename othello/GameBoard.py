# dark = 1 (goes first)
# white = 2
# capture = vertical/horizontal sandwiched pieces are flipped 
# legal move = can capture at least 1 piece
# no legal move = pass

# creates 8x8 board with 4 initial pieces in the middle
def getBoard():
    board = [[0 for x in range(8)] for x in range(8)]
    board[3][3]=2
    board[4][4]=2
    board[3][4]=1
    board[4][3]=1
    return board

#print of the board (list of lists) in a nicer fashion
def print_board(board):
    print('\n\n'.join([' '.join(['{:4}'.format(item) for item in row]) 
        for row in board]))

# Make a move, returns false if illegal, true if successful
def move(board,player,x0,y0):
    flip_tiles = legal(board,player,x0,y0)
    if flip_tiles == False:
        return False
    
    board[x0][y0] = player
    for x,y in flip_tiles:
        board[x][y] = player
    return True

# saves some time when bot has to check their legal moves
def move_with_list(board,player,x0,y0,flip_tiles):
    if len(flip_tiles)==0:
        return False
    old_tiles = {}
    old_tiles[(x0,y0)]= board[x0][y0]
    board[x0][y0] = player
    for x,y in flip_tiles:
        old_tiles[(x,y)]= board[x][y]
        board[x][y] = player
    return old_tiles

# saves space when doing recursive calls
def undo_move(board,player,old_tiles):
    for coord, val in old_tiles.items():
        board[coord[0]][coord[1]] = val

# if illegal move return false
# if legal return list of coordinates that would be flipped
def legal(board,player,x0,y0):
    if board[x0][y0]!=0 or not inbounds(x0,y0):
        return False

    board[x0][y0] = player # provisional tile placement
    if player==1:
        opponent=2
    else:
        opponent=1
    
    flip_tiles = []
    for xdir,ydir in [[1,0],[-1,0],[0,1],[0,-1]]:
        x,y=x0,y0

        x += xdir
        y += ydir
        if not inbounds(x,y):
            continue
        while board[x][y] == opponent:
            x += xdir
            y += ydir
            if not inbounds(x,y):
                break
        if not inbounds(x,y):
            continue
        if board[x][y] == player:
            while True:
                x -= xdir
                y -= ydir
                if x == x0 and y == y0:
                    break
                flip_tiles.append([x,y])
    board[x0][y0] = 0 # remove provisional tile
    if len(flip_tiles) == 0:
        return False
    return flip_tiles

# returns true if coordinates are located within board dimensions 
def inbounds(x,y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

# returns list of legal coordinates, if empty player must pass
def get_legal_moves(board,player):
    legal_moves = []

    for x in range(8):
        for y in range(8):
            if legal(board, player, x, y) != False:
                 legal_moves.append([x, y])
    return legal_moves

# returns true if no legal moves remain
def game_over(board):
    legal_moves = []
    for x in range(8):
        for y in range(8):
            if legal(board, 1, x, y) != False:
                 legal_moves.append([x, y])
            if legal(board, 2, x, y) != False:
                 legal_moves.append([x, y])
    if len(legal_moves)==0:
        return True
    else:
        return False

# returns list of legal coordinates with number of tiles flipped [[x,y,nr_of_tiles]]
def get_legal_moves_with_scores(board, player):
    legal_moves_with_scores = []

    for x in range(8):
        for y in range(8):
            legal_move = legal(board, player, x, y)
            if  legal_move != False:
                 legal_moves_with_scores.append([x, y,len(legal_move)])
    return legal_moves_with_scores

# everything the bot needs, not really killer moves but close enough, flipped tiles can be used to make a move.
def get_legal_moves_with_scores_and_flipped_tiles(board, player):
    legal_moves_with_scores = []
    for x in range(8):
        for y in range(8):
            legal_move = legal(board, player, x, y)
            if  legal_move != False:
                 legal_moves_with_scores.append([x, y,len(legal_move),legal_move])
    return legal_moves_with_scores


_strategy=[
[ 2000, -30 , 10,  5,   5, 10, -30 , 2000],
[ -30, -50 , -3, -3,  -3, -3, -50 , -30],
[  10, -3 ,  10,  1,   1,  10,  -3 , 10],
[   5, -3 ,  1,  1,   1,  1,  -3 ,    5],
[   5, -3 ,  1,  1,   1,  1,  -3 ,    5],
[  10, -3 ,  10,  1,   1,  10,  -3 , 10],
[ -30, -50 , -3, -3,  -3, -3, -50 , -30],
[ 2000, -30 , 10,  5,   5, 10, -30 , 2000]
]
# heuristic utility function, evaluates board state favourability for the player
def eval_board(board,player):
    if player == 1:
        opponent = 2
    else: 
        opponent = 1
    position=0
    pnum=0
    onum=0
    rest=0
    for x in range(8):
        for y in range(8):
            if board[x][y] == player:
                pnum+=1
                position += _strategy[x][y]
            elif board[x][y]==opponent:
                onum+=1
                position -= _strategy[x][y]
            else:
                rest +=1
    parity   = _stone_parity(pnum,onum)
    movement = _mobility(board,player,opponent)
    score=parity+movement+position
    return score

def _stone_parity(pnum,onum):
    return 100*(pnum-onum)/(pnum+onum)

def _mobility(board,player,opponent):
    playerMoves = len(get_legal_moves(board,player))
    opponentMoves = len(get_legal_moves(board,opponent))
    if playerMoves + opponentMoves != 0:
	    return 100 * (playerMoves - opponentMoves) / (playerMoves + opponentMoves)
    else:
	    return 0

# returns score [dark, light]
def count_score(board):
    flatBoard = [item for sublist in board for item in sublist]
    dark = len(list(filter(lambda x: x==1,flatBoard)))
    light = len(list(filter(lambda x: x==2,flatBoard)))
    return [dark,light]

# returns one of the player's score
def count_player_score(board,color):
    flatBoard = [item for sublist in board for item in sublist]
    score = len(list(filter(lambda x: x==color,flatBoard)))
    return score

# returns score lead (negative if losing)
def count_player_lead(board,player):
    flatBoard = [item for sublist in board for item in sublist]
    dark = len(list(filter(lambda x: x==1,flatBoard)))
    light = len(list(filter(lambda x: x==2,flatBoard)))
    if player==1:
        return dark-light
    else:
        return light-dark

