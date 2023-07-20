import numpy as np
import matplotlib.pyplot as plt

#  Задаем смещение равное половине ширины прямоугольника:
x1 = np.arange(1, 8) - 0.2
x2 = np.arange(1, 8) + 0.2
y1 = np.random.randint(1, 10, size=7)
y2 = np.random.randint(1, 10, size=7)

# fig, ax = plt.subplots()

plt.bar(x1, y1, width=0.4)
plt.bar(x2, y2, width=0.4)

# ax.set_facecolor('seashell')
# fig.set_figwidth(12)    #  ширина Figure
# fig.set_figheight(6)    #  высота Figure
# fig.set_facecolor('floralwhite')

plt.show()
