import pygame
import random

# Revenge of Chicken
# Date: 10 May 2021 00:18

# Intialize the Pygame
pygame.init()

# Create the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
background = pygame.image.load('background.jpg')

# Game Setting
pygame.display.set_caption("Revenge of Chicken")
icon = pygame.image.load('chicken.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('Montserrat-Regular.ttf', 32)
game_over_img = pygame.image.load('gameover.jpg')
go_img_width = game_over_img.get_width()
go_img_height = game_over_img.get_height()

# blur screen
blur_screen = pygame.Surface((screen_width, screen_height))  # the size of your rect
blur_screen.set_alpha(128)
blur_screen.fill((0, 0, 0))
# 1 is playing, 0 is game over
game_state = 1

# enemy setting
time_to_create = 1
start_time = 0
time_to_fire = 5

# Bullet
bulletImg = pygame.image.load('bullet.png')
bullet_width = bulletImg.get_width()
bullet_height = bulletImg.get_height()

# Player
playerImg = pygame.image.load('me.png')
player_width = playerImg.get_width()
player_height = playerImg.get_height()
player_fire_pos = [player_width / 2 - bullet_width / 2, bullet_height]
player_default_x = screen_width / 2 - player_width / 2
player_default_y = 480
player_x = player_default_x
player_y = player_default_y
player_direction = 0
player_xSpeed = 1
score_value = 0
can_fire = 1
bullet_num = 2

# ufo
enemyImg = pygame.image.load('ufo.png')
enemyWidth = enemyImg.get_width()
enemyHeight = enemyImg.get_height()
enemyGoDownDistance = enemyHeight / 2
enemyX_speed = 0.6

# pan
pan_img = pygame.image.load('pan.png')
pan_width = pan_img.get_width()
pan_height = pan_img.get_height()


class Enemy:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.timer = get_now_time()

    speed = 0.6
    state = 1

    global pans

    def flying(self):
        if self.state == 1:
            global game_state
            # fire pan
            if get_time(self.timer) == time_to_fire:
                pans.append(Pan(self.x + enemyWidth / 2, self.y + enemyWidth))
                self.timer = get_now_time()
            # bounding
            if self.x < 0 or self.x > screen_width - enemyWidth:
                self.speed *= -1
                self.y += enemyGoDownDistance
                self.speed *= 1.3
            self.x += self.speed
            screen.blit(enemyImg, (self.x, self.y))

            # check collision
            if check_collision(player_x, player_y, player_width, player_height, self.x, self.y, enemyWidth,
                               enemyHeight) or self.y > 480:
                game_state = 0


class Bullet:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    speed = 2
    state = 1

    def flying(self):
        if self.state == 1:
            if self.y < 0:
                self.state = 0
            self.y -= self.speed
            screen.blit(bulletImg, (self.x, self.y))


class Pan:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    speed = 1.5
    state = 1

    def flying(self):
        if self.state == 1:
            if self.y > screen_height:
                self.state = 0
            if check_collision(self.x, self.y, pan_width, pan_height, player_x, player_y, player_width, player_height):
                global game_state
                game_state = 0
            self.y += self.speed
            screen.blit(pan_img, (self.x, self.y))


def get_time(st):
    return (pygame.time.get_ticks() - st) / 1000


def get_now_time():
    return pygame.time.get_ticks()


def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    dist_x = (x1 + (w1 / 2) - 5) - (x2 + (w2 / 2) - 5)
    if dist_x < 0:
        dist_x = -dist_x
    dist_w = (w1 + w2) / 2
    dist_y = (y1 + (h1 / 2) - 5) - (y2 + (h2 / 2) - 5)
    if dist_y < 0:
        dist_y = -dist_y
    dist_h = (h1 + h2) / 2
    return dist_x <= dist_w and dist_y <= dist_h


def player():
    global player_x, player_xSpeed, player_direction, can_fire

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player_direction = -1
        if event.key == pygame.K_RIGHT:
            player_direction = 1
        if event.key == pygame.K_UP:
            fire()
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            player_direction = 0
        if event.key == pygame.K_UP:
            can_fire = 1

    player_x += player_xSpeed * player_direction
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_width:
        player_x = screen_width - player_width

    screen.blit(playerImg, (player_x, player_y))


# Bullet

def fire():
    global can_fire, bullet_num
    if can_fire == 1 and bullet_num > 0:
        bullet_x = player_x + player_fire_pos[0]
        bullet_y = player_y - player_fire_pos[1]
        bullets.append(Bullet(bullet_x, bullet_y))
        bullet_num -= 1
    can_fire = 0


bullets = []


def loop_fire():
    global bullets
    t_bullets = []
    for bullet in bullets:
        for enemy in enemies:
            if check_collision(bullet.x, bullet.y, bullet_width, bullet_height, enemy.x, enemy.y, enemyWidth,
                               enemyHeight):
                kill_enemy()
                enemy.state = 0
                bullet.state = 0
        bullet.flying()
        if bullet.state == 1:
            t_bullets.append(bullet)
    bullets = t_bullets


# Enemies
enemies = []


def create_enemy():
    enemy_x = random.randint(0, screen_width - enemyWidth)
    enemy_y = 50
    enemies.append(Enemy(enemy_x, enemy_y))


def loop_enemies():
    global enemies, start_time
    if get_time(start_time) >= time_to_create:
        create_enemy()
        start_time = get_now_time()

    if len(enemies) == 0:
        create_enemy()
    t_enemies = []
    for enemy in enemies:
        enemy.flying()
        if enemy.state == 1:
            t_enemies.append(enemy)
    enemies = t_enemies


# Pan

pans = []


def loop_pan():
    global pans
    t_pans = []
    for pan in pans:
        pan.flying()
        if pan.state == 1:
            t_pans.append(pan)
    pans = t_pans


# Show Score
def show_ui():
    global score_value, bullet_num
    score = font.render("Scores: " + str(score_value), True, (255, 255, 255))
    bullet = font.render("Bullets: " + str(bullet_num), True, (255, 255, 255))
    screen.blit(score, (50, 10))
    screen.blit(bullet, (50, 40))


# Game

def kill_enemy():
    global score_value, bullet_num
    score_value += 10
    bullet_num += 2


def game_init():
    global score_value, bullet_num, start_time, bullets, enemies, pans, player_x, player_y

    player_x = player_default_x
    player_y = player_default_y
    bullets = []
    enemies = []
    pans = []
    score_value = 0
    bullet_num = 2
    create_enemy()
    start_time = pygame.time.get_ticks()


# Check if game is over

def check_game_over():
    global game_state
    if game_state == 1:
        if len(bullets) == 0 and bullet_num == 0:
            game_state = 0
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            game_state = 1
            game_init()


# Game Loop
game_init()
running = True
while running:
    screen.fill((153, 221, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == 1:
        player()
        loop_fire()
        loop_enemies()
        loop_pan()
    else:
        screen.blit(blur_screen, (0, 0))
        screen.blit(game_over_img, (screen_width / 2 - go_img_width / 2, screen_height / 2 - go_img_height / 2))
    show_ui()
    check_game_over()
    pygame.display.update()
