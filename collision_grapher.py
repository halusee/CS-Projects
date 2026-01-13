import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

file = 'projectile_data.csv'
df = pd.read_csv(file, index_col=0)

max_index = df['index'].max()

times = []
masses = []
velocities = []
momentums = []
kinetic_energies = []

i = 0
while i <= max_index:
    times.append(df.loc[df['index'] == i, 'time'])
    masses.append(df.loc[df['index'] == i, 'mass'])
    velocities.append(df.loc[df['index'] == i, 'velocity'])
    momentums.append(df.loc[df['index'] == i, 'momentum'])
    kinetic_energies.append(df.loc[df['index'] == i, 'kinetic energy'])
    i += 1

def plot_quantity(times, values, choice):

    index = 0
    while index < len(times):
        plt.plot(times[index], values[index])
        index += 1

    plt.xlabel('Time (ms)')
    plt.ylabel(choice)
    plt.show()

    index = 0
    while index < len(times):
        plt.plot(times[index], kinetic_energies[index])
        index += 1

    plt.xlabel('Time')
    plt.ylabel('Kinetic Energy (J)')
    plt.show()

plot_quantity(times, velocities, 'Velocity (m/s)')
#plot_quantity(times, momentums, 'Momentum (kg * m * s^-1)')
#plot_quantity(times, kinetic_energies, 'Kinetic Energy (J)')



# choice = None
# while not choice:
#     print("(1) Velocity, (2) Momentum, (3)Kinetic Energy")
#     choice = int(input('Plot which? '))
#     if (choice != 1) and (choice != 2) and (choice != 3):
#         choice = None

# if choice == 1:
#     plot_quantity(times, velocities, 'Velocity (m/s)')
# elif choice == 2:
#     plot_quantity(times, momentums, 'Momentum (kg * m * s^-1)')
# elif choice == 3:
#     plot_quantity(times, kinetic_energies, 'Kinetic Energy (J)')


