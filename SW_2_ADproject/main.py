# 1 - Import library
import pygame
from pygame.locals import *
import random

# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
key1 = [False, False]
playerpos1 = [10, height // 2]
key2 = [False, False]
playerpos2 = [width - 75, height // 2]
arrow1_xy = []
arrow2_xy = []
healthvalue_1 = 194
healthvalue_2 = 194
pygame.mixer.init()
p1_potion_cnt = 1
p2_potion_cnt = 1

# 3 - Load images
player1 = pygame.image.load("resources/images/dude.png")
player2 = pygame.image.load("resources/images/dude2.png")
player2 = pygame.transform.rotate(player2, 180)
grass = pygame.image.load("resources/images/grass.png")
arrow = pygame.image.load("resources/images/bullet.png")
re_arrow = pygame.transform.rotate(arrow, 180)
potion = pygame.image.load("resources/images/potion.png")
FPS = 70
fpsClock = pygame.time.Clock()
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
player1_win = pygame.image.load("resources/images/player1_win.png")
player2_win = pygame.image.load("resources/images/player2_win.png")
# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - keep looping through
while 1:
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))

    # 6.2 - Draw arrows
    if len(arrow1_xy) != 0:
        for ax,ay in arrow1_xy:
            screen.blit(arrow, (ax,ay))
    if len(arrow2_xy) != 0:
        for ax,ay in arrow2_xy:
            screen.blit(re_arrow, (ax,ay))

    # 6.3.2 - Check for collisions
    index1 = 0
    for bullet in arrow1_xy:
        player2rect = pygame.Rect(player2.get_rect())
        player2rect.left = playerpos2[0]
        player2rect.top = playerpos2[1]
        bullrect = pygame.Rect(arrow.get_rect())
        bullrect.left = bullet[0]
        bullrect.top = bullet[1]
        if player2rect.colliderect(bullrect):
            hit.play()
            arrow1_xy.pop(index1)
            print('아야2')
            healthvalue_2 -= random.randint(8,20)
            if healthvalue_2 < 0:
                healthvalue_2 = 0
        index1 += 1

    index1 = 0
    for bullet in arrow2_xy:
        player1rect = pygame.Rect(player1.get_rect())
        player1rect.left = playerpos1[0]
        player1rect.top = playerpos1[1]
        bullrect = pygame.Rect(arrow.get_rect())
        bullrect.left = bullet[0]
        bullrect.top = bullet[1]
        if player1rect.colliderect(bullrect):
            hit.play()
            arrow2_xy.pop(index1)
            print('아야1')
            healthvalue_1 -= random.randint(8,20)
            if healthvalue_1 < 0:
                healthvalue_1 = 0
        index1 += 1

    # 6.5 - Draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue_1):
        screen.blit(health, (health1+8,8))
    screen.blit(healthbar, (width - 205, 5))
    for health1 in range(width - 1, (width - 1) - healthvalue_2, -1):
        screen.blit(health, (health1 - 8, 8))

    # 6.6 - Draw potion
    if p1_potion_cnt != 0:
        screen.blit(potion, (215, 5))
    if p2_potion_cnt != 0:
        screen.blit(potion, (width - 240, 5))

    # Draw player
    screen.blit(player1, playerpos1)
    screen.blit(player2, playerpos2)


    # 7 - update the screensw
    pygame.display.flip()
    fpsClock.tick(FPS)

    # 8 - loop through the eventsw
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            print(event.key)
            #shoot arrow
            if event.key==pygame.K_SPACE:
                shoot.play()
                arrow1_x = playerpos1[0]
                arrow1_y = playerpos1[1] + 30
                arrow1_xy.append([arrow1_x,arrow1_y])
            if event.key==pygame.K_SLASH:
                shoot.play()
                arrow2_x = playerpos2[0]
                arrow2_y = playerpos2[1] + 5
                arrow2_xy.append([arrow2_x,arrow2_y])
            #drink potion
            if event.key==pygame.K_q and p1_potion_cnt > 0:
                healthvalue_1 += random.randint(30, 100)
                if healthvalue_1 > 194:
                    healthvalue_1 = 194
                p1_potion_cnt -= 1
            if event.key==59 and p2_potion_cnt > 0:
                healthvalue_2 += random.randint(30, 100)
                if healthvalue_2 > 194:
                    healthvalue_2 = 194
                p2_potion_cnt -= 1
            #player1's keydown
            if event.key==K_w:
                key1[0]=True
            elif event.key==K_s:
                key1[1]=True
            #player2's keydown
            elif event.key==K_UP:
                key2[0]=True
            elif event.key==K_DOWN:
                key2[1]=True

        if event.type == pygame.KEYUP:
            #player1's keyup
            if event.key==pygame.K_w:
                key1[0]=False
            elif event.key==pygame.K_s:
                key1[1]=False

            #player2's keyup
            elif event.key==pygame.K_UP:
                key2[0]=False
            elif event.key==pygame.K_DOWN:
                key2[1]=False

    # 9.1 - Move player1
    if key1[0]:
        if playerpos1[1] > 50:
            playerpos1[1]-=5
    elif key1[1]:
        if playerpos1[1] < height - 60:
            playerpos1[1]+=5

    # 9.2 - Move player2
    if key2[0]:
        if playerpos2[1] > 50:
            playerpos2[1]-=5
    elif key2[1]:
        if playerpos2[1] < height - 60:
            playerpos2[1]+=5

    if len(arrow1_xy) != 0:
        for i, axy in enumerate(arrow1_xy):
            axy[0] += 20

            arrow1_xy[i][0] = axy[0]
            if axy[0] >= width:
                arrow1_xy.remove(axy)

    if len(arrow2_xy) != 0:
        for i, axy in enumerate(arrow2_xy):
            axy[0] -= 20
            arrow2_xy[i][0] = axy[0]
            if axy[0] <= 0:
                arrow2_xy.remove(axy)

    #10 - Winner check
    if healthvalue_1 == 0:
        running = 0
        winner = 2
        break
    elif healthvalue_2 == 0:
        running = 0
        winner = 1
        break

# 11 - Win/lose display
if winner == 2:
    pygame.mixer.music.stop()
    screen.blit(player2_win, (0,0))

elif winner == 1:
    pygame.mixer.music.stop()
    screen.blit(player1_win, (0,0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()