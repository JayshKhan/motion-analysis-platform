from abc import ABC, abstractmethod

class SensorModel(ABC):
    @abstractmethod
    def sense(self, environment, agent_position):
        """
        Simulates the sensor's reading of the environment.

        Args:
            environment: The Environment object.
            agent_position: The current position of the agent (x, y).

        Returns:
            Sensor data (can be a dictionary, tuple, etc.).
        """
        pass