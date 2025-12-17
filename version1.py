import pygame
# import clo
pygame.init()

######################3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = 1
##########################################


class movable_objects:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("box.png")
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        # self.hitbox_height = self.hitbox

    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)   

    def check_collision(self, player_obj):
        if( ((self.hitbox.left<=player_obj.hitbox.right and player_obj.hitbox.right<=self.hitbox.right) or 
               (self.hitbox.left<=player_obj.hitbox.left and player_obj.hitbox.left<=self.hitbox.right)) and player_obj.hitbox.bottom<=self.hitbox.top):
                player_obj.ground = self.hitbox.top 
        else:
            player_obj.ground = 400 
        if(abs(self.hitbox.bottom - player_obj.hitbox.bottom)<=0):
            if( (self.hitbox.left<=player_obj.hitbox.right and player_obj.hitbox.right<=self.hitbox.right) or 
               (self.hitbox.left<=player_obj.hitbox.left and player_obj.hitbox.left<=self.hitbox.right)):
                # if(player_obj.hitbox.bottom>=self.hitbox.top):
                    # print(1)
                    # print(1)
                if(player_obj.movingRight):
                    self.hitbox.left = player_obj.hitbox.right
                    self.x = self.hitbox.left + (self.hitbox.width/2) 
                elif(player_obj.movingLeft):
                    self.hitbox.right = player_obj.hitbox.left
                    self.x = self.hitbox.right - (self.hitbox.width/2)
                
                    # player_obj.y = self.hitbox.top
            # print(1)

    def update(self, player_obj):
        self.check_collision(player_obj)


class player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("player.png")
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx=self.x
        self.hitbox.bottom = self.y
        self.movingLeft = 0
        self.movingRight = 0
        self.jumping = 0
        self.time_of_flight = 20
        self.jump_counter = self.time_of_flight 
        self.velocity = 4
        self.ground = 400
        self.fall_counter = 0

    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(player_obj.image, player_obj.hitbox)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)

    def moveLeft(self):
        self.x-=self.velocity

    def moveRight(self):
        self.x+=self.velocity

    def resetJump(self):
        self.jump_counter = self.time_of_flight
        self.jumping=0

    def jump(self, height):
            if((abs(self.jump_counter)<=self.time_of_flight and (self.y-height*self.jump_counter)<=self.ground) or self.jump_counter>=0):
                self.y = self.y - height*self.jump_counter
                self.jump_counter -= 1
            else:
                self.resetJump()
                self.y = self.ground

    def fall(self, weight):
        
        if((self.y-weight*self.fall_counter)<=self.ground):
            self.y = self.y + weight*self.jump_counter
            self.fall_counter += 1
        else:
            # self.resetJump()
            self.fall_counter = 0
            self.y = self.ground    

    def update(self):
        if(self.y!=self.ground and (self.jumping==0)):
            self.fall(1)    
        if(self.jumping):
            self.jump(1)
        if(self.movingLeft):
            self.moveLeft()
        elif(self.movingRight):
            self.moveRight()


##########################################

player_obj = player(100, 400)
box1 = movable_objects(200, 400)
clock = pygame.time.Clock()
while (run):
    clock.tick(60)
    SCREEN.fill((24,255,255))
    player_obj.update()
    player_obj.draw()
    # print(player_obj.ground)
    box1.update(player_obj)
    
    box1.draw()
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            run = 0
        if(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_a):
                player_obj.movingLeft = 1
            if(event.key==pygame.K_d):
                player_obj.movingRight = 1
            if(event.key==pygame.K_SPACE):
                player_obj.jumping = 1
        if(event.type==pygame.KEYUP):
            if(event.key==pygame.K_a):
                player_obj.movingLeft = 0
            if(event.key==pygame.K_d):
                player_obj.movingRight = 0
    pygame.display.update()