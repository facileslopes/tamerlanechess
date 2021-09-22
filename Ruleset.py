import Engine
import numpy as np
rows = 10
columns = 13
x = 2

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
        #Checks if the piece or where it's moving to is outside the board
        valid_moves = []
        for move in moves:
            if move[0] > 0 and move[0] < rows and move[1] > 0 and move[1] < columns:
                #If the move is within the 10 rows and 13 columns
                if self.gamestate[move[0]][move[1]] != "N/A":
                    #If the move isn't to an absent tile
                    valid_moves.append(move)
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
        return Rules.return_valid_moves( self, [[0,1], [1,0] ,[-1,0], [0,-1]] )

    def MinisterMoves(self):
        #Minister can move one space diagonally
        return Rules.return_valid_moves( self, [[1,1], [1,-1] ,[-1,1], [-1,-1]] )

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
            print(move)
            print(self.location)
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
        return valid_moves

    def PrinceMoves(self):
        #Prince moves like a king but can be captured
        return Rules.return_valid_moves( self, [[0,1], [1,0] ,[-1,0], [0,-1],[1,1], [1,-1] ,[-1,1], [-1,-1]] )

    def PawnOfPawnsRules(self):
        #The pawn of pawns acts as a regular pawn until it moves to the final square, where it remains until a situation develops
        #where it guarantee a capture on any piece on the board, then it may be moved there.
        #When it reaches the end of the board a second time, it is moved to the square it started from
        #The third time it reaches the end of the board, it becomes a prince
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

    def KingMoves(self):
        #Moves like a King in chess
        return []
    
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
            else:
                return Rules.MinisterMoves(self)
         

