import pygame
import time
import random

class SnakeGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Game settings
        self.window_x = 720
        self.window_y = 480
        self.snake_speed = 12

        # Colors
        self.colors = {
            'black': pygame.Color(0, 0, 0),
            'white': pygame.Color(255, 255, 255),
            'red': pygame.Color(255, 0, 0),
            'green': pygame.Color(0, 255, 0)
        }

        # Create game window
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        pygame.display.set_caption('Snake Game')

        # Load sound effects
        pygame.mixer.init()
        self.eat_sound = pygame.mixer.Sound('eat.wav')  # Replace with an existing sound file

        # Initialize game variables
        self.restart_game()

    def restart_game(self):
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                               random.randrange(1, (self.window_y // 10)) * 10]
        self.fruit_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.snake_speed = 12
        self.fps = pygame.time.Clock()

    def show_score(self):
        font = pygame.font.SysFont('times new roman', 20)
        score_surface = font.render(f'Score: {self.score}', True, self.colors['white'])
        self.game_window.blit(score_surface, (10, 10))

    def game_over(self):
        font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = font.render(f'Your Score is: {self.score}', True, self.colors['red'])
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_x / 2, self.window_y / 4)
        self.game_window.fill(self.colors['black'])
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    def run(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'

            # Direction logic
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # Update snake position
            if self.direction == 'UP':
                self.snake_position[1] -= 10
            if self.direction == 'DOWN':
                self.snake_position[1] += 10
            if self.direction == 'LEFT':
                self.snake_position[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_position[0] += 10

            # Snake growing logic
            self.snake_body.insert(0, list(self.snake_position))
            if (self.snake_position[0] == self.fruit_position[0] and
                    self.snake_position[1] == self.fruit_position[1]):
                self.score += 10
                pygame.mixer.Sound.play(self.eat_sound)
                self.snake_speed += 1
                self.fruit_spawn = False
            else:
                self.snake_body.pop()

            if not self.fruit_spawn:
                self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                                       random.randrange(1, (self.window_y // 10)) * 10]
            self.fruit_spawn = True

            # Draw the game
            self.game_window.fill(self.colors['black'])
            for pos in self.snake_body:
                pygame.draw.rect(self.game_window, self.colors['green'], pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(self.game_window, self.colors['white'],
                             pygame.Rect(self.fruit_position[0], self.fruit_position[1], 10, 10))

            # Game over conditions
            if (self.snake_position[0] < 0 or self.snake_position[0] > self.window_x - 10 or
                    self.snake_position[1] < 0 or self.snake_position[1] > self.window_y - 10):
                self.game_over()

          
