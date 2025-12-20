import pygame

def helper_menu():
    print("Game Started")
    print("Shortcuts : ")
    print("\tPress 'A' to move left")
    print("\tPress 'D' to move right")
    print("\tPress 'SPACE' to jump")
    print("\tPress 'ESCAPE' to quit")

def handle_key_presses(objects):
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