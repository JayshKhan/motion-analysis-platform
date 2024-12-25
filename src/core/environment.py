from src.ui.config import DEBUG


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()
        self.start = None
        self.goal = None
        self.add_boundary()

    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

    def set_start(self, x, y):
        self.start = (x, y)

    def set_goal(self, x, y):
        self.goal = (x, y)

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.obstacles

    def add_boundary(self):
        print("Adding boundary") if DEBUG else None
        for i in range(self.width):
            self.obstacles.add((i, 0))
            self.obstacles.add((i, self.height - 1))
        for i in range(self.height):
            self.obstacles.add((0, i))
            self.obstacles.add((self.width - 1, i))
