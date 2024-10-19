import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to update the grid
def update(frame_num, img, grid, grid_size):
    new_grid = grid.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            # Count the number of live neighbors
            total = int((
                grid[i, (j-1)%grid_size] + grid[i, (j+1)%grid_size] +
                grid[(i-1)%grid_size, j] + grid[(i+1)%grid_size, j] +
                grid[(i-1)%grid_size, (j-1)%grid_size] + grid[(i-1)%grid_size, (j+1)%grid_size] +
                grid[(i+1)%grid_size, (j-1)%grid_size] + grid[(i+1)%grid_size, (j+1)%grid_size]
            ))
            
            # Apply Conway's rules
            if grid[i, j] == 1:
                if total < 2 or total > 3:
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1
    
    # Update the image
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

# Initialize the grid
grid_size = 100  # Grid size (100x100)
grid = np.random.choice([0, 1], size=(grid_size, grid_size))

# Create a figure and axis
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap='gray')

# Run the animation
ani = animation.FuncAnimation(fig, update, fargs=(img, grid, grid_size), frames=10, interval=50, save_count=50)

plt.show()
