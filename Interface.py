#Run this file in order to play the game. This file is responsible for displaying a board for you to interact with.
import pygame
import Engine
import Ruleset
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
sprites_loc = "/Users/donti/Desktop/Programming/Incomplete Projects/Python/Tamerlane Chess/Sprites/"
light_col = (232,235,239)
dark_col = (125,135,150)
#Defining functions here
def load_pieces():
    #This function loads the piece images so that they may be displayed
    is_pawn = ["","p"]
    colors = ["w","b"]
    piece_types = ["C","D","E","G","K","M","N","R","S","V"]
    for a in is_pawn:
        for b in colors:
            for c in piece_types:
                piece = a+b+c
                piece_sprites[piece] = pygame.image.load(sprites_loc + "Pieces/" + piece + ".png")
    piece_sprites["pwP"] = pygame.image.load(sprites_loc + "Pieces/pwP.png")
    piece_sprites["pbP"] = pygame.image.load(sprites_loc + "Pieces/pbP.png")    

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
                sys.exit()
        screen.fill( (0,0,0) )
        if setup == "":
            #Asking which setup the player wants to play with.
            #First initialising colors and fonts: 
            lfont = pygame.font.SysFont("Times New Roman.tff", 50)
            mfont = pygame.font.SysFont("Times New Roman.tff", 35)
            white = (255,255,255)
            black = (0,0,0)
            #Then drawing title and buttons
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
            while True:
                init_board(light_col,dark_col)
                display_gamestate(Engine.game_state)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:#For quitting the game
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN: #Finding out where the player clicks their mouse
                        mouse_loc = pygame.mouse.get_pos()
                        sq_loc = [ mouse_loc[1] // sq_dim, mouse_loc[0]//sq_dim  ]
                        if not(sq_selected):#If a piece hasn't already been selected, check if a piece is currently being clicked
                            if Engine.game_state[sq_loc[0] ][sq_loc[1] ] != "-" and Engine.game_state[sq_loc[0] ][sq_loc[1] ] != "N/A":
                                clicked_squares.append(sq_loc)
                                sq_selected = True
                        else:#If piece has been selected, move it to the location
                            if Engine.game_state[sq_loc[0] ][sq_loc[1] ] != "N/A":
                                clicked_squares.append(sq_loc)
                                sq_selected = False
                                move = Engine.Move( clicked_squares[0], clicked_squares[1], Engine.game_state )
                                if Engine.is_player_white == Engine.who_is_moving (Engine.game_state, move):
                                    Engine.game_state = Engine.make_move( Engine.game_state, move )
                                    Engine.is_player_white = not(Engine.is_player_white)
                                clicked_squares = []
                            
if __name__ == "__main__":
    main()
