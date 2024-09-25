import sqlite3
from datetime import datetime
import hashlib
import datetime
class dataBase:
    def __init__(self):
        # Database initialization
        self.conn = sqlite3.connect('tryout.db')
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create necessary tables if not exists
        table_commands = [
            '''CREATE TABLE IF NOT EXISTS Player (
                player_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                win_count INTEGER DEFAULT 0,
                loss_count INTEGER DEFAULT 0,
                total_games INTEGER DEFAULT 0
            );''',
            '''CREATE TABLE IF NOT EXISTS Game (
                game_id INTEGER PRIMARY KEY,
                date_time TEXT NOT NULL,
                player1_id INTEGER,
                player2_id INTEGER,
                outcome TEXT NOT NULL, -- Win/Loss/Draw
                winner_id INTEGER,
                FOREIGN KEY (player1_id) REFERENCES Player(player_id),
                FOREIGN KEY (player2_id) REFERENCES Player(player_id),
                FOREIGN KEY (winner_id) REFERENCES Player(player_id)
            );''',
            '''CREATE TABLE IF NOT EXISTS Move (
                move_id INTEGER PRIMARY KEY,
                game_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                move_coordinates TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (game_id) REFERENCES Game(game_id),
                FOREIGN KEY (player_id) REFERENCES Player(player_id)
            );''',
            '''CREATE TABLE IF NOT EXISTS Settings (
                setting_id INTEGER PRIMARY KEY,
                board_size INTEGER NOT NULL,
                game_mode TEXT NOT NULL, -- Single or Multiplayer
                difficulty_level TEXT NOT NULL,
                player_turn_order TEXT NOT NULL
            );'''
        ]
        for command in table_commands:
            self.cur.execute(command)
        self.conn.commit()

    def hash_password(self, password):
        """Hash a password for storing."""
       
        return hashlib.sha256(password.encode()).hexdigest()

    def create_new_player(self, name, email, password):
        """Method to create a new player and store in the Player table."""
        hashed_password = self.hash_password(password)
        try:
            self.cur.execute('''INSERT INTO Player (name, email, password)
                                VALUES (?, ?, ?)''', (name, email, hashed_password))
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.IntegrityError:
            print("A player with this email already exists.")
        except sqlite3.Error as e:
            print(f"Error creating new player: {e}")
            return None

    def get_player_id_by_email(self, email):
        try:
            self.cur.execute("SELECT player_id FROM Player WHERE email = ?", (email,))
            result = self.cur.fetchone()
            if result:
                return result[0]  # This is the player_id
            else:
                return None  # Player not found
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Exception in _query: {e}")
            return None
    def get_player_id_by_name(self, name):
        """Fetch player ID by name."""
        self.cur.execute("SELECT player_id FROM Player WHERE name = ?", (name,))
        result = self.cur.fetchone()
        return result[0] if result else None
    def register_or_fetch(self):
        player_id = self.db.get_player_id_by_email(self.player_email)
        if player_id is None:
        # Player doesn't exist, so register them
            player_id = self.db.create_new_player(self.player_name, self.player_email, self.player_password)
            if player_id:
                print(f"Player registered with ID {player_id}.")
            else:
                print("Failed to register player.")
        else:
            print(f"Player found with ID {player_id}.")
        self.player_id = player_id  # Store the player's ID in the Player object for later use
    
    def insert_move(self, game_id, player_id, move_coordinates, timestamp):
        try:
            self.cur.execute("INSERT INTO Move (game_id, player_id, move_coordinates, timestamp) VALUES (?, ?, ?, ?)", (game_id, player_id, move_coordinates, timestamp))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"SQLite integrity error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def save_player_move(self, game_id, player_id, move_coordinates, move_timestamp):
        """Method to save a player's move in the Move table."""
        try:
            print(f"Attempting to save move: Game ID: {game_id}, Player ID: {player_id}, Move: {move_coordinates}, Timestamp: {move_timestamp}")
            self.cur.execute('''INSERT INTO Move (game_id, player_id, move_coordinates, timestamp)
                                VALUES (?, ?, ?, ?)''', (game_id, player_id, move_coordinates, move_timestamp))
            self.conn.commit()
            print("Player's move saved successfully.")
        except sqlite3.Error as e:
            print("Error saving player's move: {e}")

    def save_ai_move(self, game_id, move_coordinates, move_timestamp):
        """Method to save AI's move in the Move table, assuming AI's player_id is predetermined."""
        ai_player_id = 0  # Example placeholder
        try:
            self.cur.execute('''INSERT INTO Move (game_id, player_id, move_coordinates, timestamp)
                                VALUES (?, ?, ?, ?)''', (game_id, ai_player_id, move_coordinates, move_timestamp))
            self.conn.commit()
            print("AI's move saved successfully.")
        except sqlite3.Error as e:
            print("Error saving AI's move: {e}")

    def save_game_results(self, date_time, player1_id, player2_id, outcome, winner_id):
        """Method to save game results in the Game table."""
        try:
            self.cur.execute('''INSERT INTO Game (date_time, player1_id, player2_id, outcome, winner_id)
                                VALUES (?, ?, ?, ?, ?)''', (date_time, player1_id, player2_id, outcome, winner_id))
            self.conn.commit()
            print("Game results saved successfully.")
        except sqlite3.Error as e:
            print(f"Error saving game results: {e}")

    def retrieve_player_info(self, player_id):
        """Method to retrieve player information."""
        try:
            self.cur.execute("SELECT * FROM Player WHERE player_id = ?", (player_id,))
            player_info = self.cur.fetchone()
            if player_info:
                print("Player information retrieved successfully:")
                print("Player ID:", player_info[0])
                print("Name:", player_info[1])
                print("Email:", player_info[2])
                print("Password (hashed):", player_info[3])
                print("Win count:", player_info[4])
                print("Loss count:", player_info[5])
                print("Total games:", player_info[6])
            else:
                print("Player with ID", player_id, "not found.")
        except sqlite3.Error as e:
            print(f"Error retrieving player information: {e}")

    def calculate_winlose(self, player_id):
        """Method to calculate win/loss ratio for a player."""
        try:
            self.cur.execute("SELECT win_count, loss_count FROM Player WHERE player_id = ?", (player_id,))
            results = self.cur.fetchone()
            if results and results[1] != 0:  # Ensure loss_count is not zero to avoid division by zero
                win_loss_ratio = results[0] / results[1]
                print(f"Win/loss ratio for player {player_id}: {win_loss_ratio:.2f}")
            else:
                print("No losses recorded for the player, or player not found.")
        except sqlite3.Error as e:
            print(f"Error calculating win/loss ratio: {e}")

    def calculate_popular_settings(self):
        """Method to calculate the most popular game settings."""
        try:
            self.cur.execute('''SELECT board_size, game_mode, difficulty_level, player_turn_order, COUNT(*) AS count
                                FROM Settings
                                GROUP BY board_size, game_mode, difficulty_level, player_turn_order
                                ORDER BY count DESC LIMIT 1''')
            settings = self.cur.fetchone()
            if settings:
                print("Most popular game settings:")
                print("Board Size:", settings[0])
                print("Game Mode:", settings[1])
                print("Difficulty Level:", settings[2])
                print("Player Turn Order:", settings[3])
                print("Occurrences:", settings[4])
            else:
                print("No settings found.")
        except sqlite3.Error as e:
            print(f"Error calculating popular game settings: {e}")

    def calculate_average_game_duration(self):
        """Method to calculate the average game duration."""
        try:
            self.cur.execute("SELECT date_time, outcome FROM Game")
            games = self.cur.fetchall()
            if games:
                durations = []
                for game in games:
                    start_time = datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
                    # Assuming outcome contains the end time; replace with actual logic to calculate duration
                    end_time = datetime.now()  # Example; use actual game end time
                    duration = (end_time - start_time).total_seconds()
                    durations.append(duration)
                average_duration = sum(durations) / len(durations)
                print(f"Average game duration: {average_duration:.2f} seconds")
            else:
                print("No games found.")
        except sqlite3.Error as e:
            print(f"Error calculating average game duration: {e}")
    def verify_player(self, name, email, password):
        # Method to verify player's name, email, and password
        # This requires hashing the entered password and comparing it against the stored hash
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cur.execute("SELECT player_id FROM Player WHERE name = ? AND email = ? AND password = ?", (name, email, hashed_password))
            result = self.cur.fetchone()
            return bool(result)  # True if verification successful, False otherwise
        except sqlite3.Error as e:
            print(f"Database error during verification: {e}")
            return False

