from dataclasses import dataclass


@dataclass
class SatInfo:
    """Collection of satellite data to monitor"""
    altitude: float
    battery: float
    connections: int
    attempted_connections: int
    boosting: bool
