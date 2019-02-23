#code to plot statistic of user study
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


n_groups = 7

# Mental
# means_exp = (2.66, 1.66, 2.66, 2.33, 2.66, 1.66, 1.66)
# std_exp = (1.15, 0.57, 1.15, 0.57, 0.57, 0.57, 0.57)
#
# means_inexp = (3.66, 2.33, 2.33, 3.33, 3, 2, 2.33)
# std_inexp = (1.52, 0.57, 0.57, 1.52, 2, 1, 1.15)

#time
# means_exp = (3.33, 1.66, 2.66, 2.33, 1.66, 2.33, 1.66)
# std_exp = (1.52, 1.15, 2.08, 1.52, 0.57, 1.52, 0.57)
#
# means_inexp = (2.33, 2.66, 2, 3, 2.66, 2, 3)
# std_inexp = (0.57, 1.15, 1, 1, 1.52, 1.73, 1.73)

#frust
# means_exp = (1.66, 1.66, 1.33, 1.33, 1.33, 1, 1.66)
# std_exp = (0.57, 0.57, 0.57, 0.57, 0.57, 0, 0.57)
#
# means_inexp = (3, 1.33, 2.33, 1.66, 1.66, 1, 1.33)
# std_inexp = (1.73, 0.57, 1.53, 0.57, 0.57, 0, 0.57)

#effort
# means_exp = (2.33, 2, 2.66, 2.33, 2, 1.33, 2.33)
# std_exp = (0.57, 1, 1.15, 0.57, 1, 0.57, 1.52)
#
# means_inexp = (5, 2.33, 2.33, 1.66, 3.33, 1.63, 2)
# std_inexp = (1, 0.57, 0.57, 1.15, 2.51, 0.57, 1)

#satisfaction
means_exp = (5.66, 6, 6, 5.66, 6.33, 6, 5.66)
std_exp = (0.57, 1, 0, 0.57, 0.57, 1, 0.57)

means_inexp = (5, 5.33, 3.66, 6, 6, 6, 5.66)
std_inexp = (1, 1.15, 2.08, 0, 1, 1, 0.57)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, means_exp, bar_width,
                alpha=opacity, color='b',
                yerr=std_exp, error_kw=error_config,
                label='Experienced')

rects2 = ax.bar(index + bar_width, means_inexp, bar_width,
                alpha=opacity, color='r',
                yerr=std_inexp, error_kw=error_config,
                label='Inexperienced')

ax.set_xlabel('Group')
ax.set_ylabel('Perceived satisfaction')
ax.set_title('Perceived satisfaction by group')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(('free', 'full', 'kdom', 'skfreq', 'dbr', 'dbfreq', 'random'))
ax.legend()

fig.tight_layout()
plt.show()


###############################
n_groups = 6
means_exp = (6.33, 4.33, 5.66, 5.33, 6, 6)
std_exp = (0.57, 2.87, 1.52, 1.52, 1, 0)

means_inexp = (5.66, 3, 5.66, 5, 6, 6)
std_inexp = (0.57, 2.65, 0.57, 2, 1.73, 0)
fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, means_exp, bar_width,
                alpha=opacity, color='b',
                yerr=std_exp, error_kw=error_config,
                label='Experienced')

rects2 = ax.bar(index + bar_width, means_inexp, bar_width,
                alpha=opacity, color='r',
                yerr=std_inexp, error_kw=error_config,
                label='Inexperienced')

ax.set_xlabel('Group')
ax.set_ylabel('Perceived usefulness')
ax.set_title('Perceived usefulness by group')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(('full', 'kdom', 'skfreq', 'dbr', 'dbfreq', 'random'))
ax.legend()

fig.tight_layout()
plt.show()
