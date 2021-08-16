import pygame
import random
import sys

pygame.init()

WIDTH = 700
HEIGHT = 700


EMPTY = (208, 192, 177)
WHITE = (250,250,250)
BLACK = (10,10,10)
COLOR2 = (238, 228, 218)
COLOR4 = (237, 224, 200)
COLOR8 = (242, 177, 121)
COLOR16 = (245, 149, 99)
COLOR32=(246, 124, 95)
COLOR64 = (246, 94, 59)
COLOR128 = (237, 207, 114)
COLOR256 = (237, 204,97)
COLOR512 = (237, 200, 80)
COLOR1024 = (237, 197, 63)
COLOR2048 = (237, 194, 46)
COLORELSE = BLACK

COLORFONT1 = (255, 243, 245)
COLORFONT2 = (115, 105, 95)

GREY = (50,50,50)
BACKCOLOR = (188, 172, 157)
ORANGE = (255, 165,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

myFont =pygame.font.SysFont("monospace",100)
myFont1 =pygame.font.SysFont("monospace",130)
myFont2 =pygame.font.SysFont("monospace",90)
myFont3 =pygame.font.SysFont("monospace",35)

class two:
    def __init__(self, size, value,spotX, spotY, canAdd = True):
        self.size = size
        self.spacing = 20
        self.value = value
        self.x = spotX*self.size
        self.y = spotY*self.size
        self.canAdd = canAdd
    def moveRight(self):
##        for i in range(10):
##            self.x += self.size//10
##            self.draw()
##            pygame.display.update()
        self.x += self.size
            
    def moveLeft(self):
##        for i in range(10):
##            self.x -= self.size//10
##            self.draw()
##            pygame.display.update()
        self.x -= self.size

    def moveDown(self):
##        for i in range(10):
##            self.y += self.size//10
##            self.draw()
##            pygame.display.update()
        self.y += self.size
    def moveUp(self):
##        for i in range(10):
##            self.y -= self.size//10
##            self.draw()
##            pygame.display.update()
        self.y -= self.size
    def draw(self):
        drawX = self.x/self.size*(self.size+self.spacing)+self.spacing
        drawY = self.y/self.size*(self.size+self.spacing)+self.spacing
        
        if self.value==2:
            color = COLOR2
            fontColor = COLORFONT2
            fontX = 55
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==4:
            color = COLOR4
            fontColor = COLORFONT2
            fontX = 55
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==8:
            color = COLOR8
            fontColor = COLORFONT1
            fontX = 55
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==16:
            color = COLOR16
            fontColor = COLORFONT1
            fontX = 35
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==32:
            color = COLOR32
            fontColor = COLORFONT1
            fontX = 35
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==64:
            color = COLOR64
            fontColor = COLORFONT1
            fontX = 35
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==128:
            color = COLOR128
            fontColor = COLORFONT1
            fontX = 18
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==256:
            color = COLOR256
            fontColor = COLORFONT1
            fontX = 18
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==512:
            color = COLOR512
            fontColor = COLORFONT1
            fontX = 18
            label = myFont.render(str(self.value), 1, fontColor)
        elif self.value==1024:
            color = COLOR1024
            fontColor = COLORFONT1
            fontX = 3
            label = myFont2.render(str(self.value), 1, fontColor)
        elif self.value==2048:
            color = COLOR2048
            fontColor = COLORFONT1
            fontX = 3
            label = myFont2.render(str(self.value), 1, fontColor)
        else:
            color = BLACK
            fontColor = COLORFONT1
            fontX = 3
            label = myFont2.render(str(self.value), 1, fontColor)
        pygame.draw.rect(screen,color,(drawX,drawY,self.size,self.size))
        if self.size==150:
            screen.blit(label,(drawX+fontX,drawY+45))

    def popUp(self):
        cornerX = self.x
        cornerY = self.y
        self.size = 50
        for i in range(5):
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    break
            self.size+=20
            self.x = cornerX+(150-self.size)/2
            self.y = cornerY+(150-self.size)/2
            self.draw()
            pygame.display.update()
        self.x = cornerX
        self.y = cornerY

def isOnButton(mousePos, buttonPos, buttonSize):
    if mousePos[0]>buttonPos[0] and mousePos[0]<buttonPos[0]+buttonSize[0] and mousePos[1]>buttonPos[1] and mousePos[1]<buttonPos[1]+buttonSize[1]:
        return True
    return False

def fillBoard():
    blocks = []
    for i in range(4):
        row= []
        for x in range(4):
            row.append(None)
        blocks.append(row)
    return blocks

def drawBack(blockSize):
    screen.fill(BACKCOLOR)
    for r in range(4):
        for c in range(4):
            drawX = c*(blockSize+20)+20
            drawY = r*(blockSize+20)+20
            pygame.draw.rect(screen,EMPTY,(drawX,drawY,blockSize, blockSize)) 

def checkForEnd(blocks):
    over = True
    for r in range(len(blocks)):
        for c in range(len(blocks[r])-1):
            if blocks[r][c] == None:
                over = False
            elif blocks[r][c+1]!=None:
                if blocks[r][c+1].value == blocks[r][c].value:
                    over = False

    for c in range(len(blocks[0])):
        for r in range(len(blocks)-1):
            if blocks[r][c] == None:
                over = False
            elif blocks[r+1][c] !=None:
                if blocks[r+1][c].value == blocks[r][c].value:
                    over = False
    return over

def printBoard(blocks):
    for row in blocks:
        rower = []
        for block in row:
            rower.append(block.value)
        print(rower)

def endGame(blocks):
    buttonPos = [WIDTH/2-90,HEIGHT/2]
    buttonSize = [180,50]
    buttony = buttonPos[1]
    onButton = False
    printBoard(blocks)
    while True:
        screen.fill(COLOR2)
        label = myFont1.render("GAME OVER!", 1, COLORFONT2)
        screen.blit(label,(WIDTH/2-275,150))
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
        pygame.draw.rect(screen,COLOR2048,(buttonPos[0],buttony,buttonSize[0],buttonSize[1]))
        label1 = myFont3.render("PLAY AGAIN", 1, COLORFONT1)
        screen.blit(label1,(buttonPos[0]+12,buttony+15))
        pygame.display.update()
        
def playGame():
    blockSize = 150
    blocks = []
    blockLoc = []
    newNeeded = True
    secondNew = True
    gameOver = False
    screen.fill(BACKCOLOR)
    #fill blank board in blocks
    blocks = fillBoard()
            
    while not gameOver:
        drawBack(blockSize)
        if newNeeded:
##            for i in range(10000):
##                i=0
            spotX = random.randint(0,3)
            spotY = random.randint(0,3)
            valueChoices = [2,2,2,4, 2,2,2]
            value = random.choice(valueChoices)
            toAdd = two(blockSize, value, spotX, spotY)
            toAdd.popUp()
            indR = (toAdd.y)//(toAdd.size)
            indC= (toAdd.x)//(toAdd.size)
            while(blocks[indR][indC]!=None):
                spotX = random.randint(0,3)
                spotY = random.randint(0,3)
                toAdd = two(blockSize, value, spotX, spotY)
                indR = (toAdd.y)//(toAdd.size)
                indC= (toAdd.x)//(toAdd.size)
            blocks[indR][indC] = toAdd
            blockLoc.append([toAdd.x, toAdd.y])
            newNeeded = False
        if secondNew:
            spotX = random.randint(0,3)
            spotY = random.randint(0,3)
            toAdd = two(blockSize, 2, spotX, spotY)
            indR = (toAdd.y)//(toAdd.size)
            indC= (toAdd.x)//(toAdd.size)
            while(blocks[indR][indC]!=None):
                spotX = random.randint(0,3)
                spotY = random.randint(0,3)
                toAdd = two(blockSize, 2, spotX, spotY)
                indR = (toAdd.y)//(toAdd.size)
                indC= (toAdd.x)//(toAdd.size)
            blocks[indR][indC] = toAdd
            blockLoc.append([toAdd.x, toAdd.y])
            secondNew = False
        
        
        for event in pygame.event.get():
            
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    newBlocks = fillBoard()
                    newLocs = []
                if event.key ==pygame.K_RIGHT:
                    for row in blocks:
                        for numCol in range(1,len(row)+1):
                            block = row[-numCol]
                            while (block!=None) and ([block.x+block.size,block.y] not in newLocs) and (block.x<(WIDTH-(block.spacing*5+block.size))):
                                block.moveRight()
                                newNeeded = True
                                indR = (block.y)//(block.size)
                                indC = (block.x)//(block.size)
                                
                                ##newBlocks[indR][indC] = block
                            if (block!=None):
                                newLocs.append([block.x,block.y])
                                indR = int((block.y)//(block.size))
                                indC = int((block.x)//(block.size))
                                if indC <3:
                                    if newBlocks[indR][indC+1].value==block.value:
                                        if newBlocks[indR][indC+1].canAdd:
                                            block1 = two(blockSize, block.value*2, indC+1, indR, False)
                                            newBlocks[indR][indC+1] = block1
                                            newLocs.remove([block.x,block.y])
                                            newNeeded = True
                                        else:
                                            newBlocks[indR][indC] = block
                                    else:
                                        newBlocks[int(indR)][int(indC)] = block
                                else:
                                    newBlocks[int(indR)][int(indC)] = block
                        ##print(newBlocks)
                elif event.key ==pygame.K_LEFT:
                    for row in blocks:
                        for block in row:
                            while (block!=None) and ([block.x-block.size,block.y] not in newLocs) and (block.x>0):
                                block.moveLeft()
                                newNeeded = True
                                indR = int((block.y)//(block.size))
                                indC= int((block.x)//(block.size))
                                ##newBlocks[indR][indC] = block
                            if (block!=None):
                                newLocs.append([block.x,block.y])
                                indR = int((block.y)//(block.size))
                                indC = int((block.x)//(block.size))
                                if indC >0:
                                    if newBlocks[indR][indC-1].value==block.value:
                                        if newBlocks[indR][indC-1].canAdd:
                                            block1 = two(blockSize, block.value*2, indC-1, indR, False)
                                            newBlocks[indR][indC-1] = block1
                                            newLocs.remove([block.x,block.y])
                                            newNeeded = True
                                        else:
                                            newBlocks[indR][indC] = block
                                    else:
                                        newBlocks[int(indR)][int(indC)] = block
                                else:
                                    newBlocks[int(indR)][int(indC)] = block
                elif event.key ==pygame.K_UP:
                    for row in blocks:
                        for block in row:
                            while (block!=None) and ([block.x,block.y-block.size] not in newLocs) and (block.y>0):
                                block.moveUp()
                                newNeeded = True
                                indR = int((block.y)//(block.size))
                                indC= int((block.x)//(block.size))
                                ##newBlocks[indR][indC] = block
                            if block!=None:
                                newLocs.append([block.x,block.y])
                                indR = int((block.y)//(block.size))
                                indC = int((block.x)//(block.size))
                                if indR >0:
                                    if newBlocks[indR-1][indC].value==block.value:
                                        if newBlocks[indR-1][indC].canAdd:
                                            block1 = two(blockSize, block.value*2, indC, indR-1, False)
                                            newBlocks[indR-1][indC] = block1
                                            newLocs.remove([block.x,block.y])
                                            newNeeded = True
                                        else:
                                            newBlocks[indR][indC] = block
                                    else:
                                        newBlocks[int(indR)][int(indC)] = block
                                else:
                                    newBlocks[int(indR)][int(indC)] = block
                elif event.key ==pygame.K_DOWN:
                    for numRow in range(1,len(blocks)+1):
                        for block in blocks[-numRow]:
                            while (block!=None) and ([block.x,block.y+block.size] not in newLocs) and (block.y<HEIGHT-block.size-block.spacing*5):
                                block.moveDown()
                                newNeeded = True
                                indR = int((block.y)//(block.size))
                                indC= int((block.x)//(block.size))
                                ##newBlocks[indR][indC] = block
                            if block!=None:
                                newLocs.append([block.x,block.y])
                                indR = int((block.y)//(block.size))
                                indC = int((block.x)//(block.size))
                                if indR<3 :
                                    if newBlocks[indR+1][indC].value==block.value:
                                        if newBlocks[indR+1][indC].canAdd:
                                            block1 = two(blockSize, block.value*2, indC, indR+1, False)
                                            newBlocks[indR+1][indC] = block1
                                            newLocs.remove([block.x,block.y])
                                            newNeeded = True
                                        else:
                                            newBlocks[indR][indC] = block
                                    else:
                                        newBlocks[int(indR)][int(indC)] = block
                                else:
                                    newBlocks[int(indR)][int(indC)] = block
                if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    if newBlocks!=fillBoard():
                        blocks = newBlocks
                if event.key == pygame.K_r:
                    playGame()
                    
        for r in range(len(blocks)):
            for c in range(len(blocks[r])):
                block = blocks[r][c]
                if block != None:
                    block.draw()
                    block.canAdd = True

        gameOver = checkForEnd(blocks)
        pygame.display.update()
    endGame(blocks)

playGame()
        
