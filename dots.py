
import pygame
import random
import sys
import math

pygame.init()

WIDTH = 500
HEIGHT = 650

WHITE = (255,255,255)
RED = (255,80,50)
BLUE = (100,150,255)
GREEN = (100,255,150)
YELLOW = (200,200,50)
PURPLE = (150,50,200)
BACKGROUND=WHITE
BLACK = (0,0,0)
GREY = (50,50,50)
LIGHTGREY = (150,150,150)
LIGHTESTGREY = (200,200,200)
NAVY = (30,30,150)
ICY = (230,230,255)

myFont =pygame.font.SysFont("monospace",25)
myFont1 =pygame.font.SysFont("monospace",120)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def endGame():
    pygame.quit()
    sys.exit()

def fillGrid(colorList):
    grid = []
    for r in range(11):
        grid.append([])
        for c in range(9):
            grid[r].append(random.choice(colorList))
    return grid

def isOnDot(mousePos, position, dotSize, spacing):
    dotPos = (position[1]*spacing+spacing, position[0]*spacing+spacing)
    if mousePos[0]>dotPos[0]-dotSize and mousePos[0]<dotPos[0]+dotSize and mousePos[1]>dotPos[1]-dotSize and dotPos[1]<dotPos[1]+dotSize:
        return True
    return False

def yaEstá(falling,dotR,c):
    for item in falling:
        if item[0]==dotR and item[1]==c:
            return True, item
    return False, None

def alreadyNew(falling,c):
    greatest = 1
    for ind in range(len(falling)):
        if falling[ind][0]<0 and c==falling[ind][1]:
            falling[ind][0]+=-1
            falling[ind][3]+=1
        if falling[ind][3]>greatest and c==falling[ind][1]:
            greatest = falling[ind][3]
    for i in range(len(falling)):
        if falling[ind][0]<0 and c==falling[ind][1]:
            falling[ind][3]=greatest
    return falling, greatest

def drawDots(grid, dotSize, spacing):
    pass

def removeDots(grid, toRemove, spacing, colors, dotSize, colorList, countAnc, enableAnc, moves, countNest,enableNest,numNest,numAnc,iceLoc,countGem,numGem,iceLen):
    falling = []
    alreadyRemoved =[]
    nesting = ["nesting1","nesting2","nesting3"]
    
    for i in range(len(iceLoc)-1,-1,-1):
        if i<0:
            break
        if (iceLoc[i][0],iceLoc[i][1]) in toRemove and grid[iceLoc[i][0]][iceLoc[i][1]]!="anchor":
            iceLoc[i][2]+=1
            ##print(grid[iceLoc[i][0]][iceLoc[i][1]])
        if iceLoc[i][2]>=3:
            iceLoc.remove([iceLoc[i][0],iceLoc[i][1], iceLoc[i][2]])
    for removable in toRemove:
        r = removable[0]
        c = removable[1]
       ## print(grid[r][c])
        if grid[r][c] in nesting or grid[r][c]=="bomb":
            toRemove.remove(removable)
    for removable in toRemove:
        r = removable[0]
        c = removable[1]
        if grid[r][c]=="anchor":
            countAnc+=1
        if (r,c) not in alreadyRemoved:
            falling, greatest = alreadyNew(falling, c)
            falling.append([-1,c,random.choice(colorList),greatest])
            for dotR in range(len(grid)):
                if dotR<r:
                    ya, item = yaEstá(falling,dotR,c)
                    if not ya and ((dotR,c) not in toRemove or grid[dotR][c]=="bomb" or grid[r][c] in nesting) and grid[dotR][c]!="":
                        falling.append([dotR,c,grid[dotR][c],1])
                        grid[dotR][c]=""
                    elif ya and (dotR,c):
                        falling.remove(item)
                        item[3]+=1
                        falling.append(item)
            alreadyRemoved.append((r,c))
        grid[r][c]=""
    
             
    for i in range(51):
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND)
        for ice in iceLoc:
            pygame.draw.rect(screen,ICY,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-dotSize*2, dotSize*4,dotSize*4))

        #really elaborately draws each dot
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col]!="" and grid[row][col]!="clear" and grid[row][col]!="anchor" and grid[row][col] not in nesting and grid[row][col].find("gem")==-1:
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize)
                elif grid[row][col]=="clear":
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize,1)
                elif grid[row][col]=="anchor":
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.circle(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-4),2)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-2),(col*spacing+spacing,row*spacing+spacing+7),1)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing-3,row*spacing+spacing),(col*spacing+spacing+3,row*spacing+spacing),1)                   
                    pygame.draw.arc(screen,WHITE,(col*spacing+spacing-7,row*spacing+spacing-7,14,14),math.pi,math.pi*2,1)
                elif grid[row][col]=="nesting3":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize, dotSize*2,dotSize*2),math.pi,math.pi*2,dotSize)
                elif grid[row][col]=="nesting2":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*4)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*4)//5,row*spacing+spacing-(dotSize*4)//5, (dotSize*4)//5*2,(dotSize*4)//5*2),math.pi,math.pi*2,(dotSize*4)//5)
                elif grid[row][col]=="nesting1":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*3)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*3)//5,row*spacing+spacing-(dotSize*3)//5, (dotSize*3)//5*2,(dotSize*3)//5*2),math.pi,math.pi*2,(dotSize*3)//5)
                elif grid[row][col].find("gem1")>-1: 
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize*3/2, dotSize*3,dotSize*3))
                elif grid[row][col].find("gem2")>-1:
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize, dotSize*3,dotSize*2))
                elif grid[row][col].find("gem3")>-1:
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize*3/2, dotSize*2,dotSize*3))

        #draws dots while falling
        for fall in falling:
            if fall!="":
                if fall[2]!="clear" and fall[2]!="anchor" and fall[2]  not in nesting and fall[2].find("gem")<0:
                    pygame.draw.circle(screen,colors[fall[2]],(fall[1]*spacing+spacing,fall[0]*spacing+spacing+i*fall[3]),dotSize)
                elif fall[2]=="clear":
                    pygame.draw.circle(screen,colors[fall[2]],(fall[1]*spacing+spacing,fall[0]*spacing+spacing+i*fall[3]),dotSize,1)
                elif fall[2]=="anchor":
                    pygame.draw.circle(screen,colors[fall[2]],(fall[1]*spacing+spacing,fall[0]*spacing+spacing+i*fall[3]),dotSize)
                    pygame.draw.circle(screen,WHITE,(fall[1]*spacing+spacing,fall[0]*spacing+spacing-4+i*fall[3]),2)
                    pygame.draw.line(screen,WHITE,(fall[1]*spacing+spacing,fall[0]*spacing+spacing-2+i*fall[3]),(fall[1]*spacing+spacing,fall[0]*spacing+spacing+7+i*fall[3]),1)
                    pygame.draw.line(screen,WHITE,(fall[1]*spacing+spacing-3,fall[0]*spacing+spacing+i*fall[3]),(fall[1]*spacing+spacing+3,fall[0]*spacing+spacing+i*fall[3]),1)                   
                    pygame.draw.arc(screen,WHITE,(fall[1]*spacing+spacing-7,fall[0]*spacing+spacing-7+i*fall[3],14,14),math.pi,math.pi*2,1)
                elif fall[2]=="nesting3":
                    pygame.draw.circle(screen,LIGHTGREY,(fall[1]*spacing+spacing,fall[0]*spacing+spacing+i*fall[3]),dotSize)
                    pygame.draw.arc(screen,LIGHTESTGREY,(fall[1]*spacing+spacing-dotSize,fall[0]*spacing+spacing-dotSize+i*fall[3], dotSize*2,dotSize*2),math.pi,math.pi*2,dotSize)
                elif fall[2]=="nesting2":
                    pygame.draw.circle(screen,LIGHTGREY,(fall[1]*spacing+spacing,fall[0]*spacing+spacing+i*fall[3]),(dotSize*4)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(fall[1]*spacing+spacing-(dotSize*4)//5,fall[0]*spacing+spacing-(dotSize*4)//5+i*fall[3], (dotSize*4)//5*2,(dotSize*4)//5*2),math.pi,math.pi*2,(dotSize*4)//5)
                elif fall[2]=="nesting1":
                    pygame.draw.circle(screen,LIGHTGREY,(fall[1]*spacing+spacing,fall[0]*spacing+spacing+i*fall[3]),(dotSize*3)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(fall[1]*spacing+spacing-(dotSize*3)//5,fall[0]*spacing+spacing-(dotSize*3)//5+i*fall[3], (dotSize*3)//5*2,(dotSize*3)//5*2),math.pi,math.pi*2,(dotSize*3)//5)
                elif fall[2].find("gem1")>-1: 
                    pygame.draw.rect(screen,colors[fall[2][:-4]],(fall[1]*spacing+spacing-dotSize*3/2,fall[0]*spacing+spacing-dotSize*3/2+i*fall[3], dotSize*3,dotSize*3))
                elif fall[2].find("gem2")>-1:
                    pygame.draw.rect(screen,colors[fall[2][:-4]],(fall[1]*spacing+spacing-dotSize*3/2,fall[0]*spacing+spacing-dotSize+i*fall[3], dotSize*3,dotSize*2))
                elif fall[2].find("gem3")>-1:
                    pygame.draw.rect(screen,colors[fall[2][:-4]],(fall[1]*spacing+spacing-dotSize,fall[0]*spacing+spacing-dotSize*3/2+i*fall[3], dotSize*2,dotSize*3))

        #draws ice over dots
        for ice in iceLoc:
            if ice[2]>0:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-2),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+13,ice[0]*spacing+spacing+1),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-3,ice[0]*spacing+spacing+4),(ice[1]*spacing+spacing+4,ice[0]*spacing+spacing+11),1)
            if ice[2]>1:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+dotSize*2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+6,ice[0]*spacing+spacing-dotSize*2),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)

        #tells you how many of things you need to win
        label = myFont.render("Moves: "+str(moves), 1, GREY)
        screen.blit(label,(40, HEIGHT-50))
        if enableAnc and numAnc>0:
            label1 = myFont.render("Anchors: "+str(countAnc)+"/"+str(numAnc), 1, GREY)
            screen.blit(label1,(140, HEIGHT-50))
        if enableNest and numNest>0:
            label2 = myFont.render("Nesting Dots: "+str(countNest)+"/"+str(numNest), 1, GREY)
            screen.blit(label2,(260, HEIGHT-50))
        if numGem>0:
            label3 = myFont.render("Gems: "+str(countGem)+"/"+str(numGem), 1, GREY)
            screen.blit(label3,(140, HEIGHT-25))
        if iceLen>0:
            label4 = myFont.render("Ice: "+str(iceLen-len(iceLoc))+"/"+str(iceLen), 1, GREY)
            screen.blit(label4,(240, HEIGHT-25))
        pygame.display.update()
        pygame.time.delay(5)
        
    for fallen in falling:
        grid[fallen[0]+fallen[3]][fallen[1]] = fallen[2]
    bombs=[]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col]=="":
                grid[row][col] = random.choice(colorList)
            if grid[row][col]=="bomb":
                bombs.append((row,col))
    
    return bombs, countAnc, iceLoc

def makeBombs(selected, grid):
    square = selected[selected.index(selected[-1]):]
    bombs = []
    ##print(square)
    if len(square)>7:
        length = len(square)-1
        for dotI in range(length):
            if square[dotI][0]==square[dotI+1][0]:
                square.append((square[dotI][0], (square[dotI][1]+square[dotI+1][1])/2))
            if square[dotI][1]==square[dotI+1][1]:
                square.append(((square[dotI][0]+square[dotI+1][0])/2,square[dotI][1]))
        topLeft=(20,20)
        botRight=(0,0)
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                count0=[]
                count1=[]
                count2=[]
                count3=[]
                if (row,col) not in square:
                    for point in square[1:]:
                        if row<point[0] and col==point[1]:
                            count0.append(point)
                        elif row>point[0] and col==point[1]:
                            count1.append(point)
                        elif col>point[1] and row==point[0]:
                            count2.append(point)
                        elif col<point[1] and row==point[0]:
                            count3.append(point)
                if len(count0)%2==1 and len(count1)%2==1 and len(count2)%2==1 and len(count3)%2==1:
                    bombs.append((row,col))
    return bombs

def boom(bombs,grid,colors,spacing,dotSize, enableAnc, moves, countAnc,countNest, enableNest,numNest,numAnc,iceLoc,countGem,numGem,iceLen):
    toRemove=[]
    nesting = ["nesting1","nesting2","nesting3"]
    for i in range(20):
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND)
        for ice in iceLoc:
            pygame.draw.rect(screen,ICY,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-dotSize*2, dotSize*4,dotSize*4))
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col]!="" and grid[row][col]!="clear" and grid[row][col]!="anchor" and grid[row][col] not in nesting and grid[row][col].find("gem")==-1:
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize)
                elif grid[row][col]=="clear":
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize,1)
                elif grid[row][col]=="anchor":
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.circle(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-4),2)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-2),(col*spacing+spacing,row*spacing+spacing+7),1)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing-3,row*spacing+spacing),(col*spacing+spacing+3,row*spacing+spacing),1)                   
                    pygame.draw.arc(screen,WHITE,(col*spacing+spacing-7,row*spacing+spacing-7,14,14),math.pi,math.pi*2,1)
                elif grid[row][col]=="nesting3":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize, dotSize*2,dotSize*2),math.pi,math.pi*2,dotSize)
                elif grid[row][col]=="nesting2":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*4)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*4)//5,row*spacing+spacing-(dotSize*4)//5, (dotSize*4)//5*2,(dotSize*4)//5*2),math.pi,math.pi*2,(dotSize*4)//5)
                elif grid[row][col]=="nesting1":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*3)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*3)//5,row*spacing+spacing-(dotSize*3)//5, (dotSize*3)//5*2,(dotSize*3)//5*2),math.pi,math.pi*2,(dotSize*3)//5)
                elif grid[row][col].find("gem1")>-1: 
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize*3/2, dotSize*3,dotSize*3))
                elif grid[row][col].find("gem2")>-1:
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize, dotSize*3,dotSize*2))
                elif grid[row][col].find("gem3")>-1:
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize*3/2, dotSize*2,dotSize*3))
        for ice in iceLoc:
            if ice[2]>0:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-2),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+13,ice[0]*spacing+spacing+1),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-3,ice[0]*spacing+spacing+4),(ice[1]*spacing+spacing+4,ice[0]*spacing+spacing+11),1)
            if ice[2]>1:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+dotSize*2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+6,ice[0]*spacing+spacing-dotSize*2),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
        for bomb in bombs:
            if i==0:
                for a in range(-1,2):
                    for b in range(-1,2):
                        if bomb[0]+a in range(len(grid)) and bomb[1]+b in range(len(grid[0])):
                            if grid[bomb[0]+a][bomb[1]+b] in nesting and not(a==0 and b==0):
                                toRemove.append((bomb[0]+a,bomb[1]+b))
                                if grid[bomb[0]+a][bomb[1]+b]=="nesting3":
                                    grid[bomb[0]+a][bomb[1]+b]="nesting2"
                                elif grid[bomb[0]+a][bomb[1]+b]=="nesting2":
                                    grid[bomb[0]+a][bomb[1]+b]="nesting1"
                                elif grid[bomb[0]+a][bomb[1]+b]=="nesting1":
                                    grid[bomb[0]+a][bomb[1]+b]="bomb"
                                    countNest+=1
                            else:
                                toRemove.append((bomb[0]+a,bomb[1]+b))
                grid[bomb[0]][bomb[1]]="bombE"
            for p in range(-1,2):
                for q in range(-1,2):
                    pygame.draw.line(screen, GREY,(bomb[1]*spacing+spacing+15*p,bomb[0]*spacing+spacing+15*q),(bomb[1]*spacing+spacing+(15+i)*p,bomb[0]*spacing+spacing+(15+i)*q),2)
        label = myFont.render("Moves: "+str(moves), 1, GREY)
        screen.blit(label,(40, HEIGHT-50))
        if enableAnc and numAnc>0:
            label1 = myFont.render("Anchors: "+str(countAnc)+"/"+str(numAnc), 1, GREY)
            screen.blit(label1,(140, HEIGHT-50))
        if enableNest and numNest>0:
            label2 = myFont.render("Nesting Dots: "+str(countNest)+"/"+str(numNest), 1, GREY)
            screen.blit(label2,(260, HEIGHT-50))
        if numGem>0:
            label3 = myFont.render("Gems: "+str(countGem)+"/"+str(numGem), 1, GREY)
            screen.blit(label3,(140, HEIGHT-25))
        if iceLen>0:
            label4 = myFont.render("Ice: "+str(iceLen-len(iceLoc))+"/"+str(iceLen), 1, GREY)
            screen.blit(label4,(240, HEIGHT-25))
        pygame.display.update()
        ##if i%2==0:
            ##pygame.time.delay(1)
    return toRemove, countNest

def gemExp(grid,colors,spacing,dotSize, enableAnc, moves, countAnc,countNest, enableNest,numNest,numAnc,iceLoc, gemsExpd, selected,countGem,numGem,iceLen):
    nesting = ["nesting1","nesting2","nesting3"]
    again = False
    for i in range(50):
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND)
        for gem in gemsExpd:
            maxi = 0
            for i in gem[3]:
                if i>maxi and i<=200:
                    maxi=i
            mult = 240/maxi
            r = gem[3][0]*mult
            g = gem[3][1]*mult
            b = gem[3][2]*mult
            if r>255:
                r = 255
            if b>255:
                b=255
            if g>255:
                g=255
            color = (r,g,b)
            if gem[2]==2 or gem[2]==1:
                pygame.draw.rect(screen,color,(0,gem[0]*spacing+spacing-dotSize, WIDTH,dotSize*2))
                row = gem[0]
                for c in range(len(grid[row])):
                    if (row,c) not in selected:
                        selected.append((row,c))
                    #if (row,c) not in selected and grid[row][c]=="anchor":
                        #countAnc+=1
                    if grid[row][c].find("gem")>-1 and [row,c,int(grid[row][c][-1]), colors[grid[row][c][:-4]]] not in gemsExpd:
                        again=True
            if gem[2]==3 or gem[2]==1:
                pygame.draw.rect(screen,color,(gem[1]*spacing+spacing-dotSize,0, dotSize*2, HEIGHT))
                c = gem[1]
                for row in range(len(grid)):
                    if (row,c) not in selected:
                        selected.append((row,c))
                    #if (row,c) not in selected and grid[row][c]=="anchor":
                        #countAnc+=1
                    if grid[row][c].find("gem")>-1 and [row,c,int(grid[row][c][-1]), colors[grid[row][c][:-4]]] not in gemsExpd:
                        again=True
        for ice in iceLoc:
            pygame.draw.rect(screen,ICY,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-dotSize*2, dotSize*4,dotSize*4))
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col]!="" and grid[row][col]!="clear" and grid[row][col]!="anchor" and grid[row][col] not in nesting and grid[row][col].find("gem")==-1:
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize)
                elif grid[row][col]=="clear":
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize,1)
                elif grid[row][col]=="anchor":
                    pygame.draw.circle(screen,colors[grid[row][col]],(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.circle(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-4),2)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-2),(col*spacing+spacing,row*spacing+spacing+7),1)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing-3,row*spacing+spacing),(col*spacing+spacing+3,row*spacing+spacing),1)                   
                    pygame.draw.arc(screen,WHITE,(col*spacing+spacing-7,row*spacing+spacing-7,14,14),math.pi,math.pi*2,1)
                elif grid[row][col]=="nesting3":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize, dotSize*2,dotSize*2),math.pi,math.pi*2,dotSize)
                elif grid[row][col]=="nesting2":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*4)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*4)//5,row*spacing+spacing-(dotSize*4)//5, (dotSize*4)//5*2,(dotSize*4)//5*2),math.pi,math.pi*2,(dotSize*4)//5)
                elif grid[row][col]=="nesting1":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*3)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*3)//5,row*spacing+spacing-(dotSize*3)//5, (dotSize*3)//5*2,(dotSize*3)//5*2),math.pi,math.pi*2,(dotSize*3)//5)
                elif grid[row][col].find("gem1")>-1: 
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize*3/2, dotSize*3,dotSize*3))
                elif grid[row][col].find("gem2")>-1:
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize, dotSize*3,dotSize*2))
                elif grid[row][col].find("gem3")>-1:
                    pygame.draw.rect(screen,colors[grid[row][col][:-4]],(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize*3/2, dotSize*2,dotSize*3))
        for ice in iceLoc:
            if ice[2]>0:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-2),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+13,ice[0]*spacing+spacing+1),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-3,ice[0]*spacing+spacing+4),(ice[1]*spacing+spacing+4,ice[0]*spacing+spacing+11),1)
            if ice[2]>1:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+dotSize*2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+6,ice[0]*spacing+spacing-dotSize*2),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
        
            
        label = myFont.render("Moves: "+str(moves), 1, GREY)
        screen.blit(label,(40, HEIGHT-50))
        if enableAnc and numAnc>0:
            label1 = myFont.render("Anchors: "+str(countAnc)+"/"+str(numAnc), 1, GREY)
            screen.blit(label1,(140, HEIGHT-50))
        if enableNest and numNest>0:
            label2 = myFont.render("Nesting Dots: "+str(countNest)+"/"+str(numNest), 1, GREY)
            screen.blit(label2,(260, HEIGHT-50))
        if numGem>0:
            label3 = myFont.render("Gems: "+str(countGem)+"/"+str(numGem), 1, GREY)
            screen.blit(label3,(140, HEIGHT-25))
        if iceLen>0:
            label4 = myFont.render("Ice: "+str(iceLen-len(iceLoc))+"/"+str(iceLen), 1, GREY)
            screen.blit(label4,(240, HEIGHT-25))
        pygame.display.update()
        pygame.time.delay(1)

    return selected, again

def isOnButton(mousePos, buttonPos, buttonSize):
    if mousePos[0]>buttonPos[0] and mousePos[0]<buttonPos[0]+buttonSize and mousePos[1]>buttonPos[1] and mousePos[1]<buttonPos[1]+buttonSize:
        return True
    return False

def levelSelect():
    colorList = ["red","yellow","green","blue","purple"]
    spacing = 10
    size = 40
    colors = {
        "red": RED,
        "yellow":YELLOW,
        "green":GREEN,
        "blue": BLUE,
        "purple":PURPLE,
    }
    edges = [[0,0,0],[0,1,0],[0,2,0],[0,3,0],[0,4,0],[0,5,0],[0,6,0],[0,7,0],[0,8,0],[10,0,0],[10,1,0],[10,2,0],[10,3,0],[10,4,0],[10,5,0],[10,6,0],[10,7,0],[10,8,0],[1,0,0],[2,0,0],[3,0,0],[4,0,0],[5,0,0],[6,0,0],[7,0,0],[8,0,0],[9,0,0],[1,8,0],[2,8,0],[3,8,0],[4,8,0],[5,8,0],[6,8,0],[7,8,0],[8,8,0],[9,8,0]]
    midLine = [[5,0,0],[5,1,0],[5,2,0],[5,3,0],[5,4,0],[5,5,0],[5,6,0],[5,7,0],[5,8,0]]
    while True:
        screen.fill(BACKGROUND)
        mousePressed = False
        mousePos = pygame.mouse.get_pos()
        label1 = myFont1.render("TWO DOTS", 1, GREY)
        screen.blit(label1,((spacing+size)/2,(spacing+size)/2))
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                mousePressed=True
        for row in range(HEIGHT//50-3):
            for col in range(WIDTH//50-1):
                lev = col+(WIDTH//50-1)*row
                pygame.draw.rect(screen,colors[colorList[(row)%len(colorList)]],(col*(spacing+size)+(size+spacing)/2,row*(spacing+size)+(spacing+size)*5/2,size,size))
                label = myFont.render(str(lev+1), 1, WHITE)
                screen.blit(label,(col*(spacing+size)+spacing+(size+spacing)/2,row*(spacing+size)+spacing+(size+spacing)*5/2))
                if mousePressed and isOnButton(mousePos,(col*(spacing+size)+(size+spacing)/2,row*(spacing+size)+(spacing+size)*5/2),size):
                    level = lev+1
                    if level ==1:
                        playGame(25,False,0,True,5,False,0,[])
                    elif level ==2:
                        playGame(20,False,0,True,10,False,0,[])
                    elif level ==3:
                        playGame(30,False,0,False,0,False,0, edges)
                    elif level ==4:
                        playGame(20,False,0,True,5,False,0, edges)
                    elif level==5:
                        playGame(15,False,0,False,0,True,5,[])
                    elif level==6:
                        playGame(15,False,0,True,0,True,15,[])
                    elif level==7:
                        playGame(20,False,0,True,10,True,15,midLine)
                    elif level==8:
                        playGame(15,True,5,False,0,False,0,[])
                    elif level==9:
                        playGame(20,True,10,False,0,True,5,[])
        pygame.display.update()
                
        


def playGame(moves, enableAnc, numAnc, enableNest, numNest, enableGem, numGem, iceLoc):
    colors = {
        "red": RED,
        "yellow":YELLOW,
        "green":GREEN,
        "blue": BLUE,
        "purple":PURPLE,
        "clear": BLACK,
        "bomb": GREY,
        "bombE": GREY,
        "anchor":NAVY,
        "nesting3":LIGHTGREY,
        "nesting2":LIGHTGREY,
        "nesting1":LIGHTGREY
    }
    ##colorList = ["red","yellow","green","blue","purple","red","yellow","green","blue","purple","clear"]
    colorList = ["red","yellow","green","blue","purple"]
    colorList = colorList*10+["clear","clear"]
    grid = fillGrid(colorList)
    countAnc = 0
    #enableAnc = True
    countNest = 0
    #enableNest = True
    #moves = 20
    countGem = 0
    ##enableGem = True
    gameOver = False
    spacing = 50
    dotSize = 10
    drawing = False
    selected = []
    selectedColor = ""
    onDot = False
    square = False
    exploded=True
    nestingPos = []
    nesting = ["nesting1","nesting2","nesting3"]
    gems = []
    run = 0####
    iceLen = len(iceLoc)
    while not gameOver:
        bombs=[]
        colorList = ["red","yellow","green","blue","purple"]
        colorList = colorList*100
        if enableGem and run==0:
            for color in colorList[0:5]:
                gems=gems+[color+"gem1"]
                gems=gems+[color+"gem2"]
                gems=gems+[color+"gem3"]
            run+=1
        colorList+=gems
        colorList +=["clear"]*20
        if enableAnc:
            colorList +=["anchor"]*9
        if enableNest:
            colorList +=["nesting3"]*15
        
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0] and onDot and not drawing and onColor!="anchor" and onColor not in nesting and onColor not in gems:
                selected.append(onPos)
                selectedColor = grid[onPos[0]][onPos[1]]
                drawing = True
                square=False
            elif pygame.mouse.get_pressed()[0] and onDot and drawing and len(selected)>1 and onPos==selected[-1]:
                
                moves+=-1
                if square:
                    if selectedColor!="clear":
                        bombs = makeBombs(selected, grid)
                        exploded=False
                        for dot in bombs:
                            grid[dot[0]][dot[1]]="bomb"
                    for row in range(len(grid)):
                        for col in range(len(grid[row])):
                            if grid[row][col]==selectedColor or selectedColor=="clear" or grid[row][col][:-4]==selectedColor:
                                selected.append((row,col))
                    if selectedColor!="clear":
                        while selectedColor in colorList:
                            colorList.remove(selectedColor)
                if enableGem:
                    again = True
                    while again:
                        gemsExpd = []
                        again=False
                        for item in selected:
                            if grid[item[0]][item[1]] in gems:
                                gemsExpd.append([item[0],item[1],int(grid[item[0]][item[1]][-1]), colors[grid[item[0]][item[1]][:-4]]])
                        if len(gemsExpd)>0:
                            selected, again = gemExp(grid,colors,spacing,dotSize, enableAnc, moves, countAnc,countNest, enableNest,numNest,numAnc,iceLoc, gemsExpd, selected,countGem,numGem,iceLen)
                    countGem+=len(gemsExpd)
                if enableNest:
                    for row in range(len(grid)):
                        for col in range(len(grid[row])):
                            nest = (row,col)
                            if grid[nest[0]][nest[1]] in nesting:
                                # if dots around nesting are selected, nesting dot decreases in size
                                if  (nest[0]-1,nest[1]) in selected or (nest[0],nest[1]-1) in selected  or (nest[0]+1,nest[1]) in selected or (nest[0],nest[1]+1) in selected:
                                    if grid[nest[0]][nest[1]]=="nesting3":
                                        grid[nest[0]][nest[1]]="nesting2"
                                    elif grid[nest[0]][nest[1]]=="nesting2":
                                        grid[nest[0]][nest[1]]="nesting1"
                                    elif grid[nest[0]][nest[1]]=="nesting1":
                                        grid[nest[0]][nest[1]]="bomb"
                                        exploded=False
                                        bombs.append((nest[0],nest[1]))
                                        countNest+=1
                                    selected.append((nest[0],nest[1]))
                                #if nesting dot is selected, nesting decreases in size, but we also don't want it removed
                                elif (nest[0],nest[1]) in selected:
                                    if grid[nest[0]][nest[1]]=="nesting3":
                                        grid[nest[0]][nest[1]]="nesting2"
                                        selected.remove(nest)
                                    elif grid[nest[0]][nest[1]]=="nesting2":
                                        grid[nest[0]][nest[1]]="nesting1"
                                        selected.remove(nest)
                                    elif grid[nest[0]][nest[1]]=="nesting1":
                                        grid[nest[0]][nest[1]]="bomb"
                                        exploded=False
                                        bombs.append((nest[0],nest[1]))
                                        countNest+=1
                bombs, countAnc, iceLoc = removeDots(grid, selected, spacing, colors, dotSize, colorList, countAnc, enableAnc, moves, countNest, enableNest,numNest,numAnc, iceLoc,countGem,numGem,iceLen)
        
                selected = []
                selectedColor = ""
                drawing = False
                square = False
            elif pygame.mouse.get_pressed()[0]:
                selected = []
                selectedColor = ""
                drawing = False
                square = False
        onDot=False
        if enableAnc:
            anchors = ["placeholder"]
            while anchors!=[]:
                if "placeholder" in anchors:
                    anchors.remove("placeholder")
                if anchors!=[]:
                    bombs, countAnc, iceLoc = removeDots(grid,anchors,spacing,colors,dotSize,colorList, countAnc, enableAnc, moves, countNest, enableNest,numNest,numAnc, iceLoc,countGem,numGem,iceLen)
                anchors = []
                row = len(grid)-1
                for col in range(len(grid[row])):
                    if grid[row][col]=="anchor":
                        anchors.append((row,col))
        for ice in iceLoc:
            pygame.draw.rect(screen,ICY,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-dotSize*2, dotSize*4,dotSize*4))
            
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                color = grid[row][col]
                if color!="clear" and color!="anchor" and color not in nesting and color not in gems:
                    pygame.draw.circle(screen,colors[color],(col*spacing+spacing,row*spacing+spacing),dotSize)
                elif color=="clear" and (row,col) in selected:
                    pygame.draw.circle(screen,colors[selectedColor],(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.circle(screen,colors[color],(col*spacing+spacing,row*spacing+spacing),dotSize,1)
                elif color=="clear":
                    pygame.draw.circle(screen,colors[color],(col*spacing+spacing,row*spacing+spacing),dotSize,1)
                elif color=="anchor":
                    pygame.draw.circle(screen,colors[color],(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.circle(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-4),2)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing,row*spacing+spacing-2),(col*spacing+spacing,row*spacing+spacing+7),1)
                    pygame.draw.line(screen,WHITE,(col*spacing+spacing-3,row*spacing+spacing),(col*spacing+spacing+3,row*spacing+spacing),1)                   
                    pygame.draw.arc(screen,WHITE,(col*spacing+spacing-7,row*spacing+spacing-7,14,14),math.pi,math.pi*2,1)
                elif color=="nesting3":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),dotSize)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize, dotSize*2,dotSize*2),math.pi,math.pi*2,dotSize)
                elif color=="nesting2":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*4)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*4)//5,row*spacing+spacing-(dotSize*4)//5, (dotSize*4)//5*2,(dotSize*4)//5*2),math.pi,math.pi*2,(dotSize*4)//5)
                elif color=="nesting1":
                    pygame.draw.circle(screen,LIGHTGREY,(col*spacing+spacing,row*spacing+spacing),(dotSize*3)//5)
                    pygame.draw.arc(screen,LIGHTESTGREY,(col*spacing+spacing-(dotSize*3)//5,row*spacing+spacing-(dotSize*3)//5, (dotSize*3)//5*2,(dotSize*3)//5*2),math.pi,math.pi*2,(dotSize*3)//5)
                ## gem1 explodes both ways, gem2 is horizontal, gem3 is vertical
                elif color.find("gem1")>-1: 
                    pygame.draw.rect(screen,colors[color[:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize*3/2, dotSize*3,dotSize*3))
                elif color.find("gem2")>-1:
                    pygame.draw.rect(screen,colors[color[:-4]],(col*spacing+spacing-dotSize*3/2,row*spacing+spacing-dotSize, dotSize*3,dotSize*2))
                elif color.find("gem3")>-1:
                    pygame.draw.rect(screen,colors[color[:-4]],(col*spacing+spacing-dotSize,row*spacing+spacing-dotSize*3/2, dotSize*2,dotSize*3))
                if isOnDot(pygame.mouse.get_pos(),(row,col),dotSize, spacing):
                    onDot=True
                    onPos = (row,col)
                    onColor = grid[row][col]
        for ice in iceLoc:
            if ice[2]>0:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-dotSize*2,ice[0]*spacing+spacing-2),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+13,ice[0]*spacing+spacing+1),(ice[1]*spacing+spacing,ice[0]*spacing+spacing+5),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing-3,ice[0]*spacing+spacing+4),(ice[1]*spacing+spacing+4,ice[0]*spacing+spacing+11),1)
            if ice[2]>1:
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+dotSize*2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+2,ice[0]*spacing+spacing-7),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                pygame.draw.line(screen,WHITE,(ice[1]*spacing+spacing+6,ice[0]*spacing+spacing-dotSize*2),(ice[1]*spacing+spacing+12,ice[0]*spacing+spacing-8),1)
                
        ##if not exploded and len(bombs)>0:
        while len(bombs)>0:
            toRemove, countNest = boom(bombs, grid, colors, spacing, dotSize, enableAnc, moves, countAnc, countNest, enableNest,numNest,numAnc,iceLoc,countGem,numGem,iceLen)
            if enableGem:
                again = True
                length = 0
                while again:
                    again=False
                    gemsExpd = []
                    for item in toRemove:
                        if grid[item[0]][item[1]] in gems:
                            gemsExpd.append([item[0],item[1],int(grid[item[0]][item[1]][-1]), colors[grid[item[0]][item[1]][:-4]]])
                        if len(gemsExpd)>length:
                            toRemove, again = gemExp(grid,colors,spacing,dotSize, enableAnc, moves, countAnc,countNest, enableNest,numNest,numAnc,iceLoc, gemsExpd, toRemove,countGem,numGem,iceLen)
                        length = len(gemsExpd)
                    countGem+=length
                if enableNest:
                    for row in range(len(grid)):
                        for col in range(len(grid[row])):
                            nest = (row,col)
                            if (nest[0],nest[1]) in toRemove:
                                if grid[nest[0]][nest[1]]=="nesting3":
                                    grid[nest[0]][nest[1]]="nesting2"
                                    toRemove.remove(nest)
                                elif grid[nest[0]][nest[1]]=="nesting2":
                                    grid[nest[0]][nest[1]]="nesting1"
                                    toRemove.remove(nest)
                                elif grid[nest[0]][nest[1]]=="nesting1":
                                    grid[nest[0]][nest[1]]="bomb"
                                    bombs.append((nest[0],nest[1]))
                                    countNest+=1
            bombs, countAnc, iceLoc = removeDots(grid, toRemove, spacing, colors, dotSize, colorList, countAnc, enableAnc, moves,countNest,enableNest,numNest,numAnc, iceLoc,countGem,numGem,iceLen)
            exploded=True
        if drawing:
            if onDot and not square:
                if len(selected)<=3:
                    if onPos not in selected[-len(selected):] and ((onPos[0]==selected[-1][0] and abs(onPos[1]-selected[-1][1])==1) or (onPos[1]==selected[-1][1] and abs(onPos[0]-selected[-1][0])==1)) and (onColor=="clear" or selectedColor==onColor or selectedColor=="clear") and onColor!="anchor":
                        selected.append(onPos)
                        if selectedColor =="clear":
                            selectedColor = onColor
                else:
                    if onPos not in selected[-3:] and ((onPos[0]==selected[-1][0] and abs(onPos[1]-selected[-1][1])==1) or (onPos[1]==selected[-1][1]  and abs(onPos[0]-selected[-1][0])==1)) and (onColor=="clear" or selectedColor==onColor or selectedColor=="clear") and onColor!="anchor":
                        if onPos in selected:
                            square = True
                        if selectedColor =="clear":
                            selectedColor = onColor
                        selected.append(onPos)
            for point in range(len(selected)-1):
                point1 = (selected[point][1]*spacing+spacing,selected[point][0]*spacing+spacing)
                point2 = (selected[point+1][1]*spacing+spacing,selected[point+1][0]*spacing+spacing)
                pygame.draw.line(screen, colors[selectedColor],point1,point2,5)
            if not square:
                pygame.draw.line(screen, colors[selectedColor],(selected[-1][1]*spacing+spacing,selected[-1][0]*spacing+spacing),pygame.mouse.get_pos(),5)
        label = myFont.render("Moves: "+str(moves), 1, GREY)
        screen.blit(label,(40, HEIGHT-50))
        if enableAnc and numAnc>0:
            label1 = myFont.render("Anchors: "+str(countAnc)+"/"+str(numAnc), 1, GREY)
            screen.blit(label1,(140, HEIGHT-50))
        if enableNest and numNest>0:
            label2 = myFont.render("Nesting Dots: "+str(countNest)+"/"+str(numNest), 1, GREY)
            screen.blit(label2,(260, HEIGHT-50))
        if enableGem and numGem>0:
            label3 = myFont.render("Gems: "+str(countGem)+"/"+str(numGem), 1, GREY)
            screen.blit(label3,(140, HEIGHT-25))
        if iceLen>0:
            label4 = myFont.render("Ice: "+str(iceLen-len(iceLoc))+"/"+str(iceLen), 1, GREY)
            screen.blit(label4,(240, HEIGHT-25))
        if moves==0 or (countNest>=numNest and countAnc>=numAnc and len(iceLoc)==0 and countGem>=numGem):
            gameOver=True
            levelSelect()
        pygame.display.update()


levelSelect()
playGame(200, False,0, True, 200,True,10,[])
playGame(30, True, 5, True, 5, True,10,[[0,0,0],[0,1,0],[0,2,0],[0,3,0],[0,4,0],[0,5,0],[0,6,0],[0,7,0],[0,8,0]])
playGame(20, True, 7, True, 7,False,0, [])


                
