import pygame
import numpy as np
import random

# Set up the game window
WINDOW_SIZE = 600
GRID_SIZE = 100
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colors
EMPTY_COLOR = (0, 0, 0)  # Empty space (black)
PREY_COLOR = (0, 255, 0)  # Prey (green)
PREDATOR_COLOR = (255, 0, 0)  # Predator (red)
DEPLETED_PREY_COLOR = (128, 128, 128)  # Depleted prey (grey)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Predator-Prey Simulation")

# Define a cell class to represent prey and predators
class Cell:
    def __init__(self, cell_type='empty', energy=0, depleted=False):
        self.cell_type = cell_type  # Can be 'empty', 'prey', or 'predator'
        self.energy = energy
        self.depleted = depleted  # If a prey is depleted, it becomes grey

# Initialize the grid with random prey and predators
def initialize_grid():
    grid = np.empty((GRID_SIZE, GRID_SIZE), dtype=object)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if random.random() < 0.1:  # 10% chance of prey
                grid[i][j] = Cell(cell_type='prey', energy=5)
            elif random.random() < 0.05:  # 5% chance of predator
                grid[i][j] = Cell(cell_type='predator', energy=10)
            else:
                grid[i][j] = Cell(cell_type='empty')
    return grid

grid = initialize_grid()

# Function to draw the grid
def draw_grid(screen, grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell = grid[i][j]
            if cell.cell_type == 'prey':
                if cell.depleted:
                    color = DEPLETED_PREY_COLOR  # Grey if depleted
                else:
                    color = PREY_COLOR  # Green if not depleted
            elif cell.cell_type == 'predator':
                color = PREDATOR_COLOR
            else:
                color = EMPTY_COLOR
            pygame.draw.rect(screen, color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Count neighbors of a given type (e.g., prey or predator)
def count_neighbors(grid, x, y, target_type):
    count = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y) and 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE:
                if grid[i][j].cell_type == target_type:
                    count += 1
    return count

# Function to update the grid based on predator-prey rules
def update_grid(grid):
    new_grid = np.copy(grid)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell = grid[i][j]

            # Prey logic
            if cell.cell_type == 'prey':
                if not cell.depleted:
                    # Prey reproduces if it has enough empty space around it
                    empty_neighbors = count_neighbors(grid, i, j, 'empty')
                    if empty_neighbors >= 3 and random.random() < 0.25:  # 25% chance to reproduce
                        new_grid[i][j] = Cell(cell_type='prey', energy=5)
                    else:
                        cell.energy -= 0.5  # Faster prey energy depletion

                    if cell.energy <= 0:  # Prey becomes depleted (grey) instead of dying
                        new_grid[i][j].depleted = True
                        new_grid[i][j].energy = 0  # Set energy to zero
                else:
                    # Once depleted, the prey stays grey and does not reproduce
                    pass

            # Predator logic
            elif cell.cell_type == 'predator':
                prey_neighbors = count_neighbors(grid, i, j, 'prey')

                if prey_neighbors > 0:  # Predator eats prey
                    cell.energy += 5  # Gain energy from prey
                    if cell.energy > 10:
                        cell.energy = 10  # Cap predator energy
                else:
                    cell.energy -= 0.3  # Lose energy over time

                if cell.energy <= 0:  # Predator dies if energy is depleted
                    new_grid[i][j] = Cell(cell_type='empty')

                # Predator moves randomly to an empty neighbor
                empty_neighbors = [(x, y) for x in range(i - 1, i + 2) for y in range(j - 1, j + 2)
                                   if (x, y) != (i, j) and 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x][y].cell_type == 'empty']

                if empty_neighbors:
                    new_pos = random.choice(empty_neighbors)
                    new_grid[new_pos[0]][new_pos[1]] = Cell(cell_type='predator', energy=cell.energy)
                    new_grid[i][j] = Cell(cell_type='empty')

    return new_grid

# Main game loop
running = True
clock = pygame.time.Clock()  # Set up clock to control simulation speed

while running:
    screen.fill(EMPTY_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw grid
    grid = update_grid(grid)
    draw_grid(screen, grid)

    # Update the display
    pygame.display.flip()

    # Control speed of simulation
    pygame.time.delay(20)  # Delay to slow down simulation

    clock.tick(30)  # Slow down the game loop to 10 frames per second

pygame.quit()
