import pygame as pg
import sys
from random  import randint


WIN_SIZE = 900
CELL_SIZE = WIN_SIZE // 3
INF = float('inf')
vec2 = pg.math.Vector2

# the CELL_CENTER here is [150,150]
CELL_CENTER = vec2(CELL_SIZE/2)

class TicTacToe:
    def __init__(self,game):
        self.game = game

        #load the image to the plane field(mention the path and size of the resolution)
        self.field_image = self.get_scaled_image(path = 'field.png', res = [WIN_SIZE]*2)
        self.O_image = self.get_scaled_image(path = 'o.png', res = [CELL_SIZE]*2)
        self.X_image = self.get_scaled_image(path = 'x.png', res = [CELL_SIZE]*2)

        self.game_array = [[INF, INF, INF], 
                           [INF, INF, INF], 
                           [INF, INF, INF]]
        
        # make the choice of the player 
        self.player = randint(0, 1)
        
        # make all the possible lines(x, y) combinations to an array
        self.line_indices_array = [[(0, 0),(0, 1),(0, 2)], 
                                   [(1, 0), (1, 1), (1, 2)], 
                                   [(2, 0), (2, 1), (2, 2)], 
                                   [(0, 0), (1, 0), (2, 0)], 
                                   [(0, 1), (1, 1), (2, 1)], 
                                   [(0, 2), (1, 2), (2, 2)], 
                                   [(0, 0), (1, 1), (2, 2)], 
                                   [(0, 2), (1, 1), (2, 0)]]
        self.winner = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Time New Romance', CELL_SIZE//5, True, True)
    

    def check_winner(self):
        for line_indices in self.line_indices_array:

            # add all the posible line_indices with game_array 
            sum_line = sum([self.game_array[i][j]for i, j in line_indices])

            # use dictionary to define *unordered collection of key-value pairs*
            # which the keys must be unique
            if sum_line in {0, 3}:

                # Define winner and change all the array[i][j] to be 0
                # Which stops the game from playing
                # As the self.game_array[row][col] is no longer equals to INF 
                self.winner = 'XO'[sum_line == 0]
                
                # concept: fixed the line started and ended point to facilitate the drawing of joined red line
                # **reverse is to match the (x,y) coordinate system => (0,0)&(2,2) reverse results themselves
                # NO + CELL_CENTER => out range by the left-up corner
                # The first vec2 + CELL_CENTER => the (0,0) draw line starts at its cell center
                self.winner_line = [vec2(line_indices[0][::-1])*CELL_SIZE + CELL_CENTER , 
                                    vec2(line_indices[2][::-1])*CELL_SIZE + CELL_CENTER]


    def run_game_process(self):

        # get the current position of the mouse point 
        # within the whole computer screen
        # // CELL_SIZE -> the remainder 
        # would be the mouse point position inside the game window
        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE 

        # map integer to the (x,y) position of the current_cell as vector indexes
        col, row = map(int, current_cell)

        # return mouse buttons state sequence of booleans[0]
        # which is the MOUSEBUTTONDOWN 
        left_click = pg.mouse.get_pressed()[0]

        # When the mouse click at one of the INF(x, y) 
        # not self.winner => not None => True
        if left_click and self.game_array[row][col] == INF and not self.winner:
            
            # Make the current place be 0/1 which is X_image player/ O_image player
            self.game_array[row][col] = self.player

            # Alter the current player  
            self.player = not self.player
            
            # finished one game 
            self.game_steps += 1
            self.check_winner()   

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.X_image if obj else self.O_image, vec2(x, y)* CELL_SIZE)

    def draw_winner(self):
        if self.winner:
            # //8 is the width of the red line
            pg.draw.line(self.game.screen, 'red', *self.winner_line, CELL_SIZE // 7)
            label = self.font.render(f'Player " {self.winner} " wins!',True, 'white','black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 2))
    
    
    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()   

    @staticmethod
    #to load and scale our images
    def get_scaled_image(path, res):
        img = pg.image.load(path)

        #scale a surface to an arbitrary size smoothly
        #The size is a 2 number sequence for (width, height).
        return pg.transform.smoothscale(img, res)

    def print_restart(self):
        if self.game_steps == 9:
            label = self.font.render(f'Game Over! Press Space to Restart',True, 'white','black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 2))
    

    def run(self):
        self.draw()
        self.run_game_process()
        self.print_restart()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE]*2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self)
        self.title = pg.display.set_caption('TicTacToe_Game')
        

    def new_game(self):

        # regenerate the game -> new game
        self.tic_tac_toe = TicTacToe(self)    

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.QUIT()
                sys.exit()

            # When spacebar is pressed(KEYDOWN) the game will restart    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            # run it to a max of 60 times per second
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()