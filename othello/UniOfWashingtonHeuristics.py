from GameBoard import get_legal_moves

# evaluates board state
# University of Washington.
# https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf 

strategy = [
    [20, -3, 11,  8,  8, 11, -3, 20],
    [-3, -7, -4,  1,  1, -4, -7, -3],
    [11, -4,  2,  2,  2,  2, -4, 11],
    [8,   1,  2, -3, -3,  2,  1,  8],
    [8,   1,  2, -3, -3,  2,  1,  8],
    [11, -4,  2,  2,  2,  2, -4, 11],
    [-3, -7, -4,  1,  1, -4, -7, -3],
    [20, -3, 11,  8,  8, 11, -3, 20]
]
def heuristic_board_eval(board,player):
    if player == 1:
        opponent = 2
    else: 
        opponent = 1
    my_tiles=0
    opp_tiles=0
    k=0
    my_front_tiles=0
    opp_front_tiles=0
    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0

    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

    #piece diff
    for i in range(8):
        for j in range(8):
            if board[i][j]==player:
                my_tiles += 1
                d+=strategy[i][j]
            elif board[i][j]==opponent:
                opp_tiles += 1
                d+=strategy[i][j]
            if board[i][j]!=0:
                for k in range(8):
                    x = i+X1[k]
                    y = j+Y1[k]
                    if x>=0 and x<8 and y>=0 and y<8 and board[x][y]==0:
                        if board[i][j]==player:
                            my_front_tiles += 1
                        else:
                            opp_front_tiles +=1
    if my_tiles>opp_tiles:
        p = (100*my_tiles)/(my_tiles+opp_tiles)
    elif my_tiles<opp_tiles:
        p = -(100*opp_tiles)/(my_tiles+opp_tiles)
    else:
        p = 0
    
    if my_front_tiles > opp_front_tiles:
        f = -(100*my_front_tiles)/(my_front_tiles+opp_front_tiles)
    elif my_front_tiles < opp_front_tiles:
        f = (100*opp_front_tiles)/(my_front_tiles+opp_front_tiles)
    else:
        f = 0

    #corner control
    my_tiles=opp_tiles=0
    if board[0][0]==player:
        my_tiles+=1
    elif board[0][0]:
        opp_tiles+=1
    if board[0][7]==player:
        my_tiles+=1
    elif board[0][7]:
        opp_tiles+=1
    if board[7][0]==player:
        my_tiles+=1
    elif board[7][0]:
        opp_tiles+=1
    if board[7][7]==player:
        my_tiles+=1
    elif board[7][7]:
        opp_tiles+=1
    c=25*(my_tiles-opp_tiles)

    #corner closeness
    my_tiles=opp_tiles=0
    if board[0][0]==0:
        if board[0][1] == player:
            my_tiles+=1
        elif board[0][1] == opponent:
            opp_tiles+=1
        if board[1][1] == player:
            my_tiles+=1
        elif board[1][1] == opponent:
            opp_tiles+=1
        if board[1][0] == player:
            my_tiles+=1
        elif board[1][0] == opponent:
            opp_tiles+=1
    if board[0][7]==0:
        if board[0][6] == player:
            my_tiles+=1
        elif board[0][6] == opponent:
            opp_tiles+=1
        if board[1][6] == player:
            my_tiles+=1
        elif board[1][6] == opponent:
            opp_tiles+=1
        if board[1][7] == player:
            my_tiles+=1
        elif board[1][7] == opponent:
            opp_tiles+=1
    if board[7][0]==0:
        if board[7][1] == player:
            my_tiles+=1
        elif board[7][1] == opponent:
            opp_tiles+=1
        if board[6][1] == player:
            my_tiles+=1
        elif board[6][1] == opponent:
            opp_tiles+=1
        if board[6][0] == player:
            my_tiles+=1
        elif board[6][0] == opponent:
            opp_tiles+=1
    if board[7][7]==0:
        if board[6][7] == player:
            my_tiles+=1
        elif board[6][7] == opponent:
            opp_tiles+=1
        if board[6][6] == player:
            my_tiles+=1
        elif board[6][6] == opponent:
            opp_tiles+=1
        if board[7][6] == player:
            my_tiles+=1
        elif board[7][6] == opponent:
            opp_tiles+=1
    l=-12.5*(my_tiles-opp_tiles)

    #mobility
    my_tiles=len(get_legal_moves(board,player))
    opp_tiles=len(get_legal_moves(board,opponent))
    if my_tiles > opp_tiles:
        m = (100*my_tiles)/(my_tiles+opp_tiles)
    elif my_tiles<opp_tiles:
        m = -(100*opp_tiles)/(my_tiles+opp_tiles)
    else:
        m = 0

    #final score
    score = (10*p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    return score