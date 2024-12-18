import msvcrt
import os

players = ["A","B"]

a_coords = [1, 9]
b_coords = [17, 9]
a_name = "A"
b_name = "B"
a_walls = 0
b_walls = 11

empty = "#"

turn = 0

table = []


def change_turn ():
    global turn
    turn = (turn + 1)%len(players)

def getch():
    char = msvcrt.getch()
    if char == b'\x00' or char == b'\xe0':
        # Handle arrow keys
        arrow = msvcrt.getch()
        if arrow == b'H':
            return "up"
        elif arrow == b'P':
            return "down"
    elif char == b'\r':
        return "enter"
    else:
        return char.decode()


def initiate_table():
    global table
    # Create the 19x19 table with initial layout
    table = [["+" if x % 2 == 0 and y % 2 == 0 else " " for x in range(19)] for y in range(19)]

    # Add blocks (#)
    for y in range(1, 18, 2):
        for x in range(1, 18, 2):
            if y // 2 < 9 and x // 2 < 9:
                table[y][x] = "#"

    # Add enclosing walls (- and |)
    # for x in range(1, 18, 2):
    #     table[0][x] = "-"  # Top horizontal wall
    #     table[18][x] = "-"  # Bottom horizontal wall
    for y in range(1, 18, 2):
        table[y][0] = "|"  # Left vertical wall
        table[y][18] = "|"  # Right vertical wall

    # Place players inside blocks
    table[a_coords[0]][a_coords[1]] = a_name
    table[b_coords[0]][b_coords[1]] = b_name


def print_table():
    print("   ", end="")
    for col in range(1, 10):
        print(col, end=" ")
    print()
    
    for row_idx, row in enumerate(table):
        # Print row index
        if row_idx % 2 != 0:
            print(row_idx//2 +1,end=" ")
        else:
            print(end="  ")

        for cell in row:
            if cell == a_name:  # Player A
                print(f"\033[34m{cell}\033[0m", end="")  # Blue
            elif cell == b_name:  # Player B
                print(f"\033[31m{cell}\033[0m", end="")  # Red
            elif cell == "#":  # Marked cell
                print(f"\033[32m{cell}\033[0m", end="")  # Green
            elif cell in "|-+":  # Walls and intersections
                print(f"\033[33m{cell}\033[0m", end="")  # Brown/Yellow
            else:
                print(cell, end="")  # Default
        print()  # Newline after each row
    
    print(f"Walls: \033[34m{a_walls}\033[0m        \033[31m{b_walls}\033[0m")



def move(way) -> bool | None:
    coords = a_coords if turn == 0 else b_coords
    final_coords = [coords[0],coords[1]]
    name = a_name if turn == 0 else b_name
    if way == "Right":
        if table[coords[0]][coords[1] + 1] != "|":
            if table[coords[0]][coords[1] + 2] == empty:
                final_coords = [coords[0],coords[1]+2]
            elif table[coords[0]][coords[1] + 3] != "|":
                final_coords = [coords[0],coords[1]+4]
    elif way == "Up":
        if table[coords[0] - 1][coords[1]] != "-":
            try:
                if table[coords[0] - 2][coords[1]] == empty:
                    final_coords = [coords[0]-2,coords[1]]
                elif table[coords[0] - 3][coords[1]] != "-":
                    final_coords = [coords[0]-4,coords[1]]
            except:
                if turn == 1:
                    return None
                else:
                    return False
    elif way == "Left":
        if table[coords[0]][coords[1] - 1] != "|":
            if table[coords[0]][coords[1] - 2] == empty:
                final_coords = [coords[0],coords[1]-2]
            elif table[coords[0]][coords[1] - 3] != "|":
                final_coords = [coords[0],coords[1]-4]
    elif way == "Down":
        try:
            if table[coords[0] + 1][coords[1]] != "-":
                if table[coords[0] + 2][coords[1]] == empty:
                    final_coords = [coords[0]+2,coords[1]]
                elif table[coords[0] + 3][coords[1]] != "-":
                    final_coords = [coords[0]+4,coords[1]]
        except:
            if turn == 0:
                return None
            else:
                return False
    elif way == "Up-Left":
        try:
            if (table[coords[0] - 1][coords[1]] != "-" and  table[coords[0]-2][coords[1] - 1] != "|") or \
                (table[coords[0]][coords[1] - 1] != "|" and table[coords[0] - 1][coords[1]-2] != "-"):
                if table[coords[0] - 2][coords[1] - 2] == empty:
                    final_coords = [coords[0]-2,coords[1]-2]
                elif (table[coords[0] - 3][coords[1]-2] != "-" and  table[coords[0]-4][coords[1] - 3] != "|") or \
                    (table[coords[0]-2][coords[1] - 3] != "|" and table[coords[0] - 3][coords[1]-4] != "-"):
                    final_coords = [coords[0]-4,coords[1]-4]
        except:
                print("fuck")
                input()
                if turn == 1:
                    return None
                else:
                    return False

    elif way == "Up-Right":
        try:
            if (table[coords[0] - 1][coords[1]] != "-" and table[coords[0] - 2][coords[1] + 1] != "|") or \
               (table[coords[0]][coords[1] + 1] != "|" and table[coords[0] - 1][coords[1] + 2] != "-"):
                if table[coords[0] - 2][coords[1] + 2] == empty:
                    final_coords = [coords[0] - 2, coords[1] + 2]
                elif (table[coords[0] - 3][coords[1] + 2] != "-" and table[coords[0] - 4][coords[1] + 3] != "|") or \
                     (table[coords[0] - 2][coords[1] + 3] != "|" and table[coords[0] - 3][coords[1] + 4] != "-"):
                    final_coords = [coords[0] - 4, coords[1] + 4]
        except:
            if turn == 1:
                return None
            else:
                return False
    elif way == "Down-Left":
        try:
            if (table[coords[0] + 1][coords[1]] != "-" and table[coords[0] + 2][coords[1] - 1] != "|") or \
               (table[coords[0]][coords[1] - 1] != "|" and table[coords[0] + 1][coords[1] - 2] != "-"):
                if table[coords[0] + 2][coords[1] - 2] == empty:
                    final_coords = [coords[0] + 2, coords[1] - 2]
                elif (table[coords[0] + 3][coords[1] - 2] != "-" and table[coords[0] + 4][coords[1] - 3] != "|") or \
                     (table[coords[0] + 2][coords[1] - 3] != "|" and table[coords[0] + 3][coords[1] - 4] != "-"):
                    final_coords = [coords[0] + 4, coords[1] - 4]
        except:
            if turn == 0:
                return None
            else:
                return False
            
    elif way == "Down-Right":
        try:
            if (table[coords[0] + 1][coords[1]] != "-" and table[coords[0] + 2][coords[1] + 1] != "|") or \
               (table[coords[0]][coords[1] + 1] != "|" and table[coords[0] + 1][coords[1] + 2] != "-"):
                if table[coords[0] + 2][coords[1] + 2] == empty:
                    final_coords = [coords[0] + 2, coords[1] + 2]
                elif (table[coords[0] + 3][coords[1] + 2] != "-" and table[coords[0] + 4][coords[1] + 3] != "|") or \
                     (table[coords[0] + 2][coords[1] + 3] != "|" and table[coords[0] + 3][coords[1] + 4] != "-"):
                    final_coords = [coords[0] + 4, coords[1] + 4]
        except:
            if turn == 0:
                return None
            else:
                return False


    if (final_coords[0] < 0 and turn == 1) or (final_coords[0] > 18 and turn == 0):
        table[coords[0]][coords[1]] = empty
        return None
    elif not 0<=final_coords[0]<=18:
        return False
    elif final_coords != coords:
        table[coords[0]][coords[1]] = empty
        coords[0], coords[1] = final_coords
        table[coords[0]][coords[1]] = name
        return True
    else:
        return False
    

def add_wall(coords, dir, way) -> bool: 
    coords = [coords[0]*2 -1,coords[1]*2-1]
    if dir == "right":
        if coords[1] + 1 >= 19 or table[coords[0]][coords[1] + 1] == "|":
            return False

        if way == "up" and coords[0] - 2 >= 0 and table[coords[0] - 2][coords[1] + 1] != "|":
            table[coords[0]][coords[1] + 1] = "|"
            table[coords[0] - 2][coords[1] + 1] = "|"
            return True
        elif way == "down" and coords[0] + 2 < 19 and table[coords[0] + 2][coords[1] + 1] != "|":
            table[coords[0]][coords[1] + 1] = "|"
            table[coords[0] + 2][coords[1] + 1] = "|"
            return True

        return False

    elif dir == "left":
        if coords[1] - 1 < 0 or table[coords[0]][coords[1] - 1] == "|":
            return False

        if way == "up" and coords[0] - 2 >= 0 and table[coords[0] - 2][coords[1] - 1] != "|":
            table[coords[0]][coords[1] - 1] = "|"
            table[coords[0] - 2][coords[1] - 1] = "|"
            return True
        elif way == "down" and coords[0] + 2 < 19 and table[coords[0] + 2][coords[1] - 1] != "|":
            table[coords[0]][coords[1] - 1] = "|"
            table[coords[0] + 2][coords[1] - 1] = "|"
            return True

        return False

    elif dir == "up":
        if coords[0] - 1 < 0 or table[coords[0] - 1][coords[1]] == "-":
            return False

        if way == "right" and coords[1] + 2 < 19 and table[coords[0] - 1][coords[1] + 2] != "-":
            table[coords[0] - 1][coords[1]] = "-"
            table[coords[0] - 1][coords[1] + 2] = "-"
            return True
        elif way == "left" and coords[1] - 2 >= 0 and table[coords[0] - 1][coords[1] - 2] != "-":
            table[coords[0] - 1][coords[1]] = "-"
            table[coords[0] - 1][coords[1] - 2] = "-"
            return True

        return False

    elif dir == "down":
        if coords[0] + 1 >= 19 or table[coords[0] + 1][coords[1]] == "-":
            return False

        if way == "right" and coords[1] + 2 < 19 and table[coords[0] + 1][coords[1] + 2] != "-":
            table[coords[0] + 1][coords[1]] = "-"
            table[coords[0] + 1][coords[1] + 2] = "-"
            return True
        elif way == "left" and coords[1] - 2 >= 0 and table[coords[0] + 1][coords[1] - 2] != "-":
            table[coords[0] + 1][coords[1]] = "-"
            table[coords[0] + 1][coords[1] - 2] = "-"
            return True

        return False

def remove_wall(coords, dir, way):
    coords = [coords[0]*2 - 1, coords[1]*2 - 1]
    if dir == "right":
        if coords[1] + 1 < 19:
            table[coords[0]][coords[1] + 1] = " "
            if way == "up" and coords[0] - 2 >= 0:
                table[coords[0] - 2][coords[1] + 1] = " "
            elif way == "down" and coords[0] + 2 < 19:
                table[coords[0] + 2][coords[1] + 1] = " "

    elif dir == "left":
        if coords[1] - 1 >= 0:
            table[coords[0]][coords[1] - 1] = " "
            if way == "up" and coords[0] - 2 >= 0:
                table[coords[0] - 2][coords[1] - 1] = " "
            elif way == "down" and coords[0] + 2 < 19:
                table[coords[0] + 2][coords[1] - 1] = " "

    elif dir == "up":
        if coords[0] - 1 >= 0:
            table[coords[0] - 1][coords[1]] = " "
            if way == "right" and coords[1] + 2 < 19:
                table[coords[0] - 1][coords[1] + 2] = " "
            elif way == "left" and coords[1] - 2 >= 0:
                table[coords[0] - 1][coords[1] - 2] = " "

    elif dir == "down":
        if coords[0] + 1 < 19:
            table[coords[0] + 1][coords[1]] = " "
            if way == "right" and coords[1] + 2 < 19:
                table[coords[0] + 1][coords[1] + 2] = " "
            elif way == "left" and coords[1] - 2 >= 0:
                table[coords[0] + 1][coords[1] - 2] = " "

    
initiate_table()

def choose(options):
    idx = 0
    while True:
        os.system("cls")
        print_table()
        print()

        print(f"It's {players[turn]}'s Turn:")
        for _,option in enumerate(options):
            if _ == idx:
                print(f"\033[34m- {option}\033[0m")
            else:
                print(f"- {option}")
        
        inp = getch()
        if inp == "up":
            idx = (idx -1) % len(options)
        elif inp == "down":
            idx = (idx + 1) % len(options)
        elif inp == "enter":
            break

    return idx

def warn(message):
    os.system("cls")
    print(message)
    getch()


def dfs(coords, player_turn):
    stack = [(coords[0], coords[1])]
    visited = set()

    while stack:
        checking = stack.pop()  

        if checking not in visited:
            visited.add(checking)

            # Check Up
            if checking[0] - 1 >= 0 and table[checking[0] - 1][checking[1]] != "-":
                if checking[0] == 1 and player_turn == 1:  # Player 1 reaches top goal
                    return True
                if (checking[0] - 2, checking[1]) not in visited and checking[0] - 2 >= 0:
                    stack.append((checking[0] - 2, checking[1]))

            # Check Down
            if checking[0] + 1 <= 18 and table[checking[0] + 1][checking[1]] != "-":
                if checking[0] == 17 and player_turn == 0:  # Player 0 reaches bottom goal
                    return True
                if (checking[0] + 2, checking[1]) not in visited and checking[0] + 2 <= 17:
                    stack.append((checking[0] + 2, checking[1]))

            # Check Right
            if checking[1] + 1 <= 18 and table[checking[0]][checking[1] + 1] != "|" and \
               (checking[0], checking[1] + 2) not in visited and checking[1] + 2 <= 17:
                stack.append((checking[0], checking[1] + 2))

            # Check Left
            if checking[1] - 1 >= 0 and table[checking[0]][checking[1] - 1] != "|" and \
               (checking[0], checking[1] - 2) not in visited and checking[1] - 2 >= 0:
                stack.append((checking[0], checking[1] - 2))

    return False


def check_wall(coords,dir,way):
    if not add_wall(coords,dir,way):
        return False
   
    if dfs(a_coords,0) and dfs(b_coords,1):
        return True
    
    remove_wall(coords,dir,way)
    return False


    



ended = False

def move_menu():
    global ended
    while True:
        options = ["Up","Left","Down","Right","Up-Right","Up-Left","Down-Right","Down-Left","Back"]
        choice = choose(options)
        if choice == len(options) -1 :
            break
        
        # try:
        res = move(options[choice])
        
        if res == False :
            warn("Not A Valid Move")
        elif res == None:
            ended = True
            break
        else:
            change_turn()
            break

def wall_menu():
    global a_walls,b_walls

    if (turn == 0 and a_walls <= 0) or (turn == 1 and b_walls <= 0):
        warn("No More Walls")
        return 

    while True:
        os.system("cls")
        print_table()
        print()
        coords = []
        try:
            inp = input("Where Do You Want To Wall (-1 to go back), (example: 1,1): ")
            if inp == -1:
                break
            coords = [int(x) for x in inp.split(",")]
            if not 1 <= coords[0] <= 9 or not 1 <= coords[1] <=9:
                warn("Input Valid Coords")
                continue
        except:
            warn("Input Valid Coords")
            continue
        options = ["Left","Right","Up","Down","Back"]
        choice = choose(options)
        if choice == len(options) -1:
            break
        dir = options[choice].lower()
        way = ""
        if dir == "left" or dir == "right":
            options = ["Up","Down","Back"]
            choice = choose(options)
            if choice == len(options) -1 :
                break
            way = options[choice].lower()
        else:
            options = ["Left","Right","Back"]
            choice = choose(options)
            if choice == len(options) -1 :
                break
            way = options[choice].lower()
        if check_wall(coords,dir,way):
            if turn == 0:
                a_walls -=1
            else:
                b_walls -=1
            change_turn()
            break
        else:
            warn("Wall Not Valid")


while not ended:
    options = ["Move","Wall"]
    choice = choose(options)
    if choice == 0:
        move_menu()
    elif choice ==1 :
        wall_menu()

            
print(f"{players[turn]} Won!")
getch()



