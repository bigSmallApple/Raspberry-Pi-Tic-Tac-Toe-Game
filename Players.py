from DataBase import dataBase

class Player:
    def __init__(self,db):
        self.db = db
        self.player_name = None #string  "random words"
        self.player_id = None
        self.persistent_player_id = None
        self.player_email = None    #string   "random words"
        self.player_password = None #string   "random words"
        self.player_symbol = None   #int (1 or 2)
        self.opponent = None    #String (name of other player or ai type) "random words" or "weak_ai" or "strong_ai"
        self.opponent_symbol = None #int (2 or 1)
        self.game_result = None #string ("X" or "O" or "_")
        self.player_turn_number = None #1 means first 2 means second
        
        #self.db = dataBase()    #creating database object to use methods

    def set_player_information(self):
        while True:
            self.player_email = input ("Enter your email:").strip()
            if not self.player_email:
                print("Email cannot be empty.")
                continue
                ## Check if the email exists in the database
            self.player_id = self.db.get_player_id_by_email(self.player_email)
            if self.player_id is not None:
                print("Email found. Please enter your name and password for verification.")
                self.player_name = input("Enter your name: ").strip()
                self.player_password = input("Enter your password: ").strip()
                if self.db.verify_player(self.player_name,self.player_email, self.player_password):
                    print(f"Verification successful. Welcome back, {self.player_name}!")
                    print(f"[Debug] player_id right after login: {self.player_id}")
                    self.persistent_player_id = self.player_id
                    break
                else:
                    print("Verification failed. Please try again.")
            else:
                    # Email not found, ask for name and password to register new player
                self.player_name = input("Enter your name: ").strip()
                self.player_password = input("Enter your password: ").strip()
                if self.player_name and self.player_password:
                    self.register_new_player()
                    if self.player_id:
                        print(f"New player registered with ID {self.player_id}.")
                        self.persistent_player_id = self.player_id
                        break
                    else:
                        print("Registration failed. Please try again.")
                
        
        while True:
            player_symbol = input("Enter the symbol you want to play with [X/O]: ").upper()
            
            #TODO: For Database storage, 1 = X and 2 = O and 0 = blank. You will have to make it check. If player_symbol = 1 safe 'X' in database.
            if player_symbol == "X" or player_symbol == "O":
                self.player_symbol = 1 if player_symbol == "X" else 2
                self.opponent_symbol = 2 if player_symbol == "X" else 1
                break
            else:
                print("Wrong Symbol. Please enter 'X' or 'O'")
                
                
        while True:
            player_turn_number = input("Enter if you want to go first or second. Enter '1' for first and '2' for second [1/2]: ").upper()
            if player_turn_number == '1' or player_turn_number == '2':
                self.player_turn_number = int(player_turn_number)
                break
            else:
                print("Wrong Symbol. Please enter '1' or '2'")
                

        while True:
            opponent = input("Do you want to play against a computer or player? Type 'C' for computer and 'P' for player [C/P]: ").upper()
            if opponent == "C":
                self.opponent = "ai"
                break
            elif opponent == "P":
                self.opponent = "player"
                break
            else:
                print("Wrong choice. Please enter 'C' or 'P'")
        
        if self.opponent == "ai":
            while True:
                opponent_type = input("Do you want to play against a weak ai or strong ai? Type 'W' for weak and 'S' for strong [W/S]: ").upper()
                if opponent_type == "W":
                    self.opponent = "weak_ai"
                    break
                elif opponent_type == "S":
                    self.opponent = "strong_ai"
                    break
                else:
                    print("Wrong choice. Please enter 'W' or 'S'")
        else:
            while True:
                network_type = input("Do you want to play against local player on raspberry pi or network player against someone on a computer? Type 'L' for local or 'N' for network: ").upper()
                if network_type == "L":
                    opponent_email = input("Enter Player 2 Email: ").strip()
                    opponent_id = self.db.get_player_id_by_email(opponent_email)
                    if opponent_id is not None:
                        # Player 2 exists, ask for their name and password
                        print("Email found. Please enter your name and password for verification.")
                        self.opponent = input("Enter Player 2 Name: ").strip()
                        opponent_password = input("Enter Player 2 Password: ").strip()
                        hashed_password = self.db.hash_password(opponent_password)
                        if self.db.verify_player(self.opponent, opponent_email, opponent_password):
                            print(f"Verification successful for {self.opponent}.")
                            break
                        else:
                            print("Verification failed. Please try again.")
    
                    else:
                        # Player 2 does not exist, register them
                        self.opponent = input("Enter Player 2 Name: ").strip()
                        opponent_password = input("Enter Player 2 Password: ").strip()
                        if self.opponent and opponent_password:
                            hashed_password = self.db.hash_password(opponent_password)
                            new_opponent_id = self.db.create_new_player(self.opponent, opponent_email, hashed_password)
                            if new_opponent_id:
                                print(f"Player 2 registered successfully with ID {new_opponent_id}.")
                                break
                            else:
                                print("Registration failed. Please try again.")
                        else:
                            print("Name and password cannot be empty. Please try again.")
                            self.register_new_player()
                elif network_type == "N":
                    self.opponent = "_nt"
                    break
                else:
                    print("Wrong choice. Please enter 'L' or 'N'")
                    
        self.player_id = self.db.create_new_player(self.player_name, self.player_email, self.player_password)  # Store the ID

    

   
    def register_new_player(self):
        # Assuming create_new_player returns the new player ID or None if registration fails
        new_player_id = self.db.create_new_player(self.player_name, self.player_email, self.player_password)
        if new_player_id:
            self.player_id = new_player_id
            print(f"New player registered with ID {self.player_id}.")
        else:
            print("Registration failed. Please try again.")
                    


    def get_opponent_id(self):
        if 'ai' in self.opponent:
            return 0
        else:
            opponent_id = self.db.get_player_id_by_name(self.opponent)
            if opponent_id is not None:
                return opponent_id
            else:
                print(f"Opponent {self.opponent} not found in database.")
                # Ask for opponent's email and password
                while True:
                    opponent_email = input(f"Enter {self.opponent}'s email: ").strip()
                    if opponent_email:
                        opponent_password = input(f"Enter a password for {self.opponent}: ").strip()  # Use getpass.getpass in actual use
                        if opponent_password:
                            # If both email and password are provided, exit the loop
                            break
                        else:
                            print("Password cannot be empty. Please try again.")
                    else:
                        print("Email cannot be empty. Please try again.")
                hashed_password = self.db.hash_password(opponent_password)
                # Create a new player in the database and retrieve their ID
                new_opponent_id = self.db.create_new_player(self.opponent, opponent_email, hashed_password)
                if new_opponent_id is not None:
                    print(f"Opponent {self.opponent} registered with ID {new_opponent_id}.")
                    return new_opponent_id
                else:
                    print("Failed to register opponent.")
                    return None
                
    
    def save_game_result(self, winner):
        self.game_result = winner  # Who won. A ***NAME***
        
    def get_player_turn_number(self):
        return self.player_turn_number
        
    def get_player_name(self):
        return self.player_name
        
    def get_player_symbol(self):
        return self.player_symbol
    
    def get_persistent_player_id(self):
        return self.persistent_player_id
        
    def get_opponent_name(self):
        return self.opponent
        
    def get_opponent_symbol(self):
        return self.opponent_symbol
    
    def get_player_id(self):
        return self.player_id