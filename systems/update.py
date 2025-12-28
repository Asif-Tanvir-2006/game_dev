from core.constants import INF


def update_player_wrt_immovable(objects):
    for immovable_object in objects.immovable_objects_list:
        immovable_object.update(objects.player_obj)

def update_player_wrt_movables(objects):
    is_colliding = 0;
    for box in objects.movable_objects_list:
        is_colliding = max(is_colliding, box.update(objects.player_obj, objects.player_obj))
    if(is_colliding):
        objects.player_obj.velocity = 2.5
    else:
        objects.player_obj.velocity = 5
        
def update_movables_wrt_player(objects):
    for mov in objects.movable_objects_list:
        objects.player_obj.update(mov, objects.player_obj)
def update_movables_wrt_other_movables(objects):
    for box in objects.movable_objects_list:
        for other_box in objects.movable_objects_list:
            if box != other_box:
                box.update(other_box, objects.player_obj)

def update_movables_wrt_immovables(objects):
    for mov in objects.movable_objects_list:
        for immov in objects.immovable_objects_list:
            immov.update_movables(mov)




def update_player(objects):
    objects.player_obj.update_player()


def update_FPS(clock, fps):
    clock.tick(fps)

def check_fall_movables(objects):
    for mov in objects.movable_objects_list:
        mov.fall(0.7)



def reinitalise_params(objects):
    objects.player_obj.floor = 800
    objects.player_obj.roof = 0
    objects.player_obj.can_move_right = 1
    objects.player_obj.can_move_left = 1
        
        # objects.player_obj.hitbox.width =objects.player_obj.idle_width
         
    for mov in objects.movable_objects_list:
        mov.floor = 800
        mov.roof = 0
        mov.leftWall = -INF
        mov.rightWall = INF
        if(mov.y!=mov.floor):
            mov.can_move_left = 1
            mov.can_move_right = 1