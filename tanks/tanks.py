__author__ = 'Parth'
import pygame,time,random

pygame.init()
white=(255,255,255)
black=(0,0,0)
green=(0,155,0)
light_green=(0,255,0)
yellow=(200,200,0)
light_yellow=(255,255,0)
red=(155,0,0)
light_red=(255,0,0)
blue=(0,0,255)
display_width=800
display_height=600

boom=pygame.mixer.Sound("boom.wav")
tankWidth=40
tankHeight=20
turretWidth=5
wheelWidth=5
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Just for Nishu')
gameControls=0
intro=0
clock=pygame.time.Clock()
gameExit=False

FPS=20
smallfont=pygame.font.SysFont("comicsansms",25) # ==> (nameoffont,size)
medfont=pygame.font.SysFont("comicsansms",40)
largefont=pygame.font.SysFont("comicsansms",63)

def score(score):
    textSurf,textRect=text_objects("Score : "+str(score),black,"small")
    gameDisplay.blit(textSurf,textRect)

def button(text,x,y,width,height,inactive_color,active_color,action=None):
    global gameControls,intro
    cur=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+width>cur[0]>x and y+height>cur[1]>y:
        pygame.draw.rect(gameDisplay,active_color,(x,y,width,height))
        if click[0]==1 and action!=None:
            if action=="quit":
                gameControls=0
                intro=0
                pygame.quit()
                quit()
            if action=="controls":
                gameControls=0
                intro=1
                game_controls()
            if action=="main":
                gameControls=1
                intro=0
                gameIntro()
            if action=="play":
                gameControls=0
                intro=0
                gameLoop()
    else:
        pygame.draw.rect(gameDisplay,inactive_color,(x,y,width,height))
    text_to_button(text,black,x,y,width,height)

def pause():

    paused=True
    message("Paused",red,-100,"large")
    message("Press Space to continue and q to quit",green,50,"medium")
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

        #gameDisplay.fill(white)

        pygame.display.update()
        clock.tick(5)

def barrier(xlocation,randomHeight,barrier_width):
    pygame.draw.rect(gameDisplay,black,[xlocation,display_height-randomHeight,barrier_width,randomHeight])


def game_controls():
 #   global gameControls
    gcont=True
    gameDisplay.fill(white)
    message("Controls",green,-200,"large")
    message("Fire : Spacebar",black,-110)
    message("Move Turret : Up and Down arrows",black,-70)
    message("Move Tank : Left and Right arrows",black,-20)
    message("Pause : p",black,20)
    message("Power up : a",black,70)
    message("Power down : d",black,120)
    while gcont:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

     #   gameDisplay.fill(white)

     #   message("Press c to continue , space to pause and q to quit",black,180)
        cur=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        button("play",150,450,100,50,green,light_green,"play")
      #  button("main",350,450,100,50,yellow,light_yellow,"main")
        button("quit",550,450,100,50,red,light_red,"quit")

        pygame.display.update()
        clock.tick(FPS)

def gameIntro():
    global intro
    gintro=True
    gameDisplay.fill(white)
    message("Welcome to Tanks",green,-200,"large")
    message("The objective is to shoot and destroy",black,-80)
    message("the enemy tank before they destroy you.",black,-30)
    message("More enemies you destroy,harder you get.",black,20)
    while gintro:
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

        #gameDisplay.fill(white)

     #   message("Press c to continue , space to pause and q to quit",black,180)
        cur=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        button("play",150,450,100,50,green,light_green,"play")
        button("controls",350,450,100,50,yellow,light_yellow,"controls")
        button("quit",550,450,100,50,red,light_red,"quit")
   #     if intro==1:
   #         return
        pygame.display.update()
        clock.tick(FPS)

def game_Over(str,str1,color):
    over=True
    gameDisplay.fill(white)
    message(str,color,-200,"large")
    message(str1,black,-80)
    while over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)

     #   message("Press c to continue , space to pause and q to quit",black,180)
        cur=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        button("play again",150,450,150,50,green,light_green,"play")
        button("controls",350,450,100,50,yellow,light_yellow,"controls")
        button("quit",550,450,100,50,red,light_red,"quit")
   #     if intro==1:
   #         return
        pygame.display.update()
        clock.tick(FPS)

def tank(x,y,turPos):
    x=int(x)
    y=int(y)

    possibleTurrets=[(x-27,y-2),
                    (x-26,y-5),
                    (x-25,y-8),
                    (x-23,y-12),
                    (x-20,y-14),
                    (x-18,y-15),
                    (x-15,y-17),
                    (x-13,y-19),
                    (x-11,y-21),
                    ]
    pygame.draw.circle(gameDisplay,black,(x,y),int(tankHeight/2))
    pygame.draw.rect(gameDisplay,black,(x-int(tankWidth/2),y,tankWidth,tankHeight))

    pygame.draw.line(gameDisplay,black,(x,y),possibleTurrets[turPos],turretWidth)

    startX=15
    for i in range(7):
        pygame.draw.circle(gameDisplay,black,(x-startX,y+20),wheelWidth)
        startX-=5

    return possibleTurrets[turPos]

def enemy_tank(x,y,turPos):
    x=int(x)
    y=int(y)

    possibleTurrets=[(x+27,y-2),
                    (x+26,y-5),
                    (x+25,y-8),
                    (x+23,y-12),
                    (x+20,y-14),
                    (x+18,y-15),
                    (x+15,y-17),
                    (x+13,y-19),
                    (x+11,y-21),
                    ]
    pygame.draw.circle(gameDisplay,black,(x,y),int(tankHeight/2))
    pygame.draw.rect(gameDisplay,black,(x-int(tankWidth/2),y,tankWidth,tankHeight))

    pygame.draw.line(gameDisplay,black,(x,y),possibleTurrets[turPos],turretWidth)

    startX=15
    for i in range(7):
        pygame.draw.circle(gameDisplay,black,(x-startX,y+20),wheelWidth)
        startX-=5

    return possibleTurrets[turPos]

def text_objects(msg,color,size):
    if size=="small":
        textSurf=smallfont.render(msg,True,color)
    elif size=="medium":
        textSurf=medfont.render(msg,True,color)
    elif size=="large":
        textSurf=largefont.render(msg,True,color)
    return textSurf,textSurf.get_rect()

def text_to_button(msg,color,buttonX,buttonY,buttonWidth,buttonHeight,size="small"):
    textSurf,textRect=text_objects(msg,color,size)
    textRect.center=((buttonX+buttonWidth/2),(buttonY+buttonHeight/2))
    gameDisplay.blit(textSurf,textRect)

def message(msg,color,y_displace=0,size="small"):
    textSurf,textRect = text_objects(msg,color,size)
    #screen_text=font.render(msg,True,color)
    #gameDisplay.blit(screen_text,[display_width/2,display_height/2])
    textRect.center=(display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def explosion(x,y):
    pygame.mixer.Sound.play(boom)
    explode=True

    while explode:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        colorChoices=[red,light_red,yellow,light_yellow,green,light_green]

        magnitude=1

        while magnitude<50:
            exploding_bit_x=x+random.randrange(-1*magnitude,magnitude)
            exploding_bit_y=y+random.randrange(-1*magnitude,magnitude)
            pygame.draw.circle(gameDisplay,colorChoices[random.randrange(0,6)],(exploding_bit_x,exploding_bit_y),3)
            magnitude+=1
            pygame.display.update()
            clock.tick(100)

        explode=False

def health_bars(player_health,enemy_health):
    if player_health>75:
        player_health_color=green
    elif player_health>50:
        player_health_color = yellow
    else:
        player_health_color=red

    if enemy_health>75:
        enemy_health_color=green
    elif enemy_health>50:
        enemy_health_color=yellow
    else:
        enemy_health_color=red

    pygame.draw.rect(gameDisplay,player_health_color,[680,25,player_health,25])
    pygame.draw.rect(gameDisplay,enemy_health_color,[20,25,enemy_health,25])


def fireShell(gun,tankX,tankY,turPos,gun_power,xlocation,barrier_width,randomHeight,ground_height,ptankx,ptanky):
    fire=True
    startingShell=list(gun)
    damage=0
    while fire:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay,light_red,(startingShell[0],startingShell[1]),5)

        startingShell[0]-= (12-turPos)*2
        startingShell[1]+=int((((startingShell[0]-gun[0])*0.015/(gun_power/50))**2)-(turPos+turPos/(12-turPos)))
        if startingShell[1]>display_height-ground_height:
          #  print("last shell: ",startingShell[0],startingShell[1])

            hit_x=int(startingShell[0]*(display_height-ground_height)/startingShell[1]) #cross multiply : if for startingShell[1] =>> startingShell[0] then for display_height =>> ??
            hit_y=int(display_height-ground_height)
            if ptankx+20>hit_x>ptankx-20:
            #    print("HIT")
                damage=25
            elif ptankx+30>hit_x>ptankx-30:
             #   print("HIT")
                damage=15
            elif ptankx+40>hit_x>ptankx-40:
             #   print("HIT")
                damage=10
            explosion(hit_x,hit_y)
            fire=False

        check_x_1=startingShell[0]>=xlocation
        check_x_2=startingShell[0]<=xlocation+barrier_width
        check_y_1=startingShell[1]<=display_height
        check_y_2=startingShell[1]>=display_height-randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
          #  print("last shell: ",startingShell[0],startingShell[1])

            hit_x=int(startingShell[0])
            hit_y=int(startingShell[1])

            explosion(hit_x,hit_y)
            fire=False
        pygame.display.update()
        clock.tick(60)
    return damage

def e_fireShell(gun,tankX,tankY,turPos,gun_power,xlocation,barrier_width,randomHeight,ground_height,ptankx,ptanky):
 #   print ("hi")
    currentPower=1
    damage=0
    power_found=False

    while not power_found:
        currentPower+=1
        if currentPower>100:
            power_found=True

        fire=True
        startingShell=list(gun)

        while fire:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()

            #pygame.draw.circle(gameDisplay,light_red,(startingShell[0],startingShell[1]),5)
            startingShell[0]+= (12-turPos)*2
            startingShell[1]+=int((((startingShell[0]-gun[0])*0.015/(currentPower/50))**2)-(turPos+turPos/(12-turPos)))
            if startingShell[1]>display_height-ground_height:
                hit_x=int(startingShell[0]*(display_height-ground_height)/startingShell[1]) #cross multiply : if for startingShell[1] =>> startingShell[0] then for display_height =>> ??
                hit_y=int(display_height-ground_height)
                if ptankx+15>hit_x>ptankx-15:
                 #   print("target acquired")
                    power_found=True
                #explosion(hit_x,hit_y)
                fire=False

            check_x_1=startingShell[0]>=xlocation
            check_x_2=startingShell[0]<=xlocation+barrier_width
            check_y_1=startingShell[1]<=display_height
            check_y_2=startingShell[1]>=display_height-randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x=int(startingShell[0])
                hit_y=int(startingShell[1])

                #explosion(hit_x,hit_y)
                fire=False
            #pygame.display.update()
            #clock.tick(60)

    fire=True
    startingShell=list(gun)

    while fire:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay,light_red,(startingShell[0],startingShell[1]),5)
        startingShell[0]+= (12-turPos)*2
        gun_power=random.randrange(int(currentPower*0.95),int(currentPower*1.05))
        startingShell[1]+=int((((startingShell[0]-gun[0])*0.015/(gun_power/50))**2)-(turPos+turPos/(12-turPos)))
        if startingShell[1]>display_height-ground_height:
          #  print("last shell: ",startingShell[0],startingShell[1])

            hit_x=int(startingShell[0]*(display_height-ground_height)/startingShell[1]) #cross multiply : if for startingShell[1] =>> startingShell[0] then for display_height =>> ??
            hit_y=int(display_height-ground_height)
            if ptankx+20>hit_x>ptankx-20:
              #  print("HIT")
                damage=25
            elif ptankx+30>hit_x>ptankx-30:
              #  print("HIT")
                damage=15
            elif ptankx+40>hit_x>ptankx-40:
              #  print("HIT")
                damage=10
            explosion(hit_x,hit_y)
            fire=False

        check_x_1=startingShell[0]>=xlocation
        check_x_2=startingShell[0]<=xlocation+barrier_width
        check_y_1=startingShell[1]<=display_height
        check_y_2=startingShell[1]>=display_height-randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
          #  print("last shell: ",startingShell[0],startingShell[1])

            hit_x=int(startingShell[0])
            hit_y=int(startingShell[1])

            explosion(hit_x,hit_y)
            fire=False
        pygame.display.update()
        clock.tick(60)
    return damage


def power(firePower):
    textSurf,textRect=text_objects("Power : " + str(firePower) + "%",black,"small")
    textRect.center=(display_width/2,textRect.height/2)
    gameDisplay.blit(textSurf,textRect)

def gameLoop():
    gameExit=False
    gameOver=False
    mainTankX=display_width*0.9
    mainTankY=display_height*0.9
    enemyTankX=display_width*0.1
    enemyTankY=display_height*0.9
    tankMove=0
    currentTur=0
    changeTur=0
    xlocation=(display_width/2)+random.randint(-0.1*display_width,0.1*display_width)
    randomHeight=random.randrange(display_height*0.1,display_height*0.6)
    barrier_width=50
    firePower=50
    powerChange=0
    ground_height=35

    player_health=100
    enemy_health=100
    while not gameExit:
    #    print (gun)
        if gameOver:
            message("Game Over",red,-50,"large")
            message("Press C to play again and q to Quit",black,50,"medium")
        while gameOver:
            #gameDisplay.fill(white)

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
                    tankMove=-5
                elif event.key==pygame.K_RIGHT:
                    tankMove=5
                elif event.key==pygame.K_UP:
                    changeTur=1
                elif event.key==pygame.K_DOWN:
                    changeTur=-1
                elif event.key==pygame.K_p:
                    pause()
                elif event.key==pygame.K_SPACE:
                    damage=fireShell(gun,mainTankX,mainTankY,currentTur,firePower,xlocation,barrier_width,randomHeight,ground_height,enemyTankX,enemyTankY)
                    enemy_health-=damage
                    possibleMovement=['f','r']
                    moveIndex=random.randrange(0,2)

                    for x in range(random.randrange(0,10)):
                        if display_width*0.3>enemyTankX>display_width*0.003:
                            if possibleMovement[moveIndex]=="f":
                                enemyTankX+=10
                            elif possibleMovement[moveIndex]=="r":
                                enemyTankX-=10
                            if enemyTankX<display_width*0.03:
                                enemyTankX+=10
                            gameDisplay.fill(white)

                            health_bars(player_health,enemy_health)
                            gun=tank(mainTankX,mainTankY,currentTur)
                            enemy_gun=enemy_tank(enemyTankX,enemyTankY,8)
                            power(firePower)
                            barrier(xlocation,randomHeight,barrier_width)
                            gameDisplay.fill(green,rect=[0,display_height-ground_height,display_width,ground_height])
                            pygame.display.update()
                            if player_health<1:
                                game_Over("Game Over","You lost",red)
                            elif enemy_health<1:
                                game_Over("You Won!","Congratulations",green)
                            clock.tick(FPS)
                    if enemyTankX<display_width*0.03:
                        enemyTankX+=10
                  #  print("enemy health",enemy_health,damage)

                    damage=e_fireShell(enemy_gun,enemyTankX,enemyTankY,8,50,xlocation,barrier_width,randomHeight,ground_height,mainTankX,mainTankY)
                    player_health-=damage
                elif event.key==pygame.K_a:
                    powerChange=1
                elif event.key==pygame.K_d:
                    powerChange=-1

            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                    tankMove=0
                elif event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    changeTur=0
                elif event.key==pygame.K_a or event.key==pygame.K_d:
                    powerChange=0

        mainTankX+=tankMove
        currentTur+=changeTur
        if currentTur>8:
            currentTur=8
        elif currentTur<0:
            currentTur=0

        if mainTankX-(tankWidth/2) < xlocation+barrier_width:
            mainTankX+=5
        firePower+=powerChange

        if firePower>100:
            firePower=100
        elif firePower<1:
            firePower=1
        gameDisplay.fill(white)

        health_bars(player_health,enemy_health)
        gun=tank(mainTankX,mainTankY,currentTur)
        enemy_gun=enemy_tank(enemyTankX,enemyTankY,8)
        power(firePower)
        barrier(xlocation,randomHeight,barrier_width)
        gameDisplay.fill(green,rect=[0,display_height-ground_height,display_width,ground_height])
        pygame.display.update()
        if player_health<1:
            game_Over("Game Over","You lost",red)
        elif enemy_health<1:
            game_Over("You Won!","Congratulations",green)
        clock.tick(FPS) #we are moving 15 frames per second

   # message("You lose ghonchu",red)
    gameDisplay.fill(white)
    pygame.display.update()
   # time.sleep(1)
    pygame.quit()
    quit()

gameIntro()
gameLoop()
