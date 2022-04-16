class Cell():

    def __init__(self, x_coordinate: int, y_coordinate: int) -> None:
        self.x = x_coordinate
        self.y = y_coordinate
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
