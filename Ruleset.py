import Engine
rows = 10
columns = 13
class Rules():
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
        return Rules.transform_check(self.location, possible_transforms)

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
        return Rules.transform_check(self.location, possible_transforms)
    
    def PawnMoves(self):
        #Pawns move like pawns in Chess
        #Once they reach the end of the board, they are promoted to their respective pieces
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        pawn_color = self.gamestate[x][y][1]
        if pawn_color == "w":
            #Check if the pawn is white
            if self.gamestate[x-1][y] == "-":
                #Check if the space in front of the piece is empty
                possible_transforms.append( (-1,0) )
            if x != 0 and y != 0 and self.gamestate[x-1][y-1] != "N/A" and self.gamestate[x-1][y-1] != "-":
                #Check if the piece can be moved to the top-left
                possible_transforms.append( (-1,-1) )
            if x != 0 and y != 12 and self.gamestate[x-1][y+1] != "N/A" and self.gamestate[x-1][y+1] != "-":
                #Check if the piece can be moved to the top-right
                possible_transforms.append( (-1,1) )
        elif pawn_color == "b":
            #Check if the pawn is black
            if self.gamestate[x+1][y] == "-":
                #Check if the space in front of the piece is empty
                possible_transforms.append( (1,0) )
            if x != 0 and y != 0 and self.gamestate[x+1][y-1] != "N/A" and self.gamestate[x+1][y-1] != "-":
                #Check if the piece can be moved to the bottom-left
                possible_transforms.append( (1,-1) )
            if x != 0 and y != 12 and self.gamestate[x+1][y+1] != "N/A" and self.gamestate[x+1][y+1] != "-":
                #Check if the piece can be moved to the bottom-right
                possible_transforms.append( (1,1) )
        return Rules.transform_check(self.location, possible_transforms)
    
    def RookMoves(self):
        #Rooks move just like rooks in Chess, they can move to any square on the same rank or file as them
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        n = 1
        move_directions = [True,True,True,True]
        while True in move_directions:
            if not(x - n < 0):
                if move_directions[0] == True:
                    #Check if the rook can be moved up
                    if self.gamestate[x-n][y] != "N/A":
                        possible_transforms.append ( (-n , 0 ) )
                        if self.gamestate[x-n][y] != "-":
                            move_directions[0] = False
                    
            else:
                move_directions[0] = False

            if not(x + n > 9):
                if move_directions[1] == True:
                    #Check if the rook can be moved down
                    if self.gamestate[x+n][y] != "N/A":
                        possible_transforms.append ( (n , 0 ) )
                        if self.gamestate[x+n][y] != "-":
                            move_directions[1] = False
                    
            else:
                move_directions[1] = False

            if not(y - n < 0):    
                if move_directions[2] == True:
                    #Check if the rook can be moved left
                    if self.gamestate[x][y-n] != "N/A":
                        possible_transforms.append ( (0 , -n ) )
                        if self.gamestate[x][y-n] != "-":
                            move_directions[2] = False
                    
            else:
                move_directions[2] = False

            if not(y + n > 12):
                if move_directions[3] == True:
                    #Check if the rook can be moved right
                    if self.gamestate[x][y+n] != "N/A":
                        possible_transforms.append ( (0 , n ) )
                        if self.gamestate[x][y+n] != "-":
                            move_directions[3] = False
                    
            else:
                move_directions[3] = False
                
            n += 1
        return Rules.transform_check(self.location, possible_transforms)

    def ScoutMoves(self):
        #Scouts move like bishops in regular Chess but it always skips the first square
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        n = 2
        move_directions = [True,True,True,True]
        while True in move_directions:
            if not(x - n < 0) and not(y - n < 0) :
            #Check if the scout can be moved up-leftwards
                if move_directions[0] == True:
                    if self.gamestate[x - n][y - n] != "N/A":
                        possible_transforms.append ( (-n , -n ) )
                        if self.gamestate[x - n][y - n] != "-":
                            move_directions[0] = False
            else:
                move_directions[0] = False

            if not(x - n < 0) and not(y + n > 12) :
            #Check if the scout can be moved up-rightwards
                if move_directions[1] == True:
                    if self.gamestate[x - n][y + n] != "N/A":
                        possible_transforms.append ( (-n , n) )
                        if self.gamestate[x - n][y + n] != "-":
                            move_directions[1] = False
            else:
                move_directions[1] = False
                
            if not(x + n > 9) and not(y - n < 0) :
            #Check if the scout can be moved down-leftwards
                if move_directions[2] == True:
                    if self.gamestate[x + n][y - n] != "N/A":
                        possible_transforms.append ( (n , -n ) )
                        if self.gamestate[x + n][y - n] != "-":
                            move_directions[2] = False
            else:
                move_directions[2] = False
                
            if not(x + n > 9) and not(y + n > 12) :
            #Check if the scout can be moved down-rightwards
                if move_directions[3] == True:
                    if self.gamestate[x + n][y + n] != "N/A":
                        possible_transforms.append ( (n , n) )
                        if self.gamestate[x + n][y + n] != "-":
                            move_directions[3] = False
            else:
                move_directions[3] = False

            n += 1
        return Rules.transform_check(self.location, possible_transforms)

    def DabbabaMoves(self):
        #Dabbaba can jump 2 spaces orthogonally
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        n = 2
        if x != 0 and self.gamestate[x - n][y ] != "N/A":
            #Check if the piece can be moved upwards
            possible_transforms.append( (-n , 0) )
        if x != 9 and self.gamestate[x + n][y ] != "N/A":
            #Check if the piece can be moved downwards
            possible_transforms.append( (n , 0) )
        if y != 0 and self.gamestate[x][y - n] != "N/A":
            #Check if the piece can be moved left
            possible_transforms.append( (0 , -n) )
        if y != 12 and self.gamestate[x ][y + n] != "N/A":
            #Check if the piece can be moved right
            possible_transforms.append( (0 , n) )
        return Rules.transform_check(self.location, possible_transforms)
    
    def ElephantMoves(self):
        #Elephant can jump 2 spaces diagonally
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        n = 2
        if x != 0 and y != 0 and self.gamestate[x-n][y-n] != "N/A":
            #Check if the piece can be moved to the top-left
            possible_transforms.append( (-n,-n) )
        if x != 0 and y != 12 and self.gamestate[x-n][y+n] != "N/A":
            #Check if the piece can be moved to the top-right
            possible_transforms.append( (-n,n) )
        if x != 9 and y != 12 and self.gamestate[x+n][y+n] != "N/A":
            #Check if the piece can be moved to the bottom-right
            possible_transforms.append( (n,n) )
        if x != 9 and y != 0 and self.gamestate[x+n][y-n] != "N/A":
            #Check if the piece can be moved to the bottom-left
            possible_transforms.append( (n,-n) )
        return Rules.transform_check(self.location, possible_transforms)

    def HorseMoves(self):
        #Horses moves like the Knights in chess, moves in an L shape
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        orth_n = 2
        diag_n = 1
        orth_transforms = [ [0 , orth_n] , [0 , -orth_n], [orth_n , 0] , [-orth_n , 0] ] #Storing the four orthagonal directions the horse can move in
        for x in range (0,4):
            zero_loc = orth_transforms[x].index( 0 )
            #Finding the two spots it can move to in each direction
            diag_transform =  [ orth_transforms[x] , orth_transforms[x] ]
            diag_transform[0][zero_loc] = 1
            diag_transform[0] = tuple(diag_transform[0])
            diag_transform[1][zero_loc] = -1
            diag_transform[1] = tuple(diag_transform[1])
            for transform in diag_transform:
                #Checking if the horse can be moved to the two spots
                if x + transform[0] >= 0 and x + transform[0] <= 9 and y + transform[1] >= 0 and y + transform[1] <= 12:
                    if self.gamestate[ x + transform[0] ][ y + transform[1] ] != "N/A":
                        possible_transforms.append( transform )
        return Rules.transform_check(self.location, possible_transforms)
    
    def CamelMoves(self):
        #Camels move like horses, but one step further in all orthogonal directions
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        orth_n = 3
        diag_n = 1
        orth_transforms = [ [0 , orth_n] , [0 , -orth_n], [orth_n , 0] , [-orth_n , 0] ] #Storing the four orthagonal directions the horse can move in
        for x in range (0,4):
            zero_loc = orth_transforms[x].index( 0 )
            #Finding the two spots it can move to in each direction
            diag_transform =  [ orth_transforms[x] , orth_transforms[x] ]
            diag_transform[0][zero_loc] = 1
            diag_transform[0] = tuple(diag_transform[0])
            diag_transform[1][zero_loc] = -1
            diag_transform[1] = tuple(diag_transform[1])
            for transform in diag_transform:
                #Checking if the horse can be moved to the two spots
                if x + transform[0] >= 0 and x + transform[0] <= 9 and y + transform[1] >= 0 and y + transform[1] <= 12:
                    if self.gamestate[x + transform[0] ][ y + transform[1] ] != "N/A":
                        possible_transforms.append( transform )
        return Rules.transform_check(self.location, possible_transforms)
    
    def GiraffeMoves(self):
        #Giraffes first move one step diagonally, then three or more spaces orthagonally
        #First check the diagonal transforms
        possible_transforms = []
        x,y = self.location[0],self.location[1]
        diag_transforms = []
        if x != 0 and y != 0 and self.gamestate[x-1][y-1] != "N/A":
            #Check if the piece can be moved to the top-left
            diag_transforms.append( (-1,-1) )
        if x != 0 and y != 12 and self.gamestate[x-1][y+1] != "N/A":
            #Check if the piece can be moved to the top-right
            diag_transforms.append( (-1,1) )
        if x != 9 and y != 12 and self.gamestate[x+1][y+1] != "N/A":
            #Check if the piece can be moved to the bottom-right
            diag_transforms.append( (1,1) )
        if x != 9 and y != 0 and self.gamestate[x+1][y-1] != "N/A":
            #Check if the piece can be moved to the bottom-left
            diag_transforms.append( (1,-1) )
    
        n = 2    
        for transform in diag_transforms:
            #First simulate movement along the column, starting downward
            new_transform = list(transform)
            can_move = True
            if transform[0] > 0:
                while can_move:
                    if new_transform[0] != 9:
                        new_transform = ( new_transform[0] + 1, new_transform[1])
                        if self.gamestate[x + transform[0] ][ y + transform[1] ] != "N/A":
                            if new_transform[0] >= 4:
                                possibe_transforms.append(new_transform)
                            if self.gamestate[x + transform[0] ][ y + transform[1] ] != "-":
                                can_move = False
                        else:
                            can_move = False
                    else:
                        can_move = False
            else:
                while can_move:
                    if new_transform[0] != 0:
                        new_transform = ( new_transform[0] - 1, new_transform[1])
                        if self.gamestate[x + transform[0] ][ y + transform[1] ] != "N/A":
                            if new_transform[0] <= -4:
                                possibe_transforms.append(new_transform)
                            if self.gamestate[x + transform[0] ][ y + transform[1] ] != "-":
                                can_move = False
                        else:
                            can_move = False
                    else:
                        can_move = False    
            #Next simulate movement along the row, starting rightward
            new_transform = list(transform)
            can_move = True
            if transform[1] > 0:
                while can_move:
                    if new_transform[1] != 12:
                        new_transform = ( new_transform[0] , new_transform[1] + 1)
                        if self.gamestate[x + transform[0] ][ y + transform[1] ] != "N/A":
                            if new_transform[1] >= 4:
                                possibe_transforms.append(new_transform)
                            if self.gamestate[x + transform[0] ][ y + transform[1] ] != "-":
                                can_move = False
                        else:
                            can_move = False
                    else:
                        can_move = False
            else:
                while can_move:
                    if new_transform[1] != 0:
                        new_transform = ( new_transform[0] , new_transform[1] - 1)
                        if self.gamestate[x + transform[0] ][ y + transform[1] ] != "N/A":
                            if new_transform[1] <= -4:
                                possibe_transforms.append(new_transform)
                            if self.gamestate[x + transform[0] ][ y + transform[1] ] != "-":
                                can_move = False
                        else:
                            can_move = False
                    else:
                        can_move = False
        return Rules.transform_check(self.location, possible_transforms)
    def PawnOfPawnsRules(self):
        #The pawn of pawns acts as a regular pawn until it moves to the final square, where it remains until a situation develops
        #where it guarantee a capture on any piece on the board, then it may be moved there.
        #When it reaches the end of the board a second time, it is moved to the square it started from
        #The third time it reaches the end of the board, it becomes a prince
        
        pass

    def PrinceMoves(self):
        #A prince acts like a King, but can be captured
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
        return Rules.transform_check(self.location, possible_transforms)
    
    def KingMoves(self):
        #Moves like a King in chess
        pass
    
    def transform_check(location, transforms):
        #Applies each given move to a piece to find where it's moved to
        possible_moves = []
        for transform in transforms:
            possible_moves.append( (location[0] + transform[0], location[1] + transform[1]) )
        return possible_moves

    def piece_capturing(self, moves):
        #Checks whether a piece is moving into a tile with a piece of the same colour on it
        new_moves = []
        if self.gamestate[ self.location[0] ][ self.location[1] ][0] == "p":
            color1 = self.gamestate[ self.location[0] ][ self.location[1] ][1]
        else:
            color1 = self.gamestate[ self.location[0] ][ self.location[1] ][0]
        for move in moves:
            if self.gamestate[ move[0] ][ move[1] ][0] == "p":
                color2 = self.gamestate[ move[0] ][ move[1] ][1]
            else:
                color2 = self.gamestate[ move[0] ][ move[1] ][0]
            if color1 != color2:
                new_moves.append(move)
        return new_moves

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

