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
FONT = pygame.font.SysFont("comicsans", 50)
pygame.display.set_caption("Orbit Simulation")


def main():
    run = True

    # setup bodies
    sun = Body(0, 0, radius=696.240e3, color=YELLOW, mass=1.989e30)
    sun.is_sun = True
    earth = Body(-1 * AU, 0, radius=6.371e3, color=BLUE, mass=5.972e24, initial_velocity=(0, 29.78e3))
    mars = Body(-1.524 * AU, 0, radius=3.389e3, color=RED, mass=6.39e23, initial_velocity=(0, 24.077e3))
    mercury = Body(-0.387 * AU, 0, radius=2.439e3, color=DARK_GRAY, mass=3.285e23, initial_velocity=(0, 47.362e3))
    venus = Body(-0.723 * AU, 0, radius=6.051e3, color=DARK_RED, mass=4.867e24, initial_velocity=(0, 35.02e3))
    jupiter = Body(-5.203 * AU, 0, radius=69.911e3, color=LIGHT_BROWN, mass=1.898e27, initial_velocity=(0, 13.07e3))
    saturn = Body(-9.537 * AU, 0, radius=58.232e3, color=DARK_YELLOW, mass=5.683e26, initial_velocity=(0, 9.69e3))
    uranus = Body(-19.191 * AU, 0, radius=25.362e3, color=LIGHT_BLUE, mass=8.681e25, initial_velocity=(0, 6.81e3))
    neptune = Body(-30.069 * AU, 0, radius=24.622e3, color=LIGHT_BLUE, mass=1.024e26, initial_velocity=(0, 5.43e3))

    celestial_bodies = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        CLOCK.tick(60)
        WINDOW.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user manually quits
                run = False

        # main simulation loop
        for body in celestial_bodies:
            body.update(celestial_bodies)
            body.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
