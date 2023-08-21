import matplotlib.pyplot as plt
import numpy as np

d = np.linspace(0, 5, 300)
x, y = np.meshgrid(d, d)
plt.imshow(((y >= 0) & (x >= 0) & (2*x - y >= 2) & (-2*x + 3*y <= 2)).astype(int),
           extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)

# plot the lines defining the constraints
x = np.linspace(0, 5, 100)
# 2x1 - x2 >= 2
x21 = 2 * x - 2
# -2x1 + 3x2 <= 2
x22 = (2 + 2*x) / 3
# z = 5x1 + 6x2; z = 5
x23 = -(5 * x - 5) / 6
# z = 5x1 + 6x2; z = 22
x24 = -(5 * x - 22) / 6
# z = 5x1 + 6x2; z = 33
x25 = -(5 * x - 33) / 6

# Make plot
plt.plot(x, x21, label=r'$2x_1 - x_2 \geq 2$')
plt.plot(x, x22, label=r'$-2x_1 + 3x_2 \leq 2$')
plt.plot(x, x23, label=r'$z = 5x_1 + 6x_2; z=5$')
plt.plot(x, x24, label=r'$z = 5x_1 + 6x_2; z=22$')
plt.plot(x, x25, label=r'$z = 5x_1 + 6x_2; z=33$')
plt.xlim(0, 5)
plt.ylim(0, 4)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')

# plt.figure(figsize=(48, 12))
plt.show()
