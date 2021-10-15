import Engine
import numpy as np
import time
import copy
rows = 10
columns = 13
class Rules():
    def __init__(self,location,gamestate):
        self.location = location
        self.gamestate = gamestate

    def transform_piece(self,transforms):
        #Applies each given move to a piece to find where it's moved to
        possible_moves = []
        for transform in transforms:
            possible_moves.append( (self.location[0] + transform[0], self.location[1] + transform[1]) )
        return possible_moves
        
    def check_bounds(self,moves):
        #Makes sure the piece isn't moving anywhere it can't
        valid_moves = []
        color = Rules.find_piece_color(self,location=self.location)
        for move in moves:
            if move[0] >= 0 and move[0] < rows and move[1] >= 0 and move[1] < columns:
                #If the move is within the 10 rows and 13 columns
                if self.gamestate[move[0]][move[1]] != "N/A":
                    #If the move isn't to an absent tile
                    valid_moves.append(move)
        for move in valid_moves:
            #Check if the piece is moving onto an immune pawn of pawn
            if move[0] in [0,9]:
                if self.gamestate[move[0]][move[1]] in ["pwP","pbP"]:
                    valid_moves.remove(move)
        if self.gamestate[ self.location[0] ][ self.location[1] ][1] not in ["K","A"]:
            #Check if the correct piece is entering a citadel
            if (1,0) in valid_moves:
                valid_moves.remove( (1,0) )
            elif (8,12) in valid_moves:
                valid_moves.remove( (8,12) )
        else:
            #Handles entering citadels for royal pieces
            if color == "w":
               if self.gamestate[ self.location[0] ][ self.location[1] ][1] == "A":
                   if (1,0) in valid_moves:
                       valid_moves.remove( (1,0) )
               else: 
                   if (8,12) in valid_moves:
                       valid_moves.remove( (8,12) )
                   if self.gamestate[1][0] == "bA":
                       if (1,0) in valid_moves:
                           valid_moves.remove( (1,0) )
            else:
               if self.gamestate[ self.location[0] ][ self.location[1] ][1] == "A":
                   if (8,12) in valid_moves:
                       valid_moves.remove( (8,12) )
               else: 
                   if (1,0) in valid_moves:
                       valid_moves.remove( (1,0) )
                   if self.gamestate[8][12] == "bA":
                       if (8,12) in valid_moves:
                           valid_moves.remove( (8,12) )
        return valid_moves

    def find_piece_color(self,location):
        #Finds the color of a piece
        if self.gamestate[ location[0] ][ location[1] ][0] == "p":
            return self.gamestate[ location[0] ][ location[1] ][1]
        else:
            return self.gamestate[ location[0] ][ location[1] ][0]
            
    def piece_capturing(self, moves):
        #Checks whether a piece is moving into a tile with a piece of the same colour on it
        valid_moves = []
        piece_color = Rules.find_piece_color(self,self.location)
        for move in moves:
            if piece_color != Rules.find_piece_color(self,move):
                valid_moves.append(move)
        return valid_moves
    def long_piece_pathing(self,directions):
        #Finds all valid moves for pieces that can move in multiple directions
        n = 1
        possible_moves = []
        can_move_in_direction = []
        for direction in directions:
            can_move_in_direction.append(True)
        while True in can_move_in_direction:
            for direction in directions:
                if can_move_in_direction[directions.index(direction)]:
                    #First find the value of the transform
                    transform = n * np.array(direction)    
                    transform = transform.tolist()
                    move = Rules.return_valid_moves(self,[transform])
                    if len(move) != 0:
                        possible_moves.append(move[0])
                        move = list(move[0])
                        if self.gamestate[move[0]][move[1]] != '-':
                            can_move_in_direction[directions.index(direction)] = False
                    else:
                        can_move_in_direction[directions.index(direction)] = False
            n += 1
            
        return possible_moves
    def return_valid_moves(self,transforms):
        #Both retrieves all valid moves and checks if they are valid
        return Rules.piece_capturing (self, Rules.check_bounds(self, Rules.transform_piece(self, transforms) ) )

    def VizierMoves(self):
        #Vizier can only move 1 space orthogonally(up,down,left,right)
        valid_moves = Rules.return_valid_moves( self, [[0,1], [1,0] ,[-1,0], [0,-1]] )
        return valid_moves
    
    def MinisterMoves(self):
        #Minister can move one space diagonally
        valid_moves = Rules.return_valid_moves( self, [[1,1], [1,-1] ,[-1,1], [-1,-1]] )
        return valid_moves
        
    def PawnMoves(self):
        #Pawns move like pawns in Chess
        #Once they reach the end of the board, they are promoted to their respective pieces
        if Rules.find_piece_color(self,location=self.location) == "w":
            valid_moves = Rules.transform_piece( self,[[-1,0] , [-1,-1] , [-1,1]] )
        else:
            valid_moves = Rules.transform_piece( self, [[1,0] , [1,1] , [1,-1]] )
        valid_moves = Rules.check_bounds(self,valid_moves)
        valid_moves2 = tuple(valid_moves)
        for move in valid_moves2:
            #Check if each move is valid
            if move[1] == self.location[1]:
                if self.gamestate[ move[0] ][ move[1] ] != "-":
                    valid_moves.remove(move)
            elif self.gamestate[ move[0] ][ move[1] ] == "-":
                valid_moves.remove(move)
        return Rules.piece_capturing(self,valid_moves)
                
    def RookMoves(self):
        #Rooks move just like rooks in Chess, they can move to any square on the same rank or file as them
        return Rules.long_piece_pathing(self,[[0,1],[0,-1],[1,0],[-1,0]])

    def ScoutMoves(self):
        #Scouts move like bishops in regular Chess but it always skips the first square
        available_moves = Rules.long_piece_pathing(self,[[1,1],[1,-1],[-1,1],[-1,-1]])
        exclude_moves = tuple(Rules.transform_piece( self, [[1,1], [1,-1] ,[-1,1], [-1,-1]] ))
        if len(available_moves) != 0:
            for move in exclude_moves:
                if move in available_moves:
                    available_moves.remove(move)
        return available_moves
    def ElephantMoves(self):
        #Elephant can jump 2 spaces diagonally
        return Rules.return_valid_moves( self, [[2,2], [2,-2] ,[-2,2], [-2,-2]] )

    def DabbabaMoves(self):
        #Dabbaba can jump 2 spaces orthogonally
        return Rules.return_valid_moves( self, [[0,2], [2,0] ,[-2,0], [0,-2]] )

    def HorseMoves(self):
        #Horses moves like the Knights in chess, moves in an L shape
        return Rules.return_valid_moves( self, [[2,1],[2,-1],[-2,-1],[-2,1],[1,2],[1,-2],[-1,2],[-1,-2]])

    def CamelMoves(self):
        #Camels move like horses, but one step further in all orthogonal directions
        return Rules.return_valid_moves( self, [[3,1],[3,-1],[-3,-1],[-3,1],[1,3],[1,-3],[-1,3],[-1,-3]])

    def GiraffeMoves(self):
        #Giraffes first move one step diagonally, then three or more spaces orthagonally
        diag_transforms = [[1,1], [1,-1] ,[-1,1], [-1,-1]]
        can_move_in_direction = []
        diag_moves = Rules.return_valid_moves( self, diag_transforms )
        diag_transforms = []
        n = 1
        valid_moves = []
        can_move = False
        #First check where it can move from after moving one step diagonally
        for move in diag_moves:
            can_move_in_direction.append([True,True])
            diag_transforms.append( [move[0] - self.location[0], move[1] - self.location[1] ] )
        for direction in can_move_in_direction:
            for x in direction:
                if x:
                    can_move = True
        while can_move:
            for move in diag_moves:
                for x in range(0,2):
                    if x == 0:
                        curr_move = [move[0] + diag_transforms[diag_moves.index(move)][x]*n, move[1] ]
                    else:
                        curr_move = [move[0], move[1]  + diag_transforms[diag_moves.index(move)][x]*n ]
                    if can_move_in_direction[diag_moves.index(move)][x] == True:
                        curr_move = Rules.piece_capturing (self, Rules.check_bounds(self, [curr_move]))
                        if len(curr_move) != 0:
                            if n >= 3:
                                valid_moves.append(tuple(curr_move[0]))
                            lmove = list(curr_move[0])
                            if self.gamestate[lmove[0]][lmove[1]] != '-':
                                can_move_in_direction[diag_moves.index(move)][x] = False
                        else:
                            can_move_in_direction[diag_moves.index(move)][x] = False
            can_move = False
            for direction in can_move_in_direction:
                for x in direction:
                    if x:
                        can_move = True
            n += 1
        valid_moves_copy = copy.deepcopy(valid_moves)
        for move in valid_moves_copy:
            if move ==  (1,0) or move == (8,12):
                valid_moves.remove(move)
        return valid_moves

    def PrinceMoves(self):
        #Prince moves like a king but cannot enter the opponent's citadel
        valid_moves =  Rules.return_valid_moves( self, [[0,1], [1,0] ,[-1,0], [0,-1],[1,1], [1,-1] ,[-1,1], [-1,-1]] )
        return valid_moves
    def AdventiceMoves(self):
        #An adventice king moves like a prince but can enter it's own citadel
        valid_moves =  Rules.return_valid_moves( self, [[0,1], [1,0] ,[-1,0], [0,-1],[1,1], [1,-1] ,[-1,1], [-1,-1]] )
        return valid_moves
    def PawnOfPawnsRules(self):
        #The pawn of pawns acts as a regular pawn until it moves to the final square, where it remains until a situation develops
        #where it guarantee a capture on any piece on the board, then it may be moved there.
        #When it reaches the end of the board a second time, it is moved to the square it started from
        #The third time it reaches the end of the board, it becomes a prince

        #First move it like a regular pawn
        end_row = 0 if Rules.find_piece_color(self,self.location) == "w" else 9
        if self.location[0] != end_row:
            if Rules.find_piece_color(self,location=self.location) == "w":
                valid_moves = Rules.transform_piece( self,[[-1,0] , [-1,-1] , [-1,1]] )
            else:
                valid_moves = Rules.transform_piece( self, [[1,0] , [1,1] , [1,-1]] )
            valid_moves = Rules.check_bounds(self,valid_moves) 
            valid_moves2 = tuple(valid_moves)
            for move in valid_moves2:
                #Check if each move is valid
                if move[1] == self.location[1]:
                    if self.gamestate[ move[0] ][ move[1] ] != "-":
                        valid_moves.remove(move)
                elif self.gamestate[ move[0] ][ move[1] ] == "-":
                    valid_moves.remove(move)
            return Rules.piece_capturing(self,valid_moves)
        #If the piece is at the end already, assume it has only reached the end the first time
        #and see if the piece can be moved to a place where it can guarantee a capture
        else:
            #First get a list of pieces on the board that cannot move
            immobile_pieces = Rules.immobile_pieces(self)
            valid_moves = []
            valid_moves2 = []
            #Then find the pawn's color and where it can move to capture a piece
            if Rules.find_piece_color(self,self.location) == "w":
                capture_dir = ([-1,-1],[-1,1])
            else:
                capture_dir = [[1,-1],[1,1]]
            for piece in immobile_pieces:
                for item in capture_dir:
                    #Check whether each piece can be captured by creating a copy of the board and playing out the pawn's moves on that
                    gs = copy.deepcopy(self.gamestate)
                    if len(Rules.check_bounds(self, [[piece[0] - item[0],piece[1] - item[0] ]])) != 0:
                        if gs[piece[0] - item[0] ][piece[1] - item[1] ] not in ["-","N/A","bK","wK"]:
                            #If the pawn isn't being moved out of the board, simulate moving it there
                            gs[piece[0] - item[0] ][piece[1] - item[1] ] = self.gamestate[self.location[0]][self.location[1]]
                            ChessPiece = Rules([piece[0] , piece[1]], gs)
                            if len(ChessPiece.map_piece_to_rule()) == 0:
                                valid_moves.append([piece[0] - item[0] , piece[1] - item[1] ])

            #Find all the squares from where the pawn can attack two pieces
            for x in range(rows):
                for y in range(columns):
                    #Check if that space is occupied by a king or not part of the board
                    if self.gamestate[x][y] not in ["N/A","bK","wK"]:
                        gs = copy.deepcopy(self.gamestate)
                        gs[x][y] = self.gamestate[self.location[0]][self.location[1]]
                        NewPawnLoc = Rules([x,y],gs)
                        potential_moves = NewPawnLoc.PawnMoves()
                        if len(potential_moves) >= 2:
                            #If the number of moves the pawn can make is above 2, find whether the number of pieces it can capture is 2
                            potential_move_copy = copy.deepcopy(potential_moves)
                            for move in potential_moves:
                                if gs[move[0]][move[1]] == "-":
                                    potential_move_copy.remove(move)
                            if len(potential_move_copy) == 2:
                                valid_moves.append([x,y])
                                
                            
                                
            for move in valid_moves:
                if move not in valid_moves2:
                    valid_moves2.append(move)
            return valid_moves
            
    def immobile_pieces(self):
        #Find a list of pieces that cannot be moved
        color = Rules.find_piece_color(self,self.location)
        immobiles = []
        for x in range(rows):
            for y in range(columns):
                if self.gamestate[x][y] not in ["pwP","pbP","-","N/A"]:
                    if self.gamestate[x][y][1] != "K" and Rules.find_piece_color(self,[x,y]) != color: 
                        piece = Rules([x,y], self.gamestate)
                        moves = piece.map_piece_to_rule()
                        if len(moves) == 0:
                            immobiles.append([x,y])
        return immobiles
    
        
    def KingMoves(self):
        #Moves like a King in chess
        valid_moves = Rules.return_valid_moves( self, [[0,1], [1,0] ,[-1,0], [0,-1],[1,1], [1,-1] ,[-1,1], [-1,-1]] )
        if self.gamestate[self.location[0]][self.location[1]] in Engine.current_rulers:
            color = Rules.find_piece_color(self,location=self.location)
            colorint = 0 if color == "w" else 1
            if Rules.is_ruler_check(self.gamestate,Engine.current_rulers[colorint]):
                #Check if the piece can be swapped with one of it's own pieces
                if not(Engine.king_swapped[colorint]):
                    for x in range(rows):
                        for y in range(columns):
                            if self.gamestate[x][y] not in ["-","N/A","wK","bK","wA","wP"] and color == Rules.find_piece_color(self,[x,y]):
                                if (x,y) not in valid_moves:
                                    valid_moves.append((x,y))
        return valid_moves
    
    def check_if_pofp_canmove(board,player):
    #Check if the pawn of pawns is at the end of the board and if it can capture a piece
        piece_location = []
        if player:
            if "pwP" in board[0]:
                piece_location = board[0].index("pwP")
                PawnOfPawns = Rules([0,piece_location],board)
                if len(PawnOfPawns.PawnOfPawnsRules()) != 0:
                    return True
        else:
            if "pbP" in board[0]:
                piece_location = board[9].index("pbP")
                PawnOfPawns = Rules([9,piece_location],board)
                if len(PawnOfPawns.PawnOfPawnsRules()) != 0:
                    return True    
        return False              
                    
    def is_ruler_threatened(self,move,ruler):
        #Check if the player's ruler is being threatened currently
        piece = self.gamestate[self.location[0]][self.location[1]]
        gs = copy.deepcopy(self.gamestate)
        gs[self.location[0]][self.location[1]] = "-"
        ruler_found = False
        gs[move[0]][move[1]] = piece
        for x in range(rows):
            if ruler in gs[x]:
                xloc = x
                yloc = gs[x].index(ruler)
                ruler_found = True
        if ruler_found == False:
            return ruler_found
        for x in range(rows):
            for y in range(columns):
                if gs[x][y] not in ["-","N/A"]:
                    rule_check = Rules([x,y],gs)
                    available_moves = rule_check.map_piece_to_rule()
                    if (xloc,yloc) in available_moves:
                        return True
                    

    def check_ruler_vulnerable(self,moves,ruler):
        #Checks which moves make the ruler vulnerable
        moves_copy = copy.deepcopy(moves)
        for move in moves:
            if Rules.is_ruler_threatened(self,move,ruler):
                moves_copy.remove(move)
        return moves_copy

    def is_ruler_check(gs,ruler):
        #Check if the ruler is under check
        for x in range(rows):
            if ruler in gs[x]:
                xloc = x
                yloc = gs[x].index(ruler)
        for x in range(rows):
            for y in range(columns):
                if gs[x][y] not in ["-","N/A",Engine.current_rulers[0],Engine.current_rulers[1] ]:
                    rule_check = Rules([x,y],gs)
                    available_moves = rule_check.map_piece_to_rule()
                    if (xloc,yloc) in available_moves:
                        return True
                    
    def is_ruler_mated(gs,ruler):
        #Check if a player has been checkmated or stalemated
        for x in range(rows):
            for y in range(columns):
                if gs[x][y] not in ["-","N/A"]:
                    rule_check = Rules([x,y],gs)
                    moves = rule_check.map_piece_to_rule()
                    moves = rule_check.check_ruler_vulnerable(moves,ruler)
                    if len(moves) != 0:
                        return False
        return True
    
    def find_current_ruler(gs):
        #Check if there are multiple royal pieces on the board of a certain color
        ns = [0,1]
        colors = ["w","b"]
        royals = ["A","P","K"]
        two_royals = [False,False]
        for n in ns:
            for x in range(rows):
                for royal in royals:
                    if colors[n] + royal in gs[x] and not(two_royals[n]):
                        if Engine.current_rulers[n] == "-":
                            Engine.current_rulers[n] = colors[n] + royal
                        else:
                            if colors[n] + royal != Engine.current_rulers[n]:
                                Engine.current_rulers[n] = "-"
                                two_royals[n] = True
        
    def citadel_check(gs):
        #Checks whether a king has entered a citadel
        if gs[1][0] == "wK":
            Engine.game_drawn = True
        elif gs[8][12] == "bK":
            Engine.game_drawn = True
            
    def map_piece_to_rule(self):
        #Checks the piece to see what rule applies to it
        piece_identity = self.gamestate[ self.location[0] ][ self.location[1] ]
        if piece_identity[0] == "p":
            if piece_identity[2] == "P":
                return Rules.PawnOfPawnsRules(self)
            else:
                return Rules.PawnMoves(self)
        else:
            piece_identity = piece_identity[1]
            if piece_identity == "C":
                return Rules.CamelMoves(self)
            elif piece_identity == "D":
                return Rules.DabbabaMoves(self)
            elif piece_identity == "E":
                return Rules.ElephantMoves(self)
            elif piece_identity == "R":
                return Rules.RookMoves(self)
            elif piece_identity == "N":
                return Rules.HorseMoves(self)
            elif piece_identity == "S":
                return Rules.ScoutMoves(self)
            elif piece_identity == "G":
                return Rules.GiraffeMoves(self)
            elif piece_identity == "V":
                return Rules.VizierMoves(self)
            elif piece_identity == "K":
                return Rules.KingMoves(self)
            elif piece_identity == "P":
                return Rules.PrinceMoves(self)
            elif piece_identity == "A":
                return Rules.AdventiceMoves(self)
            else:
                return Rules.MinisterMoves(self)
         

