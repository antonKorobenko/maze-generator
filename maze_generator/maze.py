import os
import random
import colorama
from colorama import Back
from .cell import Cell


WALL_PAIRS = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E"
}


def remove_wall_for_adjacent_cells(cell_1: Cell, cell_2: Cell, wall: str) -> None:
    # since one wall can be associated with 2 cells, we must remove it from both
    cell_1.remove_wall(wall)
    cell_2.remove_wall(WALL_PAIRS[wall])


class Maze():

    def __init__(self, n: int, m: int, x_start=0, y_start=0) -> None:
        self.rows_num = n
        self.columns_num = m
        self.x_start = x_start
        self.y_start = y_start
        # create an initial "maze" where all the cells are surrounded by walls
        self.maze_map = [[Cell(x, y) for y in range(m)] for x in range(n)]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.maze_map[x][y]

    def get_unvisited_neighbours(self, cell: Cell) -> list[tuple[str, Cell]]:
        """
        Checks all adjacent cell if they were visited: if cell has all 4 walls
        that mean that it wasn't added to any paths in maze. Returns a list of
        tuples with directions to adjacent unvisited cells and cells itself.
        """
        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = list()
        for direction, (delta_x, delta_y) in delta:
            x = cell.x + delta_x
            y = cell.y + delta_y
            if 0 <= x < self.rows_num and 0 <= y < self.columns_num:
                neighbour = self.get_cell(x, y)
                if neighbour.walled_aroud:
                    neighbours.append((direction, neighbour))
        return neighbours

    def generate_maze(self) -> None:
        """ Maze generator """
        total_cells_num = self.rows_num * self.columns_num
        # stack of cell which are going to be processed
        stack = list()
        current_cell = self.get_cell(self.x_start, self.y_start)
        visited_num = 1
        # while there is unvisited cells in maze map
        while visited_num < total_cells_num:
            neighbours = self.get_unvisited_neighbours(current_cell)
            # if no unvisited neighbours than this cell was processed
            if not neighbours:
                current_cell = stack.pop()
                continue
            # random selection of the next cell to process
            direction, next_cell = random.choice(neighbours)
            # remove walls for path
            remove_wall_for_adjacent_cells(current_cell, next_cell, direction)
            # add cell to stack for processing
            stack.append(current_cell)
            current_cell = next_cell
            visited_num += 1

    def show(self) -> None:
        """ Print eye-friendly maze """
        colorama.init(autoreset=True)
        print("".join([f"{Back.RED} " * (self.rows_num * 2 + 1)]))
        for y in range(self.columns_num):
            row = [f"{Back.RED} "]
            for x in range(self.rows_num):
                if self.maze_map[x][y].walls["E"]:
                    row.append(f"{Back.GREEN} {Back.RED} ")
                else:
                    row.append(f"{Back.GREEN}  ")
            print(("".join(row)))
            row = [f"{Back.RED} "]
            for x in range(self.rows_num):
                if self.maze_map[x][y].walls["S"]:
                    row.append(f"{Back.RED}  ")
                else:
                    row.append(f"{Back.GREEN} {Back.RED} ")
            print(("".join(row)))

    def write_svg(self):
        """ Save maze as .svg image"""
        # create dir for mazes
        if not os.path.exists("Mazes"):
            os.mkdir("Mazes")
        # if there is a maze of the same size, remove it
        filepath = f"Mazes/{self.rows_num}x{self.columns_num}.svg"
        if os.path.exists(filepath):
            os.remove(filepath)

        aspect_ratio = self.rows_num / self.columns_num
        # padding around maze
        padding = 10
        # height and width of the maze image in pixels (without padding)
        height = 500
        width = int(height * aspect_ratio)
        # scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.columns_num, width / self.rows_num

        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """Write a single wall to the SVG image file handle f."""
            print(
                f'<line x1="{ww_x1}" y1="{ww_y1}" x2="{ww_x2}" y2="{ww_y2}"/>', file=ww_f)

        # write the .svg image file for maze
        with open(filepath, 'w') as f:
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print(f'    width="{width + 2 * padding}" height="{height + 2 * padding}" viewBox="{-padding} {-padding} {width + 2 * padding} {height + 2 * padding}">', file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.rows_num):
                for y in range(self.columns_num):
                    if self.get_cell(x, y).walls['S']:
                        x1, y1, x2, y2 = x * \
                            scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.get_cell(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * \
                            scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
            # draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print(f'<line x1="0" y1="0" x2="{width}" y2="0"/>', file=f)
            print(f'<line x1="0" y1="0" x2="0" y2="{height}"/>', file=f)
            print('</svg>', file=f)

    def get_maze_as_boolean_matrix(self) -> list[list[bool]]:
        matrix= [[1] * (self.rows_num * 2 + 1)]
        
        for y in range(self.columns_num):
            row = [1]
            for x in range(self.rows_num):
                if self.maze_map[x][y].walls["E"]:
                    row.append(0)
                    row.append(1)
                else:
                    row.append(0)
                    row.append(0)
            matrix.append(row)
            row = [1]
            for x in range(self.rows_num):
                if self.maze_map[x][y].walls["S"]:
                    row.append(1)
                    row.append(1)
                else:
                    row.append(0)
                    row.append(1)
            matrix.append(row)
        
        return matrix
