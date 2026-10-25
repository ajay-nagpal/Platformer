import pygame, json
from os import path

pygame.init()

SCREEN_WIDTH=840
SCREEN_HEIGHT=840

#boundry block size 
BLOCK_SIZE=42 #20*20
MAX_LEVELS=3

clock = pygame.time.Clock()
fps = 60
game_over=0
main_menu=True#for main menu 
level=1
score=0

#define font
font_score=pygame.font.SysFont('Bauhaus 93',30)
font_general=pygame.font.SysFont('Bauhaus 93',100)

#define color
white=(255,255,255)

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#load images
sun_img=pygame.image.load('img/sun.png')
bg_img=pygame.image.load('img/sky.png')
restart_img=pygame.image.load('img/restart_btn.png')
start_img=pygame.image.load('img/start_btn.png')
exit_img=pygame.image.load('img/exit_btn.png')

bg_img = pygame.transform.scale(
    bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

class World():
    def __init__(self,data):
        clock.tick(fps)
        #load block image
        self.block_list=[]
        blk_img=pygame.image.load('img/blk.png')
        grass_img=pygame.image.load('img/grass.png')

        row_counter=0#counter to determine wehre we  will put block on screen row and col
        for row in data:
            col_counter=0
            for col in row:
                
                if col==1:#a block location on boundry
                    img=pygame.transform.scale(blk_img,(BLOCK_SIZE,BLOCK_SIZE))
                    #convert this img to rect obj
                    img_rect=img.get_rect()
                    #x will increase for each col in a row
                    img_rect.x=col_counter*BLOCK_SIZE
                    img_rect.y=row_counter*BLOCK_SIZE

                    block=(img,img_rect)
                    self.block_list.append(block)

                if col==2:#grass 
                    img=pygame.transform.scale(grass_img,(BLOCK_SIZE,BLOCK_SIZE))
                    #convert this img to rect obj
                    img_rect=img.get_rect()
                    #x will increase for each col in a row
                    img_rect.x=col_counter*BLOCK_SIZE
                    img_rect.y=row_counter*BLOCK_SIZE

                    block=(img,img_rect)
                    self.block_list.append(block)

                if col==3:#enemy
                    enemy=Enemy(col_counter*BLOCK_SIZE,row_counter*BLOCK_SIZE+6)
                    enemy_group.add(enemy)

                if col==6:#lava
                    lava=Lava(col_counter*BLOCK_SIZE,row_counter*BLOCK_SIZE+BLOCK_SIZE//2)
                    lava_group.add(lava)

                if col==7:#coin
                    coin=Coin(col_counter*BLOCK_SIZE+BLOCK_SIZE//2,row_counter*BLOCK_SIZE+BLOCK_SIZE//2)
                    coin_group.add(coin)

                if col==8:#exit
                    exit=Exit(col_counter*BLOCK_SIZE,row_counter*BLOCK_SIZE-(BLOCK_SIZE//2))
                    exit_group.add(exit)

                col_counter+=1
            row_counter+=1

    def draw(self):
        for block in self.block_list:
            screen.blit(block[0],block[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('img/enemy.png')
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_direction=1#1:right, -1:left
        self.move_counter=0

    def update(self):
        #move enemy left and right
        self.rect.x+=self.move_direction
        self.move_counter+=1
        if abs(self.move_counter)>50:
            self.move_direction*=-1#change direction
            self.move_counter*=-1#reset counter

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('img/lava.png')
        self.image=pygame.transform.scale(img,(BLOCK_SIZE,BLOCK_SIZE//2))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('img/coin.png')
        self.image=pygame.transform.scale(img,(BLOCK_SIZE//2,BLOCK_SIZE//2))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):

        action=False
        #get mouse position
        pos=pygame.mouse.get_pos()#it gives x,y coordinate of mouse pointer
        #check if mouse is over button and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and not self.clicked:#left click
                self.clicked=True
                action= True
            # if mouse button is released, reset clicked state
            if pygame.mouse.get_pressed()[0]==0:
                #reset clicked state
                self.clicked=False
        
        #draw button on screen
        screen.blit(self.image, self.rect)
        return action

#exit gate for level completion
class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('img/exit.png')
        self.image=pygame.transform.scale(img,(BLOCK_SIZE,BLOCK_SIZE*1.5))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class Player():
    def __init__(self,x,y):
        self.reset(x,y)

    def update(self):

        #get key presses
        #we will calculate nplayer next position based on whether we can move there or ot 
        # rather than directly going there, as movign is fast ordinary collision detection is bit normal
        #so wew will cehck collision then update player's positon
        dx=0
        dy=0
        cooldown=20#20 iteration for animation
        
        global game_over
        if game_over==0:
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                self.vel_y=-15#up
                self.jumped=True
            #release space key
            if not key[pygame.K_SPACE]:
                self.jumped=False

            if key[pygame.K_LEFT]:
                self.counter+=1
                dx-=5
                self.direction=-1
            if key[pygame.K_RIGHT]:
                self.counter+=1
                dx+=5
                self.direction=1

            #reset counter and index when no left right key pressed to get player straight position pic
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter=0
                self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction==-1:
                    self.image=self.images_left[self.index]

            #handle animation 
            if self.counter>cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images_right):
                    self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction==-1:
                    self.image=self.images_left[self.index]

                # what wehn going left, need to flip image on x axis then move adn repeat above step
            #add gravity
            self.vel_y+=1
            if self.vel_y>10:
                self.vel_y=10
            dy+=self.vel_y

            #check for collision
            self.in_air=True#assume player is in air, if we find collision then we will set it to false
            for block in world.block_list:
                #check for collision in x direction, can be on a block, but can move y dir
                if block[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                    dx=0#stop moving in x direction, but can move in y direction    
                
                #chcek for collision in y dircetion, can be on a blcok, but can move x dir
                if block[1].colliderect(self.rect.x, self.rect.y+dy,self.width,self.height):
                    #self.rect.y+dy is whtever it is planing to move to, then width adn height
                    #use dx adn dy because it is nto moved yet we can get to know about collision before moving
                    #create a temp rect based on dx and dy
                    #need to cehck whether player is above or below the block, if above then stop falling 
                    #if head hits the block then stop going up
                    if self.vel_y<0:#jumping beause +ve velocity is goign down
                        #move till block bottom because after taht we cant jump
                        dy=block[1].bottom-self.rect.top
                        self.vel_y=0#stop going up, so player can fall down
                    elif self.vel_y>=0:#falling
                        dy=block[1].top-self.rect.bottom# distance allowed to move, emasn will stop at block top, so player can stand on block
                        self.vel_y=0#stop falling #hit ground
                        self.in_air=False#player is on ground, so can jump again

            #check for collision with enemies or lava 
            if pygame.sprite.spritecollide(self,enemy_group,False) \
                or pygame.sprite.spritecollide(self,lava_group,False):#do kill false
                game_over=1#player dies

            #check for collision with exit
            if pygame.sprite.spritecollide(self,exit_group,False):
                game_over=-1#level complete

            #check for collision with coins
            coin_collisions=pygame.sprite.spritecollide(self,coin_group,True)#do kill
            if coin_collisions:
                global score
                score+=1
        
        elif game_over==1:
            self.image=self.dead_image
            self.rect.y-=5#move up to show player is dead

        #update player's position
        self.rect.x+=dx
        self.rect.y+=dy

        #draw player on screen
        screen.blit(self.image,self.rect)

    def reset(self,x,y):
        self.images_right=[]# list of images to animate for right movement
        self.images_left=[]# list of images to animate for left movement
        self.index=0# list index

        #counter to control animation rate at which it cycle through
        self.counter=0

        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right=pygame.transform.scale(img_right,(30,60))
            self.images_right.append(img_right)

            img_left=pygame.transform.flip(img_right,True,False) #flip on x axis, not y axis
            self.images_left.append(img_left)

        self.dead_image=pygame.image.load('img/ghost.png')
        self.image=self.images_right[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.width=self.image.get_width()
        self.height=self.image.get_height()

        self.vel_y=0#for jump
        self.jumped=False
        self.direction=0#1:right, -1:left

        self.in_air=True#to check whether player is in air or on ground, so that we can jump only when on ground

enemy_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()
coin_group=pygame.sprite.Group()

def reset_level(level):
    player.reset(BLOCK_SIZE,SCREEN_HEIGHT-(BLOCK_SIZE+60))
    enemy_group.empty()#empty all groups
    lava_group.empty()
    exit_group.empty()

    #create enemy group befor creating world, so that we can add enemy to this group when creating world
    #load thte world data from file
    if path.exists(f'levels/level{level}_data.json'):
        with open(f'levels/level{level}_data.json', 'r') as f:
            world_data = json.load(f)
    world=World(world_data)
    
    return world

def draw_text(text,font,text_color,x,y):
    img=font.render(text,True,text_color)
    screen.blit(img,(x,y))

player=Player(BLOCK_SIZE,SCREEN_HEIGHT-(BLOCK_SIZE+60))#player height
world=reset_level(level)


#buttons
restart_button=Button(SCREEN_WIDTH//2-50,SCREEN_HEIGHT//2-100,restart_img)

start_button=Button(SCREEN_WIDTH//2-250,SCREEN_HEIGHT//2-100,start_img)
exit_button=Button(SCREEN_WIDTH//2+50,SCREEN_HEIGHT//2-100,exit_img)

run=True
while run:
    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(80,80))

    if main_menu:
        if start_button.draw():
            main_menu=False
        if exit_button.draw():
            run=False
    else:
        if not game_over:
            enemy_group.update()
        elif game_over==1:
            draw_text('GAME OVER!',font_general,white,(SCREEN_WIDTH//2)-200,SCREEN_HEIGHT//2)
            if restart_button.draw():
                world_data=[]#reset world data
                world=reset_level(level)                
                game_over=0
                score=0
        elif game_over==-1:
            #level complete, we can show level complete screen or go to next level
            #reset the game nthen next level
            level+=1
            if level<=MAX_LEVELS:
                world_data=[]#reset world data
                world=reset_level(level)
                game_over=0
            else:
                draw_text('YOU WON!',font_general,white,(SCREEN_WIDTH//2)-200,SCREEN_HEIGHT//2)
                if restart_button.draw():
                    level=1
                    world_data=[]#reset world data
                    world=reset_level(level)
                    game_over=0
                    score=0

        world.draw()
        player.update()
        exit_group.draw(screen)

        enemy_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)

        draw_text('$¢or€:   '+str(score),font_score,white,BLOCK_SIZE-5,10)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
    
pygame.quit()
