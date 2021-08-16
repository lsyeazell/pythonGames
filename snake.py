import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600

BLACK = (0,0,0)
GREY = (50,50,50)
BACKCOLOR = (144,238,144)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
DARKRED = (200,0,0)
GREEN = (0,200,0)
WHITE = (255,255,255)
BROWN = (150,75,150)
DARKGREEN = (0,150,0)
PINK = (231, 158, 169)

myFont =pygame.font.SysFont("monospace",100)
myFont1 =pygame.font.SysFont("monospace",100)
myFont2 =pygame.font.SysFont("monospace",90)
myFont3 =pygame.font.SysFont("monospace",35)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class apple:
    def __init__(self, size):
        self.size = size
        self.x = random.randint(0,(WIDTH-self.size)//self.size)*self.size
        self.y = random.randint(0,(HEIGHT-self.size)//self.size)*self.size

    def draw(self):
        pygame.draw.rect(screen, BROWN, (self.x+self.size//2-2, self.y-4, 4, 5))
        pygame.draw.circle(screen, RED,(self.x+self.size//2, self.y+self.size//2), self.size//2)
        pygame.draw.circle(screen, DARKRED,(self.x+self.size//2, self.y+self.size//2), self.size//2, 1)
        pygame.draw.ellipse(screen, DARKGREEN, (self.x+self.size//2+2, self.y-3, 10,5))
        

def drawGrid(blockSize):
    for lineX in range(WIDTH//blockSize):
        pygame.draw.line(screen, GREEN, (lineX*blockSize, 0), (lineX*blockSize, HEIGHT), 1)
    for lineY in range(HEIGHT//blockSize):
        pygame.draw.line(screen,GREEN, (0, lineY*blockSize), (WIDTH, lineY*blockSize),1)

def checkForDuplicates(array):
    checker = []
    duplicates = False
    for element in array:
        if element in checker:
            duplicates = True
        checker.append(element)
    return duplicates

def isOnButton(mousePos, buttonPos, buttonSize):
    if mousePos[0]>buttonPos[0] and mousePos[0]<buttonPos[0]+buttonSize[0] and mousePos[1]>buttonPos[1] and mousePos[1]<buttonPos[1]+buttonSize[1]:
        return True
    return False

def drawEnds(snake,blockSize):
    pygame.draw.circle(screen, BLUE,(snake[0][0]+blockSize//2, snake[0][1]+blockSize//2), blockSize//2)
    stickOutTongue = random.random()
    i = 0
    if snake[0][0]>snake[1][0]:
        pygame.draw.rect(screen, BLUE,(snake[0][0], snake[0][1], blockSize//2, blockSize))
        pygame.draw.circle(screen, WHITE,(snake[0][0]+blockSize//2, snake[0][1]+5), 5)
        pygame.draw.circle(screen, WHITE,(snake[0][0]+blockSize//2, snake[0][1]+blockSize-5), 5)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+blockSize//2+1, snake[0][1]+5), 3)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+blockSize//2+1, snake[0][1]+blockSize-5), 3)
        if stickOutTongue<0.1 or i%3!=0:
            pygame.draw.rect(screen, PINK, (snake[0][0]+blockSize-1, snake[0][1]+blockSize//2-2, 8, 4)) 
            i+=1
    elif snake[0][0]<snake[1][0]:
        pygame.draw.rect(screen, BLUE,(snake[0][0]+blockSize//2, snake[0][1], blockSize//2, blockSize))
        pygame.draw.circle(screen, WHITE,(snake[0][0]+blockSize//2, snake[0][1]+5), 5)
        pygame.draw.circle(screen, WHITE,(snake[0][0]+blockSize//2, snake[0][1]+blockSize-5), 5)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+blockSize//2-1, snake[0][1]+5), 3)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+blockSize//2-1, snake[0][1]+blockSize-5), 3)
        if stickOutTongue<0.1 or i%3!=0:
            pygame.draw.rect(screen, PINK, (snake[0][0]-7, snake[0][1]+blockSize//2-2, 8, 4))
            i+=1
    elif snake[0][1]<snake[1][1]:
        pygame.draw.rect(screen, BLUE,(snake[0][0], snake[0][1]+blockSize//2, blockSize, blockSize//2))
        pygame.draw.circle(screen, WHITE,(snake[0][0]+5, snake[0][1]+blockSize//2), 5)
        pygame.draw.circle(screen, WHITE,(snake[0][0]+blockSize-5, snake[0][1]+blockSize//2), 5)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+5, snake[0][1]+blockSize//2-1), 3)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+blockSize-5, snake[0][1]+blockSize//2-1), 3)
        if stickOutTongue<0.1 or i%3!=0:
            pygame.draw.rect(screen, PINK, (snake[0][0]+blockSize//2-2, snake[0][1]-7, 4, 8))
            i+=1
    elif snake[0][1]>snake[1][1]:
        pygame.draw.rect(screen, BLUE,(snake[0][0], snake[0][1], blockSize, blockSize//2))
        pygame.draw.circle(screen, WHITE,(snake[0][0]+5, snake[0][1]+blockSize//2), 5)
        pygame.draw.circle(screen, WHITE,(snake[0][0]+blockSize-5, snake[0][1]+blockSize//2), 5)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+5, snake[0][1]+blockSize//2+1), 3)
        pygame.draw.circle(screen, BLACK,(snake[0][0]+blockSize-5, snake[0][1]+blockSize//2+1), 3)
        if stickOutTongue<0.1 or i%3!=0:
            pygame.draw.rect(screen, PINK, (snake[0][0]+blockSize//2-2, snake[0][1]+blockSize-1, 4, 8))
            i+=1
    
    pygame.draw.circle(screen, BLUE,(snake[-1][0]+blockSize//2, snake[0-1][1]+blockSize//2), blockSize//2)
    if snake[-2][0]>snake[-1][0]:
        pygame.draw.rect(screen, BLUE,(snake[-1][0]+blockSize//2, snake[-1][1], blockSize//2, blockSize))
    elif snake[-2][0]<snake[-1][0]:
        pygame.draw.rect(screen, BLUE,(snake[-1][0], snake[-1][1], blockSize//2, blockSize))
    elif snake[-2][1]<snake[-1][1]:
        pygame.draw.rect(screen, BLUE,(snake[-1][0], snake[-1][1], blockSize, blockSize//2))
    elif snake[-2][1]>snake[-1][1]:
        pygame.draw.rect(screen, BLUE,(snake[-1][0], snake[-1][1]+blockSize//2, blockSize, blockSize//2))
    
def drawCorner(snake,blockSize):
    pygame.draw.circle(screen, BLUE,(snake[1][0]+blockSize//2, snake[1][1]+blockSize//2), blockSize//2)
    if (snake[0][0]<snake[1][0] and snake[1][1]>snake[2][1]) or(snake[2][0]<snake[1][0] and snake[1][1]>snake[0][1]):
        pygame.draw.rect(screen, BLUE,(snake[1][0], snake[1][1], blockSize//2, blockSize))
        pygame.draw.rect(screen, BLUE,(snake[1][0], snake[1][1], blockSize, blockSize//2))
    elif (snake[0][0]>snake[1][0] and snake[1][1]>snake[2][1]) or (snake[2][0]>snake[1][0] and snake[1][1]>snake[0][1]) :
        pygame.draw.rect(screen, BLUE,(snake[1][0]+blockSize//2, snake[1][1], blockSize//2, blockSize))
        pygame.draw.rect(screen, BLUE,(snake[1][0], snake[1][1], blockSize, blockSize//2))
    elif (snake[0][0]>snake[1][0] and snake[1][1]<snake[2][1]) or (snake[2][0]>snake[1][0] and snake[1][1]<snake[0][1]):
        pygame.draw.rect(screen, BLUE,(snake[1][0]+blockSize//2, snake[1][1], blockSize//2, blockSize))
        pygame.draw.rect(screen, BLUE,(snake[1][0], snake[1][1]+blockSize//2, blockSize, blockSize//2))
    elif (snake[0][0]<snake[1][0] and snake[1][1]<snake[2][1]) or (snake[2][0]<snake[1][0] and snake[1][1]<snake[0][1]):
        pygame.draw.rect(screen, BLUE,(snake[1][0], snake[1][1], blockSize//2, blockSize))
        pygame.draw.rect(screen, BLUE,(snake[1][0], snake[1][1]+blockSize//2, blockSize, blockSize//2))
        

def endGame(length):
    buttonPos = [WIDTH/2-90,HEIGHT/2]
    buttonSize = [180,50]
    buttony = buttonPos[1]
    onButton = False
    while True:
        screen.fill(BACKCOLOR)
        drawGrid(30)
        label = myFont1.render("GAME OVER!", 1, BLUE)
        screen.blit(label,(WIDTH/2-215,150))
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if pygame.mouse.get_pressed()[0] and onButton:
                screen.fill(BACKCOLOR)
                playGame()
            if pygame.mouse.get_pressed()[0] and onButton1:
                screen.fill(BACKCOLOR)
                homeScreen()
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, buttonPos, buttonSize):
            onButton =True
            buttony = buttonPos[1]+5
        else:
            onButton = False
            buttony = buttonPos[1]
        pygame.draw.rect(screen,RED,(buttonPos[0],buttony,buttonSize[0],buttonSize[1]))
        label1 = myFont3.render("PLAY AGAIN", 1, WHITE)
        screen.blit(label1,(buttonPos[0]+12,buttony+15))
        pygame.display.update()
    print(length)
    pygame.quit()
    sys.exit()

def playGame():
    blockSize = 30
    gameOver = False
    screen.fill(BACKCOLOR)
    downPressed = False
    startX = WIDTH//2
    startY = HEIGHT//2
    snake = [[startX, startY]]
    length = 4
    direction = "right"
    apple1 = apple(blockSize)
    while not gameOver:
        screen.fill(BACKCOLOR)
        drawGrid(blockSize)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT and direction !="left":
                    direction = "right"
                elif event.key==pygame.K_LEFT and direction !="right":
                    direction = "left"
                elif event.key==pygame.K_UP and direction !="down":
                    direction = "up"
                elif event.key==pygame.K_DOWN and direction !="up":
                    direction = "down"
        if direction == "right":
            toAdd = [snake[0][0]+blockSize,snake[0][1]]
            if toAdd[0]>WIDTH-blockSize:
                gameOver = True
            snake.insert(0,toAdd)
        elif direction == "left":
            toAdd = [snake[0][0]-blockSize,snake[0][1]]
            if toAdd[0]<0:
                gameOver = True
            snake.insert(0,toAdd)
        elif direction == "up":
            toAdd = [snake[0][0],snake[0][1]-blockSize]
            if toAdd[1]<0:
                gameOver = True
            snake.insert(0,toAdd)
        elif direction == "down":
            toAdd = [snake[0][0],snake[0][1]+blockSize]
            if toAdd[1]>HEIGHT-blockSize:
                gameOver = True
            snake.insert(0,toAdd)

        if checkForDuplicates(snake):
            gameOver = True
        if [apple1.x,apple1.y]==snake[0]:
            length +=1
            apple1 = apple(blockSize)
        while [apple1.x,apple1.y] in snake and not [apple1.x,apple1.y]==snake[0]:
            apple1 = apple(blockSize)
##        if [apple1.x,apple1.y]==snake[0]:
##            length +=1
##            apple1 = apple(blockSize)
        if len(snake)>length:
            snake.pop(-1)
        for i in range(len(snake[1:-1])):
            if not ((snake[i+1][0]==snake[i][0] and snake[i+1][0]==snake[i+2][0]) or (snake[i+1][1]==snake[i][1] and snake[i+1][1]==snake[i+2][1])):
                drawCorner(snake[i:i+3], blockSize)
            else:
                pygame.draw.rect(screen, BLUE,(snake[i+1][0], snake[i+1][1], blockSize, blockSize))
        drawEnds(snake, blockSize)
        apple1.draw()
        
        clock.tick(5)
        pygame.display.update()
    endGame(length)



playGame()


            
