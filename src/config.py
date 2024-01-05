import math
import pygame
from collections import namedtuple

# pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 25)
pygame.display.set_caption("Orbit Simulation")

# colors
Color = namedtuple("Color", ["r", "g", "b"])
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
YELLOW = Color(255, 255, 0)
BLUE = Color(70, 100, 240)
RED = Color(255, 60, 0)
DARK_RED = Color(150, 0, 0)
DARK_GRAY = Color(50, 50, 50)
LIGHT_BROWN = Color(200, 150, 100)
DARK_YELLOW = Color(200, 150, 0)
LIGHT_BLUE = Color(0, 150, 255)

# astronomical constants
AU = 149_597_870_700  # meters
G = 6.67408e-11  # m^3 kg^-1 s^-2

# math constants
TIME_SCALE = 3600 * 24  # 1 standard day

# drawing constants
SCALE = 100 / AU  # pixels per meter
RADIUS_SCALE = 6  # scale radius of planets
def RADIUS_RESIZE(r): return math.log(r/100, 100)


def main_step(system, tick=0) -> bool:
    run = True
    CLOCK.tick(tick)
    WINDOW.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if user manually quits
            run = False

    # main simulation loop
    system.update()
    system.draw(WINDOW)

    return run
