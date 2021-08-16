import pygame
import random
import sys

pygame.init()

WIDTH = 1000
HEIGHT = 600

CYAN = (0,250,250)
RED = (250,0,0)
GREEN = (0,250,0)
MAGENTA = (250,0,250)
YELLOW = (250,250,0)
WHITE = (250,250,250)
DARKBLUE = (0,0,70)
BACKCOLOR = (0,0,0)

buttonPos = [450,400]
buttonSize = [100,50]
buttonColor = DARKBLUE
button1Pos = [400,475]
button1Size = [200,50]
button1Color = DARKBLUE
titlePos = [330,200]
onButton = False
onButton2 = False
easterEgg = False

SPEED = 10
playerSize = 50
playerSizeNorm = 50
playerPos = [WIDTH/2,HEIGHT-2*playerSize]
playerColor = CYAN
move = 10
enemySize = 50
enemyPos = [random.randint(0,WIDTH-enemySize),0]
enemyList = [enemyPos]
egg = "karen"
probEnemies = 0.1
numEnemies = 20
powUpSize = 10
powUpProb = 0.01
powUp = [random.randint(0,WIDTH-powUpSize),HEIGHT]
powUp2 = [random.randint(0,WIDTH-powUpSize),HEIGHT]
powUp3 = [random.randint(0,WIDTH-powUpSize),HEIGHT]
shooter = False
bullets = []
bulletSize = 10
isPowUp = False
powTimer = 10000
powUpBlink=0

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
myFont1 = pygame.font.SysFont("monospace",100)
myFont2 = pygame.font.SysFont("monospace",35)
myFont3 =pygame.font.SysFont("monospace",30)
myFont4 = pygame.font.SysFont("monospace",50)

gameOver = False
score=0
easter = ""
pressedRight = False
pressedLeft = False


def dropPower(powUp):
    powDelay = random.random()
    if powDelay<powUpProb and powUp[1]>=HEIGHT and not isPowUp:
        powUp = [random.randint(0,WIDTH-powUpSize),0]
    clear1 = True
    for enemy in enemyList:
        if detectCollision(powUp, enemy, powUpSize, enemySize):
            clear1 = False
    if not clear1:
        powUp[1] = HEIGHT
    return powUp

def powFall(powUp):
    if powUp[1]>=0 and powUp[1]<HEIGHT:
        powUp[1] +=SPEED
    return powUp

def detectPowUp(playerPos, powUp, powTimer,playerSize, isPowUp, powUpSize, shooter):
    if detectCollision(playerPos, powUp, playerSize, powUpSize):
        isPowUp = True
        playerSize = 10
        powTimer = 0
        powUp[1] = HEIGHT
        powUp2[1]=HEIGHT
        powUp3[1] = HEIGHT
        playerPos[1]+=40
        playerPos[0]+=20
    if powTimer>500 and not shooter:
        playerSize = playerSizeNorm
        isPowUp = False
    if powTimer ==500 and not shooter:
        playerPos[1]-=40
        playerPos[0]-=20
    if not shooter:
        powTimer=powTimer+1
    
    return playerSize, powTimer, isPowUp, powUp, playerPos


def detectPowUp2(playerPos, powUp2, powTimer,playerSize, isPowUp, powUpSize,shooter):
    if detectCollision(playerPos, powUp2, playerSize, powUpSize):
        isPowUp = True
        shooter = True
        powTimer = 0
        powUp2[1] = HEIGHT
        powUp[1] = HEIGHT
        powUp3[1] = HEIGHT

    if powTimer>500:
        isPowUp = False
        shooter = False
    if shooter:
        powTimer=powTimer+1
    
    return powTimer, isPowUp, shooter, powUp2

def detectPowUp3(playerPos, powUp3, playerSize, powUpSize, enemyList, score):
    if detectCollision(playerPos, powUp3, playerSize, powUpSize):
        for x in range(len(enemyList)):
            enemyList.pop(0)
            score += 1
        powUp[1] = HEIGHT
        powUp2[1] = HEIGHT
        powUp3[1] = HEIGHT
    return playerSize, powUp3, playerPos, enemyList, score

def shootBullets(bullets,playerPos):
    xPos = playerPos[0]+(playerSize-bulletSize)/2
    yPos = playerPos[1]
    bullets.append([xPos,yPos])

def drawBullets(bullets, bulletSize):
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW,(bullet[0],bullet[1], bulletSize, bulletSize))

def updateBulletPositions(bullets):
    for bullet in bullets:
        if bullet[1]>=0 and bullet[1]<HEIGHT:
            bullet[1] -=SPEED
        else:
            bullets.remove(bullet)

def bulletCollision(bullets, bulletSize, enemyList, enemySize, score):
    for enemy in enemyList:
        for bullet in bullets:
            if detectCollision(bullet, enemy, bulletSize, enemySize):
                enemyList.remove(enemy)
                score+=2
    return score, enemyList

def dropEnemies(enemyList, enemySize, easterEgg):
    delay= random.random()
    if len(enemyList) <numEnemies and delay<probEnemies:
        xPos = random.randint(0,WIDTH-enemySize)
        yPos = 0-enemySize
        toAdd = [xPos,yPos]
        clear = True
        for enemy in enemyList:
            if detectCollision(toAdd, enemy, enemySize, enemySize):
                clear = False
        if clear:
            enemyList.append(toAdd)
        if ((xPos<(playerPos[0]+playerSize) and xPos>=playerPos[0]) or (playerPos[0]<(xPos+enemySize)and playerPos[0]>=xPos)) and easterEgg and clear:
            enemyList.remove(toAdd)


def drawEnemies(enemyList):
    for enemy in enemyList:
        pygame.draw.rect(screen, MAGENTA,(enemy[0],enemy[1], enemySize, enemySize))

def updateEnemyPositions(enemyList,score):
    for enemy in enemyList:
        if enemy[1]>=0-enemySize and enemy[1]<HEIGHT:
            enemy[1] +=SPEED
        else:
            enemyList.remove(enemy)
            score=score+1
    return score

def collisionCheck(enemyList, playerPos):
    for enemy in enemyList:
        if detectCollision(playerPos,enemy, playerSize, enemySize):
            return True
    return False

def detectCollision(playerPos, enemyPos, playerSize, enemySize):
    px = playerPos[0]
    py = playerPos[1]
    ex = enemyPos[0]
    ey = enemyPos[1]
    if (ex<(px+playerSize) and ex>=px) or (px<(ex+enemySize)and px>=ex):
        if (ey<(py+playerSize) and ey>=py) or (py<(ey+enemySize)and py>=ey):
            return True
    return False

def setLevel(score, SPEED):
    if SPEED<20:
        SPEED = score//20+5
    probEnemies = score/400+0.1
    numEnemies = score//40+20
    
    return SPEED, probEnemies, numEnemies

def isOnButton(mousePos, buttonPos, buttonSize):
    if mousePos[0]>buttonPos[0] and mousePos[0]<buttonPos[0]+buttonSize[0] and mousePos[1]>buttonPos[1] and mousePos[1]<buttonPos[1]+buttonSize[1]:
        return True
    return False

def instructions():
    button2Pos = [WIDTH-250,HEIGHT-75]
    button2Size = [100,50]
    button2Color = DARKBLUE
    button3Pos = [WIDTH-125,HEIGHT-75]
    button3Size = [100,50]
    button3Color = DARKBLUE
    onButton2 = False
    onButton3 = False
    while True:
        label4 = myFont1.render("HOW TO PLAY", 1, YELLOW)
        screen.blit(label4,(50,50))
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if pygame.mouse.get_pressed()[0] and onButton2:
                screen.fill(BACKCOLOR)
                return False
            if pygame.mouse.get_pressed()[0] and onButton3:
                screen.fill(BACKCOLOR)
                return True
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, button2Pos, button2Size):
            onButton2 =True
            button2Color = CYAN
        else:
            onButton2 = False
            button2Color = DARKBLUE

        if isOnButton(mousePos, button3Pos, button3Size):
            onButton3 = True
            button3Color = CYAN
        else:
            onButton3 = False
            button3Color = DARKBLUE
        text1 = "You are a cyan-colored square in a world full of squarez! Here is how to navigate this world."
        text2 = "Objective: Pink squarez are falling from the sky, trying to get you."
        text3 = "        Avoid these squarez at all costs because if one touches you, it's game over."
        text4 = "To move: use the left and right arrow keys to move left and right arrow keys."
        text5 = "Scoring: You get one point each time a pink square reaches the ground without touching you."
        text6 = "        The game will get progressively more difficult as it continues."
        text7 = "Power Ups:"
        text7half = "If you catch white squarez, you will become small."
        text8 = "If you catch red squarez, you will gain the ability to shoot the pink squares using the space bar."
        text9 = "        For every pink square you shoot, you'll receive 2 points."
        text10 ="If you catch green squarez, the screen will be cleared."
        text11 ="        You will receive points for every square on the screen."
        texts = [text1,text2,text3,text4,text5,text6,text7,text7half,text8,text9, text10, text11]
        for i in range(len(texts)):
            texter = texts[i]
            labeler = myFont3.render(texter,1,WHITE)
            screen.blit(labeler,(50,130+38*i))
        pygame.draw.rect(screen,button2Color,(button2Pos[0],button2Pos[1],button2Size[0],button2Size[1]))
        label5 = myFont2.render("BACK", 1, WHITE)
        screen.blit(label5,(button2Pos[0]+12,button2Pos[1]+15))
        pygame.draw.rect(screen,button3Color,(button3Pos[0],button3Pos[1],button3Size[0],button3Size[1]))
        label6 = myFont2.render("START", 1, WHITE)
        screen.blit(label6,(button3Pos[0]+9,button3Pos[1]+15))
        pygame.display.update()

def endGame(score):
    button4Pos = [WIDTH/2-90,HEIGHT/2]
    button4Size = [180,50]
    button4Color = DARKBLUE
    button5Pos = [WIDTH/2-50,HEIGHT/2+75]
    button5Size = [100,50]
    button5Color = DARKBLUE
    onButton4 = False
    onButton5 = False
    while True:
        label7 = myFont1.render("GAME OVER!", 1, YELLOW)
        screen.blit(label7,(WIDTH/2-220,150))
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if pygame.mouse.get_pressed()[0] and onButton4:
                screen.fill(BACKCOLOR)
                return True # "play"
            if pygame.mouse.get_pressed()[0] and onButton5:
                screen.fill(BACKCOLOR)
                return False # "home"
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, button4Pos, button4Size):
            onButton4 =True
            button4Color = CYAN
        else:
            onButton4 = False
            button4Color = DARKBLUE

        if isOnButton(mousePos, button5Pos, button5Size):
            onButton5 = True
            button5Color = CYAN
        else:
            onButton5 = False
            button5Color = DARKBLUE
        pygame.draw.rect(screen,button4Color,(button4Pos[0],button4Pos[1],button4Size[0],button4Size[1]))
        label8 = myFont2.render("PLAY AGAIN", 1, WHITE)
        screen.blit(label8,(button4Pos[0]+12,button4Pos[1]+15))
        pygame.draw.rect(screen,button5Color,(button5Pos[0],button5Pos[1],button5Size[0],button5Size[1]))
        label9 = myFont2.render("HOME", 1, WHITE)
        screen.blit(label9,(button5Pos[0]+9,button5Pos[1]+15))
        label10 = myFont4.render("SCORE: " +str(score), 1, RED)
        screen.blit(label10,(410, 230))
        pygame.display.update()

    
   
def homeScreen():
    while True:
        breakOut = False
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0] and onButton:
                pygame.display.update()
                breakOut = True
            if pygame.mouse.get_pressed()[0] and onButton1:
                screen.fill(BACKCOLOR)
                breakOut = instructions()
        if breakOut:
            return
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, buttonPos, buttonSize):
            onButton =True
            buttonColor = CYAN
        else:
            onButton = False
            buttonColor = DARKBLUE

        if isOnButton(mousePos, button1Pos, button1Size):
            onButton1 = True
            button1Color = CYAN
        else:
            onButton1 = False
            button1Color = DARKBLUE
        
        label1 = myFont1.render("SQUAREZ", 1, YELLOW)
        screen.blit(label1,(titlePos[0],titlePos[1]))
        pygame.draw.rect(screen,buttonColor,(buttonPos[0],buttonPos[1],buttonSize[0],buttonSize[1]))
        label2 = myFont2.render("START", 1, WHITE)
        screen.blit(label2,(buttonPos[0]+9,buttonPos[1]+15))
        pygame.draw.rect(screen,button1Color,(button1Pos[0],button1Pos[1],button1Size[0],button1Size[1]))
        label3 = myFont2.render("HOW TO PLAY", 1, WHITE)
        screen.blit(label3,(button1Pos[0]+9,button1Pos[1]+15))
        pygame.display.update()

homeScreen()
while not gameOver:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                pressedLeft = True
##                x= x-move
            elif event.key == pygame.K_RIGHT:
                pressedRight = True
##                x= x+move
            if event.key==pygame.K_SPACE and shooter:
                shootBullets(bullets,playerPos)
            if event.key==pygame.K_r:
                easter +="r"
            elif event.key==pygame.K_a:
                easter +="a"
            elif event.key==pygame.K_n:
                easter +="n"
            elif event.key==pygame.K_k:
                easter +="k"
            elif event.key==pygame.K_e:
                easter +="e"
        elif event.type==pygame.KEYUP:
            if event.key ==pygame.K_LEFT:
                pressedLeft = False
            elif event.key == pygame.K_RIGHT:
                pressedRight = False
                    
    screen.fill(BACKCOLOR)
    #update enemy position
##    if enemyPos[1]>=0 and enemyPos[1]<HEIGHT:
##        enemyPos[1] +=SPEED
##    else:
##        enemyPos[0] = random.randint(0,WIDTH-enemySize)
##        enemyPos[1]=0
    x = playerPos[0]
    if pressedLeft and x>=move:
        x-=move
    elif pressedRight and x<WIDTH-playerSize:
        x+=move
    playerPos[0] = x   
    
    if collisionCheck(enemyList, playerPos):
##        gameOver = True
##        break
        playAgain = endGame(score)
        enemyList = []
        probEnemies = 0.1
        numEnemies = 10
        screen.fill(BACKCOLOR)
        score = 0
        powUp[1] = HEIGHT
        powUp2[1] = HEIGHT
        powUp3[1] = HEIGHT
        playerSize = 50
        playerPos = [WIDTH/2,HEIGHT-2*playerSize]
        shooter = False
        isPowUp = False
        playerColor = CYAN
        powTimer = 10000
        bullets = []
        pressedLeft = False
        pressedRight = False
        if not playAgain:
            homeScreen()
            
    if easter == egg:
        easterEgg = True
    
    powUp = dropPower(powUp)
    powUp = powFall(powUp)
    powUp2 = dropPower(powUp2)
    powUp2 = powFall(powUp2)
    powUp3 = dropPower(powUp3)
    powUp3 = powFall(powUp3)
    playerSize, powTimer, isPowUp, powUp, playerPos = detectPowUp(playerPos, powUp, powTimer, playerSize,isPowUp, powUpSize, shooter)
    powTimer, isPowUp, shooter, powUp2 = detectPowUp2(playerPos, powUp2, powTimer,playerSize, isPowUp, powUpSize, shooter)
    playerSize, powUp3, playerPos, enemyList, score = detectPowUp3(playerPos, powUp3, playerSize, powUpSize, enemyList, score)
    drawEnemies(enemyList)
    dropEnemies(enemyList,enemySize,easterEgg)
    
    drawBullets(bullets,bulletSize)
    updateBulletPositions(bullets)
    score, enemyList= bulletCollision(bullets, bulletSize, enemyList, enemySize,score)
    if shooter:
        if powTimer>=440 and powTimer<=500 and powTimer%10==0 and powUpBlink==0:
            playerColor = CYAN
            powUpBlink = 1
        elif powTimer>=440 and powTimer<=500 and powTimer%10==0 and powUpBlink==1:
            playerColor = RED
            powUpBlink = 0
        elif powTimer<440:
            playerColor = RED
            powUpBlink = 0
    elif isPowUp:
        if powTimer>=440 and powTimer<=500 and powTimer%10==0 and powUpBlink==0:
            playerColor = CYAN
            powUpBlink = 1
        elif powTimer>=440 and powTimer<=500 and powTimer%10==0 and powUpBlink==1:
            playerColor = WHITE
            powUpBlink = 0
        elif powTimer<440:
            playerColor = WHITE
        bullets=[]
    else:
        playerColor = CYAN
        bullets=[]
    
    score = updateEnemyPositions(enemyList,score)
    SPEED, probEnemies, numEnemies = setLevel(score, SPEED)
    
    text = "SCORE:"+str(score)
    label = myFont2.render(text, 1, YELLOW)
    screen.blit(label,(WIDTH-200,HEIGHT-40))
    
    pygame.draw.rect(screen,playerColor,(playerPos[0],playerPos[1],playerSize,playerSize))
    pygame.draw.rect(screen,WHITE,(powUp[0],powUp[1],powUpSize,powUpSize))
    pygame.draw.rect(screen,RED,(powUp2[0],powUp2[1],powUpSize,powUpSize))
    pygame.draw.rect(screen,GREEN,(powUp3[0],powUp3[1],powUpSize,powUpSize))

    clock.tick(30)
    
    pygame.display.update()
print(score)
pygame.quit()
sys.exit()
