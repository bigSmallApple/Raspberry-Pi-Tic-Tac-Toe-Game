#Use Code

import random
#from DataBase import dataBase
from GameBoard import gameBoard
from sense_hat import SenseHat

sense = SenseHat()
class Computer:
    def __init__(self,game_board):
        self.game_board = game_board
        #self.db = dataBase()
         
        return
    def some_method(self):
        # Use self.game_board to refer to the gameBoard instance
        self.game_board.show_on_sensehat(selection_board)  # Correct usage inside the class
    #---------- Get AI Moves ----------#
    
    def get_ai_move(self, tic_tac_toe_board, ai_symbol, ai_type):
        if ai_type == "weak_ai":
            return self.weak_ai(tic_tac_toe_board, ai_symbol)
        else:
            return self.strong_ai(tic_tac_toe_board, ai_symbol)
    
    def weak_ai(self, tic_tac_toe_board, ai_symbol):
        print("Weak AI checking for empty spaces...")
        empty=False
        for row in tic_tac_toe_board:
            for cell in row:
                if cell == 0:
                   empty= True
                   break
        if not empty:
            print("No empty spaces found. It's a tie or error in game logic.")
            return tic_tac_toe_board
        
        print("Weak AI is making a move...")
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if tic_tac_toe_board[row][col] == 0:
                tic_tac_toe_board[row][col] = ai_symbol
                print(f"Weak AI placed {ai_symbol} at position ({row}, {col}).")
                return tic_tac_toe_board

    def strong_ai(self, tic_tac_toe_board, ai_symbol):
        player_symbol = 2 if ai_symbol == 1 else 1# Assume the opposite symbol for the player
        
        immediate_move = self.find_immediate_move(tic_tac_toe_board, ai_symbol, player_symbol)
        if immediate_move is not None:
            tic_tac_toe_board[immediate_move[0]][immediate_move[1]] = ai_symbol
            return tic_tac_toe_board
        
        best_move = self.find_best_move(tic_tac_toe_board, ai_symbol, player_symbol)
        if best_move is not None:
            i, j = best_move
            tic_tac_toe_board[i][j] = ai_symbol
        return tic_tac_toe_board
    
    def find_immediate_move(self, board, ai_symbol, player_symbol):
        # First, check for an immediate win opportunity for AI
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = ai_symbol
                    if self.check_win(board, ai_symbol, player_symbol) == ai_symbol:
                        board[i][j] = 0  # Undo move
                        return (i, j)  # Return winning move
                    board[i][j] = 0  # Undo move for next check

    # If no immediate win, then check for a block against the player's potential win
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = player_symbol
                    if self.check_win(board, ai_symbol, player_symbol) == player_symbol:
                        board[i][j] = 0  # Undo move
                        return (i, j)  # Return blocking move
                    board[i][j] = 0  # Undo move for next iteration

    # No immediate win or block found
        return None

    def find_best_move(self, board, ai_symbol, player_symbol):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = ai_symbol
                    score = self.minimax(board, 0, False, ai_symbol, player_symbol)
                    board[i][j] = 0  # Undo the move
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, board, depth, is_maximizing, ai_symbol, player_symbol):
        win_check= self.check_win(board,ai_symbol,player_symbol)
        if win_check == ai_symbol:
            return 10 - depth
        elif win_check == player_symbol:
            return depth-10
        elif win_check ==0:  # Draw
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = ai_symbol
                        score = self.minimax(board, depth + 1, False, ai_symbol, player_symbol)
                        board[i][j] = 0
                        score -= depth
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = player_symbol
                        score = self.minimax(board, depth + 1, True, ai_symbol, player_symbol)
                        board[i][j] = 0
                        score += depth
                        best_score = min(score, best_score)
            return best_score

#---------- Functions used to get local player moves ----------#
    def player2_move_local(self, tic_tac_toe_board, opponent_symbol):
        ##code for player 2
        return self.player1_move_local(tic_tac_toe_board, opponent_symbol)
    
    
    def player1_move_local(self, tic_tac_toe_board, player_symbol):
        position_x = 1
        position_y = 1
        
        selection_board = [row[:] for row in tic_tac_toe_board]
        selection_board[position_y][position_x] = 3
        self.game_board.show_on_sensehat(selection_board)
        
        move_made = False
        while not move_made:
    
    
         for event in sense.stick.get_events():
        # Update position based on joystick movement
            if event.direction == "up" and event.action == "pressed":
                position_y = max(0, position_y - 1)
            elif event.direction == "down" and event.action == "pressed":
                position_y = min(2, position_y + 1)
            elif event.direction == "left" and event.action == "pressed":
                position_x = max(0, position_x - 1)
            elif event.direction == "right" and event.action == "pressed":
                position_x = min(2, position_x + 1)
            # Update the selection board with the current selection
            selection_board = [row[:] for row in tic_tac_toe_board]  # Refresh the selection board
            selection_board[position_y][position_x] = 3  # Mark the current selection

        # Display the selection board on Sense HAT
            self.game_board.show_on_sensehat(selection_board)
            # Print the current boards to the console
            print("Current tic_tac_toe_board:")
            for row in tic_tac_toe_board:
                print(row)
            print("\nCurrent selection_board:")
            for row in selection_board:
                print(row)

            if event.direction == "middle" and event.action == "pressed":
            # Confirm the selection
                if tic_tac_toe_board[position_y][position_x] == 0:
                    tic_tac_toe_board[position_y][position_x] = player_symbol
                    print("Player move made.")
                    move_made = True
                    
                else:
                    print("Invalid spot")
                    print("Please select valid stop (not taken)")
                    
        return tic_tac_toe_board


   #---------- Functions to check the win ----------#
    def check_win(self, tic_tac_toe_board, player_symbol, opponent_symbol):
        # Check rows and columns for player's win
        for i in range(3):
            if all(cell == player_symbol for cell in tic_tac_toe_board[i]):
                return player_symbol
            if all(tic_tac_toe_board[j][i] == player_symbol for j in range(3)):
                return player_symbol

        # Check diagonals for player's win
        if all(tic_tac_toe_board[i][i] == player_symbol for i in range(3)):
            return player_symbol
        if all(tic_tac_toe_board[i][2 - i] == player_symbol for i in range(3)):
            return player_symbol

        # Check rows and columns for opponent's win
        for i in range(3):
            if all(cell == opponent_symbol for cell in tic_tac_toe_board[i]):
                return opponent_symbol
            if all(tic_tac_toe_board[j][i] == opponent_symbol for j in range(3)):
                return opponent_symbol

        # Check diagonals for opponent's win
        if all(tic_tac_toe_board[i][i] == opponent_symbol for i in range(3)):
            return opponent_symbol
        if all(tic_tac_toe_board[i][2 - i] == opponent_symbol for i in range(3)):
            return opponent_symbol

        # Check if the game is finished or a tie
        if all(cell != 0 for row in tic_tac_toe_board for cell in row):
            return 0  # Tie
        else:
            return -1  # Game not finished


