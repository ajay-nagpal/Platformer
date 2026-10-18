import pygame

SCREEN_WIDTH=840
SCREEN_HEIGHT=840

#boundry block size 
BLOCK_SIZE=42 #20*20

clock = pygame.time.Clock()
fps = 60

game_over=0

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#load images
sun_img=pygame.image.load('img/sun.png')
bg_img=pygame.image.load('img/sky.png')

bg_img = pygame.transform.scale(
    bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

#assume  complete screen as 20*20 matrix
#we want block boundry, no passthrough[1]
#grass block [2]
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

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

class Player():
    def __init__(self,x,y):
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
            if key[pygame.K_SPACE] and not self.jumped:
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

            #check for collision with enemies or lava 
            if pygame.sprite.spritecollide(self,enemy_group,False) \
                or pygame.sprite.spritecollide(self,lava_group,False):#do kill false
                game_over=1#player dies
        
        elif game_over==1:
            self.image=self.dead_image
            self.rect.y-=5#move up to show player is dead

        #update player's position
        self.rect.x+=dx
        self.rect.y+=dy

        #draw player on screen
        screen.blit(self.image,self.rect)

enemy_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
#create enemy group befor creating world, so that we can add enemy to this group when creating world
world=World(world_data)
player=Player(100,SCREEN_HEIGHT-(BLOCK_SIZE+60))#player height

run=True
while run:
    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(80,80))

    world.draw()
    
    if not game_over:
        enemy_group.update()
    
    player.update()

    enemy_group.draw(screen)
    lava_group.draw(screen)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
    
pygame.quit()
