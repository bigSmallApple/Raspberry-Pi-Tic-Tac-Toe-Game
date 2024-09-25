from Players import Player
from GameBoard import gameBoard
from DataBase import dataBase
from sense_hat import SenseHat
from time import sleep
from Computer import Computer
import datetime
#TODO: Finish Network player and place inport here

sense = SenseHat()

#------ IMPORTANT GAME NOTES ------#
# There is a single 3 by 3 tic_tac_toe_board array that keeps the information about the game
# all other methods either update the array or read & display it
# X is represented as 1 in array
# O is represented as 2 in array
# Empty space is represented as 0 in array
# Selection space (rapsberry pi sensehat part) is represented as 3. 3 is only for selection. Must not be formally included in anything.

#-- for raspbery pi sensehat pixel display --#
# X is represented by red
# O is represented by blue
# Empty space is represented by blank square
# Selection is represented by white square





def main():
    # Creating objects from imported classes
  db = dataBase()
  game_board = gameBoard()
  computer = Computer(game_board)
  
  while True:
        print("\nMain Menu:")
        print("1 - View Player Information")
        print("2 - View Player Stats")
        print("3 - Play the Game")
        print("4 - Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            # Placeholder: Implement viewing player information
            player_id = input("Enter player ID: ")
            db.retrieve_player_info(player_id)
        elif choice == "2":
            # Placeholder: Implement viewing player stats
            player_id = input("Enter player ID: ")
            db.calculate_winlose(player_id)
        elif choice == "3":
            play_game(db, game_board, computer)
        elif choice == "4":
            print("Exiting the game. Thank you for playing!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
    
    
def play_game(db,game_board,computer):      
  while True:
    player = Player(db)
    #TODO: Create network player object
    def wait_for_middle_press():
        while True:
            for event in sense.stick.get_events():
                if event.action == 'pressed' and event.direction == 'middle':
                    return
    

    def determin_winner():
        game_winner = computer.check_win(game_array, player.get_player_symbol(), player.get_opponent_symbol())
        if game_winner == player.get_player_symbol():
            game_board.show_victory_screen(player.get_player_name(), player.get_player_symbol())
            return True
        elif game_winner == player.get_opponent_symbol():
            game_board.show_victory_screen(player.get_opponent_name(), player.get_opponent_symbol())
            return True
        elif all(cell != 0 for row in game_array for cell in row): #draw
            game_board.show_draw_screen()
            return True
        else:
            return False
        
    
    
    #prepers all the things necessary for the game and gets the player info
    game_array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    game_winner = -1
    
    #game_board.show_welcome()
    #game_board.show_logo()
    #sleep(5)
    #wait_for_middle_press()
    game_board.show_option_screen()
    
    player.set_player_information()
    
    opponent_type = player.get_opponent_name()
        
    
    if player.get_player_turn_number()==2:
        current_turn=1
        
    else:
        current_turn=2
    print(f"Player 1 ID before starting the game: {player.player_id}")

    while True:
        print(f"Current turn: {current_turn}")
        game_board.show_on_sensehat(game_array)  # Show the current board  
        if current_turn == 2:
            print("Player's turn...")
            
            game_array = computer.player1_move_local(game_array, player.get_player_symbol())
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print("Board after player's move:")
        else:
            if opponent_type[-3:] == "_ai":
                 print("Ai turn")
                 
                 game_array = computer.get_ai_move(game_array, player.get_opponent_symbol(), opponent_type)
                 
                 timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                 #db.insert_move(game_id, player.get_persistent_player_id(), move_coordinates, timestamp)
                 print("AI has made a move.")
                                    
            else: #this is pvp on the sense hat
                print("Player2's turn...")
                
                game_array = computer.player2_move_local(game_array, player.get_opponent_symbol())
                
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #db.insert_move(game_id, player.get_persistent_player_id(), move_coordinates, timestamp)
                print("Board after player 1's turn")
        for row in game_array:
            print(row)
        game_board.show_on_sensehat(game_array)
        sleep(0.5)
        # Determine the winner after each move
        game_winner = computer.check_win(game_array, player.get_player_symbol(), player.get_opponent_symbol())
        if game_winner != -1:  # Game has ended
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            player1_id = player.get_persistent_player_id()
            player2_id = player.get_opponent_id()
            outcome = "Draw"  # Default to draw
            winner_id = None  # Default no winner
            
            if game_winner == player.get_player_symbol():
                outcome = "Win"
                winner_id = player1_id
                game_board.show_victory_screen(player.get_player_name(), player.get_player_symbol())
            elif game_winner == player.get_opponent_symbol():
                outcome = "Loss"
                winner_id = player2_id
                game_board.show_victory_screen(player.get_opponent_name(), player.get_opponent_symbol())
            else:  # game_winner == 0, it's a draw
                game_board.show_draw_screen()
            print(f"Game over. Winner: {game_winner}")
            print(f"Saving game results: Date Time: {date_time}, Player 1 ID: {player1_id}, Player 2 ID: {player2_id}, Outcome: {outcome}, Winner ID: {winner_id}")
            db.save_game_results(date_time, player1_id, player2_id, outcome, winner_id)
            break  # Exit the game loop
            
            
            
        current_turn = 1 if current_turn == 2 else 2
        sleep(1)
    
    while True:
        play_again= input("Play again? (y/n): ").lower()
        if play_again == "y":
            break
        elif play_again == "n":
            print("Thanks For Playing ")
            return
        else:
            print("Invalid input. Please enter 'y' to play again or 'n' to exit.")
        

        
        
    
    #elif opponent_type[-3:] == "_nt":   #pvp verus an online oponent
    
     # print("hello")
                                    #
        ###########################################################
        #IMPLEMENT WHEN NET PLAYER IS WORKING         #
        ###########################################################
                                    
   
    
if __name__ == "__main__":
    main()

