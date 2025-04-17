import pygame
import sys
import random

# Initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 40)
WHITE = (255, 255, 255)
PADDLE_COLOR = (50, 150, 255)
BALL_COLOR = (255, 100, 100)
SHADOW_COLOR = (0, 0, 0, 100)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED = 5

# Screen and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

# Game objects
player1 = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 60, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

score1 = 0
score2 = 0
game_over = False
winner_text = ""
single_player = False

# Music only (no sound effects)
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1, 0.0)

def draw_text(text, y, font_size=36, color=WHITE):
    t = pygame.font.SysFont("Arial", font_size).render(text, True, color)
    screen.blit(t, (WIDTH//2 - t.get_width()//2, y))

def main_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text("PONG GAME", 100, 72, WHITE)
        draw_text("1 - Start Game", 200, 48)
        draw_text("2 - Credits", 260, 48)
        draw_text("3 - Exit", 320, 48)
        
        # Mouse interaction for menu options
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if 200 < mouse_y < 250 and 1 < mouse_x < 300:
            if mouse_click:
                choose_mode()
        if 260 < mouse_y < 310 and 1 < mouse_x < 300:
            if mouse_click:
                show_credits()
        if 320 < mouse_y < 370 and 1 < mouse_x < 300:
            if mouse_click:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    choose_mode()
                elif e.key == pygame.K_2:
                    show_credits()
                elif e.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def show_credits():
    screen.fill(BACKGROUND_COLOR)
    draw_text(" * Made by Parsa Heshmati * ", HEIGHT//2, 48, WHITE)
    pygame.display.flip()
    pygame.time.wait(2000)

def choose_mode():
    global single_player
    screen.fill(BACKGROUND_COLOR)
    draw_text("Play against Robot? (Y/N)", HEIGHT//2, 48, WHITE)
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_y:
                    single_player = True
                    start_game()
                elif e.key == pygame.K_n:
                    single_player = False
                    start_game()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = BALL_SPEED * random.choice((1, -1))
    ball_speed_y = BALL_SPEED * random.choice((1, -1))

def start_game():
    global score1, score2, game_over, winner_text, ball_speed_x, ball_speed_y

    score1 = 0
    score2 = 0
    reset_ball()

    while True:
        screen.fill(BACKGROUND_COLOR)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player1.top > 0:
            player1.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player1.bottom < HEIGHT:
            player1.y += PADDLE_SPEED

        if not single_player:
            if keys[pygame.K_w] and player2.top > 0:
                player2.y -= PADDLE_SPEED
            if keys[pygame.K_s] and player2.bottom < HEIGHT:
                player2.y += PADDLE_SPEED
        else:
            if ball.centerx > WIDTH//2 and ball_speed_x > 0:
                if player2.centery < ball.centery and player2.bottom < HEIGHT:
                    player2.y += PADDLE_SPEED - random.randint(1, 3)
                elif player2.centery > ball.centery and player2.top > 0:
                    player2.y -= PADDLE_SPEED - random.randint(1, 3)
                if random.random() < 0.05:
                    player2.y += random.choice([-1, 1]) * random.randint(1, 3)

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        if ball.left <= 0:
            score2 += 1
            reset_ball()
        if ball.right >= WIDTH:
            score1 += 1
            reset_ball()

        if score1 >= 5:
            winner_text = "Player 1 Wins!"
            game_over = True
        elif score2 >= 5:
            winner_text = "Robot Wins!" if single_player else "Player 2 Wins!"
            game_over = True

        pygame.draw.rect(screen, PADDLE_COLOR, player1)
        pygame.draw.rect(screen, PADDLE_COLOR, player2)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        draw_text(f"{score1} - {score2}", 20, 48)

        pygame.display.flip()
        clock.tick(60)

        if game_over:
            screen.fill(BACKGROUND_COLOR)
            draw_text(winner_text, HEIGHT//2, 72, WHITE)
            pygame.display.flip()
            pygame.time.wait(3000)
            game_over = False
            main_menu()

main_menu()
