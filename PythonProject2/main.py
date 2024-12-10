import pygame
import sys
import random

pygame.init()

SW, SH = 800, 800

BLOCK_SIZE = 30
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE * 2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake!")
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

        self.snake_head_image = pygame.image.load("snake_head.png")
        self.snake_head_image = pygame.transform.scale(self.snake_head_image, (BLOCK_SIZE, BLOCK_SIZE))

    def update(self):
        global apple

        # Check for collisions with the snake's body
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True

        # Check if the snake hits the borders
        if self.head.x < 0 or self.head.x >= SW or self.head.y < 0 or self.head.y >= SH:
            self.dead = True

        # Move the snake body
        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

    def grow(self):
        # Adds a new segment to the snake's body when it eats the apple
        self.body.append(pygame.Rect(self.body[-1].x, self.body[-1].y, BLOCK_SIZE, BLOCK_SIZE))

    def reset(self):
        # Reset the game state when snake dies
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.xdir = 1
        self.ydir = 0
        self.dead = False
        global apple
        apple = Apple()


class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.float_direction = 1  # Direction of floating (up or down)
        self.float_speed = 1  # Speed of floating

        # Load apple image
        self.apple_image = pygame.image.load("apple.png")  # Ensure the apple.png image is in the directory
        self.apple_image = pygame.transform.scale(self.apple_image, (BLOCK_SIZE, BLOCK_SIZE))  # Resize image

    def update(self):
        # Float the apple up and down
        if self.rect.top <= 0 or self.rect.bottom >= SH:
            self.float_direction *= -1  # Reverse direction when hitting top or bottom
        self.rect.y += self.float_direction * self.float_speed

        # Draw the floating apple
        screen.blit(self.apple_image, self.rect)


score = 0
score_text = FONT.render(f"Score: {score}", True, "white")
score_rect = score_text.get_rect(center=(SW / 2, SH / 20))

snake = Snake()
apple = Apple()

def display_message(text, size, color, center):
    font = pygame.font.Font(None, size)
    msg = font.render(text, True, color)
    msg_rect = msg.get_rect(center=center)
    screen.blit(msg, msg_rect)


def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    display_message(text, 40, "white", rect.center)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if snake.dead:  # Restart the game if dead and any key is pressed
                snake.reset()
                score = 0  # Reset score
                score_text = FONT.render(f"Score: {score}", True, "white")

            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1
        if snake.dead and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if exit_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()
    if snake.dead:
        # Game Over Screen
        screen.fill("black")
        display_message("Game Over", 80, "red", (SW // 2, SH // 2 - 50))
        display_message(f"Score: {score}", 50, "white", (SW // 2, SH // 2 + 50))
        display_message("Press any key to restart", 40, "white", (SW // 2, SH // 2 + 100))

        # Exit Button
        exit_button_rect = pygame.Rect(SW // 2 - 100, SH // 2 + 150, 200, 50)
        draw_button("Exit", exit_button_rect, "red")

        pygame.display.update()
        continue  # Skip the rest of the game loop if dead

    # Update the game
    snake.update()

    # Fill the screen with black
    screen.fill('black')

    # Update apple position
    apple.update()

    # Render the score
    score = len(snake.body) - 1  # Score is the length of the snake minus 1 (head doesn't count)
    score_text = FONT.render(f"Score: {score}", True, "white")
    screen.blit(score_text, score_rect)

    # Draw the snake (head and body)
    pygame.draw.rect(screen, "lightgreen", snake.head)  # Lighter green for snake head
    for square in snake.body:
        pygame.draw.rect(screen, "green", square)  # Darker green for body

    # Check if the snake has eaten the apple by comparing rects
    if snake.head.colliderect(apple.rect):
        snake.grow()  # Grow the snake by adding a new body segment
        apple = Apple()  # Generate a new apple

    pygame.display.update()
    clock.tick(10)
