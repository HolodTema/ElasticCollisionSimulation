import numpy as np
import pygame as pg
import pygame.gfxdraw
import physics as pf
from const import *

DIM = np.asarray([WINDOW_WIDTH, WINDOW_HEIGHT])
GRAVITY = np.asarray([GRAVITY_HORIZONTAL, GRAVITY_VERTICAL])
dt = ENVIRONMENT_DENSITY
env = pf.Environment(DIM, GRAVITY, dt)

n_particles = np.random.randint(MIN_PARTICLE_AMOUNT, MAX_PARTICLE_AMOUNT)
for n in range(n_particles):
    radius = np.random.randint(10, 20)
    density = np.random.randint(50, 75)
    volume = 4 / 3 * np.pi * radius ** 3
    mass = volume * density
    # it creates 1D np-array of len=2 with random float number from 0 to 1
    # we add or subtract radius not to collide borders in the beginning
    X = np.random.rand(2) * (DIM - radius) + radius
    V = np.random.rand(2) * 30
    A = np.asarray([0, 0])
    particle = pf.Particle(env, X, V, A, radius, mass, density)
    env.addParticle(particle)

pg.init()
screen = pg.display.set_mode(DIM)
pg.display.set_caption(WINDOW_TITLE)


def displayParticles(env):
    for p in env.particles:
        try:
            pg.gfxdraw.filled_circle(screen, int(p.X[0]), int(p.X[1]), p.radius, p.color)
        except OverflowError as e:
            print('OverflowError during displaying particle:', e)




running = True
while running:
    screen.fill(WINDOW_BACKGROUND_COLOR)
    env.update()
    displayParticles(env)
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
