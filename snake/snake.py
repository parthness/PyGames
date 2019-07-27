__author__ = 'Parth'
import pygame,time,random,cx_Freeze

pygame.init()
white=(255,255,255)
black=(0,0,0)
green=(0,155,0)
red=(255,0,0)
display_width=800
display_height=600
AppleThickness=30
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake')
icon=pygame.image.load('apple.png')
pygame.display.set_icon(icon)
clock=pygame.time.Clock()
gameExit=False
block_size=20
FPS=10
smallfont=pygame.font.SysFont("comicsansms",25) # ==> (nameoffont,size)
medfont=pygame.font.SysFont("comicsansms",40)
largefont=pygame.font.SysFont("comicsansms",63)

img=pygame.image.load('snakehead.png')
appleimg=pygame.image.load('apple.png')
direction="right"

def pause():

    paused=True

    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    paused=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message("Paused",red,-100,"large")
        message("Press Space to continue and q to quit",green,50,"medium")

        pygame.display.update()
        clock.tick(5)


def score(score):
    textSurf,textRect=text_objects("Score : "+str(score),black,"small")
    gameDisplay.blit(textSurf,textRect)

def randAppleGen():
    randAppleX=round(random.randrange(0,display_width-AppleThickness))#/10.0)*10.0
    randAppleY=round(random.randrange(0,display_height-AppleThickness))#/10.0)*10.0
    return randAppleX,randAppleY

def gameIntro():
    intro=True

    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)

        message("Welcome to Snake",green,-100,"large")
        message("The objective is to eat red apples",black,-30)
        message("More apples you eat,longer you get",black,10)
        message("If you run into yourself,or the edges,you die",black,50)
        message("Press c to continue , space to pause and q to quit",black,180)

        pygame.display.update()
        clock.tick(FPS)

def snake(block_size,snakeList):
    if direction=="right":
        head=pygame.transform.rotate(img,270)
    if direction=="left":
        head=pygame.transform.rotate(img,90)
    if direction=="up":
        head=img
    if direction=="down":
        head=pygame.transform.rotate(img,180)
    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],block_size,block_size])

def text_objects(msg,color,size):
    if size=="small":
        textSurf=smallfont.render(msg,True,color)
    elif size=="medium":
        textSurf=medfont.render(msg,True,color)
    elif size=="large":
        textSurf=largefont.render(msg,True,color)
    return textSurf,textSurf.get_rect()

def message(msg,color,y_displace=0,size="small"):
    textSurf,textRect = text_objects(msg,color,size)
    #screen_text=font.render(msg,True,color)
    #gameDisplay.blit(screen_text,[display_width/2,display_height/2])
    textRect.center=(display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def gameLoop():
    global direction,gameDisplay
    direction="right"
    gameExit=False
    gameOver=False

    lead_x=display_width/2
    lead_y=display_height/2
    lead_x_change=10
    lead_y_change=0
    snakeList=[]
    snakeLength=1

    randAppleX,randAppleY=randAppleGen()
    while not gameExit:
        while gameOver:
            gameDisplay.fill(white)
            message("Game Over",red,-50,"large")
            message("Press C to play again and q to Quit",black,50,"medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    gameOver=False
                    gameExit=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        gameOver=False
                        gameExit=True
                    if event.key==pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    direction="left"
                    lead_x_change=-block_size
                    lead_y_change=0
                elif event.key==pygame.K_RIGHT:
                    direction="right"
                    lead_x_change=block_size
                    lead_y_change=0
                elif event.key==pygame.K_UP:
                    direction="up"
                    lead_x_change=0
                    lead_y_change=-block_size
                elif event.key==pygame.K_DOWN:
                    direction="down"
                    lead_x_change=0
                    lead_y_change=block_size
                elif event.key==pygame.K_SPACE:
                    pause()

        if lead_x>=display_width or lead_x<0 or lead_y>=display_height or lead_y<0 or lead_x+block_size>display_width or lead_y+block_size>display_height: #lead_x and lead_y are top left corner of rectangle so we put >= for upper limits
            gameOver=True

        lead_x+=lead_x_change
        lead_y+=lead_y_change
        snakeHead=[]
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        gameDisplay.fill(white)
        #pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness])
        gameDisplay.blit(appleimg,(randAppleX,randAppleY))
        for eachSegment in snakeList[:-1]:
            if eachSegment==snakeHead:
                gameOver=True

        snake(block_size,snakeList)
        score(snakeLength-1)
        #gameDisplay.fill(red,rect=[100,100,30,30])
        pygame.display.update()

        if lead_x>randAppleX and lead_x<randAppleX+AppleThickness or lead_x+block_size>randAppleX and lead_x+block_size<randAppleX+AppleThickness:
            if lead_y>randAppleY and lead_y<randAppleY+AppleThickness or lead_y+block_size>randAppleY and lead_y+block_size<randAppleY+AppleThickness:
                randAppleX,randAppleY=randAppleGen()
                snakeLength+=1

        clock.tick(FPS) #we are moving 15 frames per second




   # message("You lose ghonchu",red)
    gameDisplay.fill(white)
    pygame.display.update()
   # time.sleep(1)
    pygame.quit()
    quit()

gameIntro()
gameLoop()
