import pygame as pg
from sys import exit
from random import randint, choice

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        playerWalk1 = pg.image.load('graphics/player/player_walk_1.png').convert_alpha()
        playerWalk2 = pg.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.playerWalk = [playerWalk1, playerWalk2]
        self.playerIndex = 0
        self.playerJump = pg.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jumpSound = pg.mixer.Sound('audio/jump.mp3')
        self.jumpSound.set_volume(0.4)

    def playerInput(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jumpSound.play()

    def applyGravity(self): 
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animationState(self):
        if self.rect.bottom < 300:
            self.image = self.playerJump
        else:
            self.playerIndex += 0.1
            if self.playerIndex >= len(self.playerWalk): self.playerIndex = 0
            self.image = self.playerWalk[int(self.playerIndex)]

    def update(self):
        self.playerInput()
        self.applyGravity()
        self.animationState()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly1 = pg.image.load('graphics/fly/fly1.png').convert_alpha()
            fly2 = pg.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            yPos = 210
        else: 
            snail1 = pg.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pg.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            yPos = 300

        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), yPos))

    def animationState(self):
        self.animationIndex += 0.1
        if self.animationIndex > len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def update(self):
        self.animationState()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

textColor = (64, 64, 64)

def displayScore():
    time = pg.time.get_ticks() - startTime
    scoreSurf = font.render(f'Score: {int(time/1000)}', False, textColor)
    scoreRect = scoreSurf.get_rect(midtop = (400, 30))
    screen.blit(scoreSurf, scoreRect)
    return time

def obstacleMovement(obstacleList):
    if obstacleList:
        for rect in obstacleList:
            rect.x -= 5

            if rect.bottom == 300:
                screen.blit(snailSurf, rect)
            else:
                screen.blit(flySurf, rect)

        obstacleList = [obst for obst in obstacleList if obst.x > -100]
        return obstacleList
    else: return [] 

def checkCollision(player, obstacles):
    if obstacles:
        for rect in obstacles:
            if player.colliderect(rect): return False;
    return True

def collision():
    if pg.sprite.spritecollide(player.sprite, obstacleGroup, False):
        obstacleGroup.empty();
        return False
    else: return True

def playerAnimation():
    global playerSurf, playerIndex

    if playerRect.bottom < 300:
        playerSurf = playerJump
    else:
        playerIndex += 0.1
        if playerIndex >= len(playerWalk): playerIndex = 0
        playerSurf = playerWalk[int(playerIndex)]

pg.init()
screen = pg.display.set_mode((800, 400))
pg.display.set_caption('Skakacz')
fpsTimer = pg.time.Clock()
font = pg.font.Font('font/Pixeltype.ttf', 50)
gameActive = False
startTime = 0
score = 0
bgMusic = pg.mixer.Sound('audio/music.wav')
  
player = pg.sprite.GroupSingle()
player.add(Player())

obstacleGroup = pg.sprite.Group()

skySurf = pg.image.load('graphics/Sky.png').convert()
groundSurf = pg.image.load('graphics/ground.png').convert()

# Obstacles
snailFrame1 = pg.image.load('graphics/snail/snail1.png').convert_alpha()
snailFrame2 = pg.image.load('graphics/snail/snail2.png').convert_alpha()
snailFrames = [snailFrame1, snailFrame2]
snailFrameIndex = 0
snailSurf = snailFrames[snailFrameIndex]

flyFrame1 = pg.image.load('graphics/fly/fly1.png').convert_alpha()
flyFrame2 = pg.image.load('graphics/fly/fly2.png').convert_alpha()
flyFrames = [flyFrame1, flyFrame2]
flyFrameIndex = 0
flySurf = flyFrames[flyFrameIndex]

obstacleRectList = []

playerWalk1 = pg.image.load('graphics/player/player_walk_1.png').convert_alpha()
playerWalk2 = pg.image.load('graphics/player/player_walk_2.png').convert_alpha()
playerWalk = [playerWalk1, playerWalk2]
playerIndex = 0
playerJump = pg.image.load('graphics/player/jump.png').convert_alpha()

playerSurf = playerWalk[playerIndex]
playerRect = playerSurf.get_rect(midbottom = (80, 300))
playerGravity = 0

# Intro screen
playerStand = pg.image.load('graphics/player/player_stand.png').convert_alpha()
playerStand = pg.transform.scale2x(playerStand)
playerStandRect = playerStand.get_rect(center = (400, 200))

gameName = font.render('Skakacz', False, textColor)
gameNameRect = gameName.get_rect(midtop = (400, 30))

gameMsg = font.render('Press space to start...', False, textColor)
gameMsgRect = gameMsg.get_rect(midbottom = (400, 370))

# Timers
obstacleTimer = pg.USEREVENT + 1
pg.time.set_timer(obstacleTimer, 1500)

snailTimer = pg.USEREVENT + 2
pg.time.set_timer(snailTimer, 500)

flyTimer = pg.USEREVENT + 3
pg.time.set_timer(flyTimer, 300)

bgMusic.play(loops = -1)
bgMusic.set_volume(0.1)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if gameActive:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and playerRect.bottom == 300:
                    playerGravity = -20
            if event.type == pg.MOUSEBUTTONDOWN:
                if playerRect.collidepoint(event.pos) and playerRect.bottom == 300:
                    playerGravity = -20
        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                gameActive = True
                startTime = pg.time.get_ticks()

        if gameActive:
            if event.type == obstacleTimer:
                obstacleGroup.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0, 2):
                #     obstacleRectList.append(snailSurf.get_rect(bottomright = (randint(900, 1100), 300)))
                # else:
                #     obstacleRectList.append(flySurf.get_rect(bottomright = (randint(900, 1100), 210)))
            
            if event.type == snailTimer:
                if snailFrameIndex == 0: snailFrameIndex = 1
                else: snailFrameIndex = 0
                snailSurf = snailFrames[snailFrameIndex]

            if event.type == flyTimer:
                if flyFrameIndex == 0: flyFrameIndex = 1
                else: flyFrameIndex = 0
                flySurf = flyFrames[flyFrameIndex]

    if gameActive:
        screen.blit(skySurf, (0, 0))
        screen.blit(groundSurf, (0, 300))
        score = displayScore()


        # PLayer
        # playerGravity += 1
        # playerRect.y += playerGravity 
        # if playerRect.bottom >= 300: playerRect.bottom = 300
        # playerAnimation()
        # screen.blit(playerSurf, playerRect)
        player.draw(screen)
        player.update()

        obstacleGroup.draw(screen)
        obstacleGroup.update()

        # Obstacle movement
        # obstacleRectList = obstacleMovement(obstacleRectList)

        # Collisions
        # gameActive = checkCollision(playerRect, obstacleRectList)
        gameActive = collision()

    else:
        screen.fill((94, 129, 162))
        screen.blit(playerStand , playerStandRect)
        obstacleRectList.clear()
        playerRect.midbottom = (80, 300)
        playerGravity = 0
        
        scoreMsg = font.render(f'Score: {int(score/1000)}', False, textColor)
        scoreMsgRect = scoreMsg.get_rect(midbottom = (400, 370))
        screen.blit(gameName, gameNameRect)

        if score == 0: screen.blit(gameMsg, gameMsgRect)
        else: screen.blit(scoreMsg, scoreMsgRect)

    pg.display.update()
    fpsTimer.tick(60)