import random
from src.core.motion_planner import MotionPlanner
from src.core.environment import Environment

class RandomWalkPlanner(MotionPlanner):
    def plan(self, environment: Environment):
        if not environment.start or not environment.goal:
            return None

        current = environment.start
        path = [current]
        max_steps = 1000  # Avoid infinite loops

        for _ in range(max_steps):
            if current == environment.goal:
                return path

            neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
            valid_neighbors = [n for n in neighbors if environment.is_valid(n[0], n[1]) and n not in path]

            if not valid_neighbors:
                return None  # Stuck

            current = random.choice(valid_neighbors)
            path.append(current)

        return None  # Did not reach goal within max steps