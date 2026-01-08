import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd

ax = plt.axes(projection="3d")

x = np.arange(-5, 5, 0.1)
y = np.arange(-5, 5, 0.1)

X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

ax.plot_surface(X, Y, Z)
ax.set_title("3d plot")
ax.set_xlabel("test")
plt.show()