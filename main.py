from maze import Maze


if __name__ == "__main__":
    rows_num = int(input("Enter rows number >> "))
    columns_num = int(input("Enter coluns number >> "))
    start_x = int(input("Enter X coordinate of initial cell >> "))
    start_y = int(input("Enter Y coordinate of initial cell >> "))
    maze = Maze(rows_num, columns_num, start_x, start_y)
    maze.generate_maze()
    maze.show()
    maze.write_svg()
