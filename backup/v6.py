import pygame
# import clo

pygame.init()
#400 is the default level of floor where everything spawns

#############################################
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
INF = 1e10


#############################################
class immovable_objects:

    def __init__(self, x, y, image, width, height) :
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image , (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.left = self.x
        self.hitbox.bottom = self.y
        self.velocity = 4

    def draw(self) :
        self.hitbox.left = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)   
        pygame.draw.rect(SCREEN, (0, 0, 0), self.hitbox, 2)
        
    def check_collision_x(self, obj) :
        #if obj is left of self return -1, obj right of self return 1, else return 0
        if(self.hitbox.left > obj.hitbox.right) : return -1 
        elif(self.hitbox.right < obj.hitbox.left) : return 1 
        return 0
    
    def check_collision_y(self, obj) :
        #if obj is above self return -1, obj below self return 1, else return 0
        if(self.hitbox.top >= obj.hitbox.bottom) : return -1
        elif(self.hitbox.bottom <= obj.hitbox.top) : return 1
        return 0
    
    def update(self, obj) :
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
                if(self.hitbox.centerx > obj.hitbox.centerx) :
                    obj.rightWall = self.hitbox.left
                elif(self.hitbox.centerx < obj.hitbox.centerx) :
                    obj.leftWall = self.hitbox.right

    def update_movables(self, obj) :
        # checks if there is a collision within x coord
        if not self.check_collision_x(obj) :

            # checks if object is above immovable object
            if (self.check_collision_y(obj) == -1) :
                obj.floor = min(self.hitbox.top, obj.floor)
                return 0
            # checks if object is colliding with immovable object in y coords
            elif not (self.check_collision_y(obj)) :
                return 1 # obj is ready for conversion from movable to immovable
                

class movable_objects:

    def __init__(self, x, y, image, width = 1, height = 1) :
        self.image_path = image
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width,height))
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        self.velocity = 4

        self.floor = 400
        self.roof = -INF
        self.leftWall = 0
        self.rightWall = SCREEN_WIDTH
        self.fall_counter = 0


    def draw(self) :
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)   
        pygame.draw.rect(SCREEN, (0, 0, 0), self.hitbox, 2)
    def check_collision_x(self, obj) :
        #if obj is left of self return -1, obj right of self return -1, else return 0
        if(self.hitbox.left > obj.hitbox.right) : return -1 
        elif(self.hitbox.right < obj.hitbox.left) : return 1 
        return 0
    
    def check_collision_y(self, obj) :
        #if obj is above self return -1, obj below self return -1, else return 0
        if(self.hitbox.top >= obj.hitbox.bottom) : return -1
        elif(self.hitbox.bottom <= obj.hitbox.top) : return 1
        return 0
    
    def fall(self, weight) :
        if(self.y + self.fall_counter * weight <= self.floor) :
            self.y = self.y+self.fall_counter * weight
            self.fall_counter +=1
        else:
            self.y = self.floor
            self.fall_counter = 0

    def update(self, obj, is_player=0) :
        # checks if there is a collision within x coord
        if not self.check_collision_x(obj) :

            # checks if object is above movable object
            if self.check_collision_y(obj) == -1 :
                obj.floor = min(obj.floor, self.hitbox.top)

            # checks if object is within movable object's y coord
            elif not self.check_collision_y(obj) :
                self.velocity += obj.velocity/100
                obj.velocity -= self.velocity/100
                # if(is_player) : 
                    # obj.velocity = max(0.5, obj.velocity-0.3)
                # moves the movable object away from the object based on which side the object is
                if(obj.hitbox.centerx > self.hitbox.centerx) :
                    
                    self.x -= (self.velocity)
                    
                elif(obj.hitbox.centerx < self.hitbox.centerx) :
                    self.x += (self.velocity)

    
class player:

    def __init__(self, x, y, image) :
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
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
        SCREEN.blit(self.image, self.hitbox)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hitbox, 2)

    def moveLeft(self) :
        if(self.hitbox.left - self.velocity >= self.leftWall) : 
            self.x -= self.velocity

    def moveRight(self) :
        if(self.hitbox.right + self.velocity <= self.rightWall) : 
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
    def fall(self, weight) :
        # handles fall according to the floor set by other objects
        if((self.y + weight*self.fall_counter) <= self.floor) :
            self.y = self.y + weight*self.fall_counter
            self.fall_counter += 1

        # reached the floor
        else:
            self.fall_counter = 0
            self.y = self.floor        

    # updates player position based on movement and jump/fall status
    def update(self) :
        if(self.y != self.floor and not self.jumping) :
            self.fall(0.7)    
        if(self.jumping) :
            self.jump(0.8)
        if(self.movingLeft) :
            self.moveLeft()
        elif(self.movingRight) :
            self.moveRight()


class ground:
    def __init__(self, y, image, width = 1920, height = 290) :
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.top = y
        self.hitbox.left = 0
    
    def draw(self) :
        SCREEN.blit(self.image, self.hitbox)

# Class to hold all objects being used in-game
##########################################
class wrapper_objects:
    def __init__(self) :
        self.movable_objects_list = [
                            movable_objects(590, 0, "./assets/image3.png", 90, 30), 
                            movable_objects(300, 0, "./assets/image3.png", 90, 165),
                            movable_objects(430, 0, "./assets/image3.png", 70, 325),
                            ]
        ## the first two immovable objects are left and right limits of the screen.
        self.immovable_objects_list = [immovable_objects(0, SCREEN_HEIGHT, "./assets/image3.png", 1, 1000), 
                                       immovable_objects(SCREEN_WIDTH, SCREEN_HEIGHT, "./assets/image3.png", 1, 1000), 
                                       immovable_objects(550, 400, "./assets/ground.jpeg", 400, 90)
                                       ]

        self.ground_obj = ground(800, "./assets/ground.jpeg")
        self.player_obj = player(100, 400, "./assets/player.png")


# Main Function Loop
#################################################################################
if __name__ == "__main__" :
    clock = pygame.time.Clock()
    objects = wrapper_objects()

    run = True
    true_floor = 800
    true_velocity_player = 4

    print("Game Started")
    print("Shortcuts : ")
    print("\tPress 'A' to move left")
    print("\tPress 'D' to move right")
    print("\tPress 'SPACE' to jump")
    print("\tPress 'ESCAPE' to quit")


    while (run) :
        clock.tick(75)
        SCREEN.fill((24, 255, 255))
        if(objects.player_obj.velocity<true_velocity_player) :
                objects.player_obj.velocity = min(true_velocity_player, 0.1+objects.player_obj.velocity) 
                
        # objects.player_obj.velocity = true_velocity_player
        objects.player_obj.floor = 800
        objects.player_obj.roof = -INF
        objects.player_obj.leftWall = 0
        objects.player_obj.rightWall = SCREEN_WIDTH
        for mov in objects.movable_objects_list:
            mov.floor = 800
        
        # Updating objects
        for immovable_object in objects.immovable_objects_list:
            immovable_object.update(objects.player_obj)
        
        for box in objects.movable_objects_list:
            for other_box in objects.movable_objects_list:
                if box != other_box:
                    box.update(other_box)

        for box in objects.movable_objects_list:
            box.update(objects.player_obj, 1)

        ############checks if any movable object becomes immovable#############    
        to_convert = []
        for mov in objects.movable_objects_list:
            for immov in objects.immovable_objects_list:
                if(immov.update_movables(mov)) :
                    to_convert.append(mov)
                    break
                
        for mov in to_convert:
            if mov in objects.movable_objects_list:
                objects.movable_objects_list.remove(mov)
                objects.immovable_objects_list.append(
                    immovable_objects(
                        mov.hitbox.left,
                        mov.hitbox.bottom,
                        mov.image_path,
                        mov.hitbox.width,
                        mov.hitbox.height
                    )
                )
        for mov in objects.movable_objects_list:
            # print(mov.floor)
            mov.fall(0.7)
        objects.player_obj.update()
        
        # Drawing objects
        for box in objects.movable_objects_list:
            box.draw()

        for platform in objects.immovable_objects_list:
            platform.draw()

        objects.player_obj.draw()
        objects.ground_obj.draw()

        # Checks for events like keypresses
        for event in pygame.event.get() :
            if(event.type==pygame.KEYDOWN) :
                if (event.key==pygame.K_ESCAPE) :
                    run = False
                elif(event.key==pygame.K_a) :
                    objects.player_obj.movingLeft = 1
                    objects.player_obj.movingRight = 0
                elif(event.key==pygame.K_d) :
                    objects.player_obj.movingRight = 1
                    objects.player_obj.movingLeft = 0
                elif(event.key==pygame.K_SPACE) :
                    objects.player_obj.jumping = 1
                    
            elif(event.type==pygame.KEYUP) :
                if(event.key==pygame.K_a) :
                    objects.player_obj.movingLeft = 0
                elif(event.key==pygame.K_d) :
                    objects.player_obj.movingRight = 0

        pygame.display.update()