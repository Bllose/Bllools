import matplotlib.pyplot as plt
import numpy as np

# plot the lines defining the constraints
x = np.linspace(0, 60, 100)
# x1+x2=40
x21 = 40 - x
# x1 + x2 = 50
x22 = 50 - x


# Make plot
plt.plot(x, x21, label=r'$x_1+x_2=40$')
plt.plot(24*(x - x + 1), x, label=r'$x_1 = 24$')
plt.plot(x, 30*(x - x + 1), label=r'$x_2 =30$')
plt.plot(x, x22, label=r'$x_1 + x_2= 50$')
plt.ylim(0, 60)
plt.xlim(0, 60)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')

plt.show()
