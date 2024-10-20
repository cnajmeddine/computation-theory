import numpy as np
import random
import matplotlib.pyplot as plt
import time

# Initialize environment (2D grid)
class Environment:
    def __init__(self, size):
        self.size = size
        # Create a random environment where each cell has a value (e.g., 0 or 1)
        self.grid = np.random.randint(2, size=(self.size, self.size))
    
    def show(self):
        plt.imshow(self.grid, cmap='gray')
        plt.show()

# Define the agent
class Agent:
    def __init__(self, env):
        self.env = env
        self.pos = [random.randint(0, env.size - 1), random.randint(0, env.size - 1)]
        # Initialize an internal model (a prediction of the environment)
        self.internal_model = np.random.randint(2, size=(env.size, env.size))
        self.prediction_error = 0
    
    def sense(self):
        # The agent can sense the value at its current position
        real_value = self.env.grid[self.pos[0], self.pos[1]]
        predicted_value = self.internal_model[self.pos[0], self.pos[1]]
        self.prediction_error = abs(real_value - predicted_value)
        return real_value
    
    def update_internal_model(self, real_value):
        # Update the internal model based on the sensed real value
        self.internal_model[self.pos[0], self.pos[1]] = real_value
    
    def move(self):
        # Move randomly to another location in the environment
        self.pos[0] = (self.pos[0] + random.choice([-1, 1])) % self.env.size
        self.pos[1] = (self.pos[1] + random.choice([-1, 1])) % self.env.size
    
    def minimize_free_energy(self):
        # Either update the internal model or move to reduce prediction error
        if self.prediction_error > 0:
            # Option 1: Update the internal model to reduce prediction error
            real_value = self.sense()
            self.update_internal_model(real_value)
        else:
            # Option 2: If the prediction was correct, move to explore a new area
            self.move()

    def show_internal_model(self):
        plt.imshow(self.internal_model, cmap='gray')
        plt.show()

# Simulation
def run_simulation(steps):
    env = Environment(10)  # Create an environment with a 10x10 grid
    agent = Agent(env)

    for step in range(steps):
        print(f"Step {step + 1}:")
        agent.sense()  # Sense the environment
        agent.minimize_free_energy()  # Minimize prediction error
        print(f"Agent position: {agent.pos}")
        print(f"Prediction Error: {agent.prediction_error}")
        env.show()  # Show the real environment
        agent.show_internal_model()  # Show the agent's internal model
        time.sleep(1)

run_simulation(20)
