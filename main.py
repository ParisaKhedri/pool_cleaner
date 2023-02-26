import time


class Node:
    """class representing a 1*1 square in the pool"""

    def __init__(self, x, y, visited):
        self.x = x # x position
        self.y = y # y position
        #self.visited = None # has the cleaner cleand that square #not sure if it's needed!

    #getters and setters
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_visited(self):
        return self.visited

    def set_visited(self):
        self.visited = True


class Cleaner:
    """
    class representing the cleaner
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = "N"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_direction(self):
        return self.direction

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_direction(self, direction):
        self.direction = direction


def update_cleaner_state(cleaner, x, y, direction):
        cleaner.set_x(x)
        cleaner.set_y(y)
        cleaner.set_direction(direction)


def print_welcome_message():
    """
    This functions prints the programmers welcome message and a description on how the program works!
    :return:
    """

    message = ("Fteen 1000 simulator by Parisa Khedri \n" + " Hi!\n" + "\n" +
               " My name is Parisa Khedri and this is a simple program simulating the movement of a pool cleaner.\n" +
               " The program is written in python and takes strings as input giving the current direction, x and y " +
               "position of the cleaner.\n" + "\n" +
               " This program does not visualize the movement of the cleaner, "
               "it only shows the output in the terminal. \n"
               " The aim is to start at home position (0,0) clean the whole pool and return home where the cleaner can "
               "charge.\n" + "\n" +
               " Please first choose if you want to control the cleaner manually or you want it to clean " +
               "the pool and return home. \n You can whenever you want the the cleaner to return home in manual mode.\n"
               )

    automate_text_message(message)


def automate_text_message(message):
    """
    Prints a single character, then wait for a short amount of time to make the message animated
    :param message:
    :return:
    """
    for character in message:
        print(character, end="", flush=True)
        time.sleep(0.01)


def get_direction_of_cleaner(old_x, old_y, x, y):
    """
    #not sure if this is needed

    :param old_x:
    :param old_y:
    :param x:
    :param y:
    :return:
    """
    if old_y + 1 == y:
        y += 1  # N
        return "N"
    elif old_y - 1 == y:
        return "S"
    elif old_x + 1 == x:
        return"E"
    elif old_x - 1 == x:
        return "W"
    else:
        return "POSITION NOT IN POLL"


def move_along_movement_command(command, cleaner):
    print("moving in manual")

    # direction changes based on turns and current direction
    left_turns = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
    right_turns = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

    y = cleaner.get_y()
    x = cleaner.get_x()
    direction = cleaner.get_direction()

    for c in command:
        if c == 'L':
            direction = left_turns[direction]
        elif c == 'R':
            direction = right_turns[direction]
        elif c == 'A':
            # Move forward in the current direction
            if direction == 'N':
                y += 1
            elif direction == 'E':
                x += 1
            elif direction == 'S':
                y -= 1
            elif direction == 'W':
                x -= 1
        print("Cleaner currently moving: " + direction + " " + str(x) + " " + str(y))
        time.sleep(0.01)
    update_cleaner_state(cleaner, x, y, direction)


def manual(new_cleaner, tiles):

    message = ("Please enter desired movement for the cleaner, for example 'LAARA' where \n" +
               "'l:turn left, r:turn right,a: forward' the movement command can be as long as you want but \n" +
               "consider that the movement should be inside of the pool size otherwise the cleaner would not move")

    automate_text_message(message)

    direction = ""

    while not direction:
        direction = input(" Please enter desired movement, H for going back home to position (0,0) and\n"
                          " E for exiting the program: ")
        if direction == "E":
            break
        elif direction == "H":
            return return_home(tiles, new_cleaner.get_x(), new_cleaner.get_y())
        else:
            move_along_movement_command(direction, new_cleaner)
            direction = ""


def automat(cleaner, tiles):
    print("test automat")
    i = 1

    for row in tiles:

        if i % 2 == 1:
            direction = "W"
            for node in row:
                x = node.get_x()
                y = node.get_y()
                print("Cleaner currently moving automatically: " + direction + " " + str(x) + " " + str(y))
                update_cleaner_state(cleaner, x, y, direction)
                time.sleep(0.2)

        else:
            direction = "E"
            for node in row[::-1]:
                x = node.get_x()
                y = node.get_y()
                print("Cleaner currently moving automatically: " + direction + " " + str(x) + " " + str(y))
                update_cleaner_state(cleaner, x, y, direction)
                time.sleep(0.2)

        direction = "N"
        print("Cleaner currently moving automatically: " + direction + " " + str(x) + " " + str(y))
        update_cleaner_state(cleaner, x, y, direction)
        time.sleep(0.2)

        i+=1

    grid_tiles = []

    for rows in tiles:
        row = []
        for node in rows:
            row.append((node.get_x(), node.get_y()))
        grid_tiles.append(row)
    start_x = cleaner.get_x()
    start_y = cleaner.get_y()

    path = return_home(grid_tiles, start_x, start_y)
    print(path)



def dfs(grid, visited, row, col, path):
    # Check if the current node is within the grid boundaries and is not visited

    if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]) and not visited[row][col]:
        # Mark the current node as visited
        visited[row][col] = True
        # Add the current node to the path
        path.append((row, col))
        # Check if the current node is (0, 0)
        if row == 0 and col == 0:
            return True
        # Recursively explore the neighbors of the current node
        if dfs(grid, visited, row-1, col, path) or dfs(grid, visited, row, col-1, path) or \
                dfs(grid, visited, row+1, col, path) or dfs(grid, visited, row, col+1, path):
            return True
        # If no path to (0, 0) is found from the current node, remove it from the path and mark it as unvisited
        path.pop()
        visited[row][col] = False
    return False


def return_home(tiles, start_x, start_y):
    # Initialize the visited matrix to False for all nodes in the grid
    visited = [[False for _ in range(len(tiles[0]))] for _ in range(len(tiles))]
    # Initialize the path with the starting node
    path = [(start_x, start_y)]
    # Run the depth-first search algorithm to find a path to (0, 0) from the starting node
    dfs(tiles, visited, start_x, start_y, path)
    # Return the path to (0, 0)
    return path


def generate_pool_tiles(x, y):
    """
    this function generates a grid with nodes each node representing a 1 by 1 tile
    in the pool
    :param x:
    :param y:
    :return:
    """

    tiles_list = []

    for i in range(y):
        row = []
        for j in range(x):
            node = Node(j, i, False)
            row.append(node)

        tiles_list.append(row)

    return tiles_list


def main(new_cleaner):
    """
    the main function calling other functions of the program
    :return:
    """

    print_welcome_message()

    pool_size = input("Please enter the size of the pool x*y in meter in following format x, y ex 2 3: ")
    x_str, y_str = pool_size.split()
    x, y = int(x_str), int(y_str)

    pool_tiles = generate_pool_tiles(x, y)

    """
    grid = ""
    for rows in pool_tiles:
        for node in rows:
            grid += "(" + str(node.get_x()) + "," + str(node.get_y()) + ") "
        grid += "\n"


    print(grid)
    """

    mode = ""

    while mode != "A" or mode != "M":
        mode = input("Please enter 'A' for automat mode and 'M' for manual mode," +
                     "enter 'E' if you wish to exit the program: ")
        print(mode)
        if mode == "M":
            manual(new_cleaner, pool_tiles)
            break
        elif mode == "A":
            automat(new_cleaner, pool_tiles)
            break
        elif mode == "E":
            break


if __name__ == '__main__':

    new_cleaner = Cleaner()
    main(new_cleaner)







