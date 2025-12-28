from core.constants import SCREEN


def draw_all(objects):
    objects.skybox.draw()
    objects.tree_obj.draw()
    objects.sign_obj.draw()
    objects.tractor_obj.draw()
    for platform in objects.immovable_objects_list:
        platform.draw()
    
    for box in objects.movable_objects_list:
        box.draw()
    objects.player_obj.draw()
    objects.ground_obj.draw()


def reset_screen():
    SCREEN.fill((24, 255, 255))