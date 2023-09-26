import random
import pygame
from pygame import mixer

pygame.init()

PLAYER_DELTA_X = 10
BULLET_DELTA_Y = 10
READY = "ready"
SHOT = "shot"
ENEMY_DELTA_X = 7
ENEMY_DELTA_Y = 75
ENEMIES = 6

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("Spaceship.png"))

player = pygame.image.load("Player.png")
player_x = 0.5 * (screen_width - player.get_width())
player_y = (0.9 * screen_height) - (0.5 * player.get_height())
player_delta_x = 0

def draw_player(x, y):
    screen.blit(player, (x, y))

bullet = pygame.image.load("Bullet.png")
bullet_x = 0
bullet_y = 0
bullet_delta_y = 0
bullet_state = READY

def draw_bullet(x, y):
    screen.blit(bullet, (x, y))

class Enemy:
    def __init__(self):
        self.image = pygame.image.load("Enemy.png")
        self.x = random.randint(0, screen_width - self.image.get_width())
        self.y = random.randint(0, 0.25 * screen_height - self.image.get_height())
        initial_direction = random.randint(0, 1)    # 0 - left, 1 - right
        self.delta_x = -ENEMY_DELTA_X if initial_direction == 0 else ENEMY_DELTA_X
        self.delta_y = ENEMY_DELTA_Y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

enemies = []
for i in range(ENEMIES):
    enemies.append(Enemy())

score = 0
score_font = pygame.font.Font('KaushanScript-Regular.ttf', 42)
score_x = score_y = 0.03 * screen_height

def draw_score(x, y):
    score_render = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_render, (x, y))

game_over = False
game_over_font = pygame.font.Font('KaushanScript-Regular.ttf', 100)
game_over_x = 0.2 * screen_width
game_over_y = 0.2 * screen_height

def draw_game_over(x, y):
    game_over_render = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_render, (x, y))

background = pygame.image.load("Background.png")

mixer.music.load("Background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.5)

laser_sound = mixer.Sound("Laser.wav")
laser_sound.set_volume(0.2)

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_delta_x = -PLAYER_DELTA_X
                if event.key == pygame.K_RIGHT:
                    player_delta_x = PLAYER_DELTA_X
                if event.key == pygame.K_SPACE:
                    if bullet_state == READY:
                        laser_sound.play()
                        bullet_state = SHOT
                        bullet_x = player_x + (player.get_width() / 2) - (bullet.get_width() / 2)
                        bullet_y = player_y - (bullet.get_height() / 2)
                        draw_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_delta_x = 0
    
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    player_x += player_delta_x
    if player_x < 0 or player_x + player.get_width() > screen_width:
        player_x -= player_delta_x
    draw_player(player_x, player_y)

    for i in range(ENEMIES):
        enemies[i].x += enemies[i].delta_x
        if enemies[i].x < 0 or enemies[i].x + enemies[i].image.get_width() > screen_width:
            enemies[i].x -= enemies[i].delta_x
            enemies[i].delta_x = -enemies[i].delta_x
            enemies[i].y += enemies[i].delta_y
        enemies[i].draw()
        if enemies[i].image.get_rect(topleft=(enemies[i].x, enemies[i].y)).colliderect(player.get_rect(topleft=(player_x, player_y))):
            for i in range(ENEMIES):
                enemies[i].y = 3 * screen_height
            game_over = True
            break

    if bullet_state == SHOT:
        for i in range(ENEMIES):
            if enemies[i].image.get_rect(topleft=(enemies[i].x, enemies[i].y)).colliderect(bullet.get_rect(topleft=(bullet_x, bullet_y))):
                score += 1
                enemies[i].x = random.randint(0, screen_width - enemies[i].image.get_width())
                enemies[i].y = random.randint(0, 0.25 * screen_height - enemies[i].image.get_height())
                bullet_state = READY
    
    if bullet_state == SHOT:
        if bullet_y + bullet.get_height() >= 0:
            bullet_y -= BULLET_DELTA_Y
            draw_bullet(bullet_x, bullet_y)
        else:
            bullet_state = READY
    
    if game_over:
        draw_game_over(game_over_x, game_over_y)
    
    draw_score(score_x, score_y)

    pygame.display.update()