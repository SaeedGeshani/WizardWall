import json
import os
def saveHistoryForPlayer1(data : dict) -> None:
    needed_data = {
        "your_name" : data["player1_name"],
        "opponent_name": data['player2_name'],
        "time_spent" : data['time_spent'],
        "game_result_for_player1": data["game_result_for_player1"],
        "end_game_date" : data["end_game_date"],
        "Game_ID" : data["Game_ID"]
                    }
    try:
        with open(f"history/{data["player1_name"]}.json", 'w') as file:

            json.dump(needed_data, file, indent = 4)

    except:
        print("Something went wrong during save process")

def catchDataForPlayer(name : str) -> dict:
    data = {}
    try:

        with open(f"history/{name}.json", 'r') as file:
            data = json.load(file)
    except:

        print("You don't have any gameHistory")

    return data

def saveTotalGame(data):
    
    if not os.path.exists(f"Games/{data["player1_name"]}"):
        os.makedirs(f"Games/{data["player1_name"]}/{data["player2_name"]}")
    elif not os.path.exists(f"Games/{data["player1_name"]}/{data["player2_name"]}"):
        os.makedirs(f"Games/{data["player1_name"]}/{data["player2_name"]}")

    if not os.path.exists(f"Games/{data["player2_name"]}"):
        os.makedirs(f"Games/{data["player2_name"]}/{data["player1_name"]}")
    elif not os.path.exists(f"Games/{data["player2_name"]}/{data["player1_name"]}"):
        os.makedirs(f"Games/{data["player2_name"]}/{data["player1_name"]}")

    path = f"Games/{data["player1_name"]}/{data["player2_name"]}/{data["Game_ID"]}.json"
    with open(path, 'w') as file:
        json.dump(data, file , indent=4)
    path = f"Games/{data["player2_name"]}/{data["player1_name"]}/{data["Game_ID"]}.json"
    with open(path, 'w') as file:
        json.dump(data, file , indent=4)

    path = f"Games/{data["player1_name"]}/opponents.json"
    dic = {}
    if os.path.exists(path):
        with open(path , 'r') as file:
            dic = json.load(file)
    if len(dic) == 0:
        dic['opponents'] = []
    if data["player2_name"] not in dic["opponents"]:
        dic["opponents"].append(data["player2_name"])
    with open(path, 'w') as file:
        json.dump(dic, file, indent = 4)
    path = f"Games/{data["player2_name"]}/opponents.json"
    dic = {}
    if os.path.exists(path):
        with open(path , 'r') as file:
            dic = json.load(file)
    if len(dic) == 0:
        dic['opponents'] = []
    if data["player1_name"] not in dic["opponents"]:
        dic["opponents"].append(data["player1_name"])
    with open(path, 'w') as file:
        json.dump(dic, file, indent = 4)
    dic = {}
    
    with open("Games/UniqueNames.json" , 'r') as file:
        dic = json.load(file)
        if data["player1_name"] not in dic["names"]:
            dic["names"].append(data["player1_name"])
        if data["player2_name"] not in dic["names"]:
            dic["names"].append(data["player2_name"]) 
        
    with open("Games/UniqueNames.json" , 'w') as file:
        json.dump(dic, file, indent = 4)
         
    

    
 

def loadGameData(fileName : str) -> list[list[list[chr]], dict]:
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
                if [i,j] in data["obstacles_loc"]:
                    Table[i][j] = "$"
                elif [i,j] == data["player1_loc"]:
                    Table[i][j] = "1"
                elif [i,j] == data["player2_loc"]:
                    Table[i][j] = "2"
        return [Table, data]

data ={
    "player1_name": "Saeed",
    "player2_name": "Parham",
    "player1_loc" : [2,10],
    "player2_loc" : [4,8],
    "obstacles_loc" : [[1,5],[3,5],[2,9]],
    "turn" : "player1",
    "time_spent" : 0,
    "game_result_for_player1": None,
    "end_game_date" : None,
    "Game_ID" : 1234
}

saveTotalGame(data)

ls = loadGameData("Games/Saeed/Parham/1234.json")


for i in range(17):
    for j in range(17):
        print(ls[0][i][j], end=" ")
    print()