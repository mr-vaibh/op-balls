import pygame
from pygame.locals import *

width = 800
height = 600

# Load the badminton image and shuttlecock image
badminton_image = pygame.image.load("sprite\\bat.png")  # Replace "badminton.png" with the actual filename of your badminton image
ball_image = pygame.image.load("sprite\\ball.png")  # Replace "shuttlecock.png" with the actual filename of your shuttlecock image

badminton_image = pygame.transform.scale(badminton_image, (300, 150))
ball_image = pygame.transform.scale(ball_image, (50, 50))

# Get the width and height of the badminton image and shuttlecock image
badminton_width = badminton_image.get_width()
badminton_height = badminton_image.get_height()
ball_width = ball_image.get_width()
ball_height = ball_image.get_height()


cursor_x = width // 2  # Initial cursor position at the center horizontally
cursor_y = height - badminton_height  # Position the badminton at the bottom of the screen

ball_x = width // 2 - ball_width // 2  # Initial ball position at the center horizontally
ball_y = height // 2 - ball_height // 2  # Initial ball position at the center vertically

ball_speed_x = 1  # Horizontal speed of the ball
ball_speed_y = 1  # Vertical speed of the ball
