import Ruleset
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
f_init_state = []#To be implemented
game_log = []
is_player_white = True
#Variables to store how many times the white and black Pawn of Pawns have reached the end of the board
b_pofp_ended = 0
w_pofp_ended = 0
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
    new_board[move.start_row][move.start_col] = "-"
    new_board[move.end_row][move.end_col] = move.piece_moved
    return new_board

def who_is_moving(board,move):
    #Returns True if a white piece is being moved, else returns False
    piece = board[move.start_row][move.start_col]
    if piece[0] == "p":
        piece = piece[1]
    else:
        piece = piece[0]

    if piece == "w":
        return True
    if piece == "b":
        return False

def promote_pieces(board):
    #Promotes all pieces at the end of the turn
    for x in [0,9]:
        for y in range( len(board[x]) ):
            if board[x][y][0] == "p":
                if board[x][y][2] == "K":
                    board[x][y] = board[x][y][1] + "P"
                elif board[x][y][2] == "P":
                    pass
                else:
                    board[x][y] = board[x][y][1:]
