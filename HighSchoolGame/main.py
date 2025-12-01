import pygame
from pygame import mixer
from player import Player
from enemy import Enemy
from bullet import Bullet

mode = 0
intro_count = 10
is_counting = True
last_count_update = pygame.time.get_ticks()

mixer.init()
pygame.init()

# Set up the screen window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Game")

# Set frame-rate
clock = pygame.time.Clock()
FPS = 60

# player variables
PLAYER_SIZE = 32
PLAYER_SCALE = 3
PLAYER_OFFSET = [7, 5]
PLAYER_DATA = [PLAYER_SIZE, PLAYER_SCALE, PLAYER_OFFSET]

# enemy vars
ENEMY_SIZE = 96
ENEMY_SCALE = 4.5
ENEMY_OFFSET = [10.05, 0]
ENEMY_DATA = [ENEMY_SIZE, ENEMY_SCALE, ENEMY_OFFSET]

# bullet stuff
bullet_group = pygame.sprite.Group()
split_group = pygame.sprite.Group()

# Background image
bg_img = pygame.image.load("assets/images/background/background.png").convert_alpha()
overlap = pygame.image.load("assets/images/background/background.png").convert_alpha()
scaled_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
scaled_ov = pygame.transform.scale(overlap, (SCREEN_WIDTH, SCREEN_HEIGHT))
b_pos = 0
o_pos = 1000
speed = -3
moving_background = False
no_background = False


bad_death_sound = pygame.mixer.Sound("assets/music/moai.mp3")
bad_death_sound.set_volume(3)

music = pygame.mixer.music
music.load("assets/music/(Official) Tower Defense Simulator OST - Raze The Void.wav")
music.set_volume(0.5)

count_font = pygame.font.Font("assets/fonts/EvilEmpire.otf", 80)

# load spreadsheets
player_sheet = pygame.image.load("assets/images/player/sprites/plane_movementV2.png").convert_alpha()
player_animation_steps = [8, 3, 3, 4]

boss_sheet = pygame.image.load("assets/images/enemy/BAD/sprites/Boss_enrage_ana (1).png").convert_alpha()
enemy_animation_steps = [8, 6, 6, 6, 6, 6, 6]


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


def draw_health_bar_e(health, x, y):
    boss_ratio = health / 5000
    pygame.draw.rect(screen, (255, 255, 255), (x - 2, y - 2, 304, 34))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 300, 30))
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 300 * boss_ratio, 30))


def draw_health_bar_p(health, x, y):
    player_ratio = health / 500
    pygame.draw.rect(screen, (255, 255, 255), (x - 2, y - 2, 304, 34))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 300, 30))
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 300 * player_ratio, 30))


def draw_menu():
    pygame.draw.rect(screen, (0, 0, 0), ((SCREEN_WIDTH / 3) - 80, SCREEN_HEIGHT / 2, 650, 100))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create player
player_1 = Player(640, 700, PLAYER_DATA, player_sheet, player_animation_steps)
bad = Enemy(500, -500, ENEMY_DATA, boss_sheet, enemy_animation_steps, bad_death_sound)

# Set up game loop
run = True
while run:
    if mode == 0:
        screen.fill((100, 100, 100))
        draw_menu()
        draw_text("Press Space to Start", count_font, (50, 50, 50), (SCREEN_WIDTH / 3) - 70, SCREEN_HEIGHT / 2)
    if mode == 1:
        clock.tick(FPS)
        if moving_background is True:
            if b_pos >= SCREEN_HEIGHT:
                b_pos = -SCREEN_HEIGHT
            if o_pos >= SCREEN_HEIGHT:
                o_pos = -SCREEN_HEIGHT

            b_pos -= speed
            o_pos -= speed
            screen.blit(scaled_bg, (0, b_pos))
            screen.blit(scaled_ov, (0, o_pos))
        elif no_background is True:
            screen.fill('black')
        else:
            draw_bg()
        #screen.fill('black')

        if intro_count <= 0:
            player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, bullet_group, bad)
            is_counting = False
        else:
            draw_text(str(intro_count), count_font, (255, 0, 0), (SCREEN_WIDTH / 2) - 50, SCREEN_HEIGHT / 2)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        bad.enemy_actions(SCREEN_WIDTH, SCREEN_HEIGHT, screen, bullet_group, split_group, player_1, is_counting)

        player_1.update()
        bad.update()
        player_1.draw(screen)
        bad.draw(screen)
        split_group.update(bullet_group, split_group)
        bullet_group.update(bullet_group, split_group)
        bullet_group.draw(screen)
        split_group.draw(screen)
        draw_health_bar_p(player_1.health, SCREEN_WIDTH - (SCREEN_WIDTH / 1.002), SCREEN_HEIGHT - (SCREEN_HEIGHT / 1.022))
        draw_text("Player HP", pygame.font.Font("assets/fonts/EvilEmpire.otf", 35), (50, 50, 50), SCREEN_WIDTH - (SCREEN_WIDTH / 1.001), SCREEN_HEIGHT - (SCREEN_HEIGHT / 1.022))
        draw_health_bar_e(bad.health, SCREEN_WIDTH - 305, SCREEN_HEIGHT - (SCREEN_HEIGHT / 1.022))
        draw_text("Boss HP", pygame.font.Font("assets/fonts/EvilEmpire.otf", 35), (50, 50, 50), SCREEN_WIDTH - 300, SCREEN_HEIGHT - (SCREEN_HEIGHT / 1.022))

        if player_1.health <= 0:
            mode = 3
            screen.fill((100, 100, 100))
            draw_text("You Died", count_font, (50, 50, 50), (SCREEN_WIDTH / 3) - 70, SCREEN_HEIGHT / 2)
        if bad.alive is False:
            mode = 4
            
            screen.fill((100, 100, 100))
            draw_text("You beat le boss!", count_font, (50, 50, 50), (SCREEN_WIDTH / 3) - 70, SCREEN_HEIGHT / 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quit")
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                moving_background = True
                no_background = False
            if event.key == pygame.K_2:
                moving_background = False
                no_background = False
            if event.key == pygame.K_3:
                no_background = True
            if event.key == pygame.K_SPACE and mode == 0:
                mode = 1
                music.play(-1)

    pygame.display.update()
pygame.quit()