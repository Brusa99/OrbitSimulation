import numpy as np
from src.monitoring import pos_bat_monitor, safe_bat_monitor, safe_alt_monitor, asym_stab_monitor, connection_monitor


def main():
    # process data
    system_info = np.load("sat_info.npy", allow_pickle=True)
    n_satellites = system_info.shape[1]

    alt_params = [[200e3, 1200e3], [200e3, 1200e3], [4500e3, 6000e3]]

    for sat_i in range(n_satellites):
        sat_info = system_info[:, sat_i]
        sat_altitude = [d.altitude for d in sat_info]
        sat_battery = [d.battery for d in sat_info]
        sat_connections = [int(d.connections) for d in sat_info]

        time = [int(i) for i in range(len(sat_altitude))]
        signals = list(zip(sat_connections, sat_altitude, sat_battery))

        pos_bat = np.array(pos_bat_monitor.monitor(time, signals))
        safe_bat = np.array(safe_bat_monitor.monitor(time, signals, parameters=20.0))
        # safe_alt = np.array(safe_alt_monitor.monitor(time, signals, parameters=alt_params[sat_i]))
        # asym_stab = np.array(asym_stab_monitor.monitor(time, signals, parameters=alt_params[sat_i]))
        connection = np.array(connection_monitor.monitor(time, signals))



if __name__ == "__main__":
    main()
