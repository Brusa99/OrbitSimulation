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
formula SafeAltitude(real a_min, real a_max) = eventually[0,20] ((altitude > a_min) & (altitude < a_max));
formula AsymptoticStability(real a_min, real a_max) = eventually ( globally ((altitude > a_min) & (altitude < a_max)));
formula Connection = ! globally[0, 10] (connections < 1);
"""

_parametrized_script = """
signal { int connections; real altitude; real battery; }
domain boolean;
formula PositiveBattery =  globally (battery > 0);
formula SafeBatteryUsage = eventually[0, 5] (battery > 20);
formula SafeAltitudeLow = eventually[0,5] ((altitude > 200000) & (altitude < 1200000));
formula SafeAltitudeHigh = eventually[0,5] ((altitude > 4600000) & (altitude < 5800000));
formula AsymptoticStabilityLow = eventually ( globally ((altitude > 200000) & (altitude < 1200000)));
formula AsymptoticStabilityHigh = eventually ( globally ((altitude > 4600000) & (altitude < 5800000)));
formula Connection = ! globally[0, 30] (connections < 1);
"""

_moonlightScript = ScriptLoader.loadFromText(_script)

pos_bat_monitor = _moonlightScript.getMonitor("PositiveBattery")
safe_bat_monitor = _moonlightScript.getMonitor("SafeBatteryUsage")
# safe_lowalt_monitor = _moonlightScript.getMonitor("SafeAltitudeLow")
# safe_highalt_monitor = _moonlightScript.getMonitor("SafeAltitudeHigh")
safe_alt_monitor = _moonlightScript.getMonitor("SafeAltitude")
# lowasym_stab_monitor = _moonlightScript.getMonitor("AsymptoticStabilityLow")
# highasym_stab_monitor = _moonlightScript.getMonitor("AsymptoticStabilityHigh")
asym_stab_monitor = _moonlightScript.getMonitor("AsymptoticStability")
connection_monitor = _moonlightScript.getMonitor("Connection")
