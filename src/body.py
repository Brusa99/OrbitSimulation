from __future__ import annotations
from collections import deque
import pygame
from src.config import *


class Body:
    """
    A class to represent a celestial body.

    Attributes
    ----------
    x, y : float
        x and y coordinates of the body in m.
    mass : float
        mass of the body in kg.
    radius : float
        radius of the body in m.
    color : Color
        RGB color of the body (only affects rendering).
    vel_x, vel_y : float
        x and y components of the velocity of the body in m/s.

    Methods
    -------
    draw(window)
        Draws the planet on the window.
    gravitational_force(other)
        Calculates the gravitational force between this body and another.
    total_force(bodies)
        Calculates the total gravitational force on this body.
    update(bodies)
        Updates the position and the velocity of the body.
    """
    def __init__(self,
                 x: float,
                 y: float,
                 mass: float,
                 radius: float,
                 color: Color,
                 initial_velocity=(0, 0),
                 max_orbit_length=1000,
                 ):
        """
        Constructor Method.

        Coordinate system is centered in the middle of the display (NOT it the pygame window origin). Coordinates are
        in meters (it is strongly suggested to factor them with AU).

        Parameters
        ----------
        x, y : float
            x and y coordinates of the body in m.
        mass : float
            mass of the body in kg.
        radius : float
            radius of the body in m.
        color : Color
            RGB color of the body (only affects rendering).
        initial_velocity : tuple[float, float], optional.
            initial velocity of the body in m/s, relative to the fixed coordinate system (default is (0, 0), which is
            stationary).
        max_orbit_length : int, optional
            maximum length of the orbit path (default is 1000).
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vel_x = initial_velocity[0]
        self.vel_y = initial_velocity[1]

        self._orbit = deque(maxlen=max_orbit_length)

    def draw(self, window, scale=SCALE):
        """Draws the planet on the window"""
        radius = RADIUS_RESIZE(self.radius) * RADIUS_SCALE
        x = self.x * scale + WIDTH / 2  # center of window is (WIDTH/2, HEIGHT/2)
        y = self.y * scale + HEIGHT / 2
        self._orbit.append((x, y))

        # draw
        if len(self._orbit) > 2:
            pygame.draw.lines(window, self.color, False, self._orbit)
        pygame.draw.circle(window, self.color, (x, y), radius)

    def gravitational_force(self, other: Body) -> tuple[float, float]:
        """
        Calculates the gravitational force between this body and another.

        Parameters
        ----------
        other : Body
            the other body.

        Returns
        -------
        tuple[float, float]
            x and y components of the gravitational force.
        """
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        force = G * self.mass * other.mass / distance ** 2

        # decompose force into x and y components
        force_x = force * distance_x / distance
        force_y = force * distance_y / distance

        # # alternative method
        # theta = math.atan2(distance_y, distance_x)  # angle between the two bodies
        # force_x = force * math.cos(theta)
        # force_y = force * math.sin(theta)

        return force_x, force_y

    def total_force(self, bodies: list[Body]) -> tuple[float, float]:
        """
        Calculates the total gravitational force on this body.

        Parameters
        ----------
        bodies : list[Body]
            list of all bodies in the simulation.

        Returns
        -------
        tuple[float, float]
            x and y components of the total gravitational force.
        """
        force_x = force_y = 0
        for body in bodies:
            if body is not self:
                force = self.gravitational_force(body)
                force_x += force[0]
                force_y += force[1]
        return force_x, force_y

    def update(self, bodies: list[Body], time_delta=TIME_SCALE):
        """
        Updates the position and the velocity of the body.

        Parameters
        ----------
        bodies : list[Body]
            list of all bodies in the simulation.
        time_delta : float, optional
            time delta to approximate the derivative of the position and the velocity of the bodies (default is
            TIME_SCALE).
        """
        force = self.total_force(bodies)
        acceleration_x = force[0] / self.mass
        acceleration_y = force[1] / self.mass
        self.vel_x += acceleration_x * time_delta
        self.vel_y += acceleration_y * time_delta
        self.x += self.vel_x * time_delta
        self.y += self.vel_y * time_delta


class System:
    """
    A class to represent a system of celestial bodies.

    Attributes
    ----------
    celestial_bodies : list[Body]
        list of all bodies in the system.
    time_delta : float
        time delta to approximate the derivative of the position and the velocity of the bodies.
    scale : float
        pixels per meter. (only affects rendering)

    Methods
    -------
    draw(window)
        Draws all the bodies in the system on the window.
    update()
        Updates the positions and the velocities of all the bodies in the system.
    """
    def __init__(self, celestial_bodies: list[Body], time_delta=TIME_SCALE, scale=SCALE):
        """Constructor Method."""
        self.celestial_bodies = celestial_bodies
        self.time_delta = time_delta
        self.scale = scale

    def draw(self, window):
        """Draws all the bodies in the system on the window."""
        for body in self.celestial_bodies:
            body.draw(window, self.scale)

    def update(self):
        """Updates the positions and the velocities of all the bodies in the system."""
        for body in self.celestial_bodies:
            body.update(self.celestial_bodies, self.time_delta)
