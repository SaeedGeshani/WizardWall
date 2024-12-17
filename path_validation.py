destination1 = [[0,0],[0,2],[0,4],[0,6],[0,8],[0,10],[0,12],[0,14],[0,16]]              #Goal state for player1
destination2 = [[16,0],[16,2],[16,4],[16,6],[16,8],[16,10],[16,12],[16,14],[16,16]]     #Goal state for player2
visited1 = []
visited2 = []

def find_adjs1(Table : list[list[chr]], current : list[int,int]) -> list[list[int,int]]:    #This functions finds neighbors
    adjs = []
    if current[0]-2 >= 0 and Table[current[0]-1][current[1]] not in ["|","__"]:
        adjs.append([current[0]-2, current[1]])
    if current[1]+2 < 17 and Table[current[0]][current[1]+1] not in ["|","__"]:
        adjs.append([current[0], current[1]+2])
    if current[1]-2 >= 0 and Table[current[0]][current[1]-1] not in ["|","__"]:
        adjs.append([current[0], current[1]-2])
    if current[0]+2 < 17 and Table[current[0]+1][current[1]] not in ["|","__"]:
        adjs.append([current[0]+2, current[1]])

    return adjs

def find_adjs2(Table : list[list[chr]], current : list[int,int]) -> list[list[int,int]]:    #This function finds neighbors too
    adjs = []
    if current[0]+2 < 17 and Table[current[0]+1][current[1]] not in ["|","__"]:
        adjs.append([current[0]+2, current[1]])
    if current[1]+2 < 17 and Table[current[0]][current[1]+1] not in ["|","__"]:
        adjs.append([current[0], current[1]+2])
    if current[1]-2 >= 0 and Table[current[0]][current[1]-1] not in ["|","__"]:
        adjs.append([current[0], current[1]-2])
    if current[0]-2 >= 0 and Table[current[0]-1][current[1]] not in ["|","__"]:
        adjs.append([current[0]-2, current[1]])
    
    return adjs

def dfs1(Table : list[list[chr]], current: list[int,int]) -> bool:                          #DFS to check if a path exists for player1                
    if current in destination1:
        visited1.clear()
        return True
    else:
        visited1.append(current)
        adjs = find_adjs1(Table, current)
        answer = False
        for adj in adjs:
            if adj not in visited1:
                answer = answer or dfs1(Table, adj)
        return answer
    
def dfs2(Table : list[list[chr]], current : list[int,int]) -> bool:                         #DFS to check if a path exists for player2
    if current in destination2:
        visited2.clear()
        return True
    else:
        visited2.append(current)
        adjs = find_adjs2(Table, current)
        answer = False
        for adj in adjs:
            if adj not in visited2:
                answer = answer or dfs2(Table, adj)
        return answer

def ExistValidPath(Table, player1 : list[int,int], player2 : list[int,int], obstacle_place : list[int,int]) -> bool:        #Return if you can put obstacle in that location or not
    copyOfTable = Table[:]
    copyOfTable[obstacle_place[0]][obstacle_place[1]] = "|"
    ans =  dfs1(copyOfTable, player1) and dfs2(copyOfTable, player2)
    visited1.clear()
    visited2.clear()
    return ans
    
Table = [

        ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', ''],
        ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', ''],
        ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', ''],
        ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', ''],
        ['#', '', '#', '', '#', '', '2', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', ''],
        ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', ''],
        ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', ''],
        ['#', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#'],
        ['|', '|', '|', '|', '|', '|', '|', '|', '', '', '', '','', '', '', '', ''],
        ['1', '', '#', '', '#', '', '#', '', '#', '', '#', '','#', '', '#', '', '#']
]


for i in range(17):
    for j in range(17):
        print(Table[i][j], end="  ")
    print()

print(ExistValidPath(Table, [16, 0], [8, 6], [16,7]))