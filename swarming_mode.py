import sys
import pygame
import pygame.freetype
import random
import math

size = width, height = 800, 600
rr = (width**2+height**2)**0.5
fps = 0
l_fps = 60
h_fps = 0
alpha = -2  # for short range force
gama = 2   # for long range force
m_pred = 1
b_pred = 1
MOD = cooperate, none, compete = 1, 0, -1
# for cooperate, + long range force between preds
# for none , no force between preds
# for compete, -long rang force between preds
mod_pred = compete
m_prey = 0.5
b_prey = 1


class Predator(object):
    def __init__(self):
        r, sita = (1+random.random())*rr*0.05, random.uniform(0, math.pi*2)
        self.pos = [
            width/2+r*math.cos(sita), height/2+r*math.sin(sita)]
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
        r, sita = random.random()*rr*0.05, random.uniform(0, math.pi*2)
        self.pos = [
            width/2+r*math.cos(sita), height/2+r*math.sin(sita)]
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
    screen.fill((0, 0, 0))
    text_draw()
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
                predators[i_pred].v[0] = (
                    predators[i_pred].v[0] + mod_pred*c[0]/m_pred)
                predators[i_pred].v[1] = (
                    predators[i_pred].v[1] + mod_pred*c[1]/m_pred)
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
    text_draw()
    for Predator in predators:
        screen.blit(Predator.image, Predator.rect)
    for Prey in preys:
        screen.blit(Prey.image, Prey.rect)
    pygame.display.update()


def text_draw():
    f1rect = font.render_to(screen, (0, 0), text1, fgcolor=(255, 251, 0))
    f2rect = font.render_to(
        screen, (0, f1rect.height), text2, fgcolor=(255, 251, 0))
    f3rect = font.render_to(
        screen, (0, f1rect.height+f2rect.height), text3, fgcolor=(255, 251, 0))
    font.render_to(
        screen, (0, f1rect.height+f2rect.height+f3rect.height),
        text4, fgcolor=(255, 251, 0))


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
    predators = [Predator(), Predator(), Predator()]
    preys = [Prey(), Prey(), Prey(), Prey(), Prey(), Prey(), Prey()]
    font = pygame.freetype.Font("C:/Windows/Fonts/msyh.ttc", 16)
    text1 = "alpha=" + str(alpha) + "    gama=" + str(gama)
    text2 = (
        "m_pred=" + str(m_pred) + "    b_pred=" + str(b_pred) +
        "    mod_pred=" + str(mod_pred))
    text3 = "m_prey=" + str(m_prey) + "    b_prey=" + str(b_prey)
    text4 = (
        "predator_count=" + str(len(predators)) +
        "    prey_count=" + str(len(preys)))
    FrameInit()
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                for Prey in preys:
                    Prey.rect = Prey.rect.move(
                        (event.size[0]-width)/2, (event.size[1]-height)/2)
                for Predator in predators:
                    Predator.rect = Predator.rect.move(
                        (event.size[0]-width)/2, (event.size[1]-height)/2)
                size = width, height = event.size
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                for Predator in predators:
                    screen.blit(Predator.image, Predator.rect)
                for Prey in preys:
                    screen.blit(Prey.image, Prey.rect)
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    if event.mod & pygame.KMOD_ALT:
                        fps = h_fps
                elif event.key == pygame.K_l:
                    if event.mod & pygame.KMOD_ALT:
                        fps = l_fps
        FrameUpdate()
    pygame.quit()
