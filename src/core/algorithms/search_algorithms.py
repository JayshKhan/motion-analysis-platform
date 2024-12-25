from collections import deque

from src.core.environment import Environment
from src.core.motion_planner import MotionPlanner


class BreadthFirstSearchPlanner(MotionPlanner):
    def __init__(self, sensor=None):
        pass

    def plan(self, environment: Environment) -> (list, int):
        if not environment.start or not environment.goal:
            return None, 0

        start = environment.start
        goal = environment.goal
        queue = deque([(start, [start])])  # Queue of (current_node, path_so_far)
        visited = {start}
        step = 0

        while queue:
            current, path = queue.popleft()
            step += 1
            yield path, step

            if current == goal:
                return path, step

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_x, next_y = current[0] + dx, current[1] + dy
                neighbor = (next_x, next_y)

                if environment.is_valid(next_x, next_y) and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None, step  # No path found


class DepthFirstSearchPlanner(MotionPlanner):
    def __init__(self, sensor=None):
        pass

    def plan(self, environment: Environment) -> (list, int):
        if not environment.start or not environment.goal:
            return None, 0

        start = environment.start
        goal = environment.goal
        stack = [(start, [start])]  # Stack of (current_node, path_so_far)
        visited = {start}
        step = 0

        while stack:
            current, path = stack.pop()
            step += 1
            yield path, step

            if current == goal:
                return path, step

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_x, next_y = current[0] + dx, current[1] + dy
                neighbor = (next_x, next_y)

                if environment.is_valid(next_x, next_y) and neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return None, step  # No path found


class DijkstraPlanner(MotionPlanner):
    def __init__(self, sensor=None):
        pass

    def plan(self, environment: Environment) -> (list, int):
        if not environment.start or not environment.goal:
            return None, 0

        start = environment.start
        goal = environment.goal
        open_set = {(0, start, tuple([start]))}  # Convert list to tuple
        visited = {}  # Store the shortest distance to each node
        step = 0

        while open_set:
            cost, current, path_tuple = min(open_set, key=lambda item: item[0])
            open_set.remove((cost, current, path_tuple))
            step += 1
            path = list(path_tuple)  # Convert back to list for yielding
            yield path, step

            if current in visited and visited[current] <= cost:
                continue
            visited[current] = cost

            if current == goal:
                return path, step

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_x, next_y = current[0] + dx, current[1] + dy
                neighbor = (next_x, next_y)

                if environment.is_valid(next_x, next_y):
                    new_cost = cost + 1  # Assuming uniform cost
                    new_path_tuple = tuple(list(path_tuple) + [neighbor])
                    if neighbor not in visited or new_cost < visited[neighbor]:
                        open_set.add((new_cost, neighbor, new_path_tuple))

        return None, step  # No path found


class AStarPlanner(MotionPlanner):
    def __init__(self, sensor=None, heuristic_weight=1.0):
        super().__init__()
        self.heuristic_weight = heuristic_weight

    def heuristic(self, a, b):
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def plan(self, environment: Environment) -> (list, int):
        if not environment.start or not environment.goal:
            return None, 0  # End the generator cleanly with a return

        start = environment.start
        goal = environment.goal
        open_set = {(self.heuristic(start, goal), 0, start, tuple([start]))}
        g_score = {start: 0}
        step = 0

        while open_set:
            _, current_g_score, current, path_tuple = min(open_set, key=lambda item: item[0])
            open_set.remove((_, current_g_score, current, path_tuple))
            step += 1
            path = list(path_tuple)
            yield path, step  # Consistently yield path and step

            if current == goal:
                return  # End the generator cleanly

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_x, neighbor_y = current[0] + dx, current[1] + dy
                neighbor = (neighbor_x, neighbor_y)

                if environment.is_valid(neighbor_x, neighbor_y):
                    tentative_g_score = current_g_score + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic_weight * self.heuristic(neighbor, goal)
                        new_path_tuple = tuple(list(path_tuple) + [neighbor])
                        open_set.add((f_score, tentative_g_score, neighbor, new_path_tuple))

        return None, step
