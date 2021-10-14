#Run this file in order to play the game. This file is responsible for displaying a board for you to interact with.
import pygame
import Engine
import Ruleset
import GameAI
import time
import sys
#Initialising some variables and stuff here
max_fps = 15
sq_dim = 64
rows = 10
columns = 13
width = sq_dim * columns
height = sq_dim * rows
piece_sprites = {}
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tamerlane Chess")
sprites_loc = "/Users/donti/Desktop/Programming/Finished Projects/Tamerlane Chess/Sprites/"
light_col = (232,235,239)
dark_col = (125,135,150)
white = (255,255,255)
black = (0,0,0)
#Defining functions here
def load_pieces():
    #This function loads the piece images so that they may be displayed
    is_pawn = ["","p"]
    colors = ["w","b"]
    piece_types = ["C","D","E","G","K","M","N","P","R","S","V"]
    for a in is_pawn:
        for b in colors:
            for c in piece_types:
                piece = a+b+c
                piece_sprites[piece] = pygame.image.load(sprites_loc + "Pieces/" + piece + ".png").convert_alpha()    
    piece_sprites["wA"] = pygame.image.load(sprites_loc + "Pieces/wA.png")
    piece_sprites["bA"] = pygame.image.load(sprites_loc + "Pieces/bA.png")
def init_board(white,black):
    #This function will initialise the board
    #First initialises of values
    alt  = True
    #Creating the board
    for x in range(0,rows):
        for y in range(0,columns):
            if y != 0 and y != 12:
                if alt:
                    pygame.draw.rect(screen, black, pygame.Rect(y * sq_dim, x * sq_dim, sq_dim, sq_dim) )
                else:
                    pygame.draw.rect(screen, white, pygame.Rect(y * sq_dim, x * sq_dim, sq_dim, sq_dim) )
            else:
                if (x,y) == (1,0) or (x,y) == (8,12):
                    if alt:
                        pygame.draw.rect(screen, black, pygame.Rect(y * sq_dim, x * sq_dim, sq_dim, sq_dim) )
                    else:
                        pygame.draw.rect(screen, white, pygame.Rect(y * sq_dim, x * sq_dim, sq_dim, sq_dim) )
            alt = not(alt)
    
def display_gamestate(gamestate):
    #Displays the current gamestate
    piece_dim = int(3 * sq_dim/4)
    for x in range (0,rows):
        for y in range(0,columns):
            if gamestate[x][y] != "-" and gamestate[x][y] != "N/A":
                piece = pygame.transform.scale( piece_sprites[gamestate[x][y] ], (piece_dim, piece_dim) )
                piece_sq = pygame.Rect(  sq_dim*y , sq_dim*x , sq_dim, sq_dim)
                piece_center_sq = piece.get_rect()
                piece_center_sq.center = piece_sq.center
                screen.blit(piece,piece_center_sq )
                
def highlight_squares(gamestate,valid_moves,squares_selected):
    #Highlights the selected piece
    if len(squares_selected) != 0:
        c,r = squares_selected[0]
        hl = pygame.Surface((sq_dim,sq_dim))
        hl.set_alpha(100)
        hl.fill(pygame.Color('blue'))
        screen.blit(hl , (r*sq_dim,c*sq_dim))
        hl.fill(pygame.Color('yellow'))
        if len(valid_moves) != 0:
            for move in valid_moves:
                screen.blit(hl, (move[1]*sq_dim, move[0]*sq_dim))

def game_drawn_screen(font):
    #Displays the game drawn screen
    screen.fill( (0,0,0) )
    draw_m = font.render("Game drawn!",True,white,black)
    screen.blit(draw_m, [width/30,height/20])
    pygame.display.flip()
    time.sleep(3)
    
def main():
    pygame.init()
    setup = ""
    player_colour = ""
    ai_colour = ""
    piece_selected = False
    clicked_areas = []
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
        screen.fill( (0,0,0) )
        if setup == "":
            #Asking which setup the player wants to play with.
            lfont = pygame.font.SysFont("Times New Roman.tff", 50)
            mfont = pygame.font.SysFont("Times New Roman.tff", 35)
            #Drawing title and buttons
            setup_q = lfont.render("What setup do you wish to play?", True, white,black)
            screen.blit(setup_q, [width/30, height/20])
            #Masculine setup
            masc_button = pygame.Rect( 36 , 120  , 240 , 100)
            masc_option = mfont.render("Masculine Setup", True, black)
            masc_rect = masc_option.get_rect()
            masc_rect.center = masc_button.center
            pygame.draw.rect(screen, white, masc_button)
            screen.blit(masc_option, masc_rect)
            #Feminine setup
            fem_button = pygame.Rect( 36 , 250  , 240, 100)
            fem_option = mfont.render("Feminine Setup", True, black)
            fem_rect = fem_option.get_rect()
            fem_rect.center = fem_button.center
            pygame.draw.rect(screen, white, fem_button)
            screen.blit(fem_option, fem_rect)
            pygame.display.flip()
            #Checking if a button was clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if masc_button.collidepoint(mouse):
                    setup = "Masculine"
                    Engine.game_state = Engine.m_init_state
                    time.sleep(0.4)
                elif fem_button.collidepoint(mouse):
                    setup = "Feminine"
                    Engine.game_state = Engine.f_init_state
                    time.sleep(0.4)
        elif player_colour == "":
            #Asking what colour the player wants to play as
            colour_q = lfont.render("Which colour do you wish to play as?", True, white,black)
            screen.blit(setup_q, [width/30, height/20])
            #Playing as White
            white_button = pygame.Rect( 36 , 120 , 240 , 100)
            white_option = mfont.render("White", True, black)
            white_rect = white_option.get_rect()
            white_rect.center = white_button.center
            pygame.draw.rect(screen, white, white_button)
            screen.blit(white_option, white_rect)
            #Playing as black
            black_button = pygame.Rect( 36 , 250 , 240 , 100)
            black_option = mfont.render("Black", True, black)
            black_rect = black_option.get_rect()
            black_rect.center = black_button.center
            pygame.draw.rect(screen, white, black_button)
            screen.blit(black_option, black_rect)
            pygame.display.flip()
            #Checking if a button was clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if white_button.collidepoint(mouse):
                    player_colour = "White"
                    ai_colour = "Black"
                elif fem_button.collidepoint(mouse):
                    player_colour = "Black"
                    ai_colour = "White"
        else:
            load_pieces()
            sq_selected = False
            clicked_squares = []
            available_moves = []
            while True:
                init_board(light_col,dark_col)
                display_gamestate(Engine.game_state)
                highlight_squares(Engine.game_state,available_moves,clicked_squares)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:#For quitting the game
                        return None
                    elif event.type == pygame.MOUSEBUTTONDOWN: #Finding out where the player clicks their mouse
                        mouse_loc = pygame.mouse.get_pos()
                        sq_loc = [ mouse_loc[1] // sq_dim, mouse_loc[0]//sq_dim  ]
                        if not(sq_selected):#If a piece hasn't already been selected, check if a piece is currently being clicked
                            if Engine.game_state[sq_loc[0] ][sq_loc[1] ] != "-" and Engine.game_state[sq_loc[0] ][sq_loc[1] ] != "N/A":
                                clicked_squares.append(sq_loc)
                                if Engine.is_player_white == Engine.who_is_moving(Engine.game_state,clicked_squares[0]):
                                    color = 0 if Engine.is_player_white else 1
                                    #Check if a pawn of pawn that has reached the end of the board can be moved
                                    if Ruleset.Rules.check_if_pofp_canmove(Engine.game_state,Engine.is_player_white):
                                        if Ruleset.Rules.is_ruler_check(Engine.game_state,Engine.current_rulers[color]):
                                            sq_selected = True
                                            rule_check = Ruleset.Rules( [clicked_squares[0][0], clicked_squares[0][1] ], Engine.game_state)
                                            available_moves = rule_check.map_piece_to_rule()
                                            available_moves = rule_check.check_ruler_vulnerable(available_moves,Engine.current_rulers[color])
                                        elif Engine.game_state[sq_loc[0] ][sq_loc[1] ] in ["pbB","pwP"]:
                                            sq_selected = True
                                            rule_check = Ruleset.Rules( [clicked_squares[0][0], clicked_squares[0][1] ], Engine.game_state)
                                            available_moves = rule_check.map_piece_to_rule()
                                            available_moves = rule_check.check_ruler_vulnerable(available_moves,Engine.current_rulers[color])
                                        else:
                                            clicked_squares = []
                                    else:
                                        #If a piece of the correct color is selected
                                        sq_selected = True
                                        rule_check = Ruleset.Rules( [clicked_squares[0][0], clicked_squares[0][1] ], Engine.game_state)
                                        available_moves = rule_check.map_piece_to_rule()
                                        available_moves = rule_check.check_ruler_vulnerable(available_moves,Engine.current_rulers[color])
                                else:
                                    clicked_squares = []
                        else:#If piece has been selected, move it to the location
                            if Engine.game_state[sq_loc[0] ][sq_loc[1] ] != "N/A":
                                clicked_squares.append(sq_loc)
                                sq_selected = False
                                move = Engine.Move( clicked_squares[0], clicked_squares[1], Engine.game_state )
                                if Engine.is_player_white == Engine.who_is_moving (Engine.game_state, clicked_squares[0]):
                                    #First check if it's the correct turn for the piece to be moved
                                    rule_check = Ruleset.Rules( [clicked_squares[0][0], clicked_squares[0][1] ], Engine.game_state)
                                    if (move.end_row , move.end_col) in available_moves or [move.end_row , move.end_col] in available_moves:
                                        #Then check if the move is a valid one
                                        Engine.game_state = Engine.make_move( Engine.game_state, move )
                                        Engine.is_player_white = not(Engine.is_player_white)
                                Engine.pofp_ended = Engine.promote_pieces(Engine.game_state, Engine.pofp_ended)
                                if Ruleset.Rules.is_ruler_mated(Engine.game_state,Engine.current_rulers[color]):
                                    if Engine.is_player_white:
                                        screen.fill( (0,0,0) )
                                        winner_m = lfont.render("Black wins!",True,white,black)
                                        screen.blit(winner_m, [width/30,height/20])
                                        pygame.display.flip()
                                    else:
                                        screen.fill( (0,0,0) )
                                        winner_m = lfont.render("White wins!",True,white,black)
                                        screen.blit(winner_m, [width/30,height/20])
                                        pygame.display.flip()
                                    time.sleep(3)
                                    return None
                                Ruleset.Rules.citadel_check(Engine.game_state)
                                if Engine.game_drawn:
                                    if not(Engine.swap_made[0]) and not(Engine.is_player_white) and Engine.current_rulers[0] == "-":
                                        #If White can swap with a prince or adventice, first check what royal pieces the player has
                                        player_royal_pieces = []
                                        for x in range(rows):
                                            for y in range(columns):
                                                if Engine.game_state[x][y] in ["wP","wA"]:
                                                    player_royal_pieces.append(Engine.game_state[x][y])
                                        #First ask the player whether they want to draw the game or swap a piece
                                        screen.fill(black)
                                        draw_q = lfont.render("Do you wish to draw the game or make a swap?", True, white,black)
                                        screen.blit(setup_q, [width/30, height/20])
                                        #Then display options for the player to choose from
                                        #Draw option
                                        y = 120
                                        draw_button = pygame.Rect( 36 , y  , 240 , 100)
                                        draw_option = mfont.render("Draw Game", True, black)
                                        draw_rect = draw_option.get_rect()
                                        draw_rect.center = draw_button.center
                                        pygame.draw.rect(screen, white, draw_button)
                                        screen.blit(draw_option, draw_rect)
                                        y += 130
                                        #Then the swap options
                                        option_buttons = {}
                                        for piece in player_royal_pieces:
                                            o_button = pygame.Rect( 36 , y  , 360 , 100)
                                            if piece == "wP":
                                                text = "Swap with white prince"
                                            else:
                                                text = "Swap with white adventice"
                                            o_option = mfont.render(text, True, black)
                                            o_rect = o_option.get_rect()
                                            o_rect.center = o_button.center
                                            pygame.draw.rect(screen, white, o_button)
                                            screen.blit(o_option, o_rect)
                                            y += 130
                                            option_buttons[piece] = o_rect
                                        pygame.display.flip()
                                        option_chosen = False
                                        while not(option_chosen):
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:#For quitting the game
                                                    return None
                                            if pygame.mouse.get_pressed()[0] == 1:
                                                pos = pygame.mouse.get_pos()
                                                if draw_rect.collidepoint(pos):
                                                    game_drawn_screen(lfont)
                                                    return None
                                                for piece in option_buttons:
                                                    if option_buttons[piece].collidepoint(pos) == 1:
                                                        for x in range(rows):
                                                            for y in range(columns):
                                                                if Engine.game_state[x][y] == piece:
                                                                    screen.fill((0,0,0))
                                                                    Engine.game_state[x][y] = "wK"
                                                                    Engine.game_state[1][0] = piece
                                                                    option_chosen = True
                                                                    break
                                    elif not(Engine.swap_made[1]) and not(Engine.is_player_white) and Engine.current_rulers[1] == "-":
                                        #If Black can swap with a prince or adventice
                                        pass
                                    else:
                                        game_drawn_screen(lfont)
                                        return None
                                clicked_squares = []
                                Ruleset.Rules.find_current_ruler(Engine.game_state)
                                
if __name__ == "__main__":
    main()
    pygame.quit()
else:
    print("This module is being imported")
