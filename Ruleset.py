import Engine
rows = 10
columns = 13
class Moves():
    def __init__(self,location,gamestate):
        self.location = location
        self.gamestate = gamestate
        
    
    def VizierMoves(self):
        #Vizier can only move 1 space orthogonally(up,down,left,right)
        possible_transforms = []
        x = self.location[0]
        y = self.location[1]
        if x != 0 and self.gamestate[x - 1][y ] != "N/A":
            #Check if the piece can be moved upwards
            possible_transforms.append( (-1 , 0) )
        if x != 9 and self.gamestate[x + 1][y ] != "N/A":
            #Check if the piece can be moved downwards
            possible_transforms.append( (1 , 0) )
        if y != 0 and self.gamestate[x][y - 1] != "N/A":
            #Check if the piece can be moved left
            possible_transforms.append( (0 , -1) )
        if y != 12 and self.gamestate[x ][y + 1] != "N/A":
            #Check if the piece can be moved right
            possible_transforms.append( (0 , 1) )
        return Moves.transform_check(self.location, possible_transforms)

    def MinisterMoves(self):
        #Minister can move one space diagonally
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        if x != 0 and y != 0 and self.gamestate[x-1][y-1] != "N/A":
            #Check if the piece can be moved to the top-left
            possible_transforms.append( (-1,-1) )
        if x != 0 and y != 12 and self.gamestate[x-1][y+1] != "N/A":
            #Check if the piece can be moved to the top-right
            possible_transforms.append( (-1,1) )
        if x != 9 and y != 12 and self.gamestate[x+1][y+1] != "N/A":
            #Check if the piece can be moved to the bottom-right
            possible_transforms.append( (1,1) )
        if x != 9 and y != 0 and self.gamestate[x+1][y-1] != "N/A":
            #Check if the piece can be moved to the bottom-left
            possible_transforms.append( (1,-1) )
        return Moves.transform_check(self.location, possible_transforms)
    
    def PawnMoves(self):
        #Pawns can only move one step at a time, and can only capture pieces to the top-right and top-left of them.
        #Once they reach the end of the board, they are promoted to their respective pieces
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        pawn_type = self.gamestate[x][y]
        if self.gamestate[x-1][y] == "-":
            #Check if the space in front of the piece is empty
            possible_transforms.append( ([x-1][y]) )
        if x != 0 and y != 0 and self.gamestate[x-1][y-1] != "N/A" and self.gamestate[x-1][y-1] != "-":
            #Check if the piece can be moved to the top-left
            possible_transforms.append( (-1,-1) )
        if x != 0 and y != 12 and self.gamestate[x-1][y-1] != "N/A" and self.gamestate[x-1][y-1] != "-":
            #Check if the piece can be moved to the top-right
            possible_transforms.append( (-1,1) )
        return Moves.transform_check(self.location, possible_transforms)
    def RookMoves(self):
        #Rooks move just like rooks in Chess, they can move to any square on the same rank or file as them
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        n = 1
        move_directions = [True,True,True,True]
        while True in move_directions:
            if move_directions[0] == True:
                #Check if the rook can be moved up
                if self.gamestate[x-n][y] != "N/A":
                    possible_transforms.append ( (-n , 0 ) )
                    if self.gamestate[x-n][y] != "-":
                        move_directions[0] = False

            if move_directions[1] == True:
                #Check if the rook can be moved down
                if self.gamestate[x+n][y] != "N/A":
                    possible_transforms.append ( (n , 0 ) )
                    if self.gamestate[x+n][y] != "-":
                        move_directions[1] = False
                        
            if move_directions[2] == True:
                #Check if the rook can be moved left
                if self.gamestate[x][y-n] != "N/A":
                    possible_transforms.append ( (0 , -n ) )
                    if self.gamestate[x][y-n] != "-":
                        move_directions[2] = False

            if move_directions[3] == True:
                #Check if the rook can be moved right
                if self.gamestate[x][y+n] != "N/A":
                    possible_transforms.append ( (0 , n ) )
                    if self.gamestate[x][y+n] != "-":
                        move_directions[3] = False
        return Moves.transform_check(self.location, possible_transforms)
    
    def transform_check(location, transforms):
        #Applies each given move to a piece to find where it's moved to 
        possible_moves = []
        for transform in transforms:
            possible_moves.append( (location[0] + transform[0], location[1] + transform[1]) )
        return possible_moves
