import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from src.config import *
from src.body import Body, System


def main():
    run = True
    focus_scale = 2_000_000 / AU
    time_delta = 60 # 1 standard minute

    # setup bodies
    sun = Body(0, 0, radius=696.240e6, color=YELLOW, mass=1.989e30)
    earth = Body(-1 * AU, 0, radius=6.371e6, color=BLUE, mass=5.972e24, initial_velocity=(0, 29.78e3))
    moon = Body(earth.x - earth.radius - 384e6, 0,  # earth.x + distance from earth
                radius=1.737e6, color=WHITE, mass=7.347e22, initial_velocity=(0, 29.78e3 + 1.022e3))
    mars = Body(-1.524 * AU, 0, radius=3.389e6, color=RED, mass=6.39e23, initial_velocity=(0, 24.077e3))
    mercury = Body(-0.387 * AU, 0, radius=2.439e6, color=DARK_GRAY, mass=3.285e23, initial_velocity=(0, 47.362e3))
    venus = Body(-0.723 * AU, 0, radius=6.051e6, color=DARK_RED, mass=4.867e24, initial_velocity=(0, 35.02e3))
    jupiter = Body(-5.203 * AU, 0, radius=69.911e6, color=LIGHT_BROWN, mass=1.898e27, initial_velocity=(0, 13.07e3))

    # natural moons
    phobos = Body(mars.x - mars.radius - 9e6, 0, radius=11e3, color=PINK, mass=1.0659e16,
                  initial_velocity=(0, 2.138e3 + 24.077e3))
    deimos = Body(mars.x - mars.radius - 23e6, 0, radius=6e3, color=DARK_RED, mass=1.4762e15,
                  initial_velocity=(0, 1.3513e3 + 24.077e3))

    # setup satellites
    # orbital speed is given by v = sqrt(GM/d), where M is the mass of th planet, d is the distance between them.
    orbital_speed = lambda d: math.sqrt(G * mars.mass / (mars.radius + d))

    # https://en.wikipedia.org/wiki/2001_Mars_Odyssey
    sat1 = Body(mars.x - mars.radius - 400e3, 0,
                radius=2e2, color=LIGHT_GRAY, mass=725, initial_velocity=(0, 24.077e3 + orbital_speed(400e3)))

    # https://en.wikipedia.org/wiki/Mars_Reconnaissance_Orbiter
    sat2 = Body(mars.x + mars.radius + 300e3, 0,
                radius=2e2, color=DARK_GRAY, mass=1125, initial_velocity=(0, 24.077e3 - orbital_speed(300e3)))

    celestial_bodies = [sun, moon, earth, mars, mercury, venus, jupiter, phobos, deimos, sat1, sat2]
    solar_system = System(celestial_bodies, time_delta=time_delta, focus_scale=focus_scale)

    while run:
        run = main_step(solar_system, tick=60)

        WINDOW.fill(BLACK)
        solar_system.draw_focused(WINDOW, focus=mars)

        pygame.display.update()


if __name__ == "__main__":
    main()
