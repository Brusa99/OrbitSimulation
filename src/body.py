from collections import deque
import pygame
from src.constants import *


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