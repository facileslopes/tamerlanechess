game_state = []
m_init_state = [
    ["N/A","bE", "-" , "bC", "-", "bD", "-", "bD", "-", "bC" ,"-" ,"bE","N/A"],
    ['-',"bR", "bN", "bS", "bG", "bV", "bK", "bM", "bG", "bS", "bN", "bR","N/A"],
    ["N/A","pbR", "pbN", "pbS", "pbG", "pbV", "pbK", "pbM", "pbE", "pbC", "pbD" ,"pbP","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","pwR", "pwN", "pwS", "pwG", "pwV", "pwK", "pwM", "pwE", "pwC", "pwD" ,"pwP","N/A"],
    ["N/A","wR", "wN", "wS", "wG", "wV", "wK", "wM", "wG", "wS", "wN", "wR",'-'],
    ["N/A","wE", "-" , "wC", "-", "wD", "-", "wD", "-", "wC" ,"-" ,"wE","N/A"]
    ]
f_init_state = [
    ["N/A","bE", "-" , "bC", "-", "bV", "bK", "bM", "-", "bC" ,"-" ,"bE","N/A"],
    ['-',"bR", "bN", "bS", "bG", "bD", "pbK", "bD", "bG", "bS", "bN", "bR","N/A"],
    ["N/A","pbR", "pbN", "pbS", "pbG", "pbV", "-", "pbM", "pbE", "pbC", "pbD" ,"pbP","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-","N/A"],
    ["N/A","pwR", "pwN", "pwS", "pwG", "pwV", "-", "pwM", "pwE", "pwC", "pwD" ,"pwP","N/A"],
    ["N/A","wR", "wN", "wS", "wG","wD", "pwK", "wD" , "wG", "wS", "wN", "wR",'-'],
    ["N/A","wE", "-" , "wC", "-", "wV", "wK", "wM", "-", "wC" ,"-" ,"wE","N/A"]
    ]
is_player_white = True
pofp_ended = [0,0]#A list to store how many times the white and black Pawn of Pawns have reached the end of the board
is_pofp_moveable = False
king_swapped = [False,False]
current_rulers = ["wK","bK"]
game_drawn = False
swap_made = [False,False]
player_colour = ""
ai_colour = ""
class Move():
    def __init__(self, start_sq,end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

def make_move(board,move):
    #Makes a move on the board
    new_board = board
    if board[move.start_row][move.start_col][1] == "K":
        #Check if it's a king being swapped
        king_color = board[move.start_row][move.start_col][0]
        if board[move.end_row][move.end_col][0] not in ["w","b","-"]:
            move_color = board[move.end_row][move.end_col][1]
        else:
            move_color = board[move.end_row][move.end_col][0]
            
        if move_color == king_color:
            new_board[move.start_row][move.start_col] = move.piece_captured
            new_board[move.end_row][move.end_col] = move.piece_moved
            n = 0 if move_color == "w" else 1
            king_swapped[n] = True
        else:
            new_board[move.start_row][move.start_col] = "-"
            new_board[move.end_row][move.end_col] = move.piece_moved
    else:        
        new_board[move.start_row][move.start_col] = "-"
        new_board[move.end_row][move.end_col] = move.piece_moved
    return new_board

def who_is_moving(board,location):
    #Returns True if a white piece is being moved, else returns False
    piece = board[location[0]][location[1]]
    if piece[0] == "p":
        piece = piece[1]
    else:
        piece = piece[0]

    if piece == "w":
        return True
    if piece == "b":
        return False
            
def promote_pieces(board,pofpended):
    #Promotes all pieces at the end of the turn
    pofp_ended = pofpended
    wpawn_moved = False
    bpawn_moved = False
    for x in [0,9]:
        for y in range( len(board[x]) ):
            if board[x][y][0] == "p":
                if board[x][y][2] == "K":
                    board[x][y] = board[x][y][1] + "P"
                elif board[x][y][2] == "P":
                    if board[x][y][1] == "w":
                        wpawn_moved = True
                        if pofp_ended[0] == 0:
                            pofp_ended[0] += 1
                        elif pofp_ended[0] == 2:
                            board[x][y] = "-"
                            board[7][6] = "pwP"
                            pofp_ended[0] += 1
                        elif pofp_ended[0] == 3:
                            board[x][y] = "wA"
                    else:
                        bpawn_moved = True
                        if pofp_ended[1] == 0:
                            pofp_ended[1] += 1
                        elif pofp_ended[1] == 2:
                            board[x][y] = "-"
                            board[2][6] = "pbP"
                            pofp_ended[1] += 1
                        elif pofp_ended[1] == 3:
                            board[x][y] = "bA"
                
                else:
                    board[x][y] = board[x][y][1:]
    if not(wpawn_moved) and pofp_ended[0] == 1:
        pofp_ended[0] += 1
    if not(bpawn_moved) and pofp_ended[1] == 1:
        pofp_ended[1] += 1
    return pofp_ended
