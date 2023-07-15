import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sports Pitch")

# Set up colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_BROWN = (181, 101, 29)
DARK_BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# Set up the pitch
pitch_width = 600
pitch_height = 300
pitch_bottom = HEIGHT - 50

# Set up the angles for the slanting lines
left_angle = math.radians(60)
right_angle = math.radians(60)

# Set up the distances for the horizontal lines
line_1_distance = HEIGHT // 4
line_2_distance = HEIGHT // 2

# Function to calculate the position of a point on the left slanting line
def calculate_left_point_x(y):
    return (HEIGHT - y) / math.tan(left_angle)

# Function to calculate the position of a point on the right slanting line
def calculate_right_point_x(y):
    return WIDTH - (HEIGHT - y) / math.tan(right_angle)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill(LIGHT_BROWN)

    # Draw the ground trapezium
    ground_points = [
        (calculate_left_point_x(0), 0),
        (calculate_right_point_x(0), 0),
        (WIDTH, HEIGHT),
        (0, HEIGHT)
    ]
    pygame.draw.polygon(window, GREEN, ground_points)

    # Create a textured ground
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if window.get_at((x, y)) == LIGHT_BROWN:
                if (x + y) % 6 == 0 or (x + y) % 6 == 1:
                    window.set_at((x, y), DARK_BROWN)

    # Draw the horizontal lines
    pygame.draw.line(window, BLACK, (0, line_1_distance), (WIDTH, line_1_distance), 1)
    pygame.draw.line(window, BLACK, (0, line_2_distance), (WIDTH, line_2_distance), 1)

    # Find the intersection points of the first line with the trapezium
    intersection_1_x = calculate_left_point_x(line_1_distance)
    intersection_2_x = calculate_right_point_x(line_1_distance)

    # Draw the perpendicular lines from the intersection points to the second line
    pygame.draw.line(window, BLACK, (intersection_1_x, line_1_distance), (intersection_1_x, line_2_distance), 1)
    pygame.draw.line(window, BLACK, (intersection_2_x, line_1_distance), (intersection_2_x, line_2_distance), 1)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
