import os
import json
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print

import SaveandDisplayData
import game

console = Console()

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
    console.clear()
    console.print(Panel("[bold green]Sign Up[/bold green]", expand=False))
    username = Prompt.ask("Enter a username")
    if username == "@":
        return None
    if os.path.exists(f"UserInformation/{username}.json"):
        console.print("[red]Username already exists. Please log in.[/red]")
        return None

    email = Prompt.ask("Enter your email")
    if not check_email(email):
        console.print("[red]Invalid email format. Please try again.[/red]")
        return None

    password = Prompt.ask("Enter a password", password=True)
    while True:
        confirm_password = Prompt.ask("Confirm your password", password=True)
        if password == confirm_password:
            break
        console.print("[red]Passwords do not match. Please try again.[/red]")

    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "play_time": 0,
        "total_wins": 0,
        "total_losses": 0
    }
    save_user_data(username, user_data)
    console.print("[green]Account created successfully! You can now log in.[/green]")
    return username

def log_in():
    """Log in an existing user."""
    console.clear()
    console.print(Panel("[bold green]Log In[/bold green]", expand=False))
    username = Prompt.ask("Enter your username")
    if username == '@':
        return None
    user_data = load_user_data(username)
    if not user_data:
        console.print("[red]Username not found. Please sign up.[/red]")
        return None

    for _ in range(3):
        password = Prompt.ask("Enter your password", password=True)
        if password == user_data["password"]:
            console.print("[green]Login successful![/green]")
            return username
        console.print("[red]Incorrect password. Please try again.[/red]")

    console.print("[red]Too many failed attempts. Please try again later.[/red]")
    return None

def view_leaderboard():
    """View the leaderboard."""
    console.clear()
    console.print(Panel("[bold green]Leaderboard[/bold green]", expand=False))
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
        console.print("[red]No users found.[/red]")
        Prompt.ask("Press any key to move forward...")
        return

    players.sort(key=lambda x: (-x["total_wins"], x["play_time"], x["total_losses"]))

    table = Table(title="Leaderboard")
    table.add_column("Rank", justify="right", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Wins", justify="right", style="green")
    table.add_column("Play Time", justify="right", style="blue")
    table.add_column("Losses", justify="right", style="red")

    for rank, player in enumerate(players, start=1):
        table.add_row(
            str(rank),
            player['username'],
            str(player['total_wins']),
            str(player['play_time']),
            str(player['total_losses'])
        )

    console.print(table)
    Prompt.ask("Press any key to move forward...")

def main_menu(username):
    """Display the main menu after login or signup."""
    while True:
        console.clear()
        console.print(Panel(f"[bold green]Main Menu - Logged in as {username}[/bold green]", expand=False))
        options = {
            "1": "New Game",
            "2": "Load Game",
            "3": "View Leaderboard",
            "4": "Exit"
        }

        for key, value in options.items():
            console.print(f"[bold cyan]{key}.[/bold cyan] {value}")

        choice = Prompt.ask("Choose an option")

        if choice == "1":
            new_game(username)
        elif choice == "2":
            loadSection(username)
        elif choice == "3":
            view_leaderboard()
        elif choice == "4":
            console.print("[green]Exiting the program. Goodbye![/green]")
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")

def main():
    """Main function to run the program."""
    console.print(Panel("[bold green]Welcome to Coridor![/bold green]", expand=False))
    while True:
        console.clear()
        console.print(Panel("[bold green]Coridor Game[/bold green]", expand=False))
        options = {
            "1": "Sign Up",
            "2": "Log In",
            "3": "Exit"
        }

        for key, value in options.items():
            console.print(f"[bold cyan]{key}.[/bold cyan] {value}")

        choice = Prompt.ask("Choose an option")

        if choice == "1":
            username = sign_up()
            if username:
                main_menu(username)
        elif choice == "2":
            username = log_in()
            if username:
                main_menu(username)
        elif choice == "3":
            console.print("[green]Goodbye![/green]")
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")

if __name__ == "__main__":
    main()
