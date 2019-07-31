import sys
import pygame
import random

size = width, height = 400, 300
fps = 60
alpha = -2
gama = -1
m_pred = 0.8
m_prey = 1


class Predator(object):
    def __init__(self):
        self.pos = [random.random()*width, random.random()*height]
        self.v = [0, 0]
        self.dx, self.dy = 0, 0
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 23, 23)
        self.image = pygame.image.load("predator.png")


class Prey(object):
    def __init__(self):
        self.pos = [random.random()*width, random.random()*height]
        self.v = [0, 0]
        self.dx, self.dy = 0, 0
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 23, 23)
        self.image = pygame.image.load("prey.png")


def FrameInit():
    screen.fill((0, 0, 0))
    screen.blit(predator.image, predator.rect)
    screen.blit(prey.image, prey.rect)
    pygame.display.update()


def FrameUpdate():
    a = long_rang_force(predator.pos, prey.pos)
    predator.v[0] = predator.v[0] + a[0]/m_pred
    predator.v[1] = predator.v[1] + a[1]/m_pred
    # print(predator.v)
    predator.pos[0] = predator.pos[0] + predator.v[0]
    predator.pos[1] = predator.pos[1] + predator.v[1]
    predator.dx = predator.dx + predator.v[0]
    predator.dy = predator.dy + predator.v[1]
    # print(predator.dx, predator.dy)
    if abs(predator.dx) > 1 or abs(predator.dy) > 1:
        predator.rect = predator.rect.move([predator.dx/1, predator.dy/1])
        predator.dx = predator.dx % (abs(predator.dx)/predator.dx)
        predator.dy = predator.dy % (abs(predator.dy)/predator.dy)

    a = long_rang_force(prey.pos, predator.pos)
    prey.v[0] = prey.v[0] - a[0]/m_prey
    prey.v[1] = prey.v[1] - a[1]/m_prey
    prey.pos[0] = prey.pos[0] + prey.v[0]
    prey.pos[1] = prey.pos[1] + prey.v[1]
    prey.dx = prey.dx + prey.v[0]
    prey.dy = prey.dy + prey.v[1]
    if abs(prey.dx) > 1 or abs(prey.dy) > 1:
        prey.rect = prey.rect.move([prey.dx/1, prey.dy/1])
        prey.dx = prey.dx % (abs(prey.dx)/prey.dx)
        prey.dy = prey.dy % (abs(prey.dy)/prey.dy)

    screen.fill((0, 0, 0))
    screen.blit(predator.image, predator.rect)
    screen.blit(prey.image, prey.rect)
    pygame.display.update()


def short_rang_force(posi, posj):
    # short-rang force acting on agent i due to agent j
    r2ij = ((posj[0]-posi[0])**2+(posj[1]-posi[1])**2)
    # print("r2ij:", r2ij)
    force = [
        r2ij**((alpha-1)/2)*(posj[0]-posi[0]),
        r2ij**((alpha-1)/2)*(posj[1]-posi[1])]
    # print("short rang force: ", force)
    return force


def long_rang_force(posi, posj):
    # long-rang force acting on agent i due to agent j
    r2ij = ((posj[0]-posi[0])**2+(posj[1]-posi[1])**2)
    # print("r2ij:", r2ij)
    force = [
        r2ij**((alpha-1)/2)*(posj[0]-posi[0]),
        r2ij**((alpha-1)/2)*(posj[1]-posi[1])]
    # print("long rang force: ", force)
    return force


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Swarming Mode")
    clock = pygame.time.Clock()
    predator = Predator()
    prey = Prey()
    FrameInit()
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                size = width, height = event.size
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fps = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    fps = 60
        FrameUpdate()
    pygame.quit()
