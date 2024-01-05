import os
import math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from src.config import *
from src.body import Body, System


def main():
    run = True
    max_orbit_length = 10000
    scale = 10 / AU  # pixels per meter
    time_delta = 3600 * 24  # 1 standard day

    # setup bodies (sirius system, initial velocity are guessed)
    siriusA = Body(10 * AU, 0, radius=6e8, color=DARK_YELLOW, mass=2.02 * 1.989e30,
                   initial_velocity=(0, 2e3), max_orbit_length=max_orbit_length)
    siriusB = Body(-10 * AU, 0, radius=6e8, color=RED, mass=1.01 * 1.989e30,
                   initial_velocity=(0, -5e3), max_orbit_length=max_orbit_length)
    planetoid = Body(0, 0, radius=6e6, color=BLUE, mass=1e22,
                     initial_velocity=(1e3, 1e4), max_orbit_length=max_orbit_length)

    celestial_bodies = [siriusA, siriusB, planetoid]
    system = System(celestial_bodies, time_delta=time_delta, scale=scale)

    while run:
        run = main_step(system)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
