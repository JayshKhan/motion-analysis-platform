from src.core.environment import Environment
from src.core.algorithms.random_walk import RandomWalkPlanner

# Create an environment
env = Environment(20, 15)
env.add_obstacle(5, 5)
env.add_obstacle(5, 6)
env.set_start(1, 1)
env.set_goal(18, 13)

# Create a motion planner
planner = RandomWalkPlanner()

# Plan the path
path = planner.plan(env)

if path:
    print("Path found:", path)
else:
    print("No path found.")