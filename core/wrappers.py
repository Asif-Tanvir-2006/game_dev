import core.game_objects as game_obj

from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT 


#############################################
# WRAPPER CLASS (HOLDS ALL OBJECTS)
#############################################
class wrapper_objects:
    def __init__(self):
        

        # First two immovables define screen bounds
        self.immovable_objects_list = [
            game_obj.immovable_objects(0, SCREEN_HEIGHT, "./assets/RTS_Crate.png", 1, 1000),
            game_obj.immovable_objects(SCREEN_WIDTH, SCREEN_HEIGHT, "./assets/RTS_Crate.png", 1, 1000),
            
            
            ############platforms
            ##x, y           image width height
            game_obj.immovable_objects(550, 550, "./assets/ground.png", 400, 90),
            game_obj.immovable_objects(1300, 250, "./assets/ground.png", 1000, 90),
        ]

        self.ground_obj = game_obj.ground(800, "./assets/ground.png")
        # self.player_obj = game_obj.player(100, 100, 1)
        self.timmy = game_obj.player(100, 100, 0.5)
        self.rani_masi = game_obj.player(100, 600, 1)
        self.shaun = game_obj.player(100, 300, 0.8)
        self.sheeps = [self.timmy, self.rani_masi, self.shaun]
        # self.player_obj1 = player(200, 100, "./assets/sheep_walk.png")
        # self.player_obj2 = player(300, 100, "./assets/sheep_walk.png")
        self.movable_objects_list = [
            # movable_objects(1000, 0, "./assets/RTS_Crate.png", 165, 165),
            # movable_objects(1200, 0, "./assets/RTS_Crate.png", 200, 420),
            game_obj.movable_objects(1600, 600, "./assets/RTS_Crate.png", 165, 165),
            game_obj.movable_objects(700, 0, "./assets/RTS_Crate.png", 200, 300),
            game_obj.movable_objects(450, 0, "./assets/RTS_Crate.png", 165, 165),
            self.rani_masi, self.timmy   
        ]
        self.player_obj = self.shaun
        
        self.skybox = game_obj.sky("./assets/sky.jpg")
        self.tree_obj = game_obj.background_objects("./assets/tree.png", 500, 500, 100, 845)
        self.tractor_obj = game_obj.background_objects("./assets/tra.png", 500, 500, 900, 880)
        self.sign_obj = game_obj.background_objects("./assets/sign.png", 200, 200, 1700, 200)