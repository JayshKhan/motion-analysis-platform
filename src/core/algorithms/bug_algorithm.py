import math

from src.config import config_instance as CONFIG
from src.core.environment import Environment
from src.core.motion_planner import MotionPlanner


class Bug0Planner(MotionPlanner):
    def __init__(self, sensor=None):
        self.sensor = sensor

    def plan(self, environment: Environment):
        if not environment.start or not environment.goal or not self.sensor:
            return

        start = environment.start
        goal = environment.goal
        current = start
        path = [current]
        step = 0
        on_boundary = False

        while current != goal:
            step += 1
            yield path, step

            direction_to_goal = (goal[0] - current[0], goal[1] - current[1])
            next_step_towards_goal = (
            current[0] + self.sign(direction_to_goal[0]), current[1] + self.sign(direction_to_goal[1]))

            sensor_data = self.sensor.sense(environment, current)
            obstacle_ahead = self.is_obstacle_at(next_step_towards_goal, sensor_data)

            if not on_boundary and obstacle_ahead:
                on_boundary = True
                print("Bug 0: Hit obstacle, starting boundary follow.")

            if on_boundary:
                moved = False
                # Try to follow boundary (keep obstacle to the left - example)
                possible_moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Left, Up, Right, Down
                for move in possible_moves:
                    next_pos = (current[0] + move[0], current[1] + move[1])
                    if environment.is_valid(next_pos[0], next_pos[1]) and not self.is_obstacle_at(next_pos,
                                                                                                  sensor_data):
                        current = next_pos
                        path.append(current)
                        moved = True
                        break
                if not moved:
                    print("Bug 0: Stuck while boundary following.")
                    return path, step
                # Check if can move towards goal again
                if not self.is_obstacle_at(next_step_towards_goal, sensor_data):
                    on_boundary = False
                    print("Bug 0: Leaving boundary, moving towards goal.")

            elif not obstacle_ahead:
                current = next_step_towards_goal
                path.append(current)
            else:
                print("Bug 0: Blocked while moving towards goal but should be on boundary.")  # Should not happen
                return path, step

            if step > 2000:  # Safety break
                print("Bug 0: Max steps reached.")
                return path, step

        return path, step

    def sign(self, n):
        if n > 0: return 1
        if n < 0: return -1
        return 0

    def is_obstacle_at(self, position, sensor_data):
        if sensor_data and "obstacles_in_range" in sensor_data:
            for obs in sensor_data["obstacles_in_range"]:
                if round(obs[0]) == round(position[0]) and round(obs[1]) == round(position[1]):
                    return True
        return False


class Bug1Planner(MotionPlanner):
    def __init__(self, sensor=None):
        self.sensor = sensor

    def plan(self, environment: Environment):
        if not environment.start or not environment.goal or not self.sensor:
            return

        start = environment.start
        goal = environment.goal
        current = start
        path = [current]
        step = 0
        hit_point = None
        on_boundary = False

        while current != goal:
            step += 1
            yield path, step

            direction_to_goal = (goal[0] - current[0], goal[1] - current[1])
            next_step_towards_goal = (
            current[0] + self.sign(direction_to_goal[0]), current[1] + self.sign(direction_to_goal[1]))

            sensor_data = self.sensor.sense(environment, current)
            obstacle_ahead = self.is_obstacle_at(next_step_towards_goal, sensor_data)

            if not on_boundary and obstacle_ahead:
                on_boundary = True
                hit_point = current
                print(f"Bug 1: Hit obstacle at {hit_point}, starting boundary follow.")

            if on_boundary:
                moved = False
                # Try to follow boundary (keep obstacle to the left - example)
                possible_moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Left, Up, Right, Down
                for move in possible_moves:
                    next_pos = (current[0] + move[0], current[1] + move[1])
                    if environment.is_valid(next_pos[0], next_pos[1]) and not self.is_obstacle_at(next_pos,
                                                                                                  sensor_data):
                        current = next_pos
                        path.append(current)
                        moved = True
                        break
                if not moved:
                    print("Bug 1: Stuck while boundary following.")
                    return path, step

                # Check leave condition (simplified: can move towards goal and closer to goal than hit_point)
                if not self.is_obstacle_at(next_step_towards_goal, sensor_data) and self.calculate_distance(current,
                                                                                                            goal) < self.calculate_distance(
                        hit_point, goal):
                    on_boundary = False
                    print(f"Bug 1: Leave condition met at {current}, moving towards goal.")

            elif not obstacle_ahead:
                current = next_step_towards_goal
                path.append(current)

            if step > 2000:  # Safety break
                print("Bug 1: Max steps reached.")
                return path, step

        return path, step

    def sign(self, n):
        if n > 0: return 1
        if n < 0: return -1
        return 0

    def is_obstacle_at(self, position, sensor_data):
        if sensor_data and "obstacles_in_range" in sensor_data:
            for obs in sensor_data["obstacles_in_range"]:
                if round(obs[0]) == round(position[0]) and round(obs[1]) == round(position[1]):
                    return True
        return False

    def calculate_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


class Bug2Planner(MotionPlanner):
    def __init__(self, sensor=None, step_size=1):
        self.step_size = step_size
        self.mode = "goal_seek"  # Modes: goal_seek, boundary_follow
        self.hit_point = None
        self.leave_point = None
        self.sensor = sensor

    def plan(self, environment: Environment):
        if CONFIG.debug:
            print(f"Starting Bug2 planner with mode {self.mode} and sensor {self.sensor}")
        if not environment.start or not environment.goal or not self.sensor:
            return

        start = environment.start
        goal = environment.goal
        current = start
        path = [current]
        step = 0

        while current != goal:
            step += 1
            yield path, step

            if self.mode == "goal_seek":
                # Move towards the goal
                direction_x = goal[0] - current[0]
                direction_y = goal[1] - current[1]
                distance_to_goal = self.calculate_distance(current, goal)

                if distance_to_goal > 0:
                    move_x = direction_x / distance_to_goal
                    move_y = direction_y / distance_to_goal
                else:
                    continue  # Already at the goal (shouldn't happen here)

                next_x = round(current[0] + move_x * self.step_size)
                next_y = round(current[1] + move_y * self.step_size)

                # Check for obstacles using the sensor
                sensor_data = self.sensor.sense(environment, current)
                obstacle_ahead = False
                if sensor_data and "obstacles_in_range" in sensor_data:
                    # Check if the immediate next cell is occupied
                    potential_obstacle = (next_x, next_y)
                    for obs in sensor_data["obstacles_in_range"]:
                        if self.are_same_location(obs, potential_obstacle):
                            obstacle_ahead = True
                            break

                if obstacle_ahead:
                    self.mode = "boundary_follow"
                    self.hit_point = current
                    print(f"Obstacle hit at {self.hit_point}, switching to boundary follow.")
                    continue
                else:
                    current = (next_x, next_y)
                    path.append(current)

            elif self.mode == "boundary_follow":
                # Follow the boundary of the obstacle (keep obstacle to the left)
                # Need to implement boundary following logic carefully

                # Possible moves (prioritizing left, forward, right)
                possible_moves = [
                    (-1, 0),  # Left
                    (0, 1),  # Forward (along the boundary)
                    (1, 0),  # Right
                    (0, -1)  # Backward (should generally avoid)
                ]

                moved = False
                for move_x, move_y in possible_moves:
                    next_x = round(current[0] + move_x)
                    next_y = round(current[1] + move_y)
                    potential_position = (next_x, next_y)

                    # Check if the potential position is valid and not an obstacle
                    sensor_data = self.sensor.sense(environment, current)
                    is_obstacle = False
                    if sensor_data and "obstacles_in_range" in sensor_data:
                        for obs in sensor_data["obstacles_in_range"]:
                            if self.are_same_location(obs, potential_position):
                                is_obstacle = True
                                break

                    if environment.is_valid(next_x, next_y) and not is_obstacle:
                        current = potential_position
                        path.append(current)
                        moved = True
                        break

                if not moved:
                    print("Stuck during boundary following!")
                    return path, step  # Or handle getting stuck differently

                # Check for leave condition
                if self.hit_point:
                    distance_to_goal_hit = self.calculate_distance(self.hit_point, goal)
                    distance_to_goal_current = self.calculate_distance(current, goal)
                    # If we are further from the goal than the hit point, we've circled back
                    # This is a simplified leave condition - more robust ones exist
                    if distance_to_goal_current < distance_to_goal_hit:  # and self.is_on_m_line(current, self.hit_point, goal):
                        self.mode = "goal_seek"
                        self.leave_point = current
                        print(f"Leave condition met at {self.leave_point}, switching to goal seek.")

            if step > 2000:  # Safety break
                print("Max steps reached, possible infinite loop.")
                return path, step

        return path, step

    def calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def are_same_location(self, p1, p2):
        return round(p1[0]) == round(p2[0]) and round(p1[1]) == round(p2[1])

    def is_on_m_line(self, current, hit_point, goal):
        # Simplified check if current is "beyond" the hit point towards the goal
        # This needs to be more robust for complex scenarios
        return (hit_point[0] - goal[0]) * (current[1] - goal[1]) == (hit_point[1] - goal[1]) * (current[0] - goal[0])
