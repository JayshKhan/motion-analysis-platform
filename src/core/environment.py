class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()
        self.start = None
        self.goal = None

    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

    def set_start(self, x, y):
        self.start = (x, y)

    def set_goal(self, x, y):
        self.goal = (x, y)

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.obstacles