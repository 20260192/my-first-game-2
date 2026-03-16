import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fancy Particle Playground")

clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 6)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(50, 90)
        self.max_life = self.life

        self.size = random.randint(4, 8)

        self.color = [
            random.randint(150,255),
            random.randint(120,255),
            random.randint(180,255)
        ]

    def update(self):

        self.x += self.vx
        self.y += self.vy

        # gravity
        self.vy += 0.08

        # slight drag
        self.vx *= 0.99
        self.vy *= 0.99

        # color fade
        self.color[1] = max(0, self.color[1] - 0.5)

        self.life -= 1

    def draw(self, surf):

        if self.life <= 0:
            return

        life_ratio = self.life / self.max_life
        size = int(self.size * life_ratio)

        # glow surface
        glow_size = int(size * 2.5)
        glow = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (*self.color, 40),
            (glow_size, glow_size),
            glow_size
        )

        surf.blit(glow, (self.x - glow_size, self.y - glow_size))

        pygame.draw.circle(
            surf,
            self.color,
            (int(self.x), int(self.y)),
            max(1, size)
        )

    def alive(self):
        return self.life > 0


def draw_background(surface, t):

    for y in range(HEIGHT):

        r = int(20 + 10 * math.sin(t + y * 0.02))
        g = int(40 + 25 * math.sin(t + y * 0.01))
        b = int(80 + 30 * math.sin(t + y * 0.015))

        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


running = True
time = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    if buttons[0]:
        for _ in range(10):
            particles.append(Particle(mouse[0], mouse[1]))

    time += 0.03

    draw_background(screen, time)

    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()