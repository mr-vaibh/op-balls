import pygame
from pygame.locals import *

import math

from sprites import badminton_height, badminton_width, badminton_image, cursor_x, cursor_y, ball_x, ball_y, ball_image, ball_height, ball_width, ball_speed_y, ball_speed_x

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Optometry Game")

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (255, 0, 0)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self, screen):
        # pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        return

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Reverse direction if the ball reaches the edges
        if self.x <= self.radius or self.x >= width - self.radius:
            self.speed_x *= -1
        if self.y <= self.radius or self.y >= height - self.radius:
            self.speed_y *= -1

    def check_collision(self, mouse_x, mouse_y):
        # Check if the mouse cursor is inside the ball
        if (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2 <= self.radius ** 2:
            print("Ball hit!")

ball = Ball(50, 50, 0.1, 0.1)  # Starting position and initial speeds

# Define colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

score = 0  # Initial score
font = pygame.font.Font(None, 36)  # Font for displaying the score

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            ball.check_collision(mouse_x, mouse_y)

    ball.update()

    # Fill the screen with green color
    screen.fill(GREEN)

    # Draw white margin on the borders
    pygame.draw.rect(screen, WHITE, (0, 0, width, 10))  # Top border
    pygame.draw.rect(screen, WHITE, (0, height-10, width, 10))  # Bottom border
    pygame.draw.rect(screen, WHITE, (0, 0, 10, height))  # Left border
    pygame.draw.rect(screen, WHITE, (width-10, 0, 10, height))  # Right border

    # Draw horizontal white line bisecting the screen
    pygame.draw.line(screen, WHITE, (0, height//2), (width, height//2), 2)

    cursor_x = pygame.mouse.get_pos()[0] - badminton_width // 2  # Center the badminton image with the cursor horizontally

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collision between the shuttle and the badminton
    if ball_x < cursor_x + badminton_width and ball_x + ball_width > cursor_x and ball_y < cursor_y + badminton_height and ball_y + ball_height > cursor_y:
        # Shuttle has collided with the badminton, change the direction
        ball_speed_y *= -1
        score += 1
    elif ball_y > cursor_y + badminton_height:
        # Ball has missed the badminton, reset the ball position
        ball_x = width // 2 - ball_width // 2
        ball_y = height // 2 - ball_height // 2

    # Check for collision with the edges of the screen
    if ball_x <= 0 or ball_x >= width - ball_width:
        ball_speed_x *= -1
    if ball_y <= 0 or ball_y >= height - ball_height:
        ball_speed_y *= -1
    
    # Calculate the angle of rotation based on shuttle's movement direction
    angle = math.degrees(math.atan2(ball_speed_y, ball_speed_x))
    rotated_shuttle = pygame.transform.rotate(ball_image, -angle)  # Rotate the shuttlecock image

    # Update shuttle width and height after rotation
    rotated_ball_width = rotated_shuttle.get_width()
    rotated_ball_height = rotated_shuttle.get_height()
    
    screen.blit(badminton_image, (cursor_x, cursor_y))  # Draw the badminton image at the current cursor position
    screen.blit(rotated_shuttle, (ball_x + ball_width // 2 - rotated_ball_width // 2, ball_y + ball_height // 2 - rotated_ball_height // 2))  # Draw the rotated shuttlecock image at the current shuttle position

    ball.draw(screen)

    # Display the score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
