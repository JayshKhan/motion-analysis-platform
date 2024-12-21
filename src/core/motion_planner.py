from abc import ABC, abstractmethod
from src.core.environment import Environment

class MotionPlanner(ABC):
    @abstractmethod
    def plan(self, environment: Environment):
        """
        Plans a path from the start to the goal in the given environment.

        Args:
            environment: The Environment object.

        Returns:
            A list of (x, y) tuples representing the path, or None if no path is found.
        """
        pass