import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from src.config import *
from src.body import Body, System


def main():
    run = True
    scale = 100 / AU  # pixels per meter
    time_delta = 3600  # 1 standard hour

    # setup bodies
    sun = Body(0, 0, radius=696.240e6, color=YELLOW, mass=1.989e30)
    earth = Body(-1 * AU, 0, radius=6.371e6, color=BLUE, mass=5.972e24, initial_velocity=(0, 29.78e3))
    moon = Body(-1 * AU - 384e6, 0,  # earth.x + distance from earth
                radius=1.737e6, color=WHITE, mass=7.347e22, initial_velocity=(0, 29.78e3 + 1.022e3))
    # Note: The TIME_SCALE should be sufficiently small to appreciate the orbit of the moon around the earth.
    mars = Body(-1.524 * AU, 0, radius=3.389e6, color=RED, mass=6.39e23, initial_velocity=(0, 24.077e3))
    mercury = Body(-0.387 * AU, 0, radius=2.439e6, color=DARK_GRAY, mass=3.285e23, initial_velocity=(0, 47.362e3))
    venus = Body(-0.723 * AU, 0, radius=6.051e6, color=DARK_RED, mass=4.867e24, initial_velocity=(0, 35.02e3))
    jupiter = Body(-5.203 * AU, 0, radius=69.911e6, color=LIGHT_BROWN, mass=1.898e27, initial_velocity=(0, 13.07e3))
    saturn = Body(-9.537 * AU, 0, radius=58.232e6, color=DARK_YELLOW, mass=5.683e26, initial_velocity=(0, 9.69e3))
    uranus = Body(-19.191 * AU, 0, radius=25.362e6, color=WHITE, mass=8.681e25, initial_velocity=(0, 6.81e3))
    neptune = Body(-30.069 * AU, 0, radius=24.622e6, color=LIGHT_BLUE, mass=1.024e26, initial_velocity=(0, 5.43e3))

    celestial_bodies = [sun, moon, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
    solar_system = System(celestial_bodies, time_delta=time_delta, scale=scale)

    while run:
        run = main_step(solar_system)

        text = f"d_MoonEarth: {round(math.sqrt((earth.x - moon.x)**2 + (earth.y - moon.y)**2)/1000000, 1)}e3km"
        d = FONT.render(text, True, WHITE)
        WINDOW.blit(d, (10, 10))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()


