# OrbitSimulation

Python simulation of celestial bodies and satellites.

This repository is made for the project of the course _"Cyber Physical Systems"_
held at the University of Trieste in 2023/2024.
The project aim is to simulate a network of satellites, which communicate with each other
and with a ground station. The satellites are able tune their orbit in order to avoid escaping or crushing.

## Contents

- `examples/`
- - `solar_system.py`: simulation of the solar system. Just to test that the gravitational forces are implemented 
                       correctly.
- - `three_body_problem.py`: simulation of the three body problem. This example shows that the in general the orbits
                             are unpredictable as the system is chaotic for most initial conditions.
- - `mars_satellite.py`: simulation of three satellite orbiting Mars. This is the main example of the project.
                         It shows how satellite behave in both communicaton and orbit tuning.
- - `satellite_monitor.py`: Monitoring and plotting of the results obtained from simulations.


