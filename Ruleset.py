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
    
    def transform_check(location, transforms):
        possible_moves = []
        for transform in transforms:
            possible_moves.append( (location[0] + transform[0], location[1] + transform[1]) )
        return possible_moves
