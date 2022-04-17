import pygame
from queue import PriorityQueue

from .spot import Spot
from .colors import EMPTY, WALL, OPEN, CLOSED, START, END, PATH 


CELL_SIZE = 8 # 8x8 px


class GUIPathfinder:

    def __init__(self, maze: list[list[bool]]) -> None:
        self.maze = maze
        self.rows_num = len(maze)
        self.columns_num = len(maze[0])

        self.draw_grid_lines = int(input("Draw grid lines(1 - YES, 0 - NO)? "))
        self.start = None
        self.end = None

        self.window = pygame.display.set_mode((
            self.rows_num * CELL_SIZE, # height
            self.columns_num * CELL_SIZE # width
            )) 
    
    def create_grid(self) -> None:
        grid = list()
        for i in range(self.rows_num):
            row = list()
            for j in range(self.columns_num):
                # if 1 in maze[i][j] - it is wall, if 0 - empty cell
                if self.maze[i][j]:
                    row.append(Spot(i, j, WALL, CELL_SIZE))
                else:
                    row.append(Spot(i, j, EMPTY, CELL_SIZE)) 
            grid.append(row)
        self.grid = grid
    
    def draw_grid(self) -> None:
        # draw vertical lines
        for i in range(self.columns_num):
            pygame.draw.line(
                self.window, # where to draw
                CLOSED, # color
                (0, i * CELL_SIZE), # start pos
                (self.rows_num * CELL_SIZE, i * CELL_SIZE)) # end pos
        # draw horizontal lines
        for j in range(self.rows_num):
            pygame.draw.line(
                self.window, # where to draw
                CLOSED, # color
                (j * CELL_SIZE, 0), # start pos
                (j * CELL_SIZE, self.columns_num * CELL_SIZE)) # end pos

    def draw(self) -> None:
        # draw whole window
        self.window.fill((255, 255, 255)) # (255, 255, 255) - white color
        for row in self.grid:
            for spot in row:
                spot.draw(self.window)
        if self.draw_grid_lines:
            self.draw_grid()
        pygame.display.update()
    
    @staticmethod
    def get_clicked_pos(position: tuple[int, int]) -> tuple[int, int]:
        x, y = position
        row = x // CELL_SIZE
        col = y // CELL_SIZE
        return row, col
    
    @staticmethod
    def get_dist(position1: tuple[int, int], position2: tuple[int, int]) -> int:
        x1, y1 = position1
        x2, y2 = position2
        return abs(x1 - x2) + abs(y1 - y2)

    def check_if_border(self, row: int, column: int) -> bool:
        if row == 0 or row == self.rows_num - 1 or column == 0 or column == self.columns_num - 1:
            return True
        return False
    
    def reconstruct_path(self, came_from: dict) -> None:
        target = self.end
        while target in came_from:
            target = came_from[target]
            target.make_path()
            self.draw()
    
    def algorithm(self):
        count = 0
        stack = PriorityQueue()
        stack.put((0, count, self.start))
        came_from = dict()
        # G and F = +inf so there can't be bigger number
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score = {spot: float("inf") for row in self.grid for spot in row}

        g_score[self.start] = 0
        h_score = self.get_dist(self.start.get_grid_pos(), self.end.get_grid_pos())
        f_score[self.start] = h_score
        stack_hash = {self.start}
        while not stack.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = stack.get()[2]
            stack_hash.remove(current)
            if current == self.end:
                self.reconstruct_path(came_from)
                return True
            for neighbor in current.neighbors:
                tmp_g_score = g_score[current] + 1
                if tmp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tmp_g_score
                    h_score = self.get_dist(neighbor.get_grid_pos(), self.end.get_grid_pos())
                    f_score[neighbor] = tmp_g_score + h_score
                    if neighbor not in stack_hash:
                        count += 1
                        stack.put((f_score[neighbor], count, neighbor))
                        stack_hash.add(neighbor)
                        neighbor.make_open()
            self.draw()
            current.make_closed()
        return False

    def run(self):
        self.create_grid()
        run = True
        while run:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:  # left mouse button
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_clicked_pos(pos)
                        # ignore if spot is on maze border
                        if self.check_if_border(row, col):
                            continue
                        spot = self.grid[row][col]
                        # if there is no start on grid - make start spot
                        if not self.start and spot != self.end:
                            self.start = spot
                            self.start.make_start()
                        # if there is no end on grid - make end
                        elif not self.end and spot != self.start:
                            self.end = spot
                            self.end.make_end()
                        # if there is both start and end on grid - make wall
                        elif spot != self.end and spot != self.start:
                            spot.make_wall()
                elif pygame.mouse.get_pressed()[2]:  # right mouse click
                        pos = pygame.mouse.get_pos()
                        row, col = self.get_clicked_pos(pos)
                        # ignore if spot is on maze border
                        if self.check_if_border(row, col):
                            continue
                        # make spot an empty one
                        spot = self.grid[row][col]
                        spot.make_empty()
                        if spot == self.start:
                            self.start = None
                        elif spot == self.end:
                            self.end = None

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and self.start and self.end:
                            for row in self.grid:
                                for spot in row:
                                    spot.update_neighbors(self.grid)
                                    pass
                            if not self.algorithm():
                                print("Path not found")

                        if event.key == pygame.K_c:
                            # reset grid
                            self.start = None
                            self.end = None
                            self.create_grid()
