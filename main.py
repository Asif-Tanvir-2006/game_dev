import pygame
# import clo
pygame.init()


######################3
SCREEN_WIDTH = 800;
SCREEN_HEIGHT = 600;
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = 1;
##########################################
class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("player.png")
        self.hitbox = self.image.get_rect();
        self.hitbox.center=(self.x, self.y)
        self.movingLeft = 0
        self.movingRight = 0
        self.jumping = 0;
        self.jump_time = 5;
        self.jump_counter = self.jump_time; 
    def draw(self):
        self.hitbox.center=(self.x, self.y)
        SCREEN.blit(player_obj.image, player_obj.hitbox)
    def moveLeft(self, velocity):
        self.x-=velocity
    def moveRight(self, velocity):
        self.x+=velocity
    def jump(self, height):
            if(abs(self.jump_counter)<=self.jump_time):
                self.y = self.y - height*self.jump_counter;
                self.jump_counter -= 1
            else:
                self.jump_counter = self.jump_time
                self.jumping=0
            
    def update(self):
        if(self.jumping):
            self.jump(10);
        if(self.movingLeft):
            self.moveLeft(10)
        elif(self.movingRight):
            self.moveRight(10)
##########################################
player_obj = player(100, 400)
clock = pygame.time.Clock();
while (run):
    clock.tick(24);
    SCREEN.fill((24,255,255))
    player_obj.update();
    player_obj.draw();
    
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            run = 0;
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
    pygame.display.update();