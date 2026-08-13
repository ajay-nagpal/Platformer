import pygame

SCREEN_WIDTH=840
SCREEN_HEIGHT=840

#boundry block size 
BLOCK_SIZE=42 #20*20

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
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class World():
    def __init__(self,data):
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

                col_counter+=1
            row_counter+=1

    def draw(self):
        for block in self.block_list:
            screen.blit(block[0],block[1])

class Player():
    def __init__(self,x,y):
        img=pygame.image.load('img/guy1.png')
        self.image=pygame.transform.scale(img,(30,60))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        self.vel_y=0#for jump
        self.jumped=False

    def update(self):

        #get key presses
        #we will calculate nplayer next position based on whether we can move there or ot 
        # rather than directly going there, as movign is fast ordinary collision detection is bit normal
        #so wew will cehck collision then update player's positon
        dx=0
        dy=0
        key=pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped:
            self.vel_y=-15#up
            self.jumped=True
        #release space key
        if not key[pygame.K_SPACE]:
            self.jumped=False

        if key[pygame.K_LEFT]:
            dx-=5
        if key[pygame.K_RIGHT]:
            dx+=5

        #add gravity
        self.vel_y+=1
        if self.vel_y>10:
            self.vel_y=10
        dy+=self.vel_y

        #check for collision

        #update player's position
        self.rect.x+=dx
        self.rect.y+=dy

        if self.rect.bottom>SCREEN_HEIGHT:
            self.rect.bottom=SCREEN_HEIGHT
            dy=0

        #draw player on screen
        screen.blit(self.image,self.rect)


world=World(world_data)
player=Player(100,SCREEN_HEIGHT-(BLOCK_SIZE+60))#player height

run=True
while run:
    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(80,80))

    world.draw()
    player.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
    
pygame.quit()
