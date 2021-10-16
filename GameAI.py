import Ruleset
import Engine
import random
from copy import deepcopy
import timeit
depth = 2
piece_values = {"R": 5.0,"N": 3.0, "S": 2.2, "C": 2.3, "G": 2.25 , "D": 1.45 , "V": 1.65 , "M": 1.5, "E": 1.15, "K": 2.1, "A": 2.05 , "P": 2.0 ,"p":1.0}
def find_ruler(gs,color):
    #Check if there are multiple royal pieces on the board
    n = 0 if color == "w" else 1
    current_ruler = ""
    royals = ["A","P","K"]
    location = None
    for x in range(Ruleset.rows):
        for royal in royals:
            if color + royal in gs[x]:
                if current_ruler == "":
                    current_ruler = color + royal
                    location = [x,gs[x].index(color+royal)]
                else:
                    current_ruler = "-"
                    location = None
                
    return current_ruler, location

def is_ruler_threatened(gs,ruler):
    #Checks if the ruler is being threatened
    enemy_color = "b" if ruler[0][0] == "w" else "w"
    enemy_ruler = find_ruler(gs,enemy_color)[0]
    for x in range(Ruleset.rows):
        for y in range(Ruleset.columns):
            if gs[x][y] not in ["-","N/A",ruler,enemy_ruler]:
                rule_check = Ruleset.Rules([x,y],gs)
                available_moves = rule_check.map_piece_to_rule()
                if tuple(ruler[1]) in available_moves:
                    return True
    return False
   
def get_available_moves(gamestate,color):
    available_moves = {}
    p_color = 0 if color == "w" else 1
    current_ruler = find_ruler(gamestate,color)
    #Gets a list of available moves that can be made by a certain player
    for x in range(Ruleset.rows):
        for y in range(Ruleset.columns):
            if gamestate[x][y] not in ["-","N/A"]:
                if color in gamestate[x][y]:
                    piece = Ruleset.Rules( [x,y], gamestate )
                    moves = piece.map_piece_to_rule()
                    moves_copy = deepcopy(moves)
                    if current_ruler[0] != "-":
                        #If there is a ruler,check whether each move puts it in danger
                        for move in moves:
                            gs_copy = deepcopy(gamestate)
                            gs_move = Engine.Move([x,y],list(move),gs_copy)
                            gs_copy = Engine.make_move(gs_copy,gs_move)
                            if is_ruler_threatened(gs_copy,current_ruler):
                                moves_copy.remove(move)
                    if len(moves_copy) != 0:
                        available_moves[ str(x) + "|" + str(y) ] = moves_copy
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
                board_score += obtain_score_value(gamestate[x][y])
    return board_score

def game_over(gamestate,color):
    #Checks if the game is over
    if len( get_available_moves(gamestate,color) ) == 0:
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
    
def max_player(gamestate,curr_depth,best_min = 10000.0):
    #Finds the best move for the white player(The player trying to increase the score)

    #If game has concluded or depth reached, return the board score
    if game_over(gamestate,"w") != None:
        return (win_score(gamestate,"w"),None)
    elif curr_depth == 0:
        return (obtain_board_score(gamestate),None)
        
    score = -10000.0
    best_move = None

    global states_explored


    available_moves = get_available_moves(gamestate,"w")
    while len(available_moves) > 0:
        random_piece = random.choice( list(available_moves.keys()) )
        random_move = list( random.choice( available_moves[random_piece] ) )
        available_moves.pop(random_piece)

        if best_min <= score:
            break
        
        random_piece = list( map( int , random_piece.split("|") ) )
        move = Engine.Move( random_piece, random_move, gamestate )
        new_gamestate = Engine.make_move(deepcopy(gamestate),move)
        states_explored += 1
        
        min_player_result = min_player(deepcopy(new_gamestate),curr_depth - 1 , score)
        if min_player_result[0] > score:
            best_move = move
            score = min_player_result[0]
        
    return (score , best_move)

def min_player(gamestate,curr_depth,best_max = -10000.0):
    #Finds the best move for the black player(The player trying to reduce the score)
    
    #If game has concluded or depth reached, return the board score
    if game_over(gamestate,"b") != None:
        return (win_score(gamestate,"b"),None)
    elif curr_depth == 0:
        return (obtain_board_score(gamestate),None)
        
    score = 10000.0
    best_move = None

    global states_explored

    available_moves = get_available_moves(gamestate,"b")
    while len(available_moves) > 0:
        random_piece = random.choice( list(available_moves.keys()) )
        random_move = list( random.choice( available_moves[random_piece] ) )
        available_moves.pop(random_piece)

        if best_max >= score:
            break
        
        random_piece = list( map( int , random_piece.split("|") ) )
        move = Engine.Move( random_piece, random_move, gamestate )
        new_gamestate = Engine.make_move(deepcopy(gamestate),move)
        states_explored += 1
        
        max_player_result = max_player(deepcopy(new_gamestate),curr_depth - 1 , score)
        if max_player_result[0] < score:
            best_move = move
            score = max_player_result[0]
        
    return (score , best_move)

def ai_make_move(gamestate,color):
    #The AI makes a move using the given information
    global states_explored
    states_explored = 0
    start = timeit.default_timer()
    if color == "w":
        best_move = max_player(gamestate,depth)[1]
    else:
        best_move = min_player(gamestate,depth)[1]
    stop = timeit.default_timer()

    print('Time: ', stop - start)   
    return Engine.make_move( Engine.game_state, best_move )  
