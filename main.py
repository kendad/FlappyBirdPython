import pygame
import random
import sys,os

#SCREEN VARIABLES
SCREEN_WIDTH=640
SCREEN_HEIGHT=960

#BACKGROUND COUNTER 
bg_counter=0

#MAX VARIABELS
MAX_SPEED=6
MAX_ANGLE=40

#SCORE
SCORE=0

#TEXT FONT
pygame.font.init()
myfont=pygame.font.SysFont("Comic Sans MS",50)
textsurface=myfont.render(str(SCORE),False,(255,255,255))

#draws the text on the screen
def drawScore():
    textsurface=myfont.render(str(SCORE),False,(255,255,255))
    screen.blit(textsurface,(SCREEN_WIDTH/2,(SCREEN_HEIGHT/2)-400))

#CLASSES
##
## BACKGROUND CLASS
# BACKGROUND-1
class Background1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(os.path.join("assets","bg2.jpg"))
        self.rect=self.image.get_rect()
        self.pos_x=0

    def update(self):
        self.pos_x-=5
        self.rect.topleft=(self.pos_x,0)
        if((self.pos_x+SCREEN_WIDTH)<0):
            self.pos_x=0

# BACKGROUND-2
class Background2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(os.path.join("assets","bg2.jpg"))
        self.rect=self.image.get_rect()
        self.pos_x=SCREEN_WIDTH

    def update(self):
        self.pos_x-=5
        self.rect.topleft=(self.pos_x,0)
        if(self.pos_x<0):
            self.pos_x=SCREEN_WIDTH
        
# BIRD CLASS
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ##bird display properties
        self.birdArray=[]
        self.birdArray.append(pygame.image.load(os.path.join("assets","bird_wing_up.png")))
        self.birdArray.append(pygame.image.load(os.path.join("assets","bird_wing_down.png")))      
        self.birdCounter=0
        self.image=self.birdArray[self.birdCounter]
        self.image=pygame.transform.scale2x(self.image)
        self.rect=self.image.get_rect()
        self.rect.x=(SCREEN_WIDTH/2)-100
        self.rect.y=(SCREEN_HEIGHT/2)-200

        #initial fall velocity
        self.velocity=0
        self.angle=0

    def update(self):
        #bird animation
        self.birdCounter+=0.2
        if self.birdCounter>=len(self.birdArray):
            self.birdCounter=0
        self.image=self.birdArray[int(self.birdCounter)]
        self.image=pygame.transform.scale2x(self.image)

        ##gravity
        self.velocity+=(MAX_SPEED-self.velocity)*0.1
        self.rect.y+=self.velocity
        self.angle+=3
        if(self.angle>=MAX_ANGLE):
            self.angle=MAX_ANGLE
        self.image=pygame.transform.rotate(self.image,-int(self.angle))

        if(self.rect.y<=0):
            self.rect.y=0
    
    def userInput(self):
        self.rect.y-=100
        self.angle=-10

    def grnd_collision(self):
        if(self.rect.y>=760):
            return True


## PIPE-CLASS
#PIPE-TOP
class PipeTop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(os.path.join("assets","pipe.png"))
        self.rect=self.image.get_rect()
        self.rect.topleft=((SCREEN_WIDTH/2)+200,0)
        self.image=pygame.transform.rotate(self.image,180)##facing down
        #resize pipe
        self.image=pygame.transform.scale(self.image,(100,400))

    def update(self):
        randY=random.randint(200,300)
        self.rect.x-=5
        if(self.rect.bottomright[0]<0):
            self.rect.x=SCREEN_WIDTH
            self.rect.bottomleft=(self.rect.x,randY)

#PIPE-BOTTOM
class PipeBottom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(os.path.join("assets","pipe.png"))
        self.rect=self.image.get_rect()
        self.rect.bottomleft=((SCREEN_WIDTH/2)+200,770)
        self.image=pygame.transform.rotate(self.image,360)##facing up

        #resize pipe
        self.image=pygame.transform.scale(self.image,(100,400))
        self.rect.y=600

    def update(self):
        randY=random.randint(500,600)
        self.rect.x-=5
        if(self.rect.topright[0]<0):
            self.rect.x=SCREEN_WIDTH
            self.rect.y=randY
            global SCORE
            SCORE+=1

# check for collision between two rectangles
def checkCollision(bird,pipeTop,pipeBottom):
   if bird.topright[0]>pipeTop.bottomleft[0] and bird.topright[0]<pipeTop.bottomleft[0]+100 and bird.topright[1]<pipeTop.bottomleft[1] and bird.topright[1]>0:
       return True
   if bird.bottomright[0]>pipeBottom.topleft[0] and bird.bottomright[0]<pipeBottom.topleft[0]+100 and bird.bottomright[1]>pipeBottom.topleft[1] and bird.topright[1]<760:
       return True
   return False


pygame.init()
clock=pygame.time.Clock()

##SCREEN
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("FlappyBird")

bird=Bird()

##BACKGROUND GROUP
bg_sprites_group=pygame.sprite.Group()
background1=Background1()
background2=Background2()
bg_sprites_group.add(background1)
bg_sprites_group.add(background2)
bg_sprites_group.add(bird)

##PIPES GROUP
pipe_collection=pygame.sprite.Group()
pipeTop=PipeTop()
pipeBottom=PipeBottom()
pipe_collection.add(pipeTop)
pipe_collection.add(pipeBottom)

def main():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    bird.userInput()

        if bird.grnd_collision():
            break
        if checkCollision(bird.rect,pipeTop.rect,pipeBottom.rect)==True:
            break

        bg_sprites_group.draw(screen)
        pipe_collection.draw(screen)
        bg_sprites_group.update()
        pipe_collection.update()
        
        drawScore()
        
        pygame.display.update()
        clock.tick(60)

    return 0



#runs this main function
if __name__ == "__main__":
    main()