from __future__ import annotations
from collections import deque
import numpy as np
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
                 name: str | None = None,
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
        name : str, optional
            name of the body, used in representation (default is None).
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vel_x = initial_velocity[0]
        self.vel_y = initial_velocity[1]

        self._orbit = deque(maxlen=max_orbit_length)
        self.name = name

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

    def draw_focused(self, window, focus: Body, scale=SCALE):
        """Draws the planet on the window, centered around the focus"""
        radius = RADIUS_RESIZE(self.radius) * RADIUS_SCALE
        x = (self.x - focus.x) * scale + WIDTH / 2
        y = (self.y - focus.y) * scale + HEIGHT / 2

        pygame.draw.circle(window, self.color, (x, y), radius)

    def _gravitational_force(self, other: Body) -> tuple[float, float]:
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

    def _total_gforce(self, bodies: list[Body]) -> tuple[float, float]:
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
                force = self._gravitational_force(body)
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
            time delta to approximate the derivative of the position and the velocity of the bodies in seconds (default
            is TIME_SCALE).
        """
        force = self._total_gforce(bodies)
        acceleration_x = force[0] / self.mass
        acceleration_y = force[1] / self.mass
        self.vel_x += acceleration_x * time_delta
        self.vel_y += acceleration_y * time_delta
        self.x += self.vel_x * time_delta
        self.y += self.vel_y * time_delta

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name}"


class Satellite(Body):
    """
    Body subclass for satellites.
    """
    interference_factor = 1

    # battery factors
    solar_charge_factor = 0.02
    battery_discharge_factor = 0.001
    transmission_factor = 0.005
    connection_factor = 0.005

    def __init__(self, *args, motherbase: Body | None = None, sun: Body | None = None, **kwargs):
        """
        Constructor Method.
        """
        super().__init__(*args, **kwargs)
        self.motherbase = motherbase
        self.sun = sun
        self.battery = 100
        self.connected = True
        self.attempted_connections = 0
        self.relay = None
        self.transmitting = False

    def calculate_path(self, target: Body, obstacles: list[Body]):
        """
        Calculates if the path between this satellite and the target is obstructed by any of the obstacles.

        Distance between each obstacle and the line passing between the center of mass of this satellite and the target.
        If such distance is less than the radius of an obstacle times a constant factor (_interference_factor_), then
        the path is obstructed.

        Parameters
        ----------
        target : Body
            the target body.
        obstacles : list[Body]
            list of all bodies that can cause obstuctions.

        Returns
        -------
        obstracted : bool
            True if the path is obstructed.
        """
        # line equation ax + by + c = 0
        a = target.y - self.y
        b = self.x - target.x
        c = target.x * self.y - self.x * target.y

        for obstacle in obstacles:
            if obstacle is self or obstacle is target:
                continue

            effective_radius = obstacle.radius * self.interference_factor

            # check of the obstacle is in bewteen the satellite and the target
            if not min(self.x, target.x) - effective_radius < obstacle.x < max(self.x, target.x) + effective_radius:
                continue
            if not min(self.y, target.y) - effective_radius < obstacle.y < max(self.y, target.y) + effective_radius:
                continue
            # distance between the obstacle and the line
            distance = abs(a * obstacle.x + b * obstacle.y + c) / math.sqrt(a ** 2 + b ** 2)
            if distance < effective_radius:  # obstacle is in the way
                return True
        return False

    def draw_connection(self, window, target: Body | None, obstacles: list[Body], scale=SCALE):
        """Draws a colored line between this satellite and the target."""
        if target is None:
            target = self.motherbase
        obstructed = self.calculate_path(target, obstacles)
        color = RED if obstructed else GREEN
        x1 = self.x * scale + WIDTH / 2
        y1 = self.y * scale + HEIGHT / 2
        x2 = target.x * scale + WIDTH / 2
        y2 = target.y * scale + HEIGHT / 2
        pygame.draw.line(window, color, (x1, y1), (x2, y2), 1)

    def draw_connection_focused(self, window, target: Body | None, obstacles: list[Body], focus: Body, scale=SCALE):
        """Draws a colored line between this satellite and the target, centered around the focus."""
        if target is None:
            target = self.motherbase
        obstructed = self.calculate_path(target, obstacles)
        color = RED if obstructed else GREEN
        x1 = (self.x - focus.x) * scale + WIDTH / 2
        y1 = (self.y - focus.y) * scale + HEIGHT / 2
        x2 = (target.x - focus.x) * scale + WIDTH / 2
        y2 = (target.y - focus.y) * scale + HEIGHT / 2
        pygame.draw.line(window, color, (x1, y1), (x2, y2), 1)

    def _battery_update(self, obstacles: list[Body], time_delta=TIME_SCALE):
        """
        Updates the battery of the satellite.

        The battery discharges at a constant rate, but it also charges when the satellite is in the sun. The battery
        discharges at a higher rate when the satellite is transmitting data.

        Parameters
        ----------
        obstacles : list[Body]
            list of all bodies that can cause obstuctions to the satellite-sun path.
        time_delta : float, optional
            time delta to approximate the derivative of the position and the velocity of the bodies (default is
            TIME_SCALE).
        """
        charging = not self.calculate_path(self.sun, obstacles)
        battery_prime = self.solar_charge_factor * charging\
                        - self.transmitting * self.transmission_factor \
                        - self.battery_discharge_factor \
                        - self.attempted_connections * self.connection_factor

        new_battery = np.clip(self.battery + battery_prime * time_delta, 0, 100)
        self.battery = new_battery

    def update(self, bodies: list[Body], time_delta=TIME_SCALE):
        super().update(bodies, time_delta)
        self._battery_update(bodies, time_delta)


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
    focus_scale : float
        pixels per meter when the system is focused on a body. (only affects rendering)

    Methods
    -------
    draw(window)
        Draws all the bodies in the system on the window.
    update()
        Updates the positions and the velocities of all the bodies in the system.
    """

    def __init__(self,
                 celestial_bodies: list[Body],
                 satellites: list[Satellite] | None = None,
                 sun: Body | None = None,
                 sat_motherbase: Body | None = None,
                 time_delta=TIME_SCALE,
                 scale=SCALE,
                 focus_scale=None,
                 ):
        """Constructor Method."""
        self.celestial_bodies = celestial_bodies
        self.satellites = satellites if satellites is not None else []

        # set default sun and motherbase for all satellites
        self.sun = sun if sun is not None else celestial_bodies[0]
        self.sat_motherbase = sat_motherbase if sat_motherbase is not None else celestial_bodies[1]
        for sat in self.satellites:
            sat.sun = self.sun
            sat.motherbase = self.sat_motherbase

        self.time_delta = time_delta
        self.scale = scale
        if focus_scale is None:
            self.focus_scale = scale
        else:
            self.focus_scale = focus_scale

    def draw(self, window):
        """Draws all the bodies in the system on the window."""
        for body in self.celestial_bodies:
            body.draw(window, self.scale)
        for satellite in self.satellites:
            satellite.draw(window, self.scale)

    def update(self):
        """Updates the positions and the velocities of all the bodies in the system."""
        for body in self.celestial_bodies:
            body.update(self.celestial_bodies, self.time_delta)
        for satellite in self.satellites:
            satellite.update(self.celestial_bodies, self.time_delta)

    def draw_focused(self, window, focus: Body):
        """Draws all the bodies in the system on the window, centerd around the focus"""
        for body in self.celestial_bodies:
            body.draw_focused(window, focus, self.focus_scale)
        for sat in self.satellites:
            sat.draw_focused(window, focus, self.focus_scale)
            sat.draw_connection_focused(window, sat.relay, self.celestial_bodies, focus, self.focus_scale)

    def satellite_connection(self):
        """Check if the satellites can connect to motherbase directly or through a relay."""
        # try to connect to motherbase
        for sat in self.satellites:
            sat.connected = False
            sat.attempted_connections = 1
            obstructed = sat.calculate_path(sat.motherbase, self.celestial_bodies)
            if not obstructed:
                sat.connected = True
                sat.relay = sat.motherbase

        # obstructed satellite try to relay through connected ones
        connected_sats = [sat for sat in self.satellites if sat.connected]
        unconnected_sats = [sat for sat in self.satellites if sat not in connected_sats]
        for sat in unconnected_sats:
            for relay in connected_sats:
                sat.attempted_connections += 1
                obstructed = sat.calculate_path(relay, self.celestial_bodies)
                if not obstructed:
                    sat.connected = True
                    sat.relay = relay
                    break
