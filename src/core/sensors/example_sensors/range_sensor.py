from src.core.sensors.sensor_model import SensorModel

class RangeSensor(SensorModel):
    def __init__(self, range_limit=5):
        self.range_limit = range_limit  # Add a range_limit attribute

    def sense(self, environment, agent_position):
        detected_obstacles = []
        for obs_x, obs_y in environment.obstacles:
            distance = ((agent_position[0] - obs_x)**2 + (agent_position[1] - obs_y)**2)**0.5
            if distance <= self.range_limit:
                detected_obstacles.append((obs_x, obs_y))
        return {"obstacles_in_range": detected_obstacles}

    def __str__(self):
        return f"RangeSensor(range_limit={self.range_limit})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.range_limit == other.range_limit
