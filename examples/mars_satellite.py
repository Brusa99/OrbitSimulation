import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from src.config import *
from src.body import Body, System, Satellite


def main():
    run = True
    focus_scale = 1_500_000 / AU
    time_delta = 60  # 1 standard minute
    bg = pygame.image.load("../src/bg1.jpg")

    # setup bodies
    sun = Body(0, 0, radius=696.240e6, color=YELLOW, mass=1.989e30, name="Sun")
    earth = Body(-1 * AU, 0, radius=6.371e6, color=BLUE, mass=5.972e24, initial_velocity=(0, 29.78e3), name="Earth")
    moon = Body(earth.x - earth.radius - 384e6, 0,  # earth.x + distance from earth
                radius=1.737e6, color=WHITE, mass=7.347e22, initial_velocity=(0, 29.78e3 + 1.022e3), name="Moon")
    mars = Body(-1.524 * AU, 0, radius=3.389e6, color=RED, mass=6.39e23, initial_velocity=(0, 24.077e3), name="Mars")
    mercury = Body(-0.387 * AU, 0,
                   radius=2.439e6, color=DARK_GRAY, mass=3.285e23,initial_velocity=(0, 47.362e3), name="Mercury")
    venus = Body(-0.723 * AU, 0,
                 radius=6.051e6, color=DARK_RED, mass=4.867e24, initial_velocity=(0, 35.02e3), name="Venus")
    jupiter = Body(-5.203 * AU, 0,
                   radius=69.911e6, color=LIGHT_BROWN, mass=1.898e27, initial_velocity=(0, 13.07e3), name="Jupiter")

    # natural moons
    phobos = Body(mars.x - mars.radius - 9e6, 0, radius=11e3, color=PINK, mass=1.0659e16,
                  initial_velocity=(0, 2.138e3 + 24.077e3), name="Phobos")
    deimos = Body(mars.x - mars.radius - 23e6, 0, radius=6e3, color=DARK_RED, mass=1.4762e15,
                  initial_velocity=(0, 1.3513e3 + 24.077e3), name="Deimos")

    # setup satellites
    # orbital speed is given by v = sqrt(GM/d), where M is the mass of th planet, d is the distance between them.
    orbital_speed = lambda d: math.sqrt(G * mars.mass / (mars.radius + d))

    # https://en.wikipedia.org/wiki/2001_Mars_Odyssey
    sat1 = Satellite(mars.x - mars.radius - 400e3, 0, name="Mars Odyssey",
                     radius=20, color=LIGHT_GRAY, mass=725, initial_velocity=(0, 24.077e3 + orbital_speed(400e3)))

    # https://en.wikipedia.org/wiki/Mars_Reconnaissance_Orbiter
    sat2 = Satellite(mars.x + mars.radius + 300e3, 0, name="Mars Reconnaissance Orbiter",
                     radius=20, color=DARK_GRAY, mass=1125, initial_velocity=(0, 24.077e3 - orbital_speed(300e3)))

    celestial_bodies = [sun, moon, earth, mars, mercury, venus, jupiter, phobos, deimos]
    satellites = [sat1, sat2]
    solar_system = System(celestial_bodies, satellites, time_delta=time_delta, focus_scale=focus_scale)

    while run:
        run = main_step(solar_system, tick=60)

        WINDOW.fill(BLACK)
        WINDOW.blit(bg, (0, 0))
        solar_system.draw_focused(WINDOW, focus=mars)

        text1 = f"{sat1.name} battery = {round(sat1.battery, 1)}%"
        text2 = f"{sat2.name} battery = {round(sat2.battery, 1)}%"
        d1 = FONT.render(text1, True, WHITE)
        d2 = FONT.render(text2, True, WHITE)
        WINDOW.blit(d1, (10, 10))
        WINDOW.blit(d2, (10, 30))

        pygame.display.update()


if __name__ == "__main__":
    main()
