from core.constants import INF, SCREEN_WIDTH
from core.game_objects import immovable_objects


def update_player_wrt_immovable(objects):
    for immovable_object in objects.immovable_objects_list:
        immovable_object.update(objects.player_obj)

def update_movables_wrt_player(objects):
    for box in objects.movable_objects_list:
        box.update(objects.player_obj, objects.player_obj)

def update_movables_wrt_other_movables(objects):
    for box in objects.movable_objects_list:
        for other_box in objects.movable_objects_list:
            if box != other_box:
                box.update(other_box, objects.player_obj)

def update_movables_wrt_immovables(objects):
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

def update_player(objects):
    objects.player_obj.update()

def update_FPS(clock, fps):
    clock.tick(fps)

def check_fall_movables(objects):
    for mov in objects.movable_objects_list:
        mov.fall(0.7)



def reinitalise_params(objects):
    objects.player_obj.floor = 800
    objects.player_obj.roof = -INF
    objects.player_obj.leftWall = 0
    objects.player_obj.velocity = 5
    objects.player_obj.rightWall = SCREEN_WIDTH
    objects.player_obj.can_move_right = 1
    objects.player_obj.can_move_left = 1
        
    # objects.player_obj.hitbox.width = objects.player_obj.idle_width
         
    for mov in objects.movable_objects_list:
        mov.floor = 800
        mov.leftWall = -INF
        mov.rightWall = INF
        if(mov.y!=mov.floor):
            mov.can_move_left = 1
            mov.can_move_right = 1