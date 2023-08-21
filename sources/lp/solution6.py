import matplotlib.pyplot as plt
import numpy as np

d = np.linspace(0, 5, 300)
x, y = np.meshgrid(d, d)
plt.imshow(((y >= 0) & (x >= 0) & (5*y <= 15) & (6*x + 2*y <= 24) & (x + y <= 5)).astype(int),
           extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)

# plot the lines defining the constraints
x = np.linspace(0, 5, 100)
# 5x2 <= 15
x21 = 3 + x*0
# 6x1 + 2x2 <= 24
x22 = 12 - 3 * x
# x1 + x2 <= 5
x23 = 5 - x
# z = 2x1 + x2; z = 8.5
x24 = 8.5 - 2 * x

x25 = 7 - 2 * x

x26 = 8 - 2 * x

# Make plot
plt.plot(x, x21, label=r'$5x_2 \leq 15$')
plt.plot(x, x22, label=r'$6x_1 + 2x_2 \leq 24$')
plt.plot(x, x23, label=r'$x_1 + x_2 \leq 5$')
plt.plot(x, x24, label=r'$z = 2x_1 + x_2; x_1=3.5, x_2= 1.5; z=8.5$')
plt.plot(x, x25, label=r'$z = 2x_1 + x_2; x_1=2, x_2= 3; z=7$')
plt.plot(x, x26, label=r'$z = 2x_1 + x_2; x_1=4, x_2= 0; z=8$')
plt.ylim(0, 4)
plt.xlim(0, 5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')

plt.show()
