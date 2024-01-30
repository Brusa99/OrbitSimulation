import numpy as np
import matplotlib.pyplot as plt
from src.monitoring import pos_bat_monitor, safe_bat_monitor, connection_monitor
# from src.monitoring import safe_lowalt_monitor, safe_highalt_monitor, lowasym_stab_monitor, highasym_stab_monitor
from src.monitoring import pos_bat_monitor, safe_bat_monitor, safe_alt_monitor, asym_stab_monitor, connection_monitor


def main():
    # process data
    system_info = np.load("sat_info2.npy", allow_pickle=True)
    n_satellites = system_info.shape[1]

    # safe_alt_monitor = [safe_lowalt_monitor, safe_lowalt_monitor, safe_highalt_monitor]
    # asym_stab_monitor = [lowasym_stab_monitor, lowasym_stab_monitor, highasym_stab_monitor]

    # for plotting
    sat_names = ["Odyssey", "Rec Orbiter", "Relay"]
    attr_names = ["connections", "altitude", "battery"]
    colors = ["orange", "fuchsia", "green"]
    def extract(ls, i): return list(map(lambda x: x[i], ls))
    fig_a, axs_a = plt.subplots(4, 1, gridspec_kw={'height_ratios': [4, 1, 1, 1]}, figsize=(20, 10), sharex=True)
    fig_b, axs_b = plt.subplots(4, 1, gridspec_kw={'height_ratios': [4, 1, 1, 1]}, figsize=(20, 10), sharex=True)
    fig_c, axs_c = plt.subplots(4, 1, gridspec_kw={'height_ratios': [4, 1, 1, 1]}, figsize=(20, 10), sharex=True)

    for sat_i in range(n_satellites):
        sat_info = system_info[:, sat_i]
        sat_altitude = [d.altitude for d in sat_info]
        sat_battery = [d.battery for d in sat_info]
        sat_connections = [int(d.connections) for d in sat_info]

        time = [int(i) for i in range(len(sat_altitude))]
        signals = list(zip(sat_connections, sat_altitude, sat_battery))

        pos_bat = np.array(pos_bat_monitor.monitor(time, signals))
        safe_bat = np.array(safe_bat_monitor.monitor(time, signals, parameters=20.0))
        connection = np.array(connection_monitor.monitor(time, signals))
        safe_alt = np.array(safe_alt_monitor.monitor(time, signals, parameters=np.array([200e3, 1200e3])))
        # asym_stab = np.array(asym_stab_monitor[sat_i].monitor(time, signals))  # NOT WORKING

        # plot altitude
        axs_a[0].plot(time, sat_altitude, color=colors[sat_i], label=sat_names[sat_i], linewidth=0.5)
        # extract
        time2 = extract(safe_alt, 0)
        values2 = extract(safe_alt, 1)
        # time3 = extract(asym_stab, 0)
        # values3 = extract(asym_stab, 1)
        axs_a[sat_i + 1].plot(time2, values2, color="orange", drawstyle="steps-post", label="Safe Altitude")
        # axs[sat_i + 1].plot(time3, values3, color="blue", drawstyle="steps", label="Asymptotic Stability")
        axs_a[sat_i + 1].set_ylim([-1.2, 1.2])
        axs_a[sat_i + 1].set_ylabel(f"{sat_names[sat_i]}\nSatisfaction")
        axs_a[sat_i + 1].legend()

        # plot battery
        axs_b[0].plot(time, sat_battery, color=colors[sat_i], label=sat_names[sat_i], linewidth=0.5)
        # extract
        time2 = extract(safe_bat, 0)
        values2 = extract(safe_bat, 1)
        axs_b[sat_i + 1].plot(time2, values2, color="orange", drawstyle="steps-post", label="Safe Battery")
        time3 = extract(pos_bat, 0)
        values3 = extract(pos_bat, 1)
        axs_b[sat_i + 1].plot(time3, values3, color="red", drawstyle="steps-post", label="Positive Battery")
        axs_b[sat_i + 1].set_ylim([-1.2, 1.2])
        axs_b[sat_i + 1].set_ylabel(f"{sat_names[sat_i]}\nSatisfaction")
        axs_b[sat_i + 1].legend()

        # plot connection
        axs_c[0].plot(time, sat_connections, color=colors[sat_i], label=sat_names[sat_i], linewidth=0.5)
        # extract
        time2 = extract(connection, 0)
        values2 = extract(connection, 1)
        axs_c[sat_i + 1].plot(time2, values2, color="orange", drawstyle="steps-post", label="Connection")
        axs_c[sat_i + 1].set_ylim([-1.2, 1.2])
        axs_c[sat_i + 1].set_ylabel(f"{sat_names[sat_i]}\nSatisfaction")
        axs_c[sat_i + 1].legend()

    # altitudes
    axs_a[0].axhline(y=200e3, color="red", linestyle="--")
    axs_a[0].axhline(y=1200e3, color="red", linestyle="--")
    axs_a[0].axhline(y=4600e3, color="red", linestyle="--")
    axs_a[0].axhline(y=5800e3, color="red", linestyle="--")
    axs_a[0].set_ylabel("Altitude (m)")
    axs_a[0].legend()
    axs_a[3].set_xlabel("Time (min)")
    fig_a.savefig("altituds.png")

    # battery
    axs_b[0].axhline(y=20, color="red", linestyle="--")
    axs_b[0].axhline(y=0, color="red")
    axs_b[0].set_ylabel("Battery (%)")
    axs_b[0].legend()
    axs_b[3].set_xlabel("Time (min)")
    fig_b.savefig("battery.png")

    # connection
    axs_c[0].axhline(y=1, color="red", linestyle="--")
    axs_c[0].set_ylabel("Connections")
    axs_c[0].legend()
    axs_c[3].set_xlabel("Time (min)")
    fig_c.savefig("connection.png")


if __name__ == "__main__":
    main()
