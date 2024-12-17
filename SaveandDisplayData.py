import json

def saveHistoryForPlayer1(data : dict) -> None:
    needed_data = {
        "your_name" : data["player1_name"],
        "opponent_name": data['player2_name'],
        "time_spent" : data['time_spent'],
        "game_result_for_player1": data["game_result_for_player1"],
        "end_game_date" : data["end_game_date"]
                    }
    try:
        with open(f"history/{data["player1_name"]}.json", 'w') as file:

            json.dump(needed_data, file, indent = 4)

    except:
        print("Something went wrong during save process")


def catchDataForPlayer(name : str) -> dict:
    data = {}
    try:

        with open(f"history/{name}.json") as file:
            data = json.load(file)
    except:

        print("You don't have any gameHistory")

    return data

