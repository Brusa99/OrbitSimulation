from dataclasses import dataclass
from moonlight import ScriptLoader


@dataclass
class SatInfo:
    """Collection of satellite data to monitor"""
    altitude: float
    battery: float
    connections: int
    attempted_connections: int
    boosting: bool


_script = """
signal { int connections; real altitude; real battery; }
domain boolean;
formula PositiveBattery =  globally (battery > 0);
formula SafeBatteryUsage(real sl) = eventually[0, 10] (battery > sl);
formula SafeAltitude(real a_min, real a_max) = eventually[0,60] ((altitude > a_min) & (altitude < a_max));
formula AsymptoticStability(real a_min, real a_max) = eventually ( globally ((altitude > a_min) & (altitude < a_max)));
formula Connection = ! globally (connections < 1);
"""

# other possibilities: (not working)
# """
# formula PositiveBattery =  globally (battery > 0);
# formula SafeBatteryUsage(real sl) = globally (battery < sl => eventually (battery > sl));
# formula SafeAltitude(real a_min, real a_max) = globally (altitude < a_min | altitude > a_max => eventually (altitude > a_min & altitude < a_max));
# formula AsymptoticStability(real a_min, real a_max) = eventually ( globally (altitude > a_min & altitude < a_max));
# formula Connection = ! globally (connections < 1);
# """

_moonlightScript = ScriptLoader.loadFromText(_script)

pos_bat_monitor = _moonlightScript.getMonitor("PositiveBattery")
safe_bat_monitor = _moonlightScript.getMonitor("SafeBatteryUsage")
safe_alt_monitor = _moonlightScript.getMonitor("SafeAltitude")
asym_stab_monitor = _moonlightScript.getMonitor("AsymptoticStability")
connection_monitor = _moonlightScript.getMonitor("Connection")
