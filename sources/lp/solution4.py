import matplotlib.pyplot as plt
import numpy as np

d = np.linspace(0, 4, 300)
x, y = np.meshgrid(d, d)
plt.imshow(((y >= 0) & (x >= 0) & (y <= 2 - 2 * x)).astype(int),
           extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)
plt.imshow(((y < 4) & (x < 4) & (y >= 3 - 3 * x / 4)).astype(int),
           extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)

# plot the lines defining the constraints
x = np.linspace(0, 5, 100)
# 2x + y <= 2
y1 = 2 - 2 * x
# 3x + 4y >= 12
y2 = 3 - 3 * x / 4
# z = 3*x+2*y
y3 = 2 - 3 * x / 2

# Make plot
plt.plot(x, y1, label=r'$2x_1 + x_2 \leq 2$')
plt.plot(x, y2, label=r'$3x_1 + 4x_2 \geq 12$')
plt.plot(x, y3, label=r'$z = 3x_1 + 2x_2; z=4$')
plt.xlim(0, 4)
plt.ylim(0, 4)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')

# plt.figure(figsize=(48, 12))
plt.show()
