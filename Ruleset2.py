import Engine
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
    def long_piece_pathing(self,directions,n):
        #Finds all valid moves for pieces that can move in multiple directions
        n = 0
        can_move_in_direction = []
        for direction in directions:
            can_move_in_direction.append(True)
        while True in can_move_in_direction:
            for direction in directions:
                i
            
            
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
        
a = Rules([2,3],Engine.m_init_state)
print(a.VizierMoves()  )           
