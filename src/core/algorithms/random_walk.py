import random
from src.core.motion_planner import MotionPlanner
from src.core.environment import Environment

class RandomWalkPlanner(MotionPlanner):
    def __init__(self, sensor=None):
        super().__init__()
        self.sensor = sensor

    def plan(self, environment: Environment):
        if not environment.start or not environment.goal:
            return

        current = environment.start
        path = [current]
        max_steps = 1000

        for _ in range(max_steps):
            if current == environment.goal:
                yield path  # Yield the final path when goal is reached
                return

            neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
            valid_neighbors = [n for n in neighbors if environment.is_valid(n[0], n[1])]

            if self.sensor:
                sensor_data = self.sensor.sense(environment, current)
                print(sensor_data)
                # Use sensor data to influence choices (example)
                valid_neighbors = [n for n in valid_neighbors if n not in sensor_data["obstacles_in_range"]]

            if not valid_neighbors:
                yield path  # Yield path so far (stuck)
                return

            current = random.choice(valid_neighbors)
            path.append(current)

            yield path  # Yield the current path after each step