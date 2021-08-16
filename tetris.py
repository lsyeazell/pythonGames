import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 700

CYAN = (0,250,250)
RED = (250,0,0)
ORANGE = (255, 165,0)
GREEN = (0,250,0)
BLUE = (0,0,250)
MAGENTA = (250,0,250)
YELLOW = (250,250,0)
WHITE = (250,250,250)
DARKBLUE = (0,0,70)
BLACK = (0,0,0)
GREY = (50,50,50)
BACKCOLOR = BLACK
COLORS = [CYAN, RED, ORANGE, GREEN, BLUE, YELLOW, MAGENTA]

myFont1 = pygame.font.SysFont("monospace",80)
myFont2 = pygame.font.SysFont("monospace",35)
myFont4 = pygame.font.SysFont("monospace",50)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#line 1x4
class Piece1:
    def __init__(self, size):
        
        self.size = size
        self.orientation = random.randint(0,3)
        self.y = 0
        if self.orientation%2==0:
            self.length= size*4
            self.width = size
        else:
            self.length = size
            self.width =size*4
        self.x = random.randint(0,(WIDTH-self.width)//self.size)*self.size
        self.timer = 0
        if self.orientation%2==0:
            self.bottom = [[self.x, self.y+self.length]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x,self.y+self.size*3]]
        else:
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size*3, self.y+self.size]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y],[self.x+self.size*3, self.y]]
        
    def updateOrientation(self):
        if self.orientation == 0 or self.orientation==2:
##            pygame.draw.rect(screen,BLUE,(self.x,self.y,self.size,self.size*4))
            self.length = self.size*4
            self.width = self.size
            self.bottom = [[self.x, self.y+self.length]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x,self.y+self.size*3]]
        else:
            pygame.draw.rect(screen,BLUE,(self.x,self.y,self.size*4,self.size))
            self.length = self.size
            self.width =self.size*4
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size*3, self.y+self.size]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y],[self.x+self.size*3, self.y]]    
    def draw(self):
        for spot in self.top:
            pygame.draw.rect(screen,CYAN,(spot[0],spot[1],self.size,self.size))
            pygame.draw.rect(screen,WHITE,(spot[0],spot[1],self.size,self.size),1)
    def rotateLeft(self):
        storage = self.orientation
        self.orientation+=1
        if self.orientation==4:
            self.orientation = 0
        self.updateOrientation()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.updateOrientation()   
    def rotateRight(self):
        storage = self.orientation
        self.orientation-=1
        if self.orientation==-1:
            self.orientation = 3
        self.updateOrientation()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.updateOrientation()
    def fall(self, delay):
        if self.timer%delay==0:
            self.y+=self.size
            self.updateOrientation()
        self.timer +=1
    def backUp(self):
        self.y-=self.size
        self.updateOrientation()
        
    def moveRight(self):
        self.x+=self.size
        self.updateOrientation()
    def moveLeft(self):
        self.x-=self.size
        self.updateOrientation()
    

#"L" shape 3 down 1 bottom right    
class Piece2:
    def __init__(self, size):
        self.size = size
        self.orientation = random.randint(0,3)
        if self.orientation%2==0:
            self.length= size*2
            self.width = size*3
        else:
            self.length = size*3
            self.width =size*2
        self.x = random.randint(0,(WIDTH-self.width)//self.size)*self.size
        self.y = 0
        self.timer = 0
        self.length= size
        if self.orientation==0:
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size*2, self.y]]
        elif self.orientation==1:
            self.bottom = [[self.x, self.y+self.size], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]
        elif self.orientation==2:
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y], [self.x, self.y+self.size]]
        elif self.orientation==3:
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x+self.size, self.y+self.size*2]]
    def update(self):
        if self.orientation == 0:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size*2, self.y]]
        elif self.orientation == 1:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.size], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]
        elif self.orientation == 2:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y], [self.x, self.y+self.size]]
        elif self.orientation == 3:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x+self.size, self.y+self.size*2]]
    def draw(self):
        for spot in self.top:
            pygame.draw.rect(screen,ORANGE,(spot[0],spot[1],self.size,self.size))
            pygame.draw.rect(screen,WHITE,(spot[0],spot[1],self.size,self.size),1)
    def rotateLeft(self):
        storage = self.orientation
        self.orientation+=1
        if self.orientation==4:
            self.orientation = 0
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()   
    def rotateRight(self):
        storage = self.orientation
        self.orientation-=1
        if self.orientation==-1:
            self.orientation = 3
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()
    def fall(self, delay):
        if self.timer%delay==0:
            self.y+=self.size
            self.update()
        self.timer +=1
    def backUp(self):
        self.y-=self.size
        self.updateOrientation()
    def moveRight(self):
        self.x+=self.size
        self.update()
    def moveLeft(self):
        self.x-=self.size
        self.update()

#square 2x2
class Piece3:
    def __init__(self, size):
        
        self.size = size
        self.y = 0
        self.length= size*2
        self.width = size*2
        self.x = random.randint(0,(WIDTH-self.width)//self.size)*self.size
        self.timer = 0
        self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.length]]
        self.top = [[self.x, self.y], [self.x+self.size, self.y], [self.x, self.y+self.size], [self.x+self.size, self.y+self.size]]       

    def update(self):
        self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.length]]
        self.top = [[self.x, self.y], [self.x+self.size, self.y], [self.x, self.y+self.size], [self.x+self.size, self.y+self.size]]
    
    def draw(self):
        for spot in self.top:
            pygame.draw.rect(screen,YELLOW,(spot[0],spot[1],self.size,self.size))
            pygame.draw.rect(screen,WHITE,(spot[0],spot[1],self.size,self.size),1)
    def rotateLeft(self):
        pass
    def rotateRight(self):
        pass
    def fall(self, delay):
        if self.timer%delay==0:
            self.y+=self.size
            self.update()
        self.timer +=1
    def backUp(self):
        self.y-=self.size
        self.updateOrientation()
    def moveRight(self):
        self.x+=self.size
        self.update()
    def moveLeft(self):
        self.x-=self.size
        self.update()

#backwards "L"
class Piece4:
    def __init__(self, size):
        self.size = size
        self.orientation = random.randint(0,3)
        if self.orientation%2==0:
            self.length= size*2
            self.width = size*3
        else:
            self.length = size*3
            self.width =size*2
        self.x = random.randint(0,(WIDTH-self.width)//self.size)*self.size
        self.y = 0
        self.timer = 0
        self.length= size
        if self.orientation==0:
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x, self.y]]
        elif self.orientation==1:
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y+self.size*2],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]
        elif self.orientation==2:
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size*2]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y], [self.x+self.size*2, self.y+self.size]]
        elif self.orientation==3:
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.size]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x+self.size, self.y]]
    def update(self):
        if self.orientation == 0:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x, self.y]]
        elif self.orientation == 1:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y+self.size*2],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]
        elif self.orientation == 2:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size*2]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y], [self.x+self.size*2, self.y+self.size]]
        elif self.orientation == 3:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.size]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x+self.size, self.y]]
    def draw(self):
        for spot in self.top:
            pygame.draw.rect(screen,BLUE,(spot[0],spot[1],self.size,self.size))
            pygame.draw.rect(screen,WHITE,(spot[0],spot[1],self.size,self.size),1)
    def rotateLeft(self):
        storage = self.orientation
        self.orientation+=1
        if self.orientation==4:
            self.orientation = 0
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()   
    def rotateRight(self):
        storage = self.orientation
        self.orientation-=1
        if self.orientation==-1:
            self.orientation = 3
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()
    def fall(self, delay):
        if self.timer%delay==0:
            self.y+=self.size
            self.update()
        self.timer +=1
    def backUp(self):
        self.y-=self.size
        self.updateOrientation()
    def moveRight(self):
        self.x+=self.size
        self.update()
    def moveLeft(self):
        self.x-=self.size
        self.update()

class Piece5:
    def __init__(self, size):
        self.size = size
        self.orientation = random.randint(0,3)
        if self.orientation%2==0:
            self.length= size*2
            self.width = size*3
        else:
            self.length = size*3
            self.width =size*2
        self.x = random.randint(0,(WIDTH-self.width)//self.size)*self.size
        self.y = 0
        self.timer = 0
        self.length= size
        if self.orientation==0:
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size, self.y]]
        elif self.orientation==1:
            self.bottom = [[self.x, self.y+self.size*2], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y+self.size],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]
        elif self.orientation==2:
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size*2],[self.x+self.size*2, self.y+self.size]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y], [self.x+self.size, self.y+self.size]]
        elif self.orientation==3:
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.size*2]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x+self.size, self.y+self.size]]
    def update(self):
        if self.orientation == 0:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size, self.y]]
        elif self.orientation == 1:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.size*2], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y+self.size],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]
        elif self.orientation == 2:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size*2],[self.x+self.size*2, self.y+self.size]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y],[self.x+self.size*2, self.y], [self.x+self.size, self.y+self.size]]
        elif self.orientation == 3:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.size*2]]
            self.top = [[self.x,self.y],[self.x,self.y+self.size],[self.x,self.y+self.size*2],[self.x+self.size, self.y+self.size]]
    def draw(self):
        for spot in self.top:
            pygame.draw.rect(screen,MAGENTA,(spot[0],spot[1],self.size,self.size))
            pygame.draw.rect(screen,WHITE,(spot[0],spot[1],self.size,self.size),1)
    def rotateLeft(self):
        storage = self.orientation
        self.orientation+=1
        if self.orientation==4:
            self.orientation = 0
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()   
    def rotateRight(self):
        storage = self.orientation
        self.orientation-=1
        if self.orientation==-1:
            self.orientation = 3
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()
    def fall(self, delay):
        if self.timer%delay==0:
            self.y+=self.size
            self.update()
        self.timer +=1
    def backUp(self):
        self.y-=self.size
        self.updateOrientation()
    def moveRight(self):
        self.x+=self.size
        self.update()
    def moveLeft(self):
        self.x-=self.size
        self.update()

#z shape
class Piece6:
    def __init__(self, size):
        self.size = size
        self.orientation = random.randint(0,3)
        if self.orientation%2==0:
            self.length= size*2
            self.width = size*3
        else:
            self.length = size*3
            self.width =size*2
        self.x = random.randint(0,(WIDTH-self.width)//self.size)*self.size
        self.y = 0
        self.timer = 0
        self.length= size
        if self.orientation%2 ==0:
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size, self.y]]
        elif self.orientation%2==1:
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.size*2]]
            self.top = [[self.x,self.y+self.size],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x, self.y+self.size*2]]
        
    def update(self):
        if self.orientation%2 == 0:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.length]]
            self.top = [[self.x, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y+self.size],[self.x+self.size, self.y]]
        elif self.orientation%2 == 1:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.length], [self.x+self.size, self.y+self.size*2]]
            self.top = [[self.x,self.y+self.size],[self.x+self.size, self.y],[self.x+self.size, self.y+self.size],[self.x, self.y+self.size*2]]
        
    def draw(self):
        for spot in self.top:
            pygame.draw.rect(screen,RED,(spot[0],spot[1],self.size,self.size))
            pygame.draw.rect(screen,WHITE,(spot[0],spot[1],self.size,self.size),1)
    def rotateLeft(self):
        storage = self.orientation
        self.orientation+=1
        if self.orientation==4:
            self.orientation = 0
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()   
    def rotateRight(self):
        storage = self.orientation
        self.orientation-=1
        if self.orientation==-1:
            self.orientation = 3
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()
    def fall(self, delay):
        if self.timer%delay==0:
            self.y+=self.size
            self.update()
        self.timer +=1
    def backUp(self):
        self.y-=self.size
        self.updateOrientation()
    def moveRight(self):
        self.x+=self.size
        self.update()
    def moveLeft(self):
        self.x-=self.size
        self.update()

#s piece
class Piece7:
    def __init__(self, size):
        self.size = size
        self.orientation = random.randint(0,3)
        if self.orientation%2==0:
            self.length= size*2
            self.width = size*3
        else:
            self.length = size*3
            self.width =size*2
        self.x = random.randint(0,(WIDTH-self.width)//self.size)*self.size
        self.y = 0
        self.timer = 0
        self.length= size
        if self.orientation%2==0:
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.size]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y],[self.x+self.size, self.y]]
        elif self.orientation%2==1:
            self.bottom = [[self.x, self.y+self.size*2], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y+self.size],[self.x, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]

    def update(self):
        if self.orientation%2 == 0:
            self.length = self.size*2
            self.width = self.size*3
            self.bottom = [[self.x, self.y+self.length],[self.x+self.size, self.y+self.length],[self.x+self.size*2, self.y+self.size]]
            self.top = [[self.x, self.y+self.size],[self.x+self.size, self.y+self.size],[self.x+self.size*2, self.y],[self.x+self.size, self.y]]
        elif self.orientation%2 == 1:
            self.length = self.size*3
            self.width = self.size*2
            self.bottom = [[self.x, self.y+self.size*2], [self.x+self.size, self.y+self.length]]
            self.top = [[self.x,self.y+self.size],[self.x, self.y],[self.x+self.size, self.y+self.size],[self.x+self.size, self.y+self.size*2]]

    def draw(self):
        for spot in self.top:
            pygame.draw.rect(screen,GREEN,(spot[0],spot[1],self.size,self.size))
            pygame.draw.rect(screen,WHITE,(spot[0],spot[1],self.size,self.size),1)
    def rotateLeft(self):
        storage = self.orientation
        self.orientation+=1
        if self.orientation==4:
            self.orientation = 0
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()   
    def rotateRight(self):
        storage = self.orientation
        self.orientation-=1
        if self.orientation==-1:
            self.orientation = 3
        self.update()
        for top in self.top:
            if top[0]>=WIDTH:
                self.orientation = storage
        self.update()
    def fall(self, delay):
        if self.timer%delay==0:
            self.y+=self.size
            self.update()
        self.timer +=1
    def backUp(self):
        self.y-=self.size
        self.updateOrientation()
    def moveRight(self):
        self.x+=self.size
        self.update()
    def moveLeft(self):
        self.x-=self.size
        self.update()
            
def addPiece1(pieces1, blockFalling, blockSize):
    piece = Piece1( blockSize)
    pieces1.append(piece)
    blockFalling = piece
    return pieces1, blockFalling

def addPiece2(pieces2, blockFalling, blockSize):
    piece = Piece2( blockSize)
    pieces2.append(piece)
    blockFalling = piece
    return pieces2, blockFalling

def addPiece3(pieces3, blockFalling, blockSize):
    piece = Piece3( blockSize)
    pieces3.append(piece)
    blockFalling = piece
    return pieces3, blockFalling

def addPiece4(pieces4, blockFalling, blockSize):
    piece = Piece4( blockSize)
    pieces4.append(piece)
    blockFalling = piece
    return pieces4, blockFalling

def addPiece5(pieces5, blockFalling, blockSize):
    piece = Piece5( blockSize)
    pieces5.append(piece)
    blockFalling = piece
    return pieces5, blockFalling

def addPiece6(pieces6, blockFalling, blockSize):
    piece = Piece6( blockSize)
    pieces6.append(piece)
    blockFalling = piece
    return pieces6, blockFalling

def addPiece7(pieces7, blockFalling, blockSize):
    piece = Piece7( blockSize)
    pieces7.append(piece)
    blockFalling = piece
    return pieces7, blockFalling

def isOnButton(mousePos, buttonPos, buttonSize):
    if mousePos[0]>buttonPos[0] and mousePos[0]<buttonPos[0]+buttonSize[0] and mousePos[1]>buttonPos[1] and mousePos[1]<buttonPos[1]+buttonSize[1]:
        return True
    return False

def drawGrid(blockSize):
    for lineX in range(WIDTH//blockSize):
        pygame.draw.line(screen, GREY, (lineX*blockSize, 0), (lineX*blockSize, HEIGHT), 1)
    for lineY in range(HEIGHT//blockSize):
        pygame.draw.line(screen,GREY, (0, lineY*blockSize), (WIDTH, lineY*blockSize),1)

def superRand(start, end):
    rand = []
    for i in range(20):
        rand.append(random.randint(start,end))
    randNum = random.choice(rand)
    return randNum

def collisionCheck(tops, blockFalling, blockSize, board):
    collision = False
    for topSpot in tops:
        if topSpot[1]//blockSize<len(board) and topSpot[0]//blockSize<len(board[0]):
            board[topSpot[1]//blockSize][topSpot[0]//blockSize] = 1
        for botSpot in blockFalling.bottom:
            if topSpot == botSpot:
                collision = True
    return collision, board
    

def homeScreen():
    buttonSize = [100,50]
    buttonPos = [(WIDTH-buttonSize[0])/2,HEIGHT/2]
    buttonPos1 = [(WIDTH-buttonSize[0])/2,HEIGHT/2+5]
    buttonColor = random.choice(COLORS)
    changeColor = True
    buttonx = buttonPos[0]
    buttony = buttonPos[1]
    titlePos = [WIDTH/2-100,HEIGHT/2-150]
    titleColor = random.choice(COLORS)
    while True:
        breakOut = False
        screen.fill(BLACK)
        drawGrid(25)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0] and onButton:
                pygame.display.update()
                chooseLevel()
            ##if pygame.mouse.get_pressed()[0] and onButton1:
                ##screen.fill(BACKCOLOR)
                ##breakOut = instructions()
        if breakOut:
            return
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, buttonPos, buttonSize):
            onButton =True
            buttonx = buttonPos1[0]
            buttony = buttonPos1[1]
            if changeColor:
                buttonColor = random.choice(COLORS)
                titleColor = random.choice(COLORS)
                changeColor = False    
        else:
            changeColor = True
            onButton = False
            buttonx = buttonPos[0]
            buttony = buttonPos[1]

##        if isOnButton(mousePos, button1Pos, button1Size):
##            onButton1 = True
##            button1Color = CYAN
##        else:
##            onButton1 = False
##            button1Color = DARKBLUE
        
        label1 = myFont1.render("TETRIS", 1, titleColor)
        screen.blit(label1,(titlePos[0],titlePos[1]))
        pygame.draw.rect(screen,buttonColor,(buttonx,buttony,buttonSize[0],buttonSize[1]))
        label2 = myFont2.render("START", 1, WHITE)
        screen.blit(label2,(buttonx+9,buttony+15))
##        pygame.draw.rect(screen,button1Color,(button1Pos[0],button1Pos[1],button1Size[0],button1Size[1]))
##        label3 = myFont2.render("HOW TO PLAY", 1, WHITE)
##        screen.blit(label3,(button1Pos[0]+9,button1Pos[1]+15))
        pygame.display.update()
        clock.tick(30)

def chooseLevel():
    buttonPos = [WIDTH/2-50,HEIGHT/2]
    buttonSize = [100,50]
    buttonColor = random.choice(COLORS)
    buttony = buttonPos[1]
    button1Pos = [WIDTH/2-70,HEIGHT/2+75]
    button1Size = [140,50]
    button1Color = random.choice(COLORS)
    button1y = button1Pos[1]
    button2Pos = [WIDTH/2-50,HEIGHT/2+150]
    button2Size = [100,50]
    button2Color = random.choice(COLORS)
    button2y = button2Pos[1]
    changeColor = True
    changeColor1 = True
    changeColor2 = True
    onButton = False
    onButton1 = False
    onButton2 = False
    while True:
        screen.fill(BLACK)
        drawGrid(25)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if pygame.mouse.get_pressed()[0] and onButton:
                screen.fill(BACKCOLOR)
                playGame(20)
            if pygame.mouse.get_pressed()[0] and onButton1:
                screen.fill(BACKCOLOR)
                playGame(12)
            if pygame.mouse.get_pressed()[0] and onButton2:
                screen.fill(BACKCOLOR)
                playGame(5)
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, buttonPos, buttonSize):
            onButton =True
            buttony = buttonPos[1]+5
            if changeColor:
                button1Color = random.choice(COLORS)
                buttonColor = random.choice(COLORS)
                button2Color = random.choice(COLORS)
                changeColor = False
        else:
            changeColor = True
            onButton = False
            buttony = buttonPos[1]

        if isOnButton(mousePos, button1Pos, button1Size):
            onButton1 = True
            button1y = button1Pos[1]+5
            if changeColor1:
                button1Color = random.choice(COLORS)
                buttonColor = random.choice(COLORS)
                button2Color = random.choice(COLORS)
                changeColor1 = False
        else:
            onButton1 = False
            changeColor1 = True
            button1y = button1Pos[1]

        if isOnButton(mousePos, button2Pos, button1Size):
            onButton2 = True
            button2y = button2Pos[1]+5
            if changeColor2:
                button1Color = random.choice(COLORS)
                buttonColor = random.choice(COLORS)
                button2Color = random.choice(COLORS)
                changeColor2 = False
        else:
            onButton2 = False
            changeColor2 = True
            button2y = button2Pos[1]
        pygame.draw.rect(screen,buttonColor,(buttonPos[0],buttony,buttonSize[0],buttonSize[1]))
        label1 = myFont2.render("EASY", 1, WHITE)
        screen.blit(label1,(buttonPos[0]+15,buttony+15))
        pygame.draw.rect(screen,button1Color,(button1Pos[0],button1y,button1Size[0],button1Size[1]))
        label2 = myFont2.render("MEDIUM", 1, WHITE)
        screen.blit(label2,(button1Pos[0]+20,button1y+15))
        pygame.draw.rect(screen,button2Color,(button2Pos[0],button2y,button2Size[0],button2Size[1]))
        label3 = myFont2.render("HARD", 1, WHITE)
        screen.blit(label3,(button2Pos[0]+15,button2y+15))
        ##label3 = myFont4.render("SCORE: " +str(score), 1, RED)
        ##screen.blit(label3,(410, 230))
        pygame.display.update()

def endGame():
    bigLabelColor = random.choice(COLORS)
    buttonPos = [WIDTH/2-90,HEIGHT/2]
    buttonSize = [180,50]
    buttonColor = random.choice(COLORS)
    buttony = buttonPos[1]
    button1Pos = [WIDTH/2-50,HEIGHT/2+75]
    button1Size = [100,50]
    button1Color = random.choice(COLORS)
    button1y = button1Pos[1]
    changeColor = True
    changeColor1 = True
    onButton = False
    onButton1 = False
    while True:
        screen.fill(BLACK)
        drawGrid(25)
        label = myFont1.render("GAME OVER!", 1, bigLabelColor)
        screen.blit(label,(WIDTH/2-175,150))
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if pygame.mouse.get_pressed()[0] and onButton:
                screen.fill(BACKCOLOR)
                chooseLevel()
            if pygame.mouse.get_pressed()[0] and onButton1:
                screen.fill(BACKCOLOR)
                homeScreen()
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, buttonPos, buttonSize):
            onButton =True
            buttony = buttonPos[1]+5
            if changeColor:
                button1Color = random.choice(COLORS)
                buttonColor = random.choice(COLORS)
                bigLabelColor = random.choice(COLORS)
                changeColor = False
        else:
            changeColor = True
            onButton = False
            buttony = buttonPos[1]

        if isOnButton(mousePos, button1Pos, button1Size):
            onButton1 = True
            button1y = button1Pos[1]+5
            if changeColor1:
                button1Color = random.choice(COLORS)
                buttonColor = random.choice(COLORS)
                bigLabelColor = random.choice(COLORS)
                changeColor1 = False
        else:
            onButton1 = False
            changeColor1 = True
            button1y = button1Pos[1]
        pygame.draw.rect(screen,buttonColor,(buttonPos[0],buttony,buttonSize[0],buttonSize[1]))
        label1 = myFont2.render("PLAY AGAIN", 1, WHITE)
        screen.blit(label1,(buttonPos[0]+12,buttony+15))
        pygame.draw.rect(screen,button1Color,(button1Pos[0],button1y,button1Size[0],button1Size[1]))
        label2 = myFont2.render("HOME", 1, WHITE)
        screen.blit(label2,(button1Pos[0]+9,button1y+15))
        ##label3 = myFont4.render("SCORE: " +str(score), 1, RED)
        ##screen.blit(label3,(410, 230))
        pygame.display.update()

def paused():
    bigLabelColor = random.choice(COLORS)
    buttonPos = [WIDTH/2-100,HEIGHT/2]
    buttonSize = [200,50]
    buttonColor = random.choice(COLORS)
    buttony = buttonPos[1]
    button1Pos = [WIDTH/2-50,HEIGHT/2+75]
    button1Size = [100,50]
    button1Color = random.choice(COLORS)
    button1y = button1Pos[1]
    changeColor = True
    changeColor1 = True
    onButton = False
    onButton1 = False
    while True:
        screen.fill(BLACK)
        drawGrid(25)
        label = myFont1.render("PAUSED", 1, bigLabelColor)
        screen.blit(label,(WIDTH/2-120,150))
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if pygame.mouse.get_pressed()[0] and onButton:
                screen.fill(BACKCOLOR)
                return
            if pygame.mouse.get_pressed()[0] and onButton1:
                screen.fill(BACKCOLOR)
                homeScreen()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    return
        mousePos = pygame.mouse.get_pos()
        if isOnButton(mousePos, buttonPos, buttonSize):
            onButton =True
            buttony = buttonPos[1]+5
            if changeColor:
                button1Color = random.choice(COLORS)
                buttonColor = random.choice(COLORS)
                bigLabelColor = random.choice(COLORS)
                changeColor = False
        else:
            changeColor = True
            onButton = False
            buttony = buttonPos[1]

        if isOnButton(mousePos, button1Pos, button1Size):
            onButton1 = True
            button1y = button1Pos[1]+5
            if changeColor1:
                button1Color = random.choice(COLORS)
                buttonColor = random.choice(COLORS)
                bigLabelColor = random.choice(COLORS)
                changeColor1 = False
        else:
            onButton1 = False
            changeColor1 = True
            button1y = button1Pos[1]
        pygame.draw.rect(screen,buttonColor,(buttonPos[0],buttony,buttonSize[0],buttonSize[1]))
        label1 = myFont2.render("KEEP PLAYING", 1, WHITE)
        screen.blit(label1,(buttonPos[0]+12,buttony+15))
        pygame.draw.rect(screen,button1Color,(button1Pos[0],button1y,button1Size[0],button1Size[1]))
        label2 = myFont2.render("HOME", 1, WHITE)
        screen.blit(label2,(button1Pos[0]+9,button1y+15))
        ##label3 = myFont4.render("SCORE: " +str(score), 1, RED)
        ##screen.blit(label3,(410, 230))
        pygame.display.update()

def playGame(delay):
    blockSize = 25
    blockFalling = None

    pieces1 = []
    pieces2=[]
    pieces3 = []
    pieces4 = []
    pieces5 = []
    pieces6 = []
    pieces7 = []
    tops = []
    collision = False
    board = []
    for numRow in range(HEIGHT//blockSize):
        row = []
        for numCol in range(WIDTH//blockSize):
            row.append(0)
        board.append(row)
    gameOver = False
    screen.fill(BACKCOLOR)
    downPressed = False
    while not gameOver:
        if blockFalling==None:
            collision = False
            downPressed = False
            randPiece = superRand(1,7)
            if randPiece==1:
                pieces1, blockFalling = addPiece1(pieces1, blockFalling, blockSize)
            elif randPiece==2:
                pieces2, blockFalling = addPiece2(pieces2, blockFalling, blockSize)
            elif randPiece==3:
                pieces3, blockFalling = addPiece3(pieces3, blockFalling, blockSize)
            elif randPiece==4:
                pieces4, blockFalling = addPiece4(pieces4, blockFalling, blockSize)
            elif randPiece==5:
                pieces5, blockFalling = addPiece5(pieces5, blockFalling, blockSize)
            elif randPiece==6:
                pieces6, blockFalling = addPiece6(pieces6, blockFalling, blockSize)
            elif randPiece==7:
                pieces7, blockFalling = addPiece7(pieces7, blockFalling, blockSize)  
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT and blockFalling.x>=blockSize:
                    blockFalling.moveLeft()
                    for top in tops:
                        for topper in blockFalling.top:
                            if top ==topper:
                                blockFalling.moveRight()    
                elif event.key == pygame.K_RIGHT and blockFalling.x<=WIDTH-blockFalling.width-blockSize:
                    blockFalling.moveRight()
                    for top in tops:
                        for topper in blockFalling.top:
                            if top ==topper:
                                blockFalling.moveLeft()
                elif event.key == pygame.K_UP:
                    blockFalling.rotateRight()
                    for top in tops:
                        for topper in blockFalling.top:
                            if top ==topper:
                                blockFalling.rotateLeft()
                elif event.key ==pygame.K_z:
                    blockFalling.rotateLeft()
                    for top in tops:
                        for topper in blockFalling.top:
                            if top ==topper:
                                blockFalling.rotateRight()
                elif event.key ==pygame.K_DOWN:
                    downPressed = True
                elif event.key==pygame.K_SPACE:
                    while not collision:
                        blockFalling.fall(1)
                        collision, board = collisionCheck(tops, blockFalling, blockSize, board)
                        if blockFalling.y==HEIGHT-blockFalling.length:
                            collision = True
                        pygame.display.update()
                if event.key==pygame.K_r:
                    playGame(delay)
                elif event.key==pygame.K_p:
                    paused()
            if event.type==pygame.KEYUP:
                if event.key ==pygame.K_DOWN:
                    downPressed = False

        screen.fill(BACKCOLOR)
        drawGrid(blockSize)
        if downPressed:
            blockFalling.fall(delay//4)
            for top in tops:
                for topper in blockFalling.top:
                    if top ==topper:
                        blockFalling.backUp()
        
        board = []
        for numRow in range(HEIGHT//blockSize):
            row = []
            for numCol in range(WIDTH//blockSize):
                row.append(0)
            board.append(row)
        collision, board = collisionCheck(tops, blockFalling, blockSize, board)

        if blockFalling.y==HEIGHT-blockFalling.length or collision:
            for spot in blockFalling.top:
                tops.append(spot)
            blockFalling = None
            collision = False
        else:
            blockFalling.fall(delay)
        for rowNum in range(len(board)):
            if 0 in board[rowNum]:
                allOnes = False
            else:
                allOnes = True
            
            if allOnes:
                for piece1 in pieces1:
                    for top in range(len(piece1.top)):
                        if piece1.top[top][1] ==(rowNum)*blockSize:
                            piece1.top[top][1] = HEIGHT
                        elif piece1.top[top][1]<(rowNum)*blockSize:
                            piece1.top[top][1]+=blockSize
                    for top in piece1.top:
                        if top[1]==HEIGHT:
                            piece1.top.remove(top)
                        if top[1]==0:
                            gameOver = True
                            print(1)
                            break
                for piece2 in pieces2:
                    for top in range(len(piece2.top)):
                        if piece2.top[top][1] ==(rowNum)*blockSize:
                            piece2.top[top][1] = HEIGHT
                        elif piece2.top[top][1]<(rowNum)*blockSize:
                            piece2.top[top][1]+=blockSize
                    for top in piece2.top:
                        if top[1]==HEIGHT:
                            piece2.top.remove(top)
                        if top[1]==0:
                            gameOver = True
                            print(1)
                            break
                for piece3 in pieces3:
                    for top in range(len(piece3.top)):
                        if piece3.top[top][1] ==(rowNum)*blockSize:
                            piece3.top[top][1] = HEIGHT
                        elif piece3.top[top][1]<(rowNum)*blockSize:
                            piece3.top[top][1]+=blockSize
                    for top in piece3.top:
                        if top[1]==HEIGHT:
                            piece3.top.remove(top)
                        if top[1]==0:
                            gameOver = True
                            print(1)
                            break
                for piece4 in pieces4:
                    for top in range(len(piece4.top)):
                        if piece4.top[top][1] ==(rowNum)*blockSize:
                            piece4.top[top][1] = HEIGHT
                        elif piece4.top[top][1]<(rowNum)*blockSize:
                            piece4.top[top][1]+=blockSize
                    for top in piece4.top:
                        if top[1]==HEIGHT:
                            piece4.top.remove(top)
                        if top[1]==0:
                            gameOver = True
                            print(1)
                            break
                for piece5 in pieces5:
                    for top in range(len(piece5.top)):
                        if piece5.top[top][1] ==(rowNum)*blockSize:
                            piece5.top[top][1] = HEIGHT
                        elif piece5.top[top][1]<(rowNum)*blockSize:
                            piece5.top[top][1]+=blockSize
                    for top in piece5.top:
                        if top[1]==HEIGHT:
                            piece5.top.remove(top)
                        if top[1]==0:
                            gameOver = True
                            print(1)
                            break
                for piece6 in pieces6:
                    for top in range(len(piece6.top)):
                        if piece6.top[top][1] ==(rowNum)*blockSize:
                            piece6.top[top][1] = HEIGHT
                        elif piece6.top[top][1]<(rowNum)*blockSize:
                            piece6.top[top][1]+=blockSize
                    for top in piece6.top:
                        if top[1]==HEIGHT:
                            piece6.top.remove(top)
                        if top[1]==0:
                            gameOver = True
                            print(1)
                            break
                for piece7 in pieces7:
                    for top in range(len(piece7.top)):
                        if piece7.top[top][1] ==(rowNum)*blockSize:
                            piece7.top[top][1] = HEIGHT
                        elif piece7.top[top][1]<(rowNum)*blockSize:
                            piece7.top[top][1]+=blockSize
                    for top in piece7.top:
                        if top[1]==HEIGHT:
                            piece7.top.remove(top)
                        if top[1]==0:
                            gameOver = True
                            print(1)
                            break
                allOnes = False
            for top in tops:
                if top[1]==0:
                    gameOver = True
                    endGame()

        for piece1 in pieces1:
            piece1.draw()
        for piece2 in pieces2:
            piece2.draw()
        for piece3 in pieces3:
            piece3.draw()
        for piece4 in pieces4:
            piece4.draw()
        for piece5 in pieces5:
            piece5.draw()
        for piece6 in pieces6:
            piece6.draw()
        for piece7 in pieces7:
            piece7.draw()           
        pygame.display.update()
homeScreen()
pygame.quit()
sys.exit()
