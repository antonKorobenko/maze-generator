from maze_generator.maze import Maze
from maze_pathfinder.visual_pathfinder import GUIPathfinder


# for maze_pathfinder testing
if __name__=="__main__":
    maze = Maze(48, 88) # 48, 88 - optimal size for CELL_SIZE = 8x8 px
    maze.generate_maze()
    pathfinder = GUIPathfinder(maze.get_maze_as_boolean_matrix())
    pathfinder.run()

# for maze_generator testing
"""
if __name__ == "__main__":
    rows_num = int(input("Enter rows number >> "))
    columns_num = int(input("Enter coluns number >> "))
    start_x = int(input("Enter X coordinate of initial cell >> "))
    start_y = int(input("Enter Y coordinate of initial cell >> "))
    maze = Maze(rows_num, columns_num, start_x, start_y)
    maze.generate_maze()
    #maze.show()
    #maze.write_svg()
    #maze.get_maze_as_boolean_matrix()
"""