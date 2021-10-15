import Ruleset
import Engine
import random
depth = 3
piece_values = {"R": 5.0,"N": 3.0, "S": 2.2, "C": 2.3, "G": 2.25 , "D": 1.45 , "V": 1.65 , "M": 1.5, "E": 1.15, "K": 2.1, "A": 2.05 , "P": 2.0 ,"p":1.0}
def get_available_moves(gamestate,color):
    available_moves = {}
    p_color = 0 if Engine.is_player_white else 1
    #Gets a list of available moves that can be made by a certain player
    for x in range(Ruleset.rows):
        for y in range(Ruleset.columns):
            if gamestate[x][y] not in ["-","N/A"]:
                if color in gamestate[x][y]:
                    piece = Ruleset.Rules( [x,y], gamestate )
                    if len(piece.check_ruler_vulnerable( piece.map_piece_to_rule(), Engine.current_rulers[p_color] ) ) != 0:
                        available_moves[ str(x) + "|" + str(y) ] = piece.check_ruler_vulnerable( piece.map_piece_to_rule(), Engine.current_rulers[p_color] )
    return available_moves

def obtain_score_value(piece):
    #Finds the score value for a certain piece
    piece_score = 0
    if piece[0] == "p":
        piece_score = piece_values["p"]
        if piece[1] == "w":
            return piece_score
        else:
            return -piece_score
    else:
        piece_score = piece_values[piece[1]]
        if piece[0] == "w":
            return piece_score
        else:
            return -piece_score
    
def obtain_board_score(gamestate):
    #Finds the current score value of the board
    board_score = 0.0#Score of the board, positive is in white's favour, negative is black's
    for x in range(Ruleset.rows):
        for y in range(Ruleset.columns):
            if gamestate[x][y] not in ["-", "N/A"]:
                board_score += obtain_score_value(gamesstate[x][y])
    return board_score

def game_over(gamestate,color):
    #Checks if the game is over
    if len( get_available_moves(Engine.game_state,color) ) == 0:
        return color
    else:
        if gamestate[1][0] == "wK":
            return "draw"
        elif gamestate[8][12] == "bK":
            return "draw"
        else:
            return None
    
def win_score(gamestate,color):
    #If a player wins, return the maximum/minimum score possible
    result = game_over(gamestate,color) 
    if result == "w":
        return 1000.0
    elif result == "b":
        return -1000.0
    elif result == "draw":
        return 0.0
    else:
        return None
    
def max_player(gamestate,best_min):
    #Finds the best move for the white player(The player trying to increase the score)
    return None

def min_player():
    #Finds the best move for the black player(The player trying to reduce the score)
    return None

def ai_make_move(gamestate,color):
    #The AI makes a move using the given information
    available_moves = get_available_moves(Engine.game_state,color)
    if len(available_moves) == 0:
        return None
    random_piece = random.choice( list(available_moves.keys()) )
    random_move = list( random.choice( available_moves[random_piece] ) )
    random_piece = list( map( int , random_piece.split("|") ) )
    move = Engine.Move( random_piece, random_move, gamestate )
    return Engine.make_move( Engine.game_state, move)
