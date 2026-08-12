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

world=World(world_data)

run=True
while run:
    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(80,80))

    world.draw()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
    
pygame.quit()
