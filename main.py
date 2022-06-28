import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

# generates the enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_ready = True

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


# displays the score on the screen
def show_score(x, y):
    score = font.render(str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


# displays "game over" on the screen when you lose
def game_over_text():
    over_text = over_font.render("game over", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


# displays the player on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# displays an enemy on the screen
def enemy(x, y, j):
    screen.blit(enemyImg[j], (x, y))


# fires a bullet if ready
def fire_bullet(x, y):
    global bullet_ready
    bullet_ready = False
    screen.blit(bulletImg, (x + 16, y + 10))


# determines if the bullet hits an enemy
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
# game continues until program is no longer running
while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # player moves left
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            # player moves right
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            # player fires bullet
            if event.key == pygame.K_SPACE:
                if bullet_ready:
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # prevents player from going off of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        # if enemy reaches the player, game will end
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # enemies move
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # checks for collision of enemy and bullet. enemy will respawn towards top of screen if hit
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_ready = True
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

    # checks if bullet is ready to be fired
    if bulletY <= 0:
        bulletY = 480
        bullet_ready = True

    # current bullet keeps moving if it is not off the screen yet
    if bullet_ready is False:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
