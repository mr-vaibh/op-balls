import pygame
import math
import random

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
RED = (255, 0, 0)  # Ball color

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

# Calculate the scaling factor for the ball
def calculate_scaling_factor(y):
    max_y = line_2_distance - line_1_distance
    scaling_factor = (max_y - (y - line_1_distance)) / max_y if max_y != 0 else 1
    scaling_rate = 3  # Adjust this value to control the rate of scaling
    return scaling_factor * scaling_rate

# Function to apply motion blur effect
# def apply_motion_blur(surface, y, radius, alpha):
#     blur_surface = pygame.Surface((2 * ball_radius, 2 * ball_radius), pygame.SRCALPHA)
#     pygame.draw.circle(blur_surface, (0, 0, 0, alpha), (radius, radius), radius)
#     surface.blit(blur_surface, (ball_x - radius, y - radius))

# Game loop
running = True
ball_y = 20  # Initial position above the screen
ball_speed = 20  # Speed at which the ball moves vertically
score = 0
new_ball_timer = 0  # Timer for new ball appearance

# Randomly generate x-coordinate within the lawn
ball_x = random.uniform(calculate_left_point_x(line_1_distance), calculate_right_point_x(line_1_distance))

# Set up clock for controlling frame rate
clock = pygame.time.Clock()
fps = 60  # Desired frame rate

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is inside the ball
            if ball_y > 0 and ball_y < HEIGHT and abs(event.pos[0] - ball_x) < ball_radius:
                score += 1
                # Reset ball position if clicked
                ball_y = 20
                ball_x = random.uniform(calculate_left_point_x(line_1_distance), calculate_right_point_x(line_1_distance))

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

    # Calculate the ball position and size based on the scaling factor
    ball_y += ball_speed
    scaling_factor = calculate_scaling_factor(ball_y)
    ball_radius = 20 / scaling_factor if scaling_factor != 0 else 5

    # Check if the ball has passed through the screen or if it's time for a new ball
    if ball_y > HEIGHT + ball_radius or new_ball_timer >= 120:
        ball_y = 20  # Reset ball position
        ball_x = random.uniform(calculate_left_point_x(line_1_distance), calculate_right_point_x(line_1_distance))
        new_ball_timer = 0

    # # Draw the motion blur effect
    # alpha = 50  # Alpha value for the motion blur effect
    # apply_motion_blur(window, ball_y, int(ball_radius), alpha)

    # Draw the ball
    pygame.draw.circle(window, RED, (int(ball_x), int(ball_y)), int(ball_radius))

    # Draw the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

    # Increment the new ball timer
    new_ball_timer += 1

# Quit the game
pygame.quit()
