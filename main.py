import math
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from collections import namedtuple, deque

# pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
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

# astronomical constants
AU = 149_597_870_700  # meters
G = 6.67408e-11  # m^3 kg^-1 s^-2

# drawing constants
SCALE = 100 / AU  # pixels per meter
TIME_SCALE = 3600 * 24  # 1 standard day
RADIUS_SCALE = 6  # scale radius of planets
def RADIUS_RESIZE(r): return math.log(r/100, 100)


class Body:
    def __init__(self,
                 x: float,
                 y: float,
                 mass: float,
                 radius: float,
                 color: Color,
                 initial_velocity=(0, 0)
                 ):
        """
        Creates a body object with the given parameters.

        Coordinate system is centered in the middle of the display (NOT it the pygame window origin). Coordinates are
        in meters (it is strongly suggested to factor them with AU).

        Parameters
        :param x: x starting coordinate of the body in meters.
        :param y: y starting coordinate of the body in meters.
        :param mass: mass of the body in kg.
        :param radius: radius of the body in meters.
        :param color: RGB color of the body (only affects rendering).
        :param initial_velocity: initial velocity of the body in m/s, relative to the fixed coordinate system.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vel_x = initial_velocity[0]
        self.vel_y = initial_velocity[1]

        self.orbit = deque(maxlen=1000)
        self.is_sun = False  # for drawing orbits
        self.dist_to_sun = 0

    def draw(self, window, ):
        """Draws the planet on the window"""
        x = self.x * SCALE + WIDTH / 2  # center of window is (WIDTH/2, HEIGHT/2)
        y = self.y * SCALE + HEIGHT / 2
        radius = RADIUS_RESIZE(self.radius) * RADIUS_SCALE
        pygame.draw.circle(window, self.color, (x, y), radius)


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
