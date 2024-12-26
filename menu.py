import os
import json
import re
import SaveandDisplayData
import game

def check_email(email):
    """Check if the email is valid using regex."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def load_user_data(username):
    """Load user data from a JSON file."""
    try:
        with open(f"UserInformation/{username}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def save_user_data(username, data):
    """Save user data to a JSON file."""
    with open(f"UserInformation/{username}.json", "w") as file:
        json.dump(data, file, indent=4)

def sign_up():
    """Sign up a new user."""
    os.system("cls")
    print("\n=== Sign Up ===")
    username = input("Enter a username: ").strip()
    if username == "@":
        return None
    if os.path.exists(f"UserInformation/{username}.json"):
        print("Username already exists. Please log in.")
        return None

    email = input("Enter your email: ").strip()
    if not check_email(email):
        print("Invalid email format. Please try again.")
        return None

    password = input("Enter a password: ").strip()
    while True:
        confirm_password = input("Confirm your password: ").strip()
        if password == confirm_password:
            break
        print("Passwords do not match. Please try again.")

    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "play_time": 0,
        "total_wins": 0,
        "total_losses": 0
    }
    save_user_data(username, user_data)
    print("Account created successfully! You can now log in.")
    return username

def log_in():
    """Log in an existing user."""
    os.system("cls")
    print("\n=== Log In ===")
    username = input("Enter your username: ").strip()
    if username == '@':
        return None
    user_data = load_user_data(username)
    if not user_data:
        print("Username not found. Please sign up.")
        return None

    for _ in range(3):
        password = input("Enter your password: ").strip()
        if password == user_data["password"]:
            print("Login successful!")
            return username
        print("Incorrect password. Please try again.")

    print("Too many failed attempts. Please try again later.")
    return None

def get_second_player(first_player):
    """Get the second player's information and ensure they exist or sign them up."""
    os.system("cls")
    print("\n=== Select Opponent ===")
    while True:
        username = input("Enter the opponent's username: ").strip()
        if username == first_player:
            print("You cannot play against yourself. Please choose a different username.")
            continue

        user_data = load_user_data(username)
        if user_data:
            for _ in range(3):
                password = input("Enter the opponent's password: ").strip()
                if password == user_data["password"]:
                    print(f"{username} successfully authenticated as the second player.")
                    return user_data
                print("Incorrect password. Please try again.")
            print("Too many failed attempts. Returning to opponent selection.")
        else:
            print("Opponent not found. Initiating sign-up for the opponent.")
            email = input("Enter the opponent's email: ").strip()
            if not check_email(email):
                print("Invalid email format. Please try again.")
                continue

            password = input("Enter a password for the opponent: ").strip()
            while True:
                confirm_password = input("Confirm the password: ").strip()
                if password == confirm_password:
                    break
                print("Passwords do not match. Please try again.")

            opponent_data = {
                "username": username,
                "email": email,
                "password": password,
                "play_time": 0,
                "total_wins": 0,
                "total_losses": 0
            }
            save_user_data(username, opponent_data)
            print(f"Opponent {username} has been successfully signed up.")
            return opponent_data

def create_game_history_file(data):
    """Create a game history file for the match."""
    os.system("cls")
    folder_name = "game_history"
    os.makedirs(folder_name, exist_ok=True)
    player1 = data['username']
    player2 = data["username"]
    base_filename = f"{player1}_vs_{player2}"
    filename = base_filename
    counter = 1
    while os.path.exists(os.path.join(folder_name, f"{filename}.json")):
        filename = f"{base_filename}_match_{counter}"
        counter += 1

    filepath = os.path.join(folder_name, f"{filename}.json")
    essentialData = {}
    with open(filepath, "w") as file:
        json.dump(essentialData, file)
    print(f"Game history file created: {filepath}")
    return filepath

def ParhamToSaeed(data1,data2):
    total_data = {
    "player1_name": data1['username'],
    "player2_name": data2['username'],
    "player1_email": data1['email'],
    "player2_email": data2['email'],
    "player1_password" : data1["password"],
    "player2_password" : data2["password"],
    "player1_total_wins" : data1['total_wins'],
    "player2_total_wins" : data2['total_wins'],
    "player1_total_losses" : data1["total_losses"],
    "player2_total_losses" : data2["total_losses"],
    "play_time" : data1['play_time'],
    "player1_loc" : [1,9],
    "player2_loc" : [17,9],
    "number_of_obs1":10,
    "number_if_obs2":10,
    "obstacles_loc" : [],
    "turn" : 0,
    "winner": None,
    "end_game_date" : None,
    "Game_ID" : 1234,
    "table" : []
    }
    return total_data

def SaeedToParham(data):
    player1_data = {
        "username": data["player1_name"],
        "email": data["player1_email"],
        "password": data["player1_password"],
        "play_time": data['play_time'],
        "total_wins": data['player1_total_wins'],
        "total_losses": data["player1_total_losses"]
    }
    player2_data = {
        "username": data["player2_name"],
        "email": data["player2_email"],
        "password": data["player2_password"],
        "play_time": data['play_time'],
        "total_wins": data['player2_total_wins'],
        "total_losses": data["player2_total_losses"]
    }
    return [player1_data, player2_data]
    

def new_game(first_player):
    """Initiate a new game by selecting an opponent."""
    os.system("cls")
    first_player_data = load_user_data(first_player)
    if not first_player_data:
        print("First player data could not be loaded. Please try again.")
        return

    second_player_data = get_second_player(first_player)
    print("\nNew game starting between:")
    print(f"Player 1: {first_player_data['username']}")
    print(f"Player 2: {second_player_data['username']}\n")
    os.system("cls")

    while True:
        user_input = input("Please enter a unique gameID:")
        path = f"Games/{first_player_data['username']}/{second_player_data['username']}/allGames.json"
        dic = {"games" : []}
        if os.path.exists(path):
            with open(path, 'r') as file:
                dic = json.load(file)
        
        if user_input not in dic['games']:
            gameID = user_input
            break
        

    total_data = ParhamToSaeed(first_player_data, second_player_data)
    total_data["Game_ID"] = gameID
    total_data = game.start(total_data)

    if total_data['winner'] is not None:  # Game finished
        # Update winner and loser statistics
        winner_username = total_data['winner']
        loser_username = (first_player_data['username'] if winner_username == second_player_data['username'] else second_player_data['username'])

        # Update play_time for both players
        first_player_data['play_time'] += total_data['play_time']
        second_player_data['play_time'] += total_data['play_time']

        # Save updated play_time
        save_user_data(first_player_data['username'], first_player_data)
        save_user_data(second_player_data['username'], second_player_data)

        # Load and update winner's data
        winner_data = load_user_data(winner_username)
        if winner_data:
            winner_data['total_wins'] += 1
            save_user_data(winner_username, winner_data)

        # Load and update loser's data
        loser_data = load_user_data(loser_username)
        if loser_data:
            loser_data['total_losses'] += 1
            save_user_data(loser_username, loser_data)

        first_player_data, second_player_data = SaeedToParham(total_data)
        create_game_history_file(first_player_data)
    else:
        SaveandDisplayData.saveTotalGame(total_data)

    return first_player_data, second_player_data


def view_leaderboard():
    """View the leaderboard."""
    os.system("cls")
    print("\n=== Leaderboard ===")
    json_files = [f for f in os.listdir('UserInformation') if f.endswith('.json')]
    players = []

    for file in json_files:
        try:
            with open(f"UserInformation/{file}", 'r') as f:
                data = json.load(f)
                if "username" in data and "total_wins" in data and "play_time" in data and "total_losses" in data:
                    players.append(data)
        except (json.JSONDecodeError, FileNotFoundError):
            continue

    if not players:
        print("No users found.")
        input("Press any key to move forward...")
        return

    players.sort(key=lambda x: (-x["total_wins"], x["play_time"], x["total_losses"]))

    print("Rank | Username       | Wins | Play Time | Losses")
    print("--------------------------------------------------")
    for rank, player in enumerate(players, start=1):
        print(f"{rank:<4} | {player['username']:<14} | {player['total_wins']:<4} | {player['play_time']:<9} | {player['total_losses']:<6}")
    input("Press any key to move forward...")

def loadSection(username):
    dic = {'names': []}
    path = f"Games/UniqueNames.json"
    if os.path.exists(path):
        with open(path, 'r') as file:
            dic = json.load(file)
    if username in dic["names"]:
        dic = {'names': []}
        path = f"Games/{username}/opponents.json"
        if os.path.exists(path):
            with open(path, 'r') as file:
                dic = json.load(file)

        if len(dic['opponents']) == 0:
            print("You don't have any saved game")
            return
        else:
            for name in dic['opponents']:
                print(name)
            oponame = input("Enter your opponent's name: ").strip()
            first_player_data = load_user_data(username)
            second_player_data = get_second_player(username)
            path = f"Games/{username}/{oponame}/allGames.json"
            dic = {'games': []}
            if os.path.exists(path):
                with open(path, 'r') as file:
                    dic = json.load(file)

            for i, gameName in enumerate(dic['games']):
                print(f"{i+1}_{gameName}")

            gameID = input("Enter ID of your game: ").strip()

            path = f"Games/{username}/{oponame}/{gameID}.json"
            if os.path.exists(path):
                data = SaveandDisplayData.loadGameData(path)
                total_data = {}
                total_data = game.start(data)
                if total_data['winner'] is not None:  # Game finished
                    # Update winner and loser statistics
                    winner_username = total_data['winner']
                    loser_username = (first_player_data['username'] if winner_username == second_player_data['username'] else second_player_data['username'])

                    # Update play_time for both players
                    first_player_data['play_time'] += total_data['play_time']
                    second_player_data['play_time'] += total_data['play_time']

                    # Save updated play_time
                    save_user_data(first_player_data['username'], first_player_data)
                    save_user_data(second_player_data['username'], second_player_data)

                    # Load and update winner's data
                    winner_data = load_user_data(winner_username)
                    if winner_data:
                        winner_data['total_wins'] += 1
                        save_user_data(winner_username, winner_data)

                    # Load and update loser's data
                    loser_data = load_user_data(loser_username)
                    if loser_data:
                        loser_data['total_losses'] += 1
                        save_user_data(loser_username, loser_data)

                    dic = {"games": []}
                    path = f"Games/{first_player_data['username']}/{second_player_data['username']}/allGames.json"
                    if os.path.exists(path):
                        with open(path, 'r') as file:
                            dic = json.load(file)

                    if total_data["Game_ID"] in dic["games"]:
                        dic["games"].remove(total_data["Game_ID"])
                        with open(path, 'w') as file:
                            json.dump(dic, file)
                        os.remove(f"Games/{first_player_data['username']}/{second_player_data['username']}/{total_data["Game_ID"]}.json")

                


                    dic = {"games": []}
                    path = f"Games/{second_player_data['username']}/{first_player_data['username']}/allGames.json"
                    if os.path.exists(path):
                        with open(path, 'r') as file:
                            dic = json.load(file)

                    if total_data["Game_ID"] in dic["games"]:
                        dic["games"].remove(total_data["Game_ID"])
                        with open(path, 'w') as file:
                            json.dump(dic, file)
                        os.remove(f"Games/{second_player_data['username']}/{first_player_data['username']}/{total_data["Game_ID"]}.json")

                
            

                    first_player_data, second_player_data = SaeedToParham(total_data)
                    create_game_history_file(first_player_data)
                else:
                    SaveandDisplayData.saveTotalGame(total_data)
            else:
                print("sorry Couldn't load data please try again")
#************************************************ PASS THIS TO SALEH's LOGIC FUNCTION***************************************************************************************************************
            

            
            

def main_menu(username):
    """Display the main menu after login or signup."""
    while True:
        os.system("cls")
        print("\n=== Main Menu ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. View Leaderboard")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            new_game(username)
        elif choice == "2":
            loadSection(username)
        elif choice == "3":
            view_leaderboard()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main function to run the program."""
    print("Welcome to Coridor!")
    while True:
        os.system("cls")
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = sign_up()
            if username:
                main_menu(username)
        elif choice == "2":
            username = log_in()
            if username:
                main_menu(username)
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
