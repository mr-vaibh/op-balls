import pygame, math, random
import sys
import requests

# Program run control
def check_url_and_execute(url):
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.text.strip().lower() == 'true':
            print("URL returned 'true', continuing with the rest of the scripts...")
            # Your additional scripts can be executed here
        else:
            print("URL did not return 'true'. Exiting...")
            sys.exit(1)  # Use a non-zero exit code to indicate failure

    except requests.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        sys.exit(1)

url_to_check = "https://raw.githubusercontent.com/mr-vaibh/op-balls/main/RELEASE"  # Replace this with the actual URL you want to check
check_url_and_execute(url_to_check)

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sports Pitch")

with open("config.txt", "r") as config_file:
    string = config_file.readline()
    contrast = string.split("=")[1] or 0
    contrast = 0 if (int(contrast) < 0 or int(contrast) > 10) else int(contrast)

# Set up colors
WHITE = (255, 255, 255)
WHITE_2 = (250, 250, 250)
CONTRAST_COEFFICIENT = 25.5 * contrast
GREEN = (CONTRAST_COEFFICIENT, 255, CONTRAST_COEFFICIENT)
LIGHT_BLUE = (0, 108, 183)  # New color for LIGHT_BLUE
DARK_BLUE = (0, 89, 165)  # New color for DARK_BLUE
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
total_balls_thrown = 0
score = 0
missed_balls = 0
new_ball_timer = 0  # Timer for new ball appearance

# Define font size for displaying statistics
font_size = 24
font = pygame.font.Font(None, font_size)

# TODO: add weightage of score. a dynamic coefficient to know after how much time the subject is taking to give response

# Randomly generate x-coordinate within the lawn
ball_x = random.uniform(calculate_left_point_x(line_1_distance), calculate_right_point_x(line_1_distance))
starting_corner = 1 if ball_x >= WIDTH / 2 else 0

# Calculate the angle of movement based on the chosen starting corner
diagonal_angle = math.radians(45)

def update_ball_x_factors():
    global ball_x, starting_corner
    ball_x = random.uniform(calculate_left_point_x(line_1_distance), calculate_right_point_x(line_1_distance))
    starting_corner = 1 if ball_x >= WIDTH / 2 else 0

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
                total_balls_thrown += 1
                # Reset ball position if clicked
                ball_y = 20
                update_ball_x_factors()

    # Clear the window
    window.fill(LIGHT_BLUE)

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
            if window.get_at((x, y)) == LIGHT_BLUE:
                if (x + y) % 6 == 0 or (x + y) % 6 == 1:
                    window.set_at((x, y), DARK_BLUE)

    # Draw the horizontal lines
    pygame.draw.line(window, BLACK, (0, line_1_distance), (WIDTH, line_1_distance), 1)
    pygame.draw.line(window, BLACK, (0, line_2_distance), (WIDTH, line_2_distance), 1)

    # Find the intersection points of the first line with the trapezium
    intersection_1_x = calculate_left_point_x(line_1_distance)
    intersection_2_x = calculate_right_point_x(line_1_distance)

    # Calculate the ball position and size based on the scaling factor
    ball_y += ball_speed
    if starting_corner == 1:
        ball_x -= ball_speed * math.cos(diagonal_angle)
    else:
        ball_x += ball_speed * math.cos(diagonal_angle)

    scaling_factor = calculate_scaling_factor(ball_y)
    ball_radius = 20 / scaling_factor if scaling_factor != 0 else 5

    # Check if the ball has passed through the screen or if it's time for a new ball
    if ball_y > HEIGHT + ball_radius or new_ball_timer >= 120:
        new_ball_timer = 0
        total_balls_thrown += 1
        missed_balls += 1
        # Reset ball position
        ball_y = 20  # Reset
        update_ball_x_factors()

    # # Draw the motion blur effect
    # alpha = 50  # Alpha value for the motion blur effect
    # apply_motion_blur(window, ball_y, int(ball_radius), alpha)

    # Draw the ball
    pygame.draw.circle(window, WHITE_2, (int(ball_x), int(ball_y)), int(ball_radius))

    # Draw the score and statistics on the screen
    score_text = font.render(f"Score: {score}", True, WHITE)
    balls_thrown_text = font.render(f"Balls Thrown: {total_balls_thrown}", True, WHITE)
    missed_balls_text = font.render(f"Missed Balls: {missed_balls}", True, WHITE)

    window.blit(score_text, (10, 10))
    window.blit(balls_thrown_text, (10, 10 + font_size + 5))
    window.blit(missed_balls_text, (10, 10 + 2 * (font_size + 5)))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

    # Increment the new ball timer
    new_ball_timer += 1

# Quit the game
pygame.quit()
