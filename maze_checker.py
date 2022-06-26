
from stack_array import Stack

def is_solvable(the_maze):

    search_locations = Stack()
    search_locations.push(find_start(the_maze))

    while not search_locations.is_empty():

        #print_maze(the_maze)
        #input()
        
        row, col = search_locations.pop()
        if the_maze[row][col] == "!":
            print_maze(the_maze)
            return True
        the_maze[row][col] = "X"
        # check left
        process_coordinate(the_maze,row,col-1,search_locations)
        # check down
        process_coordinate(the_maze,row+1,col,search_locations)
        # check right
        process_coordinate(the_maze,row,col+1,search_locations)
        # check up
        process_coordinate(the_maze,row-1,col,search_locations)

    print_maze(the_maze)
    return False

def process_coordinate(the_maze,row,col,search_locations):
    if 0 <= row < len(the_maze):
        if 0 <= col < len(the_maze[row]):
            if the_maze[row][col] == " ":
                the_maze[row][col] = "?"
                search_locations.push((row,col))
            if the_maze[row][col] == "F":
                the_maze[row][col] = "!"
                search_locations.push((row,col))
            
    

def read_maze(filepath):
    fin = open(filepath)
    maze = []
    for line in fin:
        maze_row = []
        # could use rstrip("\n")
        for c in line.rstrip():
            maze_row.append(c)
        maze.append(maze_row)
    fin.close()
    return maze

def print_maze(the_maze):
    for maze_row in the_maze:
        print("".join(maze_row))

def find_start(the_maze):
    for row_index in range(len(the_maze)):
        for col_index in range(len(the_maze[row_index])):
            if the_maze[row_index][col_index] == "S":
                return row_index, col_index

if __name__ == "__main__":
    the_maze = read_maze("maze.txt")
    print_maze(the_maze)
    print(is_solvable(the_maze))
