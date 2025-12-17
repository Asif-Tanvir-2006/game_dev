import pygame
# import clo
pygame.init()


#pls check this once
#400 is the default level of floor where everything spawns

######################3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
INF = 1e10

run = 1
##########################################


class immovable_objects:

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        self.velocity = 4
        self.movingLeft = 0;
        self.movingRight = 0;
        self.floor = self.y
        # self.hitbox_height = self.hitbox

    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y

        SCREEN.blit(self.image, self.hitbox)   
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)
        
    def check_collision_x(self, obj):
        #if obj is left of self return 0, obj right of self return -1, else return 1
        if(self.hitbox.left>obj.hitbox.right): return 0 
        if(self.hitbox.right<obj.hitbox.left): return -1 
        return 1
    
    def check_collision_y(self, obj):
        #if obj is above self return 0, obj below self return -1, else return 1
        if(self.hitbox.top>=obj.hitbox.bottom): return 0
        if(self.hitbox.bottom<=obj.hitbox.top): return -1
        return 1
    
    def update(self, obj):
        if(not self.check_collision_y(obj)==0 and self.check_collision_x(obj)==1):
            obj.floor = min(self.hitbox.top, obj.floor)
        if(self.check_collision_y(obj)==-1 and self.check_collision_x(obj)==1):
            obj.roof = self.hitbox.bottom
        if(self.check_collision_x(obj)==1 and self.check_collision_y(obj)==1):
            if(self.hitbox.centerx>obj.hitbox.centerx):
                obj.rightWall = self.hitbox.left
                pass
            if(self.hitbox.centerx<obj.hitbox.centerx):
                obj.leftWall = self.hitbox.right
                pass

class movable_objects:

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        self.velocity = 4
        self.movingLeft = 0;
        self.movingRight = 0;
        self.floor = self.y
        self.roof = -INF
        self.leftWall = -INF
        self.rightWall = INF
        # self.hitbox_height = self.hitbox

    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)   
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)
        
    def check_collision_x(self, obj):
        #if obj is left of self return 0, obj right of self return -1, else return 1
        if(self.hitbox.left>obj.hitbox.right): return 0 
        if(self.hitbox.right<obj.hitbox.left): return -1 
        return 1
    
    def check_collision_y(self, obj):
        #if obj is above self return 0, obj below self return -1, else return 1
        if(self.hitbox.top>=obj.hitbox.bottom): return 0
        if(self.hitbox.bottom<=obj.hitbox.top): return -1
        return 1
    
    def update(self, obj):
        self.movingLeft = 0
        self.movingRight = 0
        # obj.floor = 400
        
        if(self.check_collision_y(obj)==0 and self.check_collision_x(obj)==1):
            obj.floor = min(obj.floor, self.hitbox.top)
            # print(1)
        elif(self.check_collision_x(obj)==1 and self.check_collision_y(obj)==1):
            # print(obj.hitbox.height)
            if(obj.hitbox.centerx>self.hitbox.centerx):
                # self.movingLeft = 1
                # self.movingRight = 0
                self.x -= (2*self.velocity)
            elif(obj.hitbox.centerx<self.hitbox.centerx):
                # self.movingLeft = 0
                # self.movingRight = 1
                self.x += (2*self.velocity)

            # obj.floor = 400 
        # else: print(0)
        
class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/player.png")
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx=self.x
        self.hitbox.bottom = self.y
        self.movingLeft = 0
        self.movingRight = 0
        self.jumping = 0
        self.time_of_flight = 20
        self.jump_counter = self.time_of_flight 
        self.velocity = 4
        self.floor = self.y
        self.fall_counter = 0
        # self.floor = self.y
        self.roof = -10000000
        self.leftWall = -1000000
        self.rightWall = 10000000
    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(player_obj.image, player_obj.hitbox)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)

    def moveLeft(self):
        if(self.hitbox.left-self.velocity>=self.leftWall): self.x-=self.velocity
    def moveRight(self):
        if(self.hitbox.right+self.velocity<=self.rightWall): self.x+=self.velocity
    def resetJump(self):
        self.jump_counter = self.time_of_flight
        self.jumping=0
    def jump(self, height):
            if((self.y-height*self.jump_counter)<=self.floor or self.jump_counter>=0):
                self.y = max(self.y - height*self.jump_counter, self.roof+self.hitbox.height)
                if(self.y == self.roof+self.hitbox.height):
                    self.jump_counter=0
                # print(self.roof)
                # print(self.floor)
                if(self.y==self.roof): print(-1);
                self.jump_counter -= 1
            else:
                self.resetJump()
                self.y = self.floor
    def fall(self, weight):
        
        if((self.y+weight*self.fall_counter)<=self.floor):
            self.y = self.y + weight*self.jump_counter
            self.fall_counter += 1
        else:
            # self.resetJump()
            self.fall_counter = 0
            self.y = self.floor        
    def update(self):
        if(self.y!=self.floor and (self.jumping==0)):
            self.fall(1)    
        if(self.jumping):
            self.jump(0.7)
        if(self.movingLeft):
            self.moveLeft()
        elif(self.movingRight):
            self.moveRight()


##########################################

if __name__ == "__main__":

    player_obj = player(100, 400)
    box1 = movable_objects(200, 400, "assets/box.png")
    box2 = movable_objects(400, 400, "assets/3.png")
    platform = immovable_objects(1000, 185, "assets/platform.png")
    clock = pygame.time.Clock()
    
    while (run):
        clock.tick(60)

        SCREEN.fill((24,255,255))

        player_obj.floor=400
        player_obj.roof = -10000000
        player_obj.leftWall = -1000000
        player_obj.rightWall = 10000000
        platform.update(player_obj)
        box1.update(box2)
        box2.update(box1)
        box1.update(player_obj)
        box2.update(player_obj)
        player_obj.update()

        # print(player_obj.roof)
        
        box1.draw()
        box2.draw()
        platform.draw()
        player_obj.draw()
        
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                run = 0
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_a):
                    player_obj.movingLeft = 1
                    player_obj.movingRight = 0
                if(event.key==pygame.K_d):
                    player_obj.movingRight = 1
                    player_obj.movingLeft = 0
                if(event.key==pygame.K_SPACE):
                    player_obj.jumping = 1
                    
            if(event.type==pygame.KEYUP):
                if(event.key==pygame.K_a):
                    player_obj.movingLeft = 0
                if(event.key==pygame.K_d):
                    player_obj.movingRight = 0
        pygame.display.update()