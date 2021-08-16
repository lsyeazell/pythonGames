import pygame
import random
import sys

pygame.init()

WIDTH = 930
HEIGHT = 600

BLACK = (0,0,0)
BACKCOLOR = (0,0,0)
YELLOW = (250,250,0)
BLUE = (75,75,250)
WHITE = (255,255,255)
PINK = (255,184,255)
ORANGE = (255,184,82)
CYAN = (0,255,255)
GREEN = (100,250,130)
RED = (255,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

myFont =pygame.font.SysFont("monospace",25)
myFont1 =pygame.font.SysFont("monospace",60)

#Ghost class
class ghost:
    def __init__(self,color,startX, startY, walls, startTime):
        self.startTime = startTime
        self.color = color
        self.toColor = color
        self.startX = startX
        self.x = startX
        self.y = startY
        self.startY = startY
        self.size = 15
        self.speed = 1
        self.walls = walls
        self.noRight = False
        self.noLeft = False
        self.noUp = False
        self.noDown = False
        self.keepStarting = True
        self.isBlue = False
        self.direction = "right"
        self.toUse = 0
    #displays ghost, counter is like a timer which allows for switching between appearances to look animated
    def draw(self, counter):
        if self.isBlue:
            self.toColor=BLUE
        else:
            self.toColor = self.color
        #rects = [(self.x-15,self.y-3,2,18),(self.x-13,self.y-9,2,22),(self.x-11,self.y-11,2,22),(self.x-9,self.y-13,2,26),(self.x-7,self.y-13,4,28),(self.x-5,self.y-15,10,26),(self.x-3,self.y-15,2,28),(self.x+1,self.y-15,2,28),(self.x+3,self.y-13,4,28),(self.x+7,self.y-13,2,26),(self.x+9,self.y-11,2,22),(self.x+11,self.y-9,2,22), (self.x+13,self.y-3,2,18)]
        rects = [(self.x-14,self.y-2,2,16),(self.x-12,self.y-8,2,20),(self.x-10,self.y-10,2,20),(self.x-8,self.y-12,2,24),(self.x-6,self.y-12,4,26),(self.x-4,self.y-14,8,24),(self.x+2,self.y-12,4,26),(self.x+6,self.y-12,2,24),(self.x+8,self.y-10,2,20),(self.x+10,self.y-8,2,20), (self.x+12,self.y-2,2,16)]
        rects2 = [(self.x-14,self.y-2,2,14),(self.x-12,self.y-8,2,22),(self.x-10,self.y-10,2,24),(self.x-8,self.y-12,2,24),(self.x-6,self.y-12,4,22),(self.x-4,self.y-14,8,26),(self.x-2,self.y-14,4,28),(self.x+4,self.y-12,2,22),(self.x+6,self.y-12,2,24),(self.x+8,self.y-10,2,24),(self.x+10,self.y-8,2,22), (self.x+12,self.y-2,2,14)]

        if counter%20==0:
            self.toUse = 0
        elif counter%20==10:
            self.toUse = 1
        if self.toUse==0:
            rectangles = rects
        else:
            rectangles = rects2
        for rect in rectangles:
            pygame.draw.rect(screen, self.toColor, rect)
        if not self.isBlue:
            if self.direction=="right":
                whites = [(self.x-8,self.y-6,8,6),(self.x-6,self.y-8,4,10),(self.x+4,self.y-6,8,6),(self.x+6,self.y-8,4,10)]
                blacks = [(self.x-4,self.y-4,4,4),(self.x+8,self.y-4,4,4)]
            elif self.direction=="left":
                whites=[(self.x-12,self.y-6,8,6),(self.x-10,self.y-8,4,10),(self.x,self.y-6,8,6),(self.x+2,self.y-8,4,10)]
                blacks=[(self.x-12,self.y-4,4,4),(self.x,self.y-4,4,4)]
            elif self.direction=="up":
                whites=[(self.x-10,self.y-10,8,6),(self.x-8,self.y-12,4,10),(self.x+2,self.y-10,8,6),(self.x+4,self.y-12,4,10)]
                blacks = [(self.x-8,self.y-12,4,4),(self.x+4,self.y-12,4,4)]
            elif self.direction=="down":
                whites=[(self.x-10,self.y-4,8,6),(self.x-8,self.y-6,4,10),(self.x+2,self.y-4,8,6),(self.x+4,self.y-6,4,10)]
                blacks = [(self.x-8,self.y,4,4),(self.x+4,self.y,4,4)]
            for white in whites:
                pygame.draw.rect(screen, WHITE, white)
            for black in blacks:
                pygame.draw.rect(screen,BLUE,black)
        else:
            whites = [(self.x-6,self.y-4,4,4), (self.x+2,self.y-4,4,4),(self.x-12,self.y+6,2,2),(self.x-10,self.y+4,4,2),(self.x-6,self.y+6,4,2),(self.x-2,self.y+4,4,2),(self.x+2,self.y+6,4,2),(self.x+6,self.y+4,4,2),(self.x+10,self.y+6,2,2)]
            for white in whites:
                pygame.draw.rect(screen, WHITE, white)
    #puts ghost in starting location
    def startGhost(self, counter, ghosts):
        keepStarting = True
        if counter>self.startTime:
            if self.x<WIDTH//2:
                self.x+=1
            elif self.x>WIDTH//2:
                self.x-=1
            elif self.y>270-self.size:
                self.y-=1
            else:
                ghosts.append(self)
                self.keepStarting = False
        self.draw(counter)
        return ghosts
    #ghost moves in direction of pacman until ghost hits a wall
    def move(self, pacman, counter):
        if counter%2==0 or counter%3==0:
            if self.noRight and self.noLeft and self.noUp and self.noDown:
                self.noRight = False
                self.noLeft = False
                self.noUp = False
                self.noDown = False
            badMove = random.random()

            #if there is no difference between left/right or up/down then random direction is blocked to keep pacman moving
            if pacman.x-self.x==0:
                choice = random.random()
                if choice>0.5:
                    self.noLeft = True
                else:
                    self.noRight = True
            elif pacman.y-self.y==0:
                choice = random.random()
                if choice>0.5:
                    self.noUp = True
                else:
                    self.noDown = True

            #uses list to order the relative distances to pacman in each direction
            directions = [(pacman.x-self.x, "right"),(self.x-pacman.x,"left"),(self.y-pacman.y, "up"),(pacman.y-self.y,"down")]
            directions.sort()

            #checks if pacman can actually move in direction starting with furthest from pacman direction, if it can move then ghost moves
            # if pacman can't move variables are updated
            hasMoved = False
            for i in range(1,len(directions)+1):
                if not self.isBlue:
                    direction = directions[-i][1]
                else:
                    direction = directions[i-1][1]
                canMove = True
                if direction=="right" and not hasMoved and not self.noRight:
                    for wall in self.walls:
                        if not(self.x+self.size<wall[0] or self.x-self.size>=wall[0]+wall[2] or not (self.y+self.size>wall[1] and self.y-self.size<wall[1]+wall[3])) or self.x>=WIDTH-self.size:
                            canMove = False
                    if canMove:
                        self.x+=self.speed
                        hasMoved = False
                        self.noUp = False
                        self.noDown = False
                        break
                    else:
                        self.noRight = True
                if direction=="left"  and not hasMoved and not self.noLeft:
                    for wall in self.walls:
                        if not (self.x-self.size>wall[0]+wall[2] or self.x+self.size<=wall[0] or not (self.y+self.size>wall[1] and self.y-self.size<wall[1]+wall[3])) or self.x<=self.size:
                            canMove = False
                    if canMove:
                        self.x-=self.speed
                        hasMoved = False
                        self.noUp = False
                        self.noDown = False
                        break
                    else:
                        self.noLeft = True
                if direction=="up" and not hasMoved and not self.noUp:
                    for wall in self.walls:
                        if not(self.y-self.size>wall[1]+wall[3] or self.y+self.size<=wall[1]or not (self.x+self.size>wall[0] and self.x-self.size<wall[0]+wall[2])) or self.y<=self.size:
                            canMove = False
                    if canMove:
                        self.y-=self.speed
                        hasMoved = False
                        self.noRight = False
                        self.noLeft = False
                        break
                    else:
                        self.noUp = True
                if direction=="down" and not hasMoved and not self.noDown:
                    for wall in self.walls:
                        if not(self.y+self.size<wall[1] or self.y-self.size>=wall[1]+wall[3] or not (self.x+self.size>wall[0] and self.x-self.size<wall[0]+wall[2])) or self.y>=HEIGHT-self.size:
                            canMove = False
                    if canMove:
                        self.y+=self.speed
                        hasMoved = False
                        self.noRight = False
                        self.noLeft = False
                        break
                    else:
                        self.noDown = True
            self.direction = direction
            
        
#PacMan class
class pacMan:
    def __init__(self, walls):
        self.size = 15
        self.direction = "right"
        self.x = WIDTH//2
        self.y = HEIGHT//2-105
        self.speed = 1
        self.walls = walls
        self.color = YELLOW
        self.mouth = True
    #continues to move in specified direction as long as pacman doesn't hit a wall
    def move(self):
        canMove = True
        if self.direction=="right" and self.x<WIDTH-self.size:
            for wall in self.walls:
                if not(self.x+self.size<wall[0] or self.x-self.size>=wall[0]+wall[2] or not (self.y+self.size>wall[1] and self.y-self.size<wall[1]+wall[3])):
                    canMove = False
            if canMove:
                self.x+=self.speed
        elif self.direction=="left" and self.x>self.size:
            for wall in self.walls:
                if not (self.x-self.size>wall[0]+wall[2] or self.x+self.size<=wall[0] or not (self.y+self.size>wall[1] and self.y-self.size<wall[1]+wall[3])):
                    canMove = False
            if canMove:
                self.x-=self.speed
        elif self.direction=="up" and self.y>self.size:
            for wall in self.walls:
                if not(self.y-self.size>wall[1]+wall[3] or self.y+self.size<=wall[1]or not (self.x+self.size>wall[0] and self.x-self.size<wall[0]+wall[2])):
                    canMove = False
            if canMove:
                self.y-=self.speed
        elif self.direction=="down"and self.y<HEIGHT-self.size:
            for wall in self.walls:
                if not(self.y+self.size<wall[1] or self.y-self.size>=wall[1]+wall[3] or not (self.x+self.size>wall[0] and self.x-self.size<wall[0]+wall[2])):
                    canMove = False
            if canMove:
                self.y+=self.speed
                
    #Changes to new direction as long as pacman can move in that direction
    def changeDirection(self, direction):
        changeD = True
        if direction=="right" and self.x<WIDTH-self.size:
            for wall in self.walls:
                if self.x+self.size==wall[0] and (self.y+self.size>wall[1] and self.y-self.size<wall[1]+wall[3]):
                    changeD = False
        elif direction=="left" and self.x>self.size:
            for wall in self.walls:
                if self.x-self.size==wall[0]+wall[2] and (self.y+self.size>wall[1] and self.y-self.size<wall[1]+wall[3]):
                    changeD = False
        elif direction=="up" and self.y>self.size:
            for wall in self.walls:
                if self.y-self.size==wall[1]+wall[3] and (self.x+self.size>wall[0] and self.x-self.size<wall[0]+wall[2]):
                    changeD = False
        elif direction=="down"and self.y<HEIGHT-self.size:
            for wall in self.walls:
                if self.y+self.size==wall[1] and (self.x+self.size>wall[0] and self.x-self.size<wall[0]+wall[2]):
                    changeD = False
        if changeD:
            self.direction = direction
            
    #draws pacman and uses counter as timer to make mouth grow and shrink in time
    def draw(self, counter):
        pygame.draw.circle(screen, self.color, (self.x, self.y),self.size)
        if self.direction=="left":
            sizeMouth=abs((self.x-15)%30-14.5)*2//3
            if sizeMouth>1:
                pygame.draw.polygon(screen, BLACK, [(self.x+3,self.y),(self.x-self.size, self.y-sizeMouth),(self.x-self.size, self.y+sizeMouth)])
        elif self.direction=="right":
            sizeMouth=abs((self.x-15)%30-14.5)*2//3
            if sizeMouth>1:
                pygame.draw.polygon(screen, BLACK, [(self.x-3,self.y),(self.x+self.size, self.y-sizeMouth),(self.x+self.size, self.y+sizeMouth)])
        elif self.direction=="up":
            sizeMouth=abs((self.y-15)%30-14.5)*2//3
            if sizeMouth>1:
                pygame.draw.polygon(screen, BLACK, [(self.x,self.y+3),(self.x-sizeMouth, self.y-self.size),(self.x+sizeMouth, self.y-self.size)])
        elif self.direction=="down":
            sizeMouth=abs((self.y-15)%30-14.5)*2//3
            if sizeMouth>1:
                pygame.draw.polygon(screen, BLACK, [(self.x,self.y-3),(self.x-sizeMouth, self.y+self.size),(self.x+sizeMouth, self.y+self.size)])

    #when pacman overlaps with dots he gets points
    def eatDots(self,dots, score):
        powered = False
        for dot in dots:
            if (self.x<=dot[0]+10 and self.x>=dot[0]-10 and (self.y<=dot[1]+10 and self.y>=dot[1]-10)):
                dots.remove(dot)
                score+=10
                if dot[2]==True:
                    powered = True
                    score+=40
        return dots, powered, score

    #checks if collided with ghost
    def youDead(self,ghosts):
        for ghoster in ghosts:
            if (self.x-self.size<ghoster.x+ghoster.size and self.x+self.size>ghoster.x-ghoster.size) and (self.y-self.size<ghoster.y+ghoster.size and self.y+self.size>ghoster.y-ghoster.size):
                return True, ghoster
        return False, None

def checkCollision(walls, colliderX, colliderY, colliderSize):
    for wall in walls:
        if(colliderX+colliderSize>wall[0] and colliderX-colliderSize<wall[0]+wall[2]):
            if (colliderY+colliderSize>wall[1] and colliderY-colliderSize<wall[1]+wall[3]):
                return True
    return False

#game window closes when game over
def endGame(win):
    pygame.quit()
    sys.exit()

#start screen
def startGame(walls, dots, dotSize, specialSize,lives):
    screen.fill(BACKCOLOR)
    counter = 0

    pacman = pacMan(walls)
    while counter<300:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()

        #draws screen with dots, walls, score, and lives
        screen.fill(BACKCOLOR)
        for dot in dots:
            if not dot[2]:
                pygame.draw.circle(screen, WHITE, (dot[0],dot[1]), dotSize)
            else:
                pygame.draw.circle(screen, WHITE, (dot[0],dot[1]), specialSize)
        for wall in walls:
            pygame.draw.rect(screen, BLUE,wall,2)
        pacman.draw(counter)
        label = myFont.render("lives: "+str(lives), 1, WHITE)
        screen.blit(label,(10,10))

        #displays ready, set, go!
        if counter>200:
            text="  GO!  "
        elif counter>100:
            text = "  set  "
        else:
            text="ready"
        label1 = myFont1.render(text, 1, WHITE)
        screen.blit(label1,(WIDTH//2-55,HEIGHT//2-10))
        counter+=1
        pygame.display.update()

# game play screen
def playGame():
    screen.fill(BACKCOLOR)
    gameOver = False
    startPow = -100000
    counter = 0
    #define locations of walls
    walls1 = [(0,0,120,90),(0,150,30,30),(0,300,180,30),(0,570,90,30),(30,120,30,150),(30,360,30,120),(30,510,120,30),(60,450,90,30),(90,150,120,30),(90,210,30,60),(90,360,30,60),(90,90,30,30),(120,240,60,30),(120,540,30,30)]
    walls2 = [(150,30,90,30),(150,90,60,30),(150,180,30,30),(150,360,30,60),(180,390,150,30),(180,450,150,30),(180,480,30,90),(210,0,30,30),(210,210,30,30),(210,270,30,90),(240,90,30,150),(240,270,30,30),(240,510,90,30),(240,570,90,30)]
    walls3 = [(270,30,30,90),(270,330,90,30),(300,150,210,30),(300,30,30,30),(300,210,30,90),(330,90,30,60),(330,270,30,60),(360,210,180,30),(360,30,150,30),(360,390,120,30),(360,450,30,120),(390,90,120,30),(390,270,150,90)]
    walls4 = [(420,420,30,90),(420,540,90,30),(480,0,30,30),(480,120,30,30),(480,450,30,60),(510,390,120,30),(510,450,60,30),(540,30,30,120),(540,150,150,30),(540,510,90,30),(540,570,300,30),(570,30,90,30),(570,210,30,90),(570,330,90,30)]
    walls5 = [(600,90,120,30),(600,210,120,30),(600,450,30,60),(630,270,30,60),(660,270,60,30),(660,390,120,30),(660,450,120,30),(660,480,30,30),(660,540,30,30),(690,0,30,90),(690,300,30,60),(720,150,30,90),(720,510,120,30)]
    walls6 = [(750,30,30,90),(750,270,30,60),(750,360,30,30),(780,150,30,90),(780,30,120,30),(810,90,120,30),(810,150,120,30),(810,270,90,30),(810,330,60,30),(810,390,120,30),(810,450,30,60),(840,210,60,30),(870,450,30,120),(900,330,30,60)]
    walls = walls1+walls2+walls3+walls4+walls5+walls6
    pacman = pacMan(walls)#lets pacman know where the walls are

    #set keys as unpressed
    pressedRight = False
    pressedLeft = False
    pressedUp = False
    pressedDown = False
       
    #create ghosts, ghosts have different startTimes which determine when they can exit the gate
    pinky = ghost(PINK, 450, HEIGHT//2+15, walls, 100)
    inky = ghost(CYAN, 480, HEIGHT//2+15, walls, 500)
    blinky = ghost(RED, 420, HEIGHT//2+15, walls, 900)
    clyde = ghost(ORANGE, 510, HEIGHT//2+15, walls, 1300)
    dots = []
    powerer = False #this keeps track of whether pacman ate big dot
    #specify constants that really should be in all caps
    dotSize = 4
    specialSize = 7
    #set starting score/lives
    ghosts = []
    lives = 3
    score = 0

    #finds locations of dots
    for row in range(HEIGHT//30):
        for col in range(WIDTH//30):
            dotX = col*30+15
            dotY = row*30+15
            special = False
            randNum = random.random()
            if randNum<0.03:
                special = True
            if not checkCollision(walls, dotX, dotY, dotSize) and not (col<3 and row<2):
                dots.append((col*30+15, row*30+15, special))
    startGame(walls, dots, dotSize, specialSize, lives)

    #game loop
    while not gameOver:
        screen.fill(BACKCOLOR)
        for wall in walls:
            pygame.draw.rect(screen, BLUE, wall, 2)
        pacman.draw(counter)
        for dot in dots:
            if not dot[2]:
                pygame.draw.circle(screen, WHITE, (dot[0],dot[1]), dotSize)
            else:
                pygame.draw.circle(screen, WHITE, (dot[0],dot[1]), specialSize)
        label = myFont.render("lives: "+str(lives), 1, WHITE)
        screen.blit(label,(10,10))
        label = myFont.render("score: "+str(score), 1, WHITE)
        screen.blit(label,(10,40))

        #ghosts exit jail. uh oh!
        if pinky.keepStarting:
            ghosts = pinky.startGhost(counter,ghosts)
        if inky.keepStarting:
            ghosts = inky.startGhost(counter,ghosts)
        if blinky.keepStarting:
            ghosts = blinky.startGhost(counter,ghosts)
        if clyde.keepStarting:
            ghosts = clyde.startGhost(counter,ghosts)

        #checks for events such as keys being pressed or exiting game
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pressedRight = True
                elif event.key == pygame.K_LEFT:
                    pressedLeft = True
                elif event.key == pygame.K_UP:
                    pressedUp = True
                elif event.key == pygame.K_DOWN:
                    pressedDown = True
            if event.type==pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pressedRight = False
                elif event.key == pygame.K_LEFT:
                    pressedLeft = False
                elif event.key == pygame.K_UP:
                    pressedUp = False
                elif event.key == pygame.K_DOWN:
                    pressedDown = False

        #if key is pressed then pacman changes direction
        if pressedRight:
            pacman.changeDirection("right")
        elif pressedLeft:
            pacman.changeDirection("left")
        elif pressedUp:
            pacman.changeDirection("up")
        elif pressedDown:
            pacman.changeDirection("down")

        #pretty self explanatory
        pacman.move()

        #ghosts move and are redrawn
        for ghostie in ghosts:
            ghostie.move(pacman, counter)
            ghostie.draw(counter)

        #check if pacman eats any dots and update his score!
        dots, powered, score = pacman.eatDots(dots, score)
        collided, ghostie = pacman.youDead(ghosts)

        #if pacman ate a big dot then power him up!
        if powered:
            powerer = True
            startPow = counter
        if counter==startPow:
            inky.isBlue = True
            pinky.isBlue = True
            blinky.isBlue = True
            clyde.isBlue = True
        if counter==startPow+600:
            powerer = False
            inky.isBlue = False
            pinky.isBlue = False
            blinky.isBlue = False
            clyde.isBlue = False

        #If pacman hit a ghost either pacman is dead or the ghost is depending on who is powered up
        if collided:
            #good things happen when pacman has powers
            if powerer and ghostie.isBlue:
                if ghostie==pinky:
                    ghosts.remove(ghostie)
                    pinky = ghost(PINK, 450, HEIGHT//2+15, walls, 100+counter)
                elif ghostie==inky:
                    ghosts.remove(ghostie)
                    inky = ghost(CYAN, 480, HEIGHT//2+15, walls, 100+counter)
                elif ghostie==blinky:
                    ghosts.remove(ghostie)
                    blinky = ghost(RED, 420, HEIGHT//2+15, walls,100)
                elif ghostie ==clyde:
                    ghosts.remove(ghostie)
                    clyde = ghost(ORANGE, 510, HEIGHT//2+15, walls,100+counter)
                    
            #bad things happen when pacman doesn't have powers
            else:
                lives-=1
                #if pacman still has lives, then reset
                if lives>0:
                    pacman.x =WIDTH//2
                    pacman.y =HEIGHT//2-105
                    pacman.direction="right"
                    pinky = ghost(PINK, 450, HEIGHT//2+15, walls,100)
                    inky = ghost(CYAN, 480, HEIGHT//2+15, walls,300)
                    blinky = ghost(RED, 420, HEIGHT//2+15, walls,500)
                    clyde = ghost(ORANGE, 510, HEIGHT//2+15, walls,700)
                    ghosts = []
                    counter = 0
                #if pacman is out of lives then the game ends
                else:
                    win = False
                    endGame(win)
                    
        #pacman wins if he eats all of the dots
        if len(dots)==0:
            win = True
            endGame(win)
        pygame.display.update()
        counter+=1
        
        
playGame()

