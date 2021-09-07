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

class Move():
    def __init__(self, start_sq,end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

def make_move(board,move):
    new_board = board
    new_board[move.start_row][move.start_col] = "-"
    new_board[move.end_row][move.end_col] = move.piece_moved
    return new_board
                      
