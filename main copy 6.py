import pygame
import sys
from random import randint

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collect Coins")

game_over = False

game_font = pygame.font.SysFont("Arial", 24)

robot = pygame.image.load("robot.png")
coin = pygame.image.load("coin.png")
coins = 0
monster = pygame.image.load("monster.png")

robot_rect = robot.get_rect()
coin_rect = coin.get_rect()
monster_rect = monster.get_rect()

robot_rect.x = width/2-robot.get_width()/2
robot_rect.y = (height-40)/2-robot.get_height()/2
coin_rect.x = randint(0, width - coin_rect.width)
coin_rect.y = randint(40, height - coin_rect.height)

def new_monster():
    i = randint(1, 4)
    if i == 1:
        monster_rect.x = randint(0, width+100)
        monster_rect.y = -100
    if i == 2:
        monster_rect.x = width+100
        monster_rect.y = randint(0, height+100)
    if i == 3:
        monster_rect.x = randint(-100, width)
        monster_rect.y = height+100
    if i == 4:
        monster_rect.x = -100
        monster_rect.y = randint(-100, height)

def get_direction():
    if width/2 <= monster_rect.x and monster_rect.y < height/2:
        monster_direction = 1
    if width/2 <= monster_rect.x and height/2 <= monster_rect.y:
        monster_direction = 2
    if width/2 > monster_rect.x and height/2 < monster_rect.y:
        monster_direction = 3
    if width/2 > monster_rect.x and height/2 > monster_rect.y:
        monster_direction = 4
    return monster_direction

monster_direction = get_direction()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            robot_rect.x -= 3
        if keys[pygame.K_RIGHT]:
            robot_rect.x += 3
        if keys[pygame.K_UP]:
            robot_rect.y -= 3
        if keys[pygame.K_DOWN]:
            robot_rect.y += 3

    # four walls
    robot_rect.x = max(robot_rect.x,0)
    robot_rect.x = min(robot_rect.x, width- robot.get_width())
    robot_rect.y = max(robot_rect.y,40)
    robot_rect.y = min(robot_rect.y, height- robot.get_height())

    if keys[pygame.K_F2]: #new game
        coins = 0
        robot_rect.x = width/2-robot.get_width()/2
        robot_rect.y = (height-40)/2-robot.get_height()/2
        game_over = False
        new_monster()
    if keys[pygame.K_ESCAPE]:
        exit()

    # Check for collision
    if robot_rect.colliderect(coin_rect):
        coin_rect.x = randint(0, width - coin_rect.width)
        coin_rect.y = randint(40, height - coin_rect.height)
        coins += 1

    if robot_rect.colliderect(monster_rect):
        game_over = True

    screen.fill((0, 153, 76))
    screen.blit(coin, coin_rect)
    screen.blit(robot, robot_rect)
    screen.blit(monster, monster_rect)

    if not game_over:
        if coins < 10:
            monster_velocity = 1
        if 10 < coins < 20:
            monster_velocity = 2
        if 20 < coins < 30:
            monster_velocity = 3
        if 30 < coins < 40:
            monster_velocity = 4
        if 40 < coins:
            monster_velocity = 5

        if monster_direction == 1:
            monster_rect.x -= monster_velocity
            monster_rect.y += monster_velocity
            if monster_rect.y > height or monster_rect.x < 0-monster.get_width():
                new_monster()
                monster_direction = get_direction()
        if monster_direction == 2:
            monster_rect.x -= monster_velocity
            monster_rect.y -= monster_velocity
            if monster_rect.y < 0-monster.get_height() or monster_rect.x < 0-monster.get_width():
                new_monster()
                monster_direction = get_direction()
        if monster_direction == 3:
            monster_rect.x += monster_velocity
            monster_rect.y -= monster_velocity
            if monster_rect.y < 0-monster.get_height() or monster_rect.x > width:
                new_monster()
                monster_direction = get_direction()
        if monster_direction == 4:
            monster_rect.x += monster_velocity
            monster_rect.y += monster_velocity
            if monster_rect.y > height or monster_rect.x > width:
                new_monster()
                monster_direction = get_direction()
        
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, 40))
    pygame.draw.circle(screen, (255, 255, 0), (30, 18), 10)
    pygame.draw.circle(screen, (0, 0, 0), (30, 18), 10, 1)
    game_text = game_font.render(str(coins), True, (255, 0, 0))
    screen.blit(game_text, (50, 5))
        
    game_text = game_font.render("F2 = new game", True, (255, 0, 0))
    screen.blit(game_text, (200, 5))

    game_text = game_font.render("Esc = exit game", True, (255, 0, 0))
    screen.blit(game_text, (400, 5))

    pygame.draw.line(screen, (255, 0, 0), (0, 40), (width, 40))

    if game_over:
        game_text = game_font.render(f"Game over. You've collected {coins} coins.", True, (255, 0, 0))
        game_text_x = width / 2 - game_text.get_width() / 2
        game_text_y = height / 2 - game_text.get_height() / 2
        pygame.draw.rect(screen, (0, 0, 0), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
        screen.blit(game_text, (game_text_x, game_text_y))

    pygame.display.flip()
    clock.tick(60)
