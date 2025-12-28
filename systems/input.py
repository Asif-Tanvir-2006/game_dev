import pygame

def helper_menu():
    print("Game Started")
    print("Shortcuts : ")
    print("\tPress 'A' to move left")
    print("\tPress 'D' to move right")
    print("\tPress 'SPACE' to jump")
    print("\tPress 'ESCAPE' to quit")


def switch_player(objects, new_player):
    # Put current player back into movable list
    if objects.player_obj not in objects.movable_objects_list:
        objects.movable_objects_list.append(objects.player_obj)

    # Switch player
    objects.player_obj = new_player
    objects.player_obj.roof = 0

    # Remove new player from movable list
    if new_player in objects.movable_objects_list:
        objects.movable_objects_list.remove(new_player)


def handle_key_presses(objects):
    for event in pygame.event.get():

        # ---------- QUIT ----------
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return False

            # ---------- CHARACTER SWITCH ----------
            if event.key == pygame.K_s:
                switch_player(objects, objects.shaun)

            elif event.key == pygame.K_t:
                switch_player(objects, objects.timmy)

            elif event.key == pygame.K_r:
                switch_player(objects, objects.rani_masi)

            # ---------- MOVEMENT ----------
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

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                objects.player_obj.movingLeft = 0
            elif event.key == pygame.K_d:
                objects.player_obj.movingRight = 0

    return True
