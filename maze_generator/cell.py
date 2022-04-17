class Cell():

    def __init__(self, row: int, column: int) -> None:
        self.x = row
        self.y = column
        self.walls = {
            "N": True,
            "S": True,
            "E": True,
            "W": True
        }
        self.walled_aroud = True

    def remove_wall(self, wall: str) -> None:
        self.walls[wall] = False
        self.walled_aroud = False

    # methods for pygame