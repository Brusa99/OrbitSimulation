import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from src.config import *
from src.body import Body, System


def main():
    run = True
    scale = 100 / AU  # pixels per meter
    time_delta = 3600  # 1 standard hour

    # setup bodies
    sun = Body(0, 0, radius=696.240e6, color=YELLOW, mass=1.989e30, name="Sun")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 1 * AU, 29.78e3)
    earth = Body(x, y, radius=6.371e6, color=BLUE, mass=5.972e24, initial_velocity=(vx, vy), name="Earth")

    x, y, vx, vy = get_start_cond(theta, 1 * AU + earth.radius + 384e6, 29.78e3 + 1.022e3)
    moon = Body(x, y, radius=1.737e6, color=WHITE, mass=7.347e22, initial_velocity=(vx, vy), name="Moon")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 1.524 * AU, 24.077e3)
    mars = Body(x, y, radius=3.389e6, color=RED, mass=6.39e23, initial_velocity=(vx, vy), name="Mars")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 0.387 * AU, 47.362e3)
    mercury = Body(x, y, radius=2.439e6, color=DARK_GRAY, mass=3.285e23, initial_velocity=(vx, vy), name="Mercury")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 0.723 * AU, 35.02e3)
    venus = Body(x, y, radius=6.051e6, color=DARK_RED, mass=4.867e24, initial_velocity=(vx, vy), name="Venus")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 5.203 * AU, 13.07e3)
    jupiter = Body(x, y, radius=69.911e6, color=LIGHT_BROWN, mass=1.898e27, initial_velocity=(vx, vy), name="Jupiter")

    celestial_bodies = [sun, moon, earth, mars, mercury, venus, jupiter]# , saturn, uranus, neptune]
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


