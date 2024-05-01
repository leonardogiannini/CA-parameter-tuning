import uproot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import utils
import os
num_agents = 100
num_iterations = 20
# num_params = 61
num_params = 5
default = utils.read_csv('checkpoint/default.csv')[0]
default_params = default[:num_params]
default_metrics = default[num_params:]
metrics = [pd.read_csv('history/iteration' + str(i) + '.csv', header=None, usecols=[num_params, num_params + 1]).transpose().to_numpy()
           for i in range(num_iterations)]
import matplotlib.animation as animation

fig, ax = plt.subplots()

def animate(i):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_xlim(0.0, 0.2)#(0., 0.1)
    ax.set_ylim(0.0, 0.2)#(0.6, 0.8)
    # s = ax.scatter(metrics[0][1], 1 - metrics[0][0], s=10)
    s = ax.scatter(metrics[i][1], 1 - metrics[i][0], s=5, color='orchid', label='particles')
    # s = ax.scatter(metrics[num_iterations - 1][1], 1 - metrics[num_iterations - 1][0], c='green', s=10)
    s = ax.scatter([default_metrics[1]], [1 - default_metrics[0]], marker='s', color='blue', s=10, label='default')
    # ax.set_xlabel(r'fakes $=\frac{(N_{rec}-N_{ass})}{N_{rec}}$')
    # ax.set_ylabel(r'eff $=\frac{N_{ass}}{N_{sim}}$')
    # ax.legend(loc='best')
    ax.set_xlabel("Fake + duplicate rate")
    ax.set_ylabel("Efficiency")
    ax.legend()
    ax.set_title(str(i))

ani=animation.FuncAnimation(fig, animate, interval=200, frames=range(num_iterations))
ani.save('checkpoint/metrics.gif', writer='pillow')
pareto_front = utils.read_csv('checkpoint/pareto_front.csv')
pareto_front = pareto_front[pareto_front[:, num_params + 1].argsort()]
pareto_x = [particle[num_params + 1] for particle in pareto_front]

pareto_y = [1 - particle[num_params] for particle in pareto_front]
# pareto_z = [particle[6] for particle in pareto_front]
# pareto_t = [particle[5] + particle[6] for particle in pareto_front]
len(pareto_front)

point1 = pareto_front[10]
point2 = pareto_front[20]
point3 = pareto_front[30]


plt.scatter(pareto_x, pareto_y, s=5, color='turquoise', label='pareto front')

plt.scatter(default_metrics[1], 1 - default_metrics[0], marker='s', color='blue', s=10, label='default')
plt.scatter([point1[num_params + 1]], [1 - point1[num_params]], color='red', s=10, label='sample1')
plt.scatter([point2[num_params + 1]], [1 - point2[num_params]], marker='^', color='black', s=10, label='sample2')
plt.scatter([point3[num_params + 1]], [1 - point3[num_params]], marker='P', color='coral', s=15, label='sample3')
plt.legend()

# plt.scatter([point1[5] + point1[6], point2[5] + point2[6], point3[5] + point3[6]], [1 - point1[4], 1 - point2[4], 1 - point3[4]], color='red', s=8)

# plt.scatter(point1[5], 1 - point1[4], color='red', s=8)
plt.xlim(0.0, 0.2)
plt.ylim(0.0, 0.2)
plt.xlabel('Fake + duplicate rate')
plt.ylabel('Efficiency')
plt.title('Pareto Front')
plt.savefig('checkpoint/pf.png')
plt.show()

print([point1[i] for i in range(num_params)])
print([point2[i] for i in range(num_params)])
print([point3[i] for i in range(num_params)])

selected_params = [default_params, point1[:num_params], point2[:num_params], point3[:num_params]]
# selected_params

utils.write_csv('checkpoint/selected_params.csv', selected_params)
