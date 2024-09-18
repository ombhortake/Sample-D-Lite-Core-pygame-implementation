import pygame
import random
import heapq

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 400
window_height = 450  # Increased height for UI
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
button_color = (100, 100, 255)
button_hover_color = (150, 150, 255)

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

# Button class
class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = rect

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        color = button_hover_color if self.rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(window, color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, black)
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

# Create a button for pathfinding (positioned below the grid)
button = Button("Find Path", pygame.Rect((window_width - 120) // 2, window_height - 45, 120, 40))

# Main game loop
running = True
path = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_clicked():
                path = d_star_lite(start, goal)
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // cell_size
                grid_y = mouse_y // cell_size
                # Check if the click is within the grid area
                if grid_y < grid_size:
                    # Toggle obstacle
                    if grid[grid_y][grid_x] == 0:
                        grid[grid_y][grid_x] = 1  # Place obstacle
                    else:
                        grid[grid_y][grid_x] = 0  # Remove obstacle

                    # Recalculate path
                    path = d_star_lite(start, goal)

    window.fill(white)

    # Draw grid and obstacles
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

    # Draw the path
    if path:
        for node in path:
            rect = (node[0] * cell_size, node[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(window, blue, rect)

    # Draw the button
    button.draw(window)

    pygame.display.flip()

pygame.quit()
