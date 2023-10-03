import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])

        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body = [new_head] + self.body[:-1]

    def change_direction(self, new_direction):
        if new_direction == UP and self.direction != DOWN:
            self.direction = new_direction
        elif new_direction == DOWN and self.direction != UP:
            self.direction = new_direction
        elif new_direction == LEFT and self.direction != RIGHT:
            self.direction = new_direction
        elif new_direction == RIGHT and self.direction != LEFT:
            self.direction = new_direction

    def check_collision(self):
        if (
            self.body[0][0] < 0
            or self.body[0][0] >= GRID_WIDTH
            or self.body[0][1] < 0
            or self.body[0][1] >= GRID_HEIGHT
        ):
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False

    def grow_snake(self):
        self.grow = True

    def get_head_position(self):
        return self.body[0]

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.is_food_on_screen = True

    def spawn_food(self):
        if not self.is_food_on_screen:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            self.is_food_on_screen = True
        return self.position

    def set_food_on_screen(self, choice):
        self.is_food_on_screen = choice

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Initialize snake and food
snake = Snake()
food = Food()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)

    snake.move()
    if snake.check_collision():
        pygame.quit()
        sys.exit()

    if snake.get_head_position() == food.position:
        snake.grow_snake()
        food.set_food_on_screen(False)

    screen.fill(BLACK)

    for position in snake.body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    food_position = food.spawn_food()
    pygame.draw.rect(screen, WHITE, pygame.Rect(food_position[0] * GRID_SIZE, food_position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    pygame.time.Clock().tick(10)