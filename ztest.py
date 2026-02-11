import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

k = 0.3
n_max = 20
confidence_0_values = np.linspace(0.1, 1.0, 100)

n = np.arange(n_max)
X, Y = np.meshgrid(n, confidence_0_values)
Z = 1 - (1 - Y) * (1 - k) ** X

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, cmap='viridis')

ax.set_xlabel('Number of Iterations (n)')
ax.set_ylabel('Initial Confidence (confidence_0)')
ax.set_zlabel('Updated Confidence')

ax.set_title('3D Surface Plot of Confidence Update over Iterations')

plt.show()
