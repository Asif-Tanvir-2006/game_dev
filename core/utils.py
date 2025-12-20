import pygame


#############################################
# Screen Setup
#############################################

def load_spritesheet(path, frame_width, frame_height, num_frames, scale=1):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []

    for i in range(num_frames):
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))

        if scale != 1:
            frame = pygame.transform.scale(
                frame,
                (int(frame_width * scale), int(frame_height * scale))
            )

        frames.append(frame)

    return frames