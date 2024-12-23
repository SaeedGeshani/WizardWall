import json
import os

def saveHistoryForPlayer1(data: dict) -> None:
    needed_data = {
        "your_name": data["player1_name"],
        "opponent_name": data['player2_name'],
        "time_spent": data['time_spent'],
        "game_result_for_player1": data["game_result_for_player1"],
        "end_game_date": data["end_game_date"],
        "Game_ID": data["Game_ID"]
    }
    try:
        with open(f"history/{data['player1_name']}.json", 'w') as file:
            json.dump(needed_data, file, indent=4)
    except Exception as e:
        print(f"Something went wrong during save process: {e}")

def catchDataForPlayer(name: str) -> dict:
    data = {}
    try:
        with open(f"history/{name}.json", 'r') as file:
            data = json.load(file)
    except:
        print("You don't have any game history")
    return data

def makeSureNestedFolderExists(data):
    if not os.path.exists(f"Games/{data['player1_name']}"):
        os.makedirs(f"Games/{data['player1_name']}/{data['player2_name']}")
    elif not os.path.exists(f"Games/{data['player1_name']}/{data['player2_name']}"):
        os.makedirs(f"Games/{data['player1_name']}/{data['player2_name']}")

    if not os.path.exists(f"Games/{data['player2_name']}"):
        os.makedirs(f"Games/{data['player2_name']}/{data['player1_name']}")
    elif not os.path.exists(f"Games/{data['player2_name']}/{data['player1_name']}"):
        os.makedirs(f"Games/{data['player2_name']}/{data['player1_name']}")

def fillDataInNestedFolder(data):
    path = f"Games/{data['player1_name']}/{data['player2_name']}/{data['Game_ID']}.json"
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
    path = f"Games/{data['player2_name']}/{data['player1_name']}/{data['Game_ID']}.json"
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def makeFileOfOpponents(data):
    path = f"Games/{data['player1_name']}/opponents.json"
    dic = {}
    if os.path.exists(path):
        with open(path, 'r') as file:
            dic = json.load(file)
    if len(dic) == 0:
        dic['opponents'] = []
    if data["player2_name"] not in dic["opponents"]:
        dic["opponents"].append(data["player2_name"])
    with open(path, 'w') as file:
        json.dump(dic, file, indent=4)
    path = f"Games/{data['player2_name']}/opponents.json"
    dic = {}
    if os.path.exists(path):
        with open(path, 'r') as file:
            dic = json.load(file)
    if len(dic) == 0:
        dic['opponents'] = []
    if data["player1_name"] not in dic["opponents"]:
        dic["opponents"].append(data["player1_name"])
    with open(path, 'w') as file:
        json.dump(dic, file, indent=4)

def updateUniqueNamesInGamesFolder(data):
    dic = {'names': []}
    path = "Games/UniqueNames.json"
    if os.path.exists(path):
        with open(path, 'r') as file:
            dic = json.load(file)
    if data["player1_name"] not in dic["names"]:
        dic["names"].append(data["player1_name"])
    if data["player2_name"] not in dic["names"]:
        dic["names"].append(data["player2_name"])
    with open(path, 'w') as file:
        json.dump(dic, file, indent=4)

def updateAllGameBetweenTwoPlayers(data):
    path = f"Games/{data['player1_name']}/{data['player2_name']}/allGames.json"
    dic = {"games": []}
    if os.path.exists(path):
        with open(path, 'r') as file:
            dic = json.load(file)
    if data["Game_ID"] not in dic["games"]:
        dic["games"].append(data["Game_ID"])
    with open(path, 'w') as file:
        json.dump(dic, file, indent=4)
    path = f"Games/{data['player2_name']}/{data['player1_name']}/allGames.json"
    dic = {"games": []}
    if os.path.exists(path):
        with open(path, 'r') as file:
            dic = json.load(file)
    if data["Game_ID"] not in dic["games"]:
        dic["games"].append(data["Game_ID"])
    with open(path, 'w') as file:
        json.dump(dic, file, indent=4)

def saveTotalGame(data):
    makeSureNestedFolderExists(data)
    fillDataInNestedFolder(data)
    makeFileOfOpponents(data)
    updateUniqueNamesInGamesFolder(data)
    updateAllGameBetweenTwoPlayers(data)

def loadGameData(fileName: str) -> list:
    data = {}
    try:
        with open(fileName, 'r') as file:
            data = json.load(file)
    except:
        print("There isn't anything to load")
    if len(data) > 0:
        Table = [['#' if i % 2 == 0 else '' for i in range(17)] if j % 2 == 0 else ["" for _ in range(17)] for j in range(17)]
        for i in range(17):
            for j in range(17):
                if [i, j] in data["obstacles_loc"]:
                    Table[i][j] = "$"
                elif [i, j] == data["player1_loc"]:
                    Table[i][j] = "1"
                elif [i, j] == data["player2_loc"]:
                    Table[i][j] = "2"
        return [Table, data]
