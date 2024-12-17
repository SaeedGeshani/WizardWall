import os
import json
import re

def check_email(email):
    """Check if the email is valid using regex."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def load_user_data(username):
    """Load user data from a JSON file."""
    try:
        with open(f"{username}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def save_user_data(username, data):
    """Save user data to a JSON file."""
    with open(f"{username}.json", "w") as file:
        json.dump(data, file, indent=4)

def sign_up():
    """Sign up a new user."""
    print("\n=== Sign Up ===")
    username = input("Enter a username: ").strip()
    if os.path.exists(f"{username}.json"):
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
    print("\n=== Log In ===")
    username = input("Enter your username: ").strip()
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

def new_game(first_player):
    """Initiate a new game by selecting an opponent."""
    first_player_data = load_user_data(first_player)
    if not first_player_data:
        print("First player data could not be loaded. Please try again.")
        return

    second_player_data = get_second_player(first_player)
    print("\nNew game starting between:")
    print(f"Player 1: {first_player_data['username']}")
    print(f"Player 2: {second_player_data['username']}")

    # Placeholder for game logic
    return first_player_data, second_player_data

def view_leaderboard():
    """View the leaderboard."""
    print("\n=== Leaderboard ===")
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    players = []

    for file in json_files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                if "username" in data and "total_wins" in data and "play_time" in data and "total_losses" in data:
                    players.append(data)
        except (json.JSONDecodeError, FileNotFoundError):
            continue

    if not players:
        print("No users found.")
        return

    players.sort(key=lambda x: (-x["total_wins"], x["play_time"], x["total_losses"]))

    print("Rank | Username       | Wins | Play Time | Losses")
    print("--------------------------------------------------")
    for rank, player in enumerate(players, start=1):
        print(f"{rank:<4} | {player['username']:<14} | {player['total_wins']:<4} | {player['play_time']:<9} | {player['total_losses']:<6}")

def main_menu(username):
    """Display the main menu after login or signup."""
    while True:
        print("\n=== Main Menu ===")
        print("1. New Game")
        print("2. View Leaderboard")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            new_game(username)
        elif choice == "2":
            view_leaderboard()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            return  # Exit the main menu loop
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main function to run the program."""
    print("Welcome to Coridor!")
    while True:
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
            return  # Exit the program loop
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
