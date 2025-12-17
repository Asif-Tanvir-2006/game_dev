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

    def __init__(self, x, y, image, width, height):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image , (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.left = self.x
        self.hitbox.bottom = self.y
        self.velocity = 4

    def draw(self):
        self.hitbox.left = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)   
        
    def check_collision_x(self, obj):
        #if obj is left of self return -1, obj right of self return 1, else return 0
        if(self.hitbox.left > obj.hitbox.right): return -1 
        if(self.hitbox.right < obj.hitbox.left): return 1 
        return 0
    
    def check_collision_y(self, obj):
        #if obj is above self return -1, obj below self return 1, else return 0
        if(self.hitbox.top >= obj.hitbox.bottom): return -1
        if(self.hitbox.bottom <= obj.hitbox.top): return 1
        return 0
    
    def update(self, obj):
        # checks if there is a collision within x coord
        if not self.check_collision_x(obj) :

            # checks if object is above immovable object
            if (self.check_collision_y(obj) == -1) :
                obj.floor = min(self.hitbox.top, obj.floor)

            # checks if object is below immovable object
            elif (self.check_collision_y(obj) == 1) :
                obj.roof = self.hitbox.bottom

            else :
                # sets a wall on the object based on which side the immovable object is
                if(self.hitbox.centerx > obj.hitbox.centerx):
                    obj.rightWall = self.hitbox.left
                elif(self.hitbox.centerx < obj.hitbox.centerx):
                    obj.leftWall = self.hitbox.right


class movable_objects:

    def __init__(self, x, y, image, width=1, height=1):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width,height))
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        self.velocity = 4

        self.floor = self.y
        self.roof = -INF
        self.leftWall = 0
        self.rightWall = SCREEN_WIDTH

    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)   
        pygame.draw.rect(SCREEN, (0, 0, 0), self.hitbox, 2)
        
    def check_collision_x(self, obj):
        #if obj is left of self return -1, obj right of self return -1, else return 0
        if(self.hitbox.left>obj.hitbox.right): return -1 
        if(self.hitbox.right<obj.hitbox.left): return 1 
        return 0
    
    def check_collision_y(self, obj):
        #if obj is above self return -1, obj below self return -1, else return 0
        if(self.hitbox.top>=obj.hitbox.bottom): return -1
        if(self.hitbox.bottom<=obj.hitbox.top): return 1
        return 0
    
    def update(self, obj):

        # checks if there is a collision within x coord
        if not self.check_collision_x(obj) :

            # checks if object is above movable object
            if self.check_collision_y(obj) == -1 :
                obj.floor = min(obj.floor, self.hitbox.top)

            # checks if object is within movable object's y coord
            elif not self.check_collision_y(obj) :
                
                # moves the movable object away from the object based on which side the object is
                if(obj.hitbox.centerx>self.hitbox.centerx):
                    self.x -= (2*self.velocity)
                elif(obj.hitbox.centerx<self.hitbox.centerx):
                    self.x += (2*self.velocity)

    
class player:

    def __init__(self, x, y, image) :
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)

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
        self.roof = -INF
        self.leftWall = 0
        self.rightWall = SCREEN_WIDTH

    def draw(self) :
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(player_obj.image, player_obj.hitbox)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)

    def moveLeft(self) :
        if(self.hitbox.left - self.velocity >= self.leftWall): 
            self.x -= self.velocity

    def moveRight(self) :
        if(self.hitbox.right + self.velocity <= self.rightWall): 
            self.x += self.velocity

    def resetJump(self) :
        self.jump_counter = self.time_of_flight
        self.jumping = 0


    # when jump is initiated by pressing space bar
    def jump(self, height) : 
            # handles jump according to the roof and floor set by other objects
            if((self.y - height*self.jump_counter) <= self.floor) or (self.jump_counter >= 0) :
                self.y = max(self.y - height*self.jump_counter, self.roof + self.hitbox.height)

                # if jump reaches roof, stop further jump
                if(self.y == self.roof + self.hitbox.height) :
                    self.jump_counter = 0

                self.jump_counter -= 1      # to simulate gravity

            # reached floor again after jump
            else:
                self.resetJump()
                self.y = self.floor

    # when player is falling from a height (not jumping)
    def fall(self, weight):
        # handles fall according to the floor set by other objects
        if((self.y + weight*self.fall_counter) <= self.floor):
            self.y = self.y + weight*self.fall_counter
            self.fall_counter += 1

        # reached the floor
        else:
            self.fall_counter = 0
            self.y = self.floor        

    def update(self):
        if(self.y != self.floor and not self.jumping):
            self.fall(0.4)    
        if(self.jumping):
            self.jump(0.8)
        if(self.movingLeft):
            self.moveLeft()
        elif(self.movingRight):
            self.moveRight()


class ground:
    def __init__(self, y, image, width=1, height=1):
        self.image = pygame.image.load(image)
        # self.image = pygame.transform.scale(self.image, (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.top = y
        self.hitbox.left = 0
    
    def draw(self):
        SCREEN.blit(self.image, self.hitbox)


##########################################

if __name__ == "__main__":
    clock = pygame.time.Clock()

    movable_objects_list = [movable_objects(200, 400, "./assets/image3.png", 90, 70),
                            movable_objects(400, 400, "./assets/image3.png", 90, 150)]

    immovable_objects_list = [immovable_objects(550, 185, "./assets/ground.jpeg", 400, 90)]

    ground_obj = ground(400, "./assets/ground.jpeg")
    player_obj = player(100, 400, "./assets/player.png")

    while (run):
        clock.tick(60)
        SCREEN.fill((24,255,255))

        player_obj.floor=400
        player_obj.roof = -INF
        player_obj.leftWall = 0
        player_obj.rightWall = SCREEN_WIDTH

        # Updating objects
        for platform in immovable_objects_list:
            platform.update(player_obj)
        
        for box in movable_objects_list:
            for other_box in movable_objects_list:
                if box != other_box:
                    box.update(other_box)

        for box in movable_objects_list:
            box.update(player_obj)

        player_obj.update()
        # print(player_obj.roof)
        
        # Drawing objects
        for box in movable_objects_list:
            box.draw()

        for platform in immovable_objects_list:
            platform.draw()

        player_obj.draw()
        ground_obj.draw()

        # Checks for events like keypresses
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