import os
a_coords = [1, 9]
b_coords = [17, 9]
a_name = "a"
b_name = "b"
a_walls = 11
b_walls = 11

empty = "#"

turn = 0

table = []

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



def move(way) -> bool | None:
    coords = a_coords if turn == 0 else b_coords
    final_coords = [coords[0],coords[1]]
    name = a_name if turn == 0 else b_name
    if way == "right":
        if table[coords[0]][coords[1] + 1] != "|":
            if table[coords[0]][coords[1] + 2] == empty:
                final_coords = [coords[0],coords[1]+2]
            elif table[coords[0]][coords[1] + 3] != "|":
                final_coords = [coords[0],coords[1]+4]

    elif way == "up":
        if table[coords[0] - 1][coords[1]] != "-":
            if table[coords[0] - 2][coords[1]] == empty:
                final_coords = [coords[0]-2,coords[1]]
            elif table[coords[0] - 3][coords[1]] != "-":
                final_coords = [coords[0]-4,coords[1]]

    elif way == "left":
        if table[coords[0]][coords[1] - 1] != "|":
            if table[coords[0]][coords[1] - 2] == empty:
                final_coords = [coords[0],coords[1]-2]
            elif table[coords[0]][coords[1] - 3] != "|":
                final_coords = [coords[0],coords[1]-4]

    elif way == "down":
        if table[coords[0] + 1][coords[1]] != "-":
            if table[coords[0] + 2][coords[1]] == empty:
                final_coords = [coords[0]+2,coords[1]]
            elif table[coords[0] + 3][coords[1]] != "-":
                final_coords = [coords[0]+4,coords[1]]
    
    elif way == "up_left":
        if (table[coords[0] - 1][coords[1]] != "-" and  table[coords[0]-2][coords[1] - 1] != "|") or \
            (table[coords[0]][coords[1] - 1] != "|" and table[coords[0] - 1][coords[1]-2] != "-"):
            if table[coords[0] - 2][coords[1] - 2] == empty:
                final_coords = [coords[0]-2,coords[1]-2]
            elif (table[coords[0] - 3][coords[1]-2] != "-" and  table[coords[0]-4][coords[1] - 3] != "|") or \
                (table[coords[0]-2][coords[1] - 3] != "|" and table[coords[0] - 3][coords[1]-4] != "-"):
                final_coords = [coords[0]-4,coords[1]-4]

    elif way == "up_right":
        if (table[coords[0] - 1][coords[1]] != "-" and table[coords[0] - 2][coords[1] + 1] != "|") or \
           (table[coords[0]][coords[1] + 1] != "|" and table[coords[0] - 1][coords[1] + 2] != "-"):
            if table[coords[0] - 2][coords[1] + 2] == empty:
                final_coords = [coords[0] - 2, coords[1] + 2]
            elif (table[coords[0] - 3][coords[1] + 2] != "-" and table[coords[0] - 4][coords[1] + 3] != "|") or \
                 (table[coords[0] - 2][coords[1] + 3] != "|" and table[coords[0] - 3][coords[1] + 4] != "-"):
                final_coords = [coords[0] - 4, coords[1] + 4]
    
    elif way == "down_left":
        if (table[coords[0] + 1][coords[1]] != "-" and table[coords[0] + 2][coords[1] - 1] != "|") or \
           (table[coords[0]][coords[1] - 1] != "|" and table[coords[0] + 1][coords[1] - 2] != "-"):
            if table[coords[0] + 2][coords[1] - 2] == empty:
                final_coords = [coords[0] + 2, coords[1] - 2]
            elif (table[coords[0] + 3][coords[1] - 2] != "-" and table[coords[0] + 4][coords[1] - 3] != "|") or \
                 (table[coords[0] + 2][coords[1] - 3] != "|" and table[coords[0] + 3][coords[1] - 4] != "-"):
                final_coords = [coords[0] + 4, coords[1] - 4]
    
    elif way == "down_right":
        if (table[coords[0] + 1][coords[1]] != "-" and table[coords[0] + 2][coords[1] + 1] != "|") or \
           (table[coords[0]][coords[1] + 1] != "|" and table[coords[0] + 1][coords[1] + 2] != "-"):
            if table[coords[0] + 2][coords[1] + 2] == empty:
                final_coords = [coords[0] + 2, coords[1] + 2]
            elif (table[coords[0] + 3][coords[1] + 2] != "-" and table[coords[0] + 4][coords[1] + 3] != "|") or \
                 (table[coords[0] + 2][coords[1] + 3] != "|" and table[coords[0] + 3][coords[1] + 4] != "-"):
                final_coords = [coords[0] + 4, coords[1] + 4]
    

    if (final_coords[0] < 0 and turn == 1) or (final_coords[0] > 18 and turn == 0):
        table[coords[0]][coords[1]] = empty
        return None
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



for i in range(10):
    print_table()
    input()
    if move("right") != True:
        break
    os.system("cls")



