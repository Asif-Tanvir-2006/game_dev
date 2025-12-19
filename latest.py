import pygame

pygame.init()

#############################################
# Global Constants & Screen Setup
#############################################
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
INF = 1e10

#############################################
# IMMUTABLE / STATIC OBJECTS (PLATFORMS, WALLS)
#############################################
class immovable_objects:

    def __init__(self, x, y, image, width, height):
        self.x = x
        self.y = y

        # Load and scale image
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))

        # Create hitbox
        self.hitbox = self.image.get_rect()
        self.hitbox.left = self.x
        self.hitbox.bottom = self.y

        # self.velocity = 4

    def draw(self):
        # Sync hitbox with position
        self.hitbox.left = self.x
        self.hitbox.bottom = self.y

        SCREEN.blit(self.image, self.hitbox)
        pygame.draw.rect(SCREEN, (0, 0, 0), self.hitbox, 2)

    def check_collision_x(self, obj):
        # If obj is left of self return -1
        # If obj is right of self return 1
        # Else return 0
        if self.hitbox.left > obj.hitbox.right:
            return -1
        elif self.hitbox.right < obj.hitbox.left:
            return 1
        return 0

    def check_collision_y(self, obj):
        # If obj is above self return -1
        # If obj is below self return 1
        # Else return 0
        if self.hitbox.top >= obj.hitbox.bottom:
            return -1
        elif self.hitbox.bottom <= obj.hitbox.top:
            return 1
        return 0

    def update(self, obj):
        # Checks if there is a collision within x-coordinates
        if not self.check_collision_x(obj):

            # Object is above immovable
            if self.check_collision_y(obj) == -1:
                obj.floor = min(self.hitbox.top, obj.floor)

            # Object is below immovable
            elif self.check_collision_y(obj) == 1:
                obj.roof = self.hitbox.bottom

            # Object is colliding horizontally
            else:
                # Assign wall based on relative position
                if self.hitbox.centerx > obj.hitbox.centerx:
                    obj.rightWall = self.hitbox.left
                elif self.hitbox.centerx < obj.hitbox.centerx:
                    obj.leftWall = self.hitbox.right

    def update_movables(self, obj):
        # Checks if there is a collision within x-coordinates
        if not self.check_collision_x(obj):

            # Movable object is above
            if self.check_collision_y(obj) == -1:
                obj.floor = min(self.hitbox.top, obj.floor)
                return 0

            # Movable object collides vertically
            elif not self.check_collision_y(obj):
                if(obj.hitbox.centerx<self.hitbox.centerx):
                    obj.can_move_right = 0
                elif(obj.hitbox.centerx>self.hitbox.centerx):
                    obj.can_move_left = 0
            return 0

#############################################
# MOVABLE OBJECTS (BOXES)
#############################################

class movable_objects:

    def __init__(self, x, y, image, width=1, height=1):
        self.image_path = image
        self.x = x
        self.y = y

        # Load and scale image
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.can_move_right = 1
        self.can_move_left = 1
        
        # Create hitbox
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y

        # Physics properties
        self.floor = 400
        self.roof = -INF
        self.fall_counter = 0

    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)
        pygame.draw.rect(SCREEN, (0, 0, 0), self.hitbox, 2)

    def check_collision_x(self, obj):
        # If obj is left return -1
        # If obj is right return 1
        # Else return 0
        if self.hitbox.left > obj.hitbox.right:
            return -1
        elif self.hitbox.right < obj.hitbox.left:
            return 1
        return 0

    def check_collision_y(self, obj):
        # If obj is above return -1
        # If obj is below return 1
        # Else return 0
        if self.hitbox.top >= obj.hitbox.bottom:
            return -1
        elif self.hitbox.bottom <= obj.hitbox.top:
            return 1
        return 0

    def fall(self, weight):
        if self.y + self.fall_counter * weight <= self.floor:
            self.y = self.y + self.fall_counter * weight
            self.fall_counter += 1
        else:
            # self.can_move_left = 1
            # self.can_move_right = 1
            self.y = self.floor
            self.fall_counter = 0

    def update(self, obj, player_obj):
        # Checks if there is a collision within x-coordinates
        if not self.check_collision_x(obj):

            # Object is above this movable
            if self.check_collision_y(obj) == -1:
                obj.floor = min(obj.floor, self.hitbox.top)

            # Object is colliding vertically
            elif not self.check_collision_y(obj):
                if(not self.can_move_right and self.hitbox.centerx>obj.hitbox.centerx):
                    obj.can_move_right = self.can_move_right
                if(not self.can_move_left and self.hitbox.centerx<obj.hitbox.centerx):
                    obj.can_move_left = self.can_move_left

                # Player pushing right

                if obj.hitbox.centerx < self.hitbox.centerx and player_obj.hitbox.centerx < self.hitbox.centerx and self.can_move_right:
                    self.can_move_left=1
                    self.hitbox.left = obj.hitbox.right
                    self.x = self.hitbox.centerx
                    

                # Player pushing left
                elif obj.hitbox.centerx > self.hitbox.centerx and player_obj.hitbox.centerx > self.hitbox.centerx and self.can_move_left:
                    self.can_move_right = 1
                    print(self.can_move_right)
                    print("alpha")
                    self.hitbox.right = obj.hitbox.left
                    self.x = self.hitbox.centerx



#############################################
# PLAYER CLASS
#############################################
class player:

    def __init__(self, x, y, image):
        self.x = x
        self.y = y

        self.image = pygame.image.load(image)
        self.hitbox = self.image.get_rect()
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        self.can_move_right = 1
        self.can_move_left = 1
        # Movement state
        self.in_motion = 1
        self.movingLeft = 0
        self.movingRight = 0
        self.jumping = 0

        # Jump physics
        self.time_of_flight = 20
        self.jump_counter = self.time_of_flight
        self.velocity = 4

        # Collision constraints
        self.floor = self.y
        self.fall_counter = 0
        self.roof = -INF
        self.leftWall = 0
        self.rightWall = SCREEN_WIDTH

    def draw(self):
        self.hitbox.centerx = self.x
        self.hitbox.bottom = self.y
        SCREEN.blit(self.image, self.hitbox)
        pygame.draw.rect(SCREEN, (0, 0, 255), self.hitbox, 3)

    def moveLeft(self):
        if(not self.can_move_left):
            return
        if self.hitbox.left - self.velocity >= self.leftWall:
            self.x -= self.velocity
        else:
            self.x = self.leftWall + self.hitbox.width / 2

    def moveRight(self):
        if(not self.can_move_right):
            return
        if self.hitbox.right + self.velocity <= self.rightWall:
            self.x += self.velocity
        else:
            self.x = self.rightWall - self.hitbox.width / 2
            print("wow")

    def resetJump(self):
        self.jump_counter = self.time_of_flight
        self.jumping = 0

    def jump(self, height):
        # Handles jump relative to roof and floor
        if (self.y - height * self.jump_counter) <= self.floor or self.jump_counter >= 0:
            self.y = max(self.y - height * self.jump_counter, self.roof + self.hitbox.height)

            if self.y == self.roof + self.hitbox.height:
                self.jump_counter = 0

            self.jump_counter -= 1
        else:
            self.resetJump()
            self.y = self.floor

    def fall(self, weight):
        if (self.y + weight * self.fall_counter) <= self.floor:
            self.y = self.y + weight * self.fall_counter
            self.fall_counter += 1
        else:
            self.fall_counter = 0
            self.y = self.floor

    def update(self):
        if self.y != self.floor and not self.jumping:
            self.fall(0.7)
        if self.jumping:
            self.jump(0.8)
        if self.movingLeft:
            self.moveLeft()
        elif self.movingRight:
            self.moveRight()


#############################################
# GROUND CLASS
#############################################
class ground:
    def __init__(self, y, image, width=1920, height=290):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.top = y
        self.hitbox.left = 0

    def draw(self):
        SCREEN.blit(self.image, self.hitbox)
        pygame.draw.rect(SCREEN, (0, 0, 0), self.hitbox, 3)
        

class sky:
    def __init__(self, image, width=1920, height=1080):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.top = 0
        self.hitbox.left = 0

    def draw(self):
        SCREEN.blit(self.image, self.hitbox)
class background_objects:
    def __init__(self, image, width, height, x, y):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.bottom = y
        self.hitbox.left = x

    def draw(self):
        SCREEN.blit(self.image, self.hitbox)
#############################################
# WRAPPER CLASS (HOLDS ALL OBJECTS)
#############################################
class wrapper_objects:
    def __init__(self):
        self.movable_objects_list = [
            # movable_objects(1000, 0, "./assets/RTS_Crate.png", 165, 165),
            # movable_objects(1200, 0, "./assets/RTS_Crate.png", 200, 420),
            movable_objects(1600, 0, "./assets/RTS_Crate.png", 165, 165),
            movable_objects(1400, 0, "./assets/RTS_Crate.png", 330, 330),
        ]

        # First two immovables define screen bounds
        self.immovable_objects_list = [
            immovable_objects(0, SCREEN_HEIGHT, "./assets/image3.png", 1, 1000),
            immovable_objects(SCREEN_WIDTH, SCREEN_HEIGHT, "./assets/image3.png", 1, 1000),
            
            
            ############platforms
            immovable_objects(550, 400, "./assets/ground.png", 400, 90),
        ]

        self.ground_obj = ground(800, "./assets/ground.png")
        self.player_obj = player(100, 400, "./assets/player.png")
        self.skybox = sky("./assets/sky.jpg")
        self.tree_obj = background_objects("./assets/tree.png", 500, 500, 100, 845)
        self.tractor_obj = background_objects("./assets/tra.png", 500, 500, 700, 880)
#############################################
# MAIN LOOP HELPERS
#############################################
objects = wrapper_objects()
clock = pygame.time.Clock()

def helper_menu():
    print("Game Started")
    print("Shortcuts : ")
    print("\tPress 'A' to move left")
    print("\tPress 'D' to move right")
    print("\tPress 'SPACE' to jump")
    print("\tPress 'ESCAPE' to quit")

def reinitalise_params():
    objects.player_obj.floor = 800
    objects.player_obj.roof = -INF
    objects.player_obj.leftWall = 0
    objects.player_obj.velocity = 8
    objects.player_obj.rightWall = SCREEN_WIDTH
    objects.player_obj.can_move_right = 1
    objects.player_obj.can_move_left = 1
    
    for mov in objects.movable_objects_list:
        mov.floor = 800
        mov.leftWall = -INF
        mov.rightWall = INF
        if(mov.y!=mov.floor):
            mov.can_move_left = 1
            mov.can_move_right = 1

def draw_all():
    objects.skybox.draw()
    objects.tree_obj.draw()
    objects.tractor_obj.draw()
    for platform in objects.immovable_objects_list:
        platform.draw()
    
    for box in objects.movable_objects_list:
        box.draw()
    
    objects.player_obj.draw()
    objects.ground_obj.draw()
def update_player_wrt_immovable():
    for immovable_object in objects.immovable_objects_list:
        immovable_object.update(objects.player_obj)

def update_movables_wrt_player():
    for box in objects.movable_objects_list:
        box.update(objects.player_obj, objects.player_obj)

def update_movables_wrt_other_movables():
    for box in objects.movable_objects_list:
        for other_box in objects.movable_objects_list:
            if box != other_box:
                box.update(other_box, objects.player_obj)

def update_movables_wrt_immovables():
    to_convert = []
    for mov in objects.movable_objects_list:
        for immov in objects.immovable_objects_list:
            if immov.update_movables(mov):
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
                    mov.hitbox.height,
                )
            )

def check_fall_movables():
    for mov in objects.movable_objects_list:
        mov.fall(0.7)

def update_player():
    objects.player_obj.update()

def reset_screen():
    SCREEN.fill((24, 255, 255))

def update_FPS(fps):
    clock.tick(fps)

def handle_key_presses():
    run = 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_a:
                objects.player_obj.movingLeft = 1
                objects.player_obj.movingRight = 0
            elif event.key == pygame.K_d:
                objects.player_obj.movingRight = 1
                objects.player_obj.movingLeft = 0
            elif event.key == pygame.K_SPACE:
                objects.player_obj.jumping = 1
            elif event.key == pygame.K_w:
                objects.player_obj.y -= 700
            elif event.key == pygame.K_s:
                objects.player_obj.y += 135

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                objects.player_obj.movingLeft = 0
            elif event.key == pygame.K_d:
                objects.player_obj.movingRight = 0

    return run


#############################################
# PROGRAM ENTRY POINT
#############################################
if __name__ == "__main__":

    run = True
    helper_menu()

    while run:
        update_FPS(100)

        reset_screen()
        reinitalise_params()

        update_player_wrt_immovable()
        update_movables_wrt_immovables()

        update_movables_wrt_player()
        update_movables_wrt_other_movables()

        check_fall_movables()
        update_player()

        draw_all()

        run = handle_key_presses()
        pygame.display.update()
