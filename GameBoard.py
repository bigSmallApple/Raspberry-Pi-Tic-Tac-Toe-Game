from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

class gameBoard:
    def __init__(self):
        self.colors = {
            'r': (255, 0, 0),
            'b': (0, 0, 255),
            'w': (255, 255, 255),
            'o': (0, 0, 0),
            'g': (0, 255, 0),
            'y': (255, 255, 0),
            'n': (255, 165, 0)
        }
    def show_draw_screen(self):
    
    # Blue on the left half, Red on the right half
        print("The Game is DRAW")
        draw_pattern = []
        for i in range(8):
            for j in range(8):
                if j < 4:
                    draw_pattern.append([0, 0, 255])  # Blue
                else:
                    draw_pattern.append([255, 0, 0])  # Red
        sense.set_pixels(draw_pattern)

        
        
    def show_victory_screen(self, winner_name, winner_symbol):
        victory_board = []
        if winner_symbol == 1:
            victory_board = [self.colors['b']] * 64
            print(winner_name + " Has Won!!")
        elif winner_symbol == 2:
            victory_board = [self.colors['r']] * 64
            print(winner_name + "Player 2 Has Won!!")
        else:
            victory_board = [self.colors['y']] * 64
            print("It Is A DRAW!!!")
        sense.set_pixels(victory_board)
        
        

    def show_option_screen(self):
        y = (150, 150, 0)
        option_board = [y] * 64
        sense.set_pixels(option_board)
        

    def show_welcome(self):
        sense.show_message("Welcome to Tic Tac Toe")
        print("Welcome to Tic Tac Toe!!!")
        
        
    def show_logo(self):
        b = (0, 0, 255)
        g = (0, 255, 0)
        o = (0, 0, 0)
        logo_board = [
            b,b,b,b,b,b,b,b,
            b,b,b,b,b,o,b,b,
            b,b,b,o,o,o,o,b,
            b,b,g,o,o,g,o,b,
            b,o,o,o,o,o,o,o,
            b,o,g,o,o,g,o,o,
            o,o,o,g,g,o,o,o,
            o,o,o,o,o,o,o,o,
            ]
        sense.set_pixels(logo_board)
        print("""
        /////////////
        /////     ///
        ///U    U  //
        /|    w    |
          \_______/
        """)
        
        
    def show_on_console(self, tic_tac_toe_board):
        
        for row in tic_tac_toe_board:
            formatted_row = ""
            for cell in row:
                if cell == 1:
                    formatted_row += "X"
                elif cell == 2:
                    formatted_row += "O"
                else:
                    formatted_row += " "
                formatted_row += "|"
            print(formatted_row[:-1])  # Print the row without the last "|"
            print("-" * 5)


    def show_on_sensehat(self, tic_tac_toe_board):
        print("Updating Sense HAT display...")          
        # Define colors
        r = [255, 0, 0]   # Red
        b = [0, 0, 255]   # Blue
        w = [255, 255, 255]   # White
        o = [0, 0, 0]   # Black
        g = [0, 255, 0]   # Green

        n = [255, 255, 0]   # this is yellow, idk why but when i put 'y' it crashes
        
        print("Current game board:")
        for row in tic_tac_toe_board:
            print(row)

        # Define initial empty tic-tac-toe board
        empty_board = [
            o, o, g, o, o, g, o, o,
            o, o, g, o, o, g, o, o,
            g, g, g, g, g, g, g, g,
            o, o, g, o, o, g, o, o,
            o, o, g, o, o, g, o, o,
            g, g, g, g, g, g, g, g,
            o, o, g, o, o, g, o, o,
            o, o, g, o, o, g, o, o,
        ]
        sense.set_pixels(empty_board)

        # Define fill lists for different states
        player_one_fill = [0, 2, 2, 0]
        player_two_fill = [1, 0, 0, 1]
        selection_fill = [3, 3, 3, 3]
        empty_fill = [0, 0, 0, 0]

        # tic_tac_toe_board = [[3] * 3 for _ in range(3)] #*** TicTacToeBoard ***#

        # Define board coordinates
        coords_map = {
            (0, 0): [(x, y) for x in range(2) for y in range(2)],
            (0, 1): [(x, y) for x in range(3, 5) for y in range(2)],
            (0, 2): [(x, y) for x in range(6, 8) for y in range(2)],
            (1, 0): [(x, y) for x in range(2) for y in range(3, 5)],
            (1, 1): [(x, y) for x in range(3, 5) for y in range(3, 5)],
            (1, 2): [(x, y) for x in range(6, 8) for y in range(3, 5)],
            (2, 0): [(x, y) for x in range(2) for y in range(6, 8)],
            (2, 1): [(x, y) for x in range(3, 5) for y in range(6, 8)],
            (2, 2): [(x, y) for x in range(6, 8) for y in range(6, 8)],
        }

        # Iterate over the board and set colors based on the current state
        for row_index, row in enumerate(tic_tac_toe_board):
            for col_index, cell in enumerate(row):
                fill = (
                    player_one_fill if cell == 1
                    else player_two_fill if cell == 2
                    else selection_fill if cell == 3
                    else empty_fill
                )
                coords = coords_map.get((row_index, col_index))  # Corrected coordinates retrieval
                if coords:
                    for index, pixel in enumerate(coords):
                        color = r if fill[index] == 1 else b if fill[index] == 2 else n if fill[index] == 3 else o
                        sense.set_pixel(pixel[0], pixel[1], color)

