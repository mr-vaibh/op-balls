import pygame, math, random, time
import sys
import requests
from datetime import datetime

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

growth_rate = 1.5
ball_radius = 0.1

# Delay and Time control
do_delay = True
last_record_time = None

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

EXPORT_DATA = {
    "response_game2_array": []
}

button_clicked = False
i = 1
while running and i <= 5:
    for event in pygame.event.get():
        # this 0.2 is a hack that the player can't score by pressing the button before the ball even appears
        not_pressed_before_appeared = ball_radius > 0.2

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not button_clicked and not_pressed_before_appeared:
            mouse_x, mouse_y = event.pos
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                score += 1
                total_balls_thrown += 1
                # Reset ball position if clicked
                ball_y = 20
                ball_radius = 0.1
                update_ball_x_factors()
                do_delay = True

                print((datetime.now() - last_record_time).total_seconds())
                EXPORT_DATA["response_game2_array"].append((datetime.now() - last_record_time).total_seconds())
                i += 1
                button_clicked = True  # Set the flag to prevent further button clicks

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
    ball_y += 1

    scaling_factor = calculate_scaling_factor(ball_y)
    # ball_radius = 20 / scaling_factor if scaling_factor != 0 else 5
    ball_radius *= 1.3

    # Check if the ball has passed through the screen or if it's time for a new ball
    if ball_y + ball_radius >= line_1_distance:
        new_ball_timer = 0
        total_balls_thrown += 1
        missed_balls += 1
        # Reset ball position
        ball_y = line_1_distance - ball_radius  # Reset just above the line
        ball_radius = 0.1
        update_ball_x_factors()
        do_delay = True

        print((datetime.now() - last_record_time).total_seconds())

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

    # Define the button properties
    button_width = 100
    button_height = 40
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - button_height - 10

    # Define the font for the button text
    button_font = pygame.font.Font(None, 24)

    # Create a "PRESS!" button surface
    button_surface = pygame.Surface((button_width, button_height))
    button_surface.fill(RED)
    pygame.draw.rect(button_surface, BLACK, (0, 0, button_width, button_height), 2)  # Add a black border

    # Render the text on the button surface
    button_text = button_font.render("PRESS!", True, BLACK)
    text_x = (button_width - button_text.get_width()) // 2
    text_y = (button_height - button_text.get_height()) // 2
    button_surface.blit(button_text, (text_x, text_y))

    # Draw the "PRESS!" button
    window.blit(button_surface, (button_x, button_y))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

    # Increment the new ball timer
    new_ball_timer += 1

    if do_delay:
        button_clicked = False
        do_delay = False
        duration = random.randint(1, 5)
        time.sleep(duration)

        last_record_time = datetime.now()
        print(last_record_time)

# Quit the game
pygame.quit()

print(EXPORT_DATA["response_game2_array"])

import os, csv
# Create the "response" folder if it doesn't exist
response_folder = "response"
os.makedirs(response_folder, exist_ok=True)
# Export response time data to CSV
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"{response_folder}/DistanceVsNearTarget_{current_datetime}.csv"
with open(csv_filename, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Index", "Appear Response Time (seconds)"])  # Write header row
    for idx, response_time in enumerate(EXPORT_DATA["response_game2_array"], start=1):
        csv_writer.writerow([idx, response_time])
    csv_writer.writerow([])
    csv_writer.writerow(["Scored Balls", "Missed Balls", "Total Balls Thrown"])
    csv_writer.writerow([score, missed_balls, total_balls_thrown])

print(f"Response data exported to {csv_filename}")