import math
import time
import heapq



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


def get_direction_of_cleaner(direction, old_x, old_y, x, y):
    """
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
        return direction


def valid_point(node, grid_nodes):
    if node in grid_nodes:
        return True
    else:
        return False


def move_along_movement_command(command, cleaner, grid_nodes):

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
        # ignoring command if out of bounderies
        if valid_point((x, y), grid_nodes):
            print("Cleaner currently moving: " + direction + " " + str(x) + " " + str(y))
            time.sleep(0.01)
            update_cleaner_state(cleaner, x, y, direction)
        else:
            print("skipping command out of bounderies of poll")
            time.sleep(0.01)
            continue



def manual(cleaner, tiles):

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
            grid_nodes = get_nodes(tiles)
            return_home(cleaner, grid_nodes, (cleaner.get_x(), cleaner.get_y()))
        else:
            grid_nodes = get_nodes(tiles)
            move_along_movement_command(direction, cleaner, grid_nodes)
            direction = ""


def return_home(cleaner, tiles, start_node):
    goal_node = (0, 0)
    path = astar(start_node, goal_node, tiles)
    for node in path:
        x = node[0]
        y = node[1]
        direction = get_direction_of_cleaner(cleaner.get_direction(), cleaner.get_x(), cleaner.get_y(), x, y)
        update_cleaner_state(cleaner, node[0], node[1], direction)
        print("Cleaner currently moving back home: " + direction + " " + str(x) + " " + str(y))
        time.sleep(0.01)




def heuristic(node, goal):
    """Function calculates euclidean distance between the two points"""
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5


def get_neighbors(node, nodes):
    """function getting the neighboring nodes of the current node"""
    neighbors = []
    for n in nodes:
        if (n[0] == node[0] and abs(n[1] - node[1]) == 1) or (n[1] == node[1] and abs(n[0] - node[0]) == 1):
            neighbors.append(n)
    return neighbors


def astar(start, goal, nodes):
    """
    A* search
    """
    # Initialize data structures
    open_set = []
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    # Add start node to open set
    heapq.heappush(open_set, (f_score[start], start))

    # Run A* search
    while open_set:
        current = heapq.heappop(open_set)[1]

        # Check if goal node reached
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path))

        # Add current node to closed set
        closed_set.add(current)

        # Explore neighboring nodes
        for neighbor in get_neighbors(current, nodes):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if neighbor not in [n[1] for n in open_set] or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # No path found
    return None


def get_nodes(tiles):
    """
    function creating
    """

    grid_tiles = []

    for rows in tiles:
        for node in rows:
            grid_tiles.append((node.get_x(), node.get_y()))
    return grid_tiles


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

    print("cleaner done cleaning returning home (0,0)")
    grid_tiles = get_nodes(tiles)
    return_home(cleaner, grid_tiles, (cleaner.get_x(), cleaner.get_y()))


def generate_pool_tiles(x, y):
    """
    this function generates a grid with nodes each node representing a 1 by 1 tile
    in the pool
    """

    tiles_list = []

    for i in range(y):
        row = []
        for j in range(x):
            node = Node(j, i, False)
            row.append(node)

        tiles_list.append(row)

    return tiles_list


def main(cleaner):
    """
    the main function calling other functions of the program
    :return:
    """

    print_welcome_message()

    pool_size = input("Please enter the size of the pool x*y in meter in following format x, y ex 2 3: ")
    x_str, y_str = pool_size.split()
    x, y = int(x_str), int(y_str)

    pool_tiles = generate_pool_tiles(x, y)

    mode = ""

    while mode != "A" or mode != "M":
        mode = input("Please enter 'A' for automat mode and 'M' for manual mode," +
                     "enter 'E' if you wish to exit the program: ")
        print(mode)
        if mode == "M":
            manual(cleaner, pool_tiles)
            break
        elif mode == "A":
            automat(cleaner, pool_tiles)
            break
        elif mode == "E":
            break


if __name__ == '__main__':
    new_cleaner = Cleaner()
    main(new_cleaner)












