import sys
import pygame


class Predator(object):
    def __init__(self):
        pass


class Prey(object):
    def __init__(self):
        pass


def FrameInit():
    pass


def FrameUpdate():
    pass


if __name__ == "__main__":
    pygame.init()
    size = width, height = 400, 300
    fps = 60
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Swarming Mode")
    clock = pygame.time.Clock()
    FrameInit()
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                size = width, height = event.size
        FrameUpdate()
    pygame.quit()
