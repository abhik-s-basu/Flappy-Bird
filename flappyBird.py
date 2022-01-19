import random
import sys
import pygame 
import time
from pygame.locals import *

fps = 32
screenWidth = 289  #can change later
screenHeight = 511 #can change later
displayScreenWindow = pygame.display.set_mode((screenWidth,screenHeight))
playGround = screenHeight*0.8
gameImage = {}
gameSound = {}

player = 'sprites/bluebird-downflap.png'
bgImage = 'sprites/background-day.png'
pipeImage = 'sprites/pipe-green.png'

pygameIcon = pygame.image.load('sprites/redbird-downflap.png')
pygame.display.set_icon(pygameIcon)


def welcomeScreen():
    #showing welcome images on the screen
    playerX = int(screenWidth/5)
    playerY = int((screenHeight - gameImage['player'].get_height())/2)
    messageX = int((screenWidth - gameImage['message'].get_width())/2)
    messageY = int(screenHeight * 0.13)
    baseX = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                displayScreenWindow.blit(gameImage['background'], (0, 0))
                displayScreenWindow.blit(gameImage['player'], (playerX, playerY))
                displayScreenWindow.blit(gameImage['message'], (messageX, messageY))
                displayScreenWindow.blit(gameImage['base'], (baseX, playGround))
                pygame.display.update()
                timeClock.tick(fps)


def mainGame():
    score = 0
    playerX = int(screenWidth / 5)
    playerY = int(screenWidth / 2)
    baseX = 0

    pipe1 = getRandPipes()
    pipe2 = getRandPipes()

    upPipe = [
        {'x': screenWidth + 200, 'y': pipe1[0]['y']},
        {'x': screenWidth + 200 + (screenWidth / 2), 'y': pipe2[0]['y']},
    ]

    lowPipe = [
        {'x': screenWidth + 200, 'y': pipe1[1]['y']},
        {'x': screenWidth + 200 + (screenWidth/2), 'y': pipe2[1]['y']},
    ]

    pipeXVelocity = -4
    playerXVelocity = -9
    playerXMVelocity = 10
    playerYMVelocity = -8
    playerAccuracy = 1
    playerFlapAccuracy = -8
    playerFlap = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerXVelocity = playerFlapAccuracy
                    playerFlap = True
                    gameSound['wing'].play()
        
        crashTesting = isColliding(playerX, playerY, upPipe, lowPipe)
        if crashTesting:
            return
            print("crashed")
        
        playerMiddlePosition = playerX + gameImage['player'].get_width() / 2
        for pipe in upPipe:
            pipeMiddlePosition = pipe['x'] + gameImage['pipe'][0].get_width() / 2
            if pipeMiddlePosition <= playerMiddlePosition < pipeMiddlePosition + 4:
                score += 1
                gameSound['point'].play()
            
        if playerXVelocity < playerXMVelocity and not playerFlap:
            playerXVelocity += playerAccuracy
            
        if playerFlap:
            playerFlap = False
        playerHeight = gameImage['player'].get_height()
        playerY = playerY + min(playerXVelocity, playGround - playerY - playerHeight)

        for pipeUpper, pipeLower in zip(upPipe, lowPipe):
            pipeUpper['x'] += pipeXVelocity
            pipeLower['x'] += pipeXVelocity

        if 0 < upPipe[0]['x'] < 5:
            newPipe = getRandPipes()
            upPipe.append(newPipe[0])
            lowPipe.append(newPipe[1])

        if upPipe[0]['x'] < -gameImage['pipe'][0].get_width():
            upPipe.pop(0)
            lowPipe.pop(0)
        
        displayScreenWindow.blit(gameImage['background'], (0,0))
        for pipeUpper, pipeLower in zip(upPipe,lowPipe):
            displayScreenWindow.blit(gameImage['pipe'][0], (pipeUpper['x'],pipeUpper['y']))
            displayScreenWindow.blit(gameImage['pipe'][1], (pipeLower['x'], pipeLower['y']))

        displayScreenWindow.blit(gameImage['base'], (baseX,playGround))
        displayScreenWindow.blit(gameImage['player'], (playerX, playerY))
        digi = [int(x) for x in list(str(score))]
        w = 0
        for digit in digi:
            w += gameImage['numbers'][digit].get_width()
        xOffset = (screenWidth - w) / 2

        for digit in digi:
            displayScreenWindow.blit(gameImage['numbers'][digit], (xOffset, screenHeight * 0.12))
            xOffset += gameImage['numbers'][digit].get_width()
        pygame.display.update()
        timeClock.tick(fps)
        



def isColliding(playerX, playerY, upPipe, lowPipe):
    if playerY > playGround - 25 or playerY < 0:
        gameSound['hit'].play()
        return True
    
    for pipe in upPipe:
        pipeHeight = gameImage['pipe'][0].get_height()
        if (playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < gameImage['pipe'][0].get_width()):
            print("hello we are here")
            gameSound['hit'].play()
            return True
    
    for pipe in lowPipe:
        if (playerY + gameImage['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < gameImage['pipe'][0].get_width():
            print("hello we here instead")
            gameSound['hit'].play()
            return True
    
    return False

def getRandPipes():
    pipeHeight = gameImage['pipe'][0].get_height()
    offset = screenHeight/3
    y2 = offset + random.randrange(0,int(screenHeight - gameImage['base'].get_height() - 1.2*offset))
    xPipe = screenWidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': xPipe, 'y': -y1}, #upper pipe
        {'x': xPipe, 'y': y2}  #lower pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    timeClock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    gameImage['numbers'] = (
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )

    mytime = time.localtime()
    if mytime.tm_hour <6 or mytime.tm_hour>18:
        player = 'sprites/yellowbird-downflap.png'
        bgImage = 'sprites/background-night.png'
        pipeImage = 'sprites/pipe-red.png'

    gameImage['message'] = pygame.image.load('sprites/message.png').convert_alpha()
    gameImage['base'] = pygame.image.load('sprites/base.png').convert_alpha()
    gameImage['pipe'] = (pygame.transform.rotate(pygame.image.load(pipeImage).convert_alpha(),180), pygame.image.load(pipeImage).convert_alpha())

    gameSound['die'] = pygame.mixer.Sound('audio/die.wav')
    gameSound['hit'] = pygame.mixer.Sound('audio/hit.wav')
    gameSound['point'] = pygame.mixer.Sound('audio/point.wav')
    gameSound['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    gameSound['wing'] = pygame.mixer.Sound('audio/wing.wav')

    gameImage['background'] = pygame.image.load(bgImage).convert()
    gameImage['player'] = pygame.image.load(player).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()





