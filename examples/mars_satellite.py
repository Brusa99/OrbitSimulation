import math
import os
from collections import deque

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from src.config import *
from src.body import Body, System, Satellite
import matplotlib.pyplot as plt


def main():
    run = True
    focus_scale = 1_500_000 / AU
    time_delta = 60  # 1 standard minute
    bg = pygame.image.load("../src/bg1.jpg")

    # setup bodies
    sun = Body(0, 0, radius=696.240e6, color=YELLOW, mass=1.989e30, name="Sun")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 1 * AU, 29.78e3)
    earth = Body(x, y, radius=6.371e6, color=BLUE, mass=5.972e24, initial_velocity=(vx, vy), name="Earth")

    x, y, vx, vy = get_start_cond(theta, 1 * AU + earth.radius + 384e6, 29.78e3 + 1.022e3)
    moon = Body(x, y, radius=1.737e6, color=WHITE, mass=7.347e22, initial_velocity=(vx, vy), name="Moon")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 0.387 * AU, 47.362e3)
    mercury = Body(x, y, radius=2.439e6, color=DARK_GRAY, mass=3.285e23, initial_velocity=(vx, vy), name="Mercury")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 0.723 * AU, 35.02e3)
    venus = Body(x, y, radius=6.051e6, color=DARK_RED, mass=4.867e24, initial_velocity=(vx, vy), name="Venus")

    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 5.203 * AU, 13.07e3)
    jupiter = Body(x, y, radius=69.911e6, color=LIGHT_BROWN, mass=1.898e27, initial_velocity=(vx, vy), name="Jupiter")

    # mars
    theta = random.uniform(0, 2 * math.pi)
    x, y, vx, vy = get_start_cond(theta, 1.524 * AU, 24.077e3)
    mars = Body(x, y, radius=3.389e6, color=RED, mass=6.39e23, initial_velocity=(vx, vy), name="Mars")
    # natural moons
    x, y, vx, vy = get_start_cond(theta, 1.524 * AU + mars.radius + 9e6, 24.077e3 + 2.138e3)
    phobos = Body(x, y, radius=11e3, color=PINK, mass=1.0659e16, initial_velocity=(vx, vy), name="Phobos")
    x, y, vx, vy = get_start_cond(theta, 1.524 * AU + mars.radius + 23e6, 24.077e3 + 1.3513e3)
    deimos = Body(x, y, radius=6e3, color=DARK_RED, mass=1.4762e15, initial_velocity=(vx, vy), name="Deimos")

    # setup satellites
    # orbital speed is given by v = sqrt(GM/d), where M is the mass of th planet, d is the distance between them.
    orbital_speed = lambda d: math.sqrt(G * mars.mass / (mars.radius + d))

    # https://en.wikipedia.org/wiki/2001_Mars_Odyssey
    x, y, vx, vy = get_start_cond(theta, 1.524 * AU + mars.radius + 400e3, 24.077e3 + orbital_speed(400e3))
    sat1 = Satellite(x, y, name="Odyssey", orbit_target=mars, radius=20, color=LIGHT_GRAY, mass=725,
                     initial_velocity=(vx, vy), min_altitude=200e3, max_altitude=1200e3)

    # https://en.wikipedia.org/wiki/Mars_Reconnaissance_Orbiter
    x, y, vx, vy = get_start_cond(theta, 1.524 * AU + mars.radius + 300e3, 24.077e3 + orbital_speed(300e3))
    sat2 = Satellite(x, y, name="Rec Orbiter", orbit_target=mars, radius=20, color=DARK_GRAY, mass=1125,
                     initial_velocity=(vx, vy), min_altitude=200e3, max_altitude=1200e3)

    x, y, vx, vy = get_start_cond(theta, 1.524 * AU + mars.radius + 5000e3, 24.077e3 + orbital_speed(5000e3))
    sat3 = Satellite(x, y, name="Relay", orbit_target=mars, radius=10, color=WHITE, mass=420,
                     initial_velocity=(vx, vy), min_altitude=4500e3, max_altitude=6000e3)

    celestial_bodies = [sun, earth, moon, mars, mercury, venus, jupiter, phobos, deimos]
    satellites = [sat1, sat2, sat3]
    solar_system = System(celestial_bodies, satellites, time_delta=time_delta, focus_scale=focus_scale)

    max_len = 15000
    system_info = deque(maxlen=max_len)

    while run:
        run = main_step(solar_system, tick=60)

        WINDOW.fill(BLACK)
        WINDOW.blit(bg, (0, 0))

        solar_system.satellite_connection()
        solar_system.draw_focused(WINDOW, focus=mars)

        text1 = f"[{sat1.name}] battery = {round(sat1.battery, 1)}%, altitude = {round(sat1.altitude/1000, 1)}km"
        text2 = f"[{sat2.name}] battery = {round(sat2.battery, 1)}%, altitude = {round(sat2.altitude/1000, 1)}km"
        text3 = f"[{sat3.name}] battery = {round(sat3.battery, 1)}%, altitude = {round(sat3.altitude/1000, 1)}km"
        # text1 = f"{sat1.name} relay = {sat1.relay}"
        # text2 = f"{sat2.name} relay = {sat2.relay}"
        d1 = FONT.render(text1, True, WHITE)
        d2 = FONT.render(text2, True, WHITE)
        d3 = FONT.render(text3, True, WHITE)
        WINDOW.blit(d1, (10, 10))
        WINDOW.blit(d2, (10, 30))
        WINDOW.blit(d3, (10, 50))
        pygame.display.update()

        system_info.append(solar_system.get_sat_info())

    plt.gcf().set_size_inches(18, 8)
    sat1_altituds = [x[0].altitude for x in system_info]
    sat2_altituds = [x[1].altitude for x in system_info]
    sat3_altituds = [x[2].altitude for x in system_info]
    plt.plot(sat1_altituds, color="orange")
    plt.plot(sat2_altituds, color="yellow")
    plt.plot(sat3_altituds, color="green")
    # plot min and max altitudes
    plt.plot([sat1.min_altitude for _ in range(max_len)], color="red")
    plt.plot([sat1.max_altitude for _ in range(max_len)], color="red")
    plt.plot([sat3.min_altitude for _ in range(max_len)], color="black")
    plt.plot([sat3.max_altitude for _ in range(max_len)], color="black")
    # set minimum y value to 0
    plt.ylim(bottom=0, top=0.8e7)
    plt.savefig("sat_altituds.png")


if __name__ == "__main__":
    main()
