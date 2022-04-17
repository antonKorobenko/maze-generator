import pygame

from .colors import EMPTY, WALL, OPEN, CLOSED, START, END, PATH 

class Spot:
    def __init__(self, row: int, col: int, color: tuple, cell_size: int) -> None:
        self.row = row # row number in maze
        self.col = col # column number in maze
        self.x = row * cell_size # x coordinate in pygame window
        self.y = col * cell_size # y coordinate in pygame window
        self.cell_size = cell_size
        self.color = color
        self.neighbors = list()

    def get_grid_pos(self) -> tuple[int, int]:
        return self.row, self.col

    def is_closed(self) -> bool:
        return self.color == CLOSED

    def is_open(self) -> bool:
        return self.color == OPEN

    def is_wall(self) -> bool:
        return self.color == WALL

    def is_start(self) -> bool:
        return self.color == START

    def is_end(self) -> bool:
        return self.color == END

    def make_empty(self) -> None:
        self.color = EMPTY

    def make_closed(self) -> None:
        if not self.is_wall() and not self.is_start() and not self.is_end():
            self.color = CLOSED

    def make_open(self) -> None:
        if not self.is_wall() and not self.is_start() and not self.is_end():
            self.color = OPEN

    def make_wall(self) -> None:
        self.color = WALL

    def make_start(self) -> None:
        self.color = START

    def make_end(self) -> None:
        self.color = END

    def make_path(self) -> None:
        if not self.is_wall() and not self.is_start() and not self.is_end():
            self.color = PATH

    def draw(self, win) -> None:
        pygame.draw.rect(
            win, # where to draw
            self.color, # color
            (self.x, self.y, self.cell_size, self.cell_size)) # rect params

    def update_neighbors(self, grid: list[list]) -> None:
        self.neighbors = list()
        total_rows = len(grid)
        total_columns = len(grid[0])
        # DOWN
        if self.row < total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < total_columns - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])
