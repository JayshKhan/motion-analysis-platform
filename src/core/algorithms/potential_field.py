import math
from src.core.motion_planner import MotionPlanner
from src.core.environment import Environment


class PotentialFieldPlanner(MotionPlanner):
    def __init__(self, sensor=None, attractive_gain=1.0, repulsive_gain=100.0, min_repulsive_distance=2.0):
        super().__init__()
        self.sensor = sensor
        self.attractive_gain = attractive_gain  # Gain for attractive force
        self.repulsive_gain = repulsive_gain  # Gain for repulsive force
        self.min_repulsive_distance = min_repulsive_distance  # Minimum distance to apply repulsive force
        self.step_size = 0.1  # Step size for motion

    def plan(self, environment: Environment):
        if not environment.start or not environment.goal:
            return

        current = environment.start
        path = [current]
        yield path

        while self.calculate_distance(current, environment.goal) > self.step_size:
            force = self.calculate_total_force(current, environment)

            # Normalize the force
            force_magnitude = math.sqrt(force[0] ** 2 + force[1] ** 2)
            if force_magnitude > 0:
                force = (force[0] / force_magnitude, force[1] / force_magnitude)

            # Update position
            new_x = current[0] + force[0] * self.step_size
            new_y = current[1] + force[1] * self.step_size

            # Check for collisions
            if not environment.is_valid(new_x, new_y):
                print("Collision detected or position outside environment")
                yield path
                return

            current = (new_x, new_y)
            path.append(current)
            yield path

            if len(path) > 1000:  # Prevent infinite loops (you might need a better way to detect this)
                print("Path too long - potential local minimum or oscillation")
                yield path
                return

        yield path

    def calculate_total_force(self, current, environment):
        attractive_force = self.calculate_attractive_force(current, environment.goal)
        repulsive_force = self.calculate_repulsive_force(current, environment)
        total_force = (attractive_force[0] + repulsive_force[0], attractive_force[1] + repulsive_force[1])
        return total_force

    def calculate_attractive_force(self, current, goal):
        dx = goal[0] - current[0]
        dy = goal[1] - current[1]
        distance = self.calculate_distance(current, goal)

        force_magnitude = self.attractive_gain * distance
        force_x = force_magnitude * (dx / distance)
        force_y = force_magnitude * (dy / distance)

        return (force_x, force_y)

    def calculate_repulsive_force(self, current, environment):
        total_repulsive_force_x = 0
        total_repulsive_force_y = 0

        if self.sensor:
            print("Using sensor to detect obstacles")
            # Use sensor to detect obstacles if available
            sensor_data = self.sensor.sense(environment, current)
            obstacles_in_range = sensor_data.get("obstacles_in_range", [])
            print(obstacles_in_range)
        else:
            print("No sensor provided - using all obstacles in environment")
            # Fallback to environment.obstacles if no sensor is provided
            obstacles_in_range = environment.obstacles

        for obstacle in obstacles_in_range:
            dx = current[0] - obstacle[0]
            dy = current[1] - obstacle[1]
            distance = self.calculate_distance(current, obstacle)

            if distance <= self.min_repulsive_distance:
                force_magnitude = self.repulsive_gain * (1.0 / distance - 1.0 / self.min_repulsive_distance) / (
                            distance ** 2)
                force_x = force_magnitude * (dx / distance)
                force_y = force_magnitude * (dy / distance)

                total_repulsive_force_x += force_x
                total_repulsive_force_y += force_y

        return (total_repulsive_force_x, total_repulsive_force_y)

    def calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
