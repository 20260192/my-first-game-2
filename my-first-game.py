import pygame
import random
import math
import colorsys

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultra Particle Engine")

clock = pygame.time.Clock()

particles = []


class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 8)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(60, 120)
        self.max_life = self.life

        self.size = random.uniform(4, 8)

        self.hue = random.random()

        self.trail = []

    def update(self):

        self.trail.append((self.x, self.y))

        if len(self.trail) > 8:
            self.trail.pop(0)

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.05

        # swirl motion
        self.vx += random.uniform(-0.05, 0.05)

        # air resistance
        self.vx *= 0.99
        self.vy *= 0.99

        self.hue += 0.003

        self.life -= 1

    def draw(self, surf):

        if self.life <= 0:
            return

        life_ratio = self.life / self.max_life

        r, g, b = colorsys.hsv_to_rgb(self.hue % 1, 0.7, 1)

        color = (int(r * 255), int(g * 255), int(b * 255))

        size = int(self.size * life_ratio)

        # draw trail
        for i, pos in enumerate(self.trail):

            t = i / len(self.trail)

            pygame.draw.circle(
                surf,
                color,
                (int(pos[0]), int(pos[1])),
                max(1, int(size * t))
            )

        # glow
        glow_size = int(size * 4)

        glow = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (*color, 40),
            (glow_size, glow_size),
            glow_size
        )

        surf.blit(glow, (self.x - glow_size, self.y - glow_size))

        pygame.draw.circle(
            surf,
            color,
            (int(self.x), int(self.y)),
            max(1, size)
        )

    def alive(self):
        return self.life > 0


def draw_background(surface, t):

    for y in range(HEIGHT):

        r = int(20 + 15 * math.sin(t + y * 0.01))
        g = int(30 + 25 * math.sin(t + y * 0.015))
        b = int(60 + 35 * math.sin(t + y * 0.02))

        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


running = True
time = 0

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            for _ in range(120):
                particles.append(Particle(mx, my))

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    if buttons[0]:

        for _ in range(10):
            particles.append(Particle(mouse[0], mouse[1]))

    time += 0.02

    draw_background(screen, time)

    for p in particles:

        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()

    clock.tick(60)

pygame.quit()