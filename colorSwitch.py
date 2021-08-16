import pygame
import random
import sys
import math

pygame.init()

WIDTH = 500
HEIGHT = 600

BLUE = (50, 226, 241)
YELLOW = (255, 232, 15)
PURPLE = (140, 18, 251)
PINK = (255, 0, 128)
WHITE = (255,255,255)
BACKCOLOR = (39, 39, 39)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class rotatingCircle:
    def __init__(self,size, thickness):
        self.size = size
        self.angle = int(random.random()*360)
        self.thickness = thickness
        self.colors = {
            "purple": [self.angle*math.pi/180,(self.angle+90)*math.pi/180],
            "pink": [(self.angle+90)*math.pi/180,(self.angle+180)*math.pi/180],
            "blue": [(self.angle+180)*math.pi/180,(self.angle+270)*math.pi/180],
            "yellow": [(self.angle+270)*math.pi/180,(self.angle+360)*math.pi/180]
        }
        self.rect = (WIDTH//2-size//2,0-size//2,size,size)
        self.y = 0-size//2
        
    def rotate(self):
        for color in self.colors:
            self.colors[color][0]+=.05
            self.colors[color][1]+=.05
        
    def draw(self):
        pygame.draw.arc(screen, PURPLE, self.rect, self.colors["purple"][0], self.colors["purple"][1],self.thickness)
        pygame.draw.arc(screen, BLUE, self.rect, self.colors["blue"][0], self.colors["blue"][1],self.thickness)
        pygame.draw.arc(screen, PINK, self.rect, self.colors["pink"][0], self.colors["pink"][1],self.thickness)
        pygame.draw.arc(screen, YELLOW, self.rect, self.colors["yellow"][0], self.colors["yellow"][1],self.thickness)

    def move(self, direction):
        self.y +=2*direction
        self.rect = (WIDTH//2-self.size//2,self.y,self.size,self.size)
    def checkCollision(self,dotColor, dotSize):
        
        if (self.y+self.size>HEIGHT//2-dotSize and self.y+self.size-self.thickness<HEIGHT//2+dotSize):
            if not(self.colors[dotColor][0]%(2*math.pi)<(3*math.pi/2) and self.colors[dotColor][1]%(2*math.pi)>(3*math.pi/2)):
                print(self.colors[dotColor][0]%(2*math.pi), self.colors[dotColor][1]%(2*math.pi))
                return True, False
        elif (self.y>HEIGHT//2-dotSize and self.y+self.thickness<HEIGHT//2+dotSize):
            if not(self.colors[dotColor][0]%(2*math.pi)<math.pi/2 and self.colors[dotColor][1]%(2*math.pi)>math.pi/2):
                return True, False
        return False, False

class rotatingTriangle:
    def __init__(self, size, thickness, dotColor):
        self.size = size
        self.thickness = thickness
        self.angle = random.random()*math.pi*2
        self.x = WIDTH//2
        self.y = 0
        self.xs = []
        self.ys=[]
        self.colors = [(PINK,"pink"), (PURPLE,"purple"), (BLUE,"blue"), (YELLOW,"yellow")]
        toRemove = random.choice(self.colors)
        while toRemove==dotColor:
            toRemove = random.choice(self.colors)
        self.colors.remove(toRemove)
        self.updatePos()

    def updatePos(self):
        self.xs = [self.x+math.cos(self.angle)*self.size,self.x+math.cos(self.angle+2*math.pi/3)*self.size,self.x+math.cos(self.angle+4*math.pi/3)*self.size]
        self.ys= [self.y+math.sin(self.angle)*self.size, self.y+math.sin(self.angle+2*math.pi/3)*self.size,self.y+math.sin(self.angle+4*math.pi/3)*self.size]
    def move(self, direction):
        self.y +=2*direction
        self.updatePos()
    def rotate(self):
        self.angle+=0.05
        self.updatePos()
    def draw(self):
        for i in range(3):
            pygame.draw.line(screen, self.colors[i][0],(self.xs[i],self.ys[i]),(self.xs[(i+1)%3],self.ys[(i+1)%3]),self.thickness)
            pygame.draw.circle(screen, self.colors[i][0],(int(self.xs[i]//1),int(self.ys[i]//1)), self.thickness//2)
        pygame.draw.circle(screen, self.colors[0][0],(int(self.xs[0]//1),int(self.ys[0]//1)), self.thickness//2)
    def checkCollision(self, dotColor, dotSize):
        for i in range(3):
            if(self.xs[i]>self.x and self.xs[(i+1)%3]<self.x) or (self.xs[i]<self.x and self.xs[(i+1)%3]>self.x):
                m = (self.ys[i]-self.ys[(i+1)%3])/(self.xs[i]-self.xs[(i+1)%3])
                y = m*(WIDTH//2-self.xs[i])+self.ys[i]
                if (y>HEIGHT//2-dotSize and y<HEIGHT//2+dotSize):
                    if dotColor!=self.colors[i][1]:
                        return True,False
        
        return False, False
                
class colorChanger:
    def __init__(self):
        self.size = 30
        self.y = -self.size//2
        self.rect = (WIDTH//2-self.size//2,self.y,self.size,self.size)
        
    def draw(self):
        pygame.draw.arc(screen, PURPLE, self.rect, 0, math.pi/2,self.size//2)
        pygame.draw.arc(screen, YELLOW, self.rect, math.pi/2, math.pi,self.size//2)
        pygame.draw.arc(screen, BLUE, self.rect, math.pi,3*math.pi/2,self.size//2)
        pygame.draw.arc(screen, PINK, self.rect, 3*math.pi/2, 2*math.pi,self.size//2)
    def move(self, direction):
        self.y +=2*direction
        self.rect = (WIDTH//2-self.size//2,self.y,self.size,self.size)   
    def rotate(self):
        pass
    def checkCollision(self, dotColor,dotSize):
        if(self.y+self.size>HEIGHT//2-dotSize and self.y<HEIGHT//2+dotSize):
           return False, True
        return False, False

class star:
    def __init__(self):
        self.x = WIDTH//2
        self.y=0
        self.size = -10
    def move(self, direction):
        self.y +=2*direction
    def draw(self):
        points = [(self.x,self.y+1*self.size),(self.x-.225*self.size,self.y+.309*self.size),(self.x-.951*self.size,self.y+.309*self.size),(self.x-.363*self.size,self.y-.118*self.size),(self.x-.558*self.size,self.y-.809*self.size),(self.x,self.y-.382*self.size),(self.x+.588*self.size,self.y-.809*self.size),(self.x+.363*self.size,self.y-.118*self.size),(self.x+.951*self.size,self.y+.309*self.size),(self.x+.225*self.size,self.y+.309*self.size)]
        pygame.draw.polygon(screen,WHITE,points)
    def rotate(self):
        pass
    def checkCollision(self, dotColor,dotSize):
        if self.y>WIDTH//2:
            return True, True
        return False,False
        

def endGame(score):
    print(score)
    pygame.quit()
    sys.exit()
        
def playGame():
    screen.fill(BACKCOLOR)
    gameOver = False
    
    dotSize = 10
    dotColors = [(PINK,"pink"), (PURPLE,"purple"), (BLUE,"blue"), (YELLOW,"yellow")]
    dotColor = dotColors[(int)(random.random()*4)]
    obstacles = [rotatingTriangle(120,10,dotColor)]##Circle(150,10)]
    score = 0
    fallSpeed = -1
    while not gameOver:
        screen.fill(BACKCOLOR)
        incSpeed = False
        for cir in obstacles:
            cir.draw()
            cir.rotate()
            if cir!=obstacles[0]:
                incSpeed=True
                cir.move(fallSpeed)
            elif cir.y>-cir.size//2 or fallSpeed>0:
                incSpeed=True
                cir.move(fallSpeed)
        if incSpeed:
            fallSpeed-=0.6
        if obstacles[-1].y>obstacles[-1].size*4:
            rando = random.random()
            if rando>.4:
                size = random.randint(80,280)
                thickness = random.randint(size//30, size//8)
                obstacles.append(star())
                obstacles.append(rotatingCircle(size,thickness))##150,10
            elif rando>.1:
                obstacles.append(star())
                obstacles.append(rotatingTriangle(120,10,dotColor))
            elif rando>0:
                obstacles.append(colorChanger())
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    ##for cir in obstacles:
                        ##for i in range(20):
                            ##cir.move(1)
                    fallSpeed = 5
        for cir in obstacles:
            over, changeColor = cir.checkCollision(dotColor[1], dotSize)
            if over and changeColor:
                score+=1
                obstacles.remove(cir)
            elif over:
                gameOver = True
                break
            elif changeColor:
                dotColor = dotColors[(int)(random.random()*4)]
                obstacles.remove(cir)
                break
        pygame.draw.circle(screen, dotColor[0], (WIDTH//2,HEIGHT//2),dotSize)
        pygame.display.update()
        clock.tick(10)
            
    endGame(score)

playGame()
