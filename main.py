import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from src.constants import *
from src.body import Body

# pygame setup
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Orbit Simulation")


def main():
    run = True

    # setup planets
    sun = Body(0, 0, radius=696.240e3, color=YELLOW, mass=1.989e30)
    sun.is_sun = True
    earth = Body(-1 * AU, 0, radius=6.371e3, color=BLUE, mass=5.972e24, initial_velocity=(0, 29.78e3))
    mars = Body(-1.524 * AU, 0, radius=3.389e3, color=RED, mass=6.39e23, initial_velocity=(0, 24.077e3))
    mercury = Body(-0.387 * AU, 0, radius=2.439e3, color=DARK_GRAY, mass=3.285e23, initial_velocity=(0, 47.362e3))
    venus = Body(-0.723 * AU, 0, radius=6.051e3, color=DARK_RED, mass=4.867e24, initial_velocity=(0, 35.02e3))

    celestial_bodies = [sun, earth, mars, mercury, venus]

    while run:
        CLOCK.tick(60)
        WINDOW.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user manually quits
                run = False
        for body in celestial_bodies:
            body.draw(WINDOW)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
