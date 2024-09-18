import pygame
import random
import heapq

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 400
window_height = 400
grid_size = 20
cell_size = window_width // grid_size
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("D* Lite Dynamic Environment")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Initialize the grid with random obstacles
grid = [[0 if random.random() > 0.3 else 1 for _ in range(grid_size)] for _ in range(grid_size)]
start = (0, 0)
goal = (grid_size - 1, grid_size - 1)
grid[start[1]][start[0]] = 0  # Ensure start is free
grid[goal[1]][goal[0]] = 0  # Ensure goal is free

# D* Lite algorithm implementation
def d_star_lite(start, goal):
    cost = {start: 0}
    parent = {start: None}
    open_set = [(0, start)]
    closed_set = set()

    while open_set:
        current_cost, current = heapq.heappop(open_set)

        if current in closed_set:
            continue
        closed_set.add(current)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and
                    grid[neighbor[1]][neighbor[0]] == 0):
                new_cost = current_cost + 1
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    parent[neighbor] = current
                    heapq.heappush(open_set, (new_cost, neighbor))

    return []

# Main game loop
running = True
pathfinding = False
path = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pathfinding = True
                path = d_star_lite(start, goal)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size
            # Toggle obstacle
            if grid[grid_y][grid_x] == 0:
                grid[grid_y][grid_x] = 1  # Place obstacle
            else:
                grid[grid_y][grid_x] = 0  # Remove obstacle

            # Recalculate path
            path = d_star_lite(start, goal)

    window.fill(white)

    for x in range(grid_size):
        for y in range(grid_size):
            rect = (x * cell_size, y * cell_size, cell_size, cell_size)
            if grid[y][x] == 1:
                pygame.draw.rect(window, black, rect)
            elif (x, y) == start:
                pygame.draw.rect(window, green, rect)
            elif (x, y) == goal:
                pygame.draw.rect(window, red, rect)
            pygame.draw.rect(window, blue, rect, 1)

    if path:
        for node in path:
            rect = (node[0] * cell_size, node[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(window, blue, rect)

    pygame.display.flip()

pygame.quit()
