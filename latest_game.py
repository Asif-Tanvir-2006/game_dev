import pygame
from systems.input import handle_key_presses, helper_menu
from systems.draw import draw_all, reset_screen
import systems.update as Update
from core.wrappers import wrapper_objects

objects = wrapper_objects()
clock = pygame.time.Clock()

#############################################
# PROGRAM ENTRY POINT
#############################################
if __name__ == "__main__":

    run = True
    helper_menu()

    while run:
        Update.update_FPS(clock, 100)

        reset_screen()
        Update.reinitalise_params(objects)

        Update.update_player_wrt_immovable(objects)
        Update.update_movables_wrt_immovables(objects)

        Update.update_movables_wrt_player(objects)
        Update.update_movables_wrt_other_movables(objects)

        Update.check_fall_movables(objects)
        Update.update_player(objects)

        draw_all(objects)

        run = handle_key_presses(objects)
        pygame.display.update()