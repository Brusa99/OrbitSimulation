import math
from collections import namedtuple

# pygame
WIDTH, HEIGHT = 800, 800

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
