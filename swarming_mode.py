import sys
import pygame
import random

size = width, height = 800, 600
fps = 0
l_fps = 60
h_fps = 0
alpha = -2
gama = 0.32
m_pred = 1
b_pred = 0.1
m_prey = 0.5
b_prey = 0.5


class Predator(object):
    def __init__(self):
        self.pos = [
            random.random()*width/5+width*0.3,
            random.random()*height/5+height*0.3]
        self.v = [0, 0]
        self.dx, self.dy = 0, 0
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 23, 23)
        self.image = pygame.image.load("predator.png")

    def move(self):
        self.pos[0] = self.pos[0] + self.v[0]
        self.pos[1] = self.pos[1] + self.v[1]
        self.dx = self.dx + self.v[0]
        self.dy = self.dy + self.v[1]
        # print(self.dx, self.dy)
        if abs(self.dx) > 1 or abs(self.dy) > 1:
            self.rect = self.rect.move([self.dx/1, self.dy/1])
            self.dx = self.dx % (abs(self.dx)/self.dx)
            self.dy = self.dy % (abs(self.dy)/self.dy)


class Prey(object):
    def __init__(self):
        self.pos = [
            random.random()*width/5+width*0.3,
            random.random()*height/5+height*0.3]
        self.v = [0, 0]
        self.dx, self.dy = 0, 0
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 23, 23)
        self.image = pygame.image.load("prey.png")

    def move(self):
        self.pos[0] = self.pos[0] + self.v[0]
        self.pos[1] = self.pos[1] + self.v[1]
        self.dx = self.dx + self.v[0]
        self.dy = self.dy + self.v[1]
        # print(self.dx, self.dy)
        if abs(self.dx) > 1 or abs(self.dy) > 1:
            self.rect = self.rect.move([self.dx/1, self.dy/1])
            self.dx = self.dx % (abs(self.dx)/self.dx)
            self.dy = self.dy % (abs(self.dy)/self.dy)


def FrameInit():
    # screen.fill((0, 0, 0))
    for Predator in predators:
        screen.blit(Predator.image, Predator.rect)
    for Prey in preys:
        screen.blit(Prey.image, Prey.rect)
    pygame.display.update()


def FrameUpdate():
    i_pred = 0
    while i_pred < len(predators):
        predators[i_pred].v[0] = (
            predators[i_pred].v[0] - b_pred*predators[i_pred].v[0])
        predators[i_pred].v[1] = (
            predators[i_pred].v[1] - b_pred*predators[i_pred].v[1])
        for Prey in preys:
            a = long_rang_force(predators[i_pred].pos, Prey.pos)
            predators[i_pred].v[0] = predators[i_pred].v[0] + a[0]/m_pred
            predators[i_pred].v[1] = predators[i_pred].v[1] + a[1]/m_pred
        j_pred = 0
        while j_pred < len(predators):
            if not i_pred == j_pred:
                c = long_rang_force(
                    predators[i_pred].pos, predators[j_pred].pos)
                predators[i_pred].v[0] = predators[i_pred].v[0] - c[0]/m_pred
                predators[i_pred].v[1] = predators[i_pred].v[1] - c[1]/m_pred
            j_pred = j_pred + 1
        i_pred = i_pred + 1
        # print("predator.v:", predator.v)

    i_prey = 0
    while i_prey < len(preys):
        preys[i_prey].v[0] = preys[i_prey].v[0] - b_prey*preys[i_prey].v[0]
        preys[i_prey].v[1] = preys[i_prey].v[1] - b_prey*preys[i_prey].v[1]
        for Predator in predators:
            a = long_rang_force(preys[i_prey].pos, Predator.pos)
            preys[i_prey].v[0] = preys[i_prey].v[0] - a[0]/m_prey
            preys[i_prey].v[1] = preys[i_prey].v[1] - a[1]/m_prey
        j_prey = 0
        while j_prey < len(preys):
            if not i_prey == j_prey:
                b = short_rang_force(preys[i_prey].pos, preys[j_prey].pos)
                c = long_rang_force(preys[i_prey].pos, preys[j_prey].pos)
                preys[i_prey].v[0] = preys[i_prey].v[0] - b[0]/m_prey
                + c[0]/m_prey
                preys[i_prey].v[1] = preys[i_prey].v[1] - b[1]/m_prey
                + c[1]/m_prey
            j_prey = j_prey + 1
        i_prey = i_prey + 1

    for Predator in predators:
        Predator.move()
    for Prey in preys:
        Prey.move()

    screen.fill((0, 0, 0))
    for Predator in predators:
        screen.blit(Predator.image, Predator.rect)
    for Prey in preys:
        screen.blit(Prey.image, Prey.rect)
    pygame.display.update()


def short_rang_force(posi, posj):
    # short-rang force acting on agent i due to agent j
    if(posi == posj):
        return 0
    else:
        r2ij = ((posj[0]-posi[0])**2+(posj[1]-posi[1])**2)
        # print("r2ij:", r2ij)
        force = [
            r2ij**((alpha-1)/2)*(posj[0]-posi[0]),
            r2ij**((alpha-1)/2)*(posj[1]-posi[1])]
        # print("short rang force: ", force)
        return force


def long_rang_force(posi, posj):
    # long-rang force acting on agent i due to agent j
    if(posi == posj):
        return 0
    else:
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
    predators = [Predator(), Predator()]
    preys = [Prey(), Prey(), Prey(), Prey(), Prey(), Prey(), Prey(), Prey()]
    FrameInit()
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                size = width, height = event.size
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                predators = [Predator(), Predator()]
                preys = [
                    Prey(), Prey(), Prey(), Prey(),
                    Prey(), Prey(), Prey(), Prey()]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fps = h_fps
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    fps = l_fps
        FrameUpdate()
    pygame.quit()
